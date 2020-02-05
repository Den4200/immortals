from random import randrange
from connectIO import Server, threaded

from typing import Dict

from .playerdata import PlayerData
from .room import Room
from .exceptions import RoomIsFull


class ImmortalsServer(Server):

    def __init__(self, ip: str = '127.0.0.1', port: int = 5555):
        super(ImmortalsServer, self).__init__()
        self.func = self.player

        self.players = dict()
        self.rooms = dict()

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
            prev = list(self.players.values())[-1]

            self.players[raddr] = (
                PlayerData(
                    prev.data[0] + 100,
                    prev.data[1],
                    50, 50,
                    color
                )
            )

        self.send(conn, (raddr, self.players[raddr]))

        while True:
            try:
                data = self.recieve(conn)
                self.players[raddr] = data[1]

                if not data:
                    print(f'Disconnected from player {raddr}')
                    break

                else:
                    players = list(self.players.items())
                    self.send(
                        conn,
                        {addr: player for addr, player in players if addr != raddr}
                    )
                    # print(*(x[1].data for x in players))

            except Exception:
                break

        self.players.pop(raddr)

        print(f'Player {raddr} disconnected')
        conn.close()

    def create_room(self, party: Dict[str, PlayerData] = None):
        if party is None:
            # we can handle this better
            return
        room_id = 12345  # Todo - Generate room id
        room = Room(self, room_id)

        if not room.can_party_join(len(party)):
            # Todo Need to send the client a message
            return

        for ip, player in party:
            room.add_player(ip, player)

        self.rooms[room_id] = Room

    def join_room(self, room_id: int, party: Dict[str, PlayerData] = None):
        room = self.rooms.get(room_id)
        if room is None:
            # Todo Need to send the client a message
            return
        if not room.can_party_join(len(party)):
            # Todo Need to send the client a message
            return

        for ip, player in party:
            room.add_player(ip, player)
