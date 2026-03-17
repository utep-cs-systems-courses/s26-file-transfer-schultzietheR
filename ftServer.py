# ftServer.py
import socket, sys, os, threading, struct
from Framer import Framer

host = '127.0.0.1'
port = 50000
output_dir = 'received_files'

def ensureOutputDir():
    # Create an output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
def handleClient(client_socket, client_address):
    # Handle individual client connection
    try:
        print(f"Client connected: {client_address}")
        # Receive filename
        filename = Framer.read(client_socket)
        if not filename:
            print("No filename received")
            return
        print(f"Receiving file: {filename}")
        # Receive file content
        file_data = client_socket.recv(4)
        if not file_data:
            print("No file data received")
            return
        length = struct.unpack('!I', file_data)[0]
        file_content = b''
        while len(file_content) < length:
            chunk = client_socket.recv(min(4096, length - len(file_content)))
            if not chunk:
                break
            file_content += chunk
        # Save file
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'wb') as f:
            f.write(file_content)
        print(f"File saved: {output_path}")
    except Exception as e:
        print (f"Error handling client {client_address}: {e}")
        import traceback
        traceback.print_exc()
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
    startServer()