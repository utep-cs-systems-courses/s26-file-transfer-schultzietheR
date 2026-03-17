# Framer.py
import struct

class Framer:
    def __init__(self, file_des):
        # Constructor for the framer
        self.file_des = file_des
    #@staticmethod
    def frame(self, data):
        # Adds a frame header w/data length
        if isinstance(data, str):
            data = data.encode()
        length = len(data)
        header = struct.pack('!I', length)
        framed_data = header + data
        self.file_des.write(framed_data)
        return framed_data
    
class Deframer:
    
    def __init__(self, file_des):
        # Constructor for the deframer
        self.file_des = file_des
    #@staticmethod
    def deframe(self, buffer_size=4096, decode=False):
        
        # Read a framed message from a file descriptor.
        
        try:
            # Try to read 8 bytes (largest possible header)
            header = self.file_des.read(8)
            if not header:
                return None
            header_size = len(header)
            # Unpack based on actual header size received
            if header_size == 1:
                length = struct.unpack('!B', header)[0]
            elif header_size == 2:
                length = struct.unpack('!H', header)[0]
            elif header_size == 4:
                length = struct.unpack('!I', header)[0]
            elif header_size == 8:
                length = struct.unpack('!Q', header)[0]
            else:
                raise ValueError(f"Invalid header size: {header_size}") 
            
            # Validate frame length
            if length > 1024 * 1024 * 100:  # 100MB max
                raise ValueError(f"Frame size too large: {length} bytes")
            
            # Read exactly 'length' bytes of data
            data = b''
            while len(data) < length:
                chunk = self.file_des.read(min(buffer_size, length - len(data)))
                if not chunk:
                    raise EOFError("File closed unexpectedly")
                data += chunk
            
            # Return decoded or raw based on parameter
            return data.decode() if decode else data
        
        except struct.error as e:
            print(f"Frame header error: {e}")
            return None
        except Exception as e:
            print(f"Deframing error: {e}")
            return None
         
