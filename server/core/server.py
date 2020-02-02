from random import randrange
from connectIO import Server, threaded

from .playerdata import PlayerData


class ImmortalsServer(Server):

    def __init__(self, ip: str = '127.0.0.1', port: int = 5555):
        super(ImmortalsServer, self).__init__()
        self.func = self.player

        self.players = dict()

    @threaded
    def player(self, conn, addr) -> None:
        raddr = conn.getpeername()
        color = (
            randrange(0, 256, 64),
            randrange(0, 256, 64),
            randrange(0, 256, 64)
        )

        if len(self.players) == 0:
            self.players[raddr] = (
                PlayerData(
                    600, 50,
                    50, 50,
                    color
                )
            )
        else:
            prev = list(self.players.values())

            self.players[raddr] = (
                PlayerData(
                    prev[-1].data[0] + 100,
                    prev[-1].data[1],
                    50, 50,
                    color
                )
            )

        self.send(conn, self.players[raddr])
        
        while True:
            try:
                data = self.recieve(conn)
                self.players[raddr] = data

                if not data:
                    print(f'Disconnected from player {raddr}')
                    break

                else:
                    players = list(self.players.items())
                    self.send(
                        conn,
                        [player for addr, player in players if addr != raddr]
                    )
                    # print(*(x[1].data for x in players))

            except Exception:
                break
        
        self.players.pop(raddr)

        print(f'Player {raddr} disconnected')
        conn.close()
