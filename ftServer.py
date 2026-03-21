# ftServer.py
import socket, sys, os, threading, struct
from Framer import Framer, Deframer

host = '127.0.0.1'
port = 50000
output_dir = 'received_files'

def ensureOutputDir():
    # Create an output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
def handleClient(client_socket, client_address):
    try:
        sock_file = client_socket.makefile('rb')
        deframer = Deframer(sock_file)
        
        # 1. Get filename
        filename = deframer.deframe(decode=True)
        if not filename: return

        # 2. Receive chunks and write to file
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'wb') as f:
            while True:
                chunk = deframer.deframe(decode=False)
                if chunk is None or len(chunk) == 0: # EOF reached
                    break
                f.write(chunk)
        
        print(f"File saved: {output_path}")
    finally:
        client_socket.close()

def startServer(max_clients=5):
    # Starts the file transfer server.
    ensureOutputDir()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(max_clients)
    print(f"Server listening on {host}:{port}")
    print(f"Received files will be saved to: {output_dir}")
    try:
        while True:
            client_socket, client_address = sock.accept()
            # Handle each client in a separate thread
            client_thread = threading.Thread(
                target=handleClient,
                args=(client_socket, client_address)
            )
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\n Server shutting down...")
    finally:
        sock.close()
if __name__ == '__main__':
    # Default values
    listen_port = port 
    
    # Simple argument check for -p <port>
    if len(sys.argv) > 2 and sys.argv[1] == '-p':
        try:
            listen_port = int(sys.argv[2])
            port = listen_port # Update the global port variable
        except ValueError:
            print("Invalid port number. Using default 50000.")

    startServer()
