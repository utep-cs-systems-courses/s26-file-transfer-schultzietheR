# ftClient.py
import socket, sys, re, os
from Framer import Framer, Deframer

def sendFile(filename, host, port):
    try:
        if not os.path.isfile(filename):
            print(f"ERROR: File '{filename}' not found")
            return False
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock_file = sock.makefile('wb', buffering=0)
        framer = Framer(sock_file)

        # 1. Send Filename
        framer.frame(os.path.basename(filename))

        # 2. Send File Content in Chunks
        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(16384) # 16KB chunks
                if not chunk:
                    break
                framer.frame(chunk)
        
        # 3. Send an empty frame to signal EOF (End of File)
        framer.frame(b'') 

        print(f"File '{filename}' sent successfully")
        sock_file.close()
        sock.close()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python ftClient.py <filename> <host> [port]")
        sys.exit(1)
    filename = sys.argv[1]
    host = sys.argv[2]
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 50000
    
    sendFile(filename, host, port)