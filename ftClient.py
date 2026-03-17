# ftClient.py
import socket, sys, re, os
from Framer import Framer

host = '127.0.0.1'
port = 50000

def sendFile(filename):
    # Send a file to the server
    try:
        # Check if the target file exists
        if not os.path.isfile(filename):
            print(f"ERROR: File '{filename}' not found")
            return False
        # Create socket and connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Send the file's name first
        filename_framed = Framer.frame(filename)
        sock.sendall(filename_framed)

        # Send file content
        with open(filename, 'rb') as f:
            file_data = f.read()
        
        file_framed = Framer.frame(file_data)
        sock.sendall(file_framed)
        print(f"File '{filename}' sent successfully")
        sock.close()
        return True
    except Exception as e:
        print (f"Error sending file: {e}")
        import traceback
        traceback.print_exc()
        return False
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Usage: python ftClient.py <filename>")
        sys.exit(1)
    sendFile(sys.argv[1])