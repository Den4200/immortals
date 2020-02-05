# Exceptions


class ConfigurationException(Exception):
    pass


class MissingConfiguration(ConfigurationException):
    pass


class RoomException(Exception):
    pass


class RoomIsFull(RoomException):
    pass


class RoomDoesNotExist(RoomException):
    pass
