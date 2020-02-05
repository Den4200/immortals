from .exceptions import RoomIsFull
from immortals.core.settings import ROOM_PLAYER_LIMIT


class Room:
    def __init__(self, server, room_id):
        self._id = room_id
        self._server = server
        self._players = dict()

    def add_player(self, client, player):
        """
        :param client: The client which controls the player
        :param player: the player instance owned by the client
        :return: None
        :raise: RoomIsFull if the number of connected players in the room is bigger than ROOM_PLAYER_LIMIT
        """
        if len(self._players) == ROOM_PLAYER_LIMIT:
            raise RoomIsFull(
                f"Room ({self._id}) is full"
            ) from None
        self._players[client.ip] = player

    @property
    def id(self):
        return self._id

    @property
    def players(self):
        return self._players

    @property
    def player_count(self):
        return len(self._players)
