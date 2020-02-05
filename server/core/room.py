from .constants import ROOM_PLAYER_LIMIT, COLORS
from .exceptions import ConfigurationException, RoomIsFull


class Room:
    def __init__(self, server, room_id):
        self._id = room_id
        self.__server = server
        self._players = dict()
        self.colors = list(COLORS.values())

        if len(COLORS) < ROOM_PLAYER_LIMIT:
            raise ConfigurationException(
                'Unsufficient amount of colors for the player limit.'
            )

    @property
    def id(self):
        return self._id

    @property
    def players(self):
        return self._players

    @property
    def player_count(self):
        return len(self._players)

    def can_party_join(self, length: int):
        return (len(self._players) + length) <= ROOM_PLAYER_LIMIT

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
        player.color = self.colors.pop()
