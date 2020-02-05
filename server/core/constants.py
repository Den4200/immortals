import toml

TOML = toml.load('server/config.toml')

COLORS = TOML['colors']
ROOM_PLAYER_LIMIT = TOML['game_room']['player_limit']
