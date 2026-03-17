# Framer.py
import struct

class Framer:

    @staticmethod
    def frame(data):
        # Adds a frame header w/data length
        if isinstance(data, str):
            data = data.encode()
        length = len(data)
        header = struct.pack('!I', length)
        return header + data
    @staticmethod
    def read (sock, buffer_size=4096):
        # Read a framed message from socket
        # Read the 4-byte length header first
        header = sock.recv(4)
        if not header:
            return None
        length = struct.unpack('!I', header)[0]
        # Now read just the 'length' bytes of data
        data = b''
        while len(data) < length:
            chunk = sock.recv(min(buffer_size, length - len(data)))
            if not chunk:
                break
            data += chunk
        return data.decode()