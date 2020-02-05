from .constants import ROOM_PLAYER_LIMIT, COLORS
from .exceptions import ConfigurationException, RoomIsFull, PlayerDoesNotExist


class Room:
    def __init__(self, server, room_id: int, private: bool = False):
        self._id = room_id
        self.__server = server
        self.is_private = private
        self.full: bool = False
        self._players = dict()
        self.colors = list(COLORS.values())

        if len(COLORS) < ROOM_PLAYER_LIMIT:
            raise ConfigurationException(
                'Insufficient amount of colors for the player limit.'
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
        return self.full or (len(self._players) + length) <= ROOM_PLAYER_LIMIT

    def add_player(self, ip, playerdata):
        """
        :param ip: The ip which controls the playerdata's client is running on
        :param playerdata: the playerdata
        :return: None
        :raise: RoomIsFull if the number of connected players in the room is bigger than ROOM_PLAYER_LIMIT
        """
        if len(self._players) == ROOM_PLAYER_LIMIT:
            raise RoomIsFull(
                f"Room ({self._id}) is full"
            ) from None

        self._players[ip] = playerdata
        playerdata.color = self.colors.pop()

    def remove_player(self, player, ip: str = None):
        players = self._players
        if not ip:
            keys = players.keys()
            ip = keys[players.values().index(player)]  # getting the ip by the player
        if not all(ip, player) or ip not in self._players:
            raise PlayerDoesNotExist(f"The Player  Isn't in room {self._id}") from None
        self._players.pop(ip)
        self.colors.append(player.color)

        self._players[ip] = player
        player.color = self.colors.pop()
