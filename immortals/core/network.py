import struct
import socket
import pickle


class Network:
    
    def __init__(
        self, 
        ip: str = '127.0.0.1', 
        port: int = 5555
    ) -> None:

        self.socket = socket.socket(
            socket.AF_INET, 
            socket.SOCK_STREAM
        )
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)

    def recieve(self):
        size = struct.calcsize('L')
        size = self.socket.recv(size)
        size = socket.ntohl(struct.unpack('L', size)[0])

        result = b''

        while len(result) < size:
            result += self.socket.recv(size - len(result))

        return pickle.loads(result)

    def connect(self):
        self.socket.connect(self.addr)
        return self.recieve()

    def send(self, data):
        packets = pickle.dumps(data)
        value = socket.htonl(len(packets))
        size = struct.pack('L', value)
        self.socket.send(size)
        self.socket.send(packets)
        
        return self.recieve()
