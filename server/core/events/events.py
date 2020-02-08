from typing import Dict
from dataclasses import (
    dataclass,
    asdict,
    field
)

from .movement import MOVE_MAP


@dataclass
class PlayerEvent:
    """
    Player events sent to and from a server.
    """
    keys: Dict[int, bool] = field(
        default_factory=lambda: {
            key: False for key in MOVE_MAP
        }
    )

    def __post_init__(self) -> None:
        self.keys = {
            int(k): v for k, v in self.keys.items()
        }

    def asdict(self):
        return asdict(self)
