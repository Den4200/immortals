import pickle
import socket
from random import randrange

from player import Player
from utils import threaded


class Server:

    def __init__(
            self, 
            ip: str = '127.0.0.1', 
            port: int = 5555
        ) -> None:

        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.ip = ip
        self.port = port
        self.players = dict()

    @threaded
    def player(self, conn: 'socket.socket') -> None:
        raddr = conn.getpeername()
        color = (
            randrange(0, 256, 64),
            randrange(0, 256, 64),
            randrange(0, 256, 64)
        )

        if len(self.players) == 0:
            self.players[raddr] = (
                Player(
                    0, 50,
                    50, 50,
                    color
                )
            )
        else:
            prev = list(self.players.values())

            self.players[raddr] = (
                Player(
                    prev[-1].x + 100,
                    prev[-1].y,
                    50, 50,
                    color
                )
            )

        conn.send(pickle.dumps(self.players[raddr]))

        while True:
            try:
                data = pickle.loads(conn.recv(2048))
                self.players[raddr] = data

                if not data:
                    print(f'Disconnected from player {raddr}')
                    break

                else:
                    players = list(self.players.items())
                    conn.sendall(pickle.dumps(
                        [player for addr, player in players if addr != raddr]
                    ))

            except:
                break
        
        self.players.pop(raddr)

        print(f'Player {raddr} disconnected')
        conn.close()

    def run(self) -> None:
        try:
            self.socket.bind((self.ip, self.port))

        except socket.error as e:
            print(e)

        else:
            print('Server sucessfully initialized')
            self.socket.listen()
            print('Server awaiting new connections')

            while True:
                conn, addr = self.socket.accept()
                print(f'Connection established to {addr}')

                self.player(conn)
