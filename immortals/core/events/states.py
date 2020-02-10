from __future__ import annotations

import json
from dataclasses import (
    dataclass,
    asdict
)
from typing import List


@dataclass
class PlayerState:
    updated: float = 0
    x: float = 0
    y: float = 0
    health: float = 0
    speed: float = 5.0
    

@dataclass
class GameState:
    player_states: List[PlayerState]

    def to_json(self):
        dct = dict(
            player_states=[
                asdict(p) for p in self.player_states
            ]
        )
        return json.dumps(dct)

    def from_json(self, data):
        dct = json.loads(data)

        for idx, player in enumerate(dct['player_states']):
            self.player_states[idx] = PlayerState(**player)

