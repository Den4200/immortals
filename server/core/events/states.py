from __future__ import annotations

from typing import (
    Dict, 
    List, 
    Tuple,
    Optional
)
from dataclasses import (
    dataclass,
    asdict
)
import json


@dataclass
class PlayerState:
    color: Tuple[int, int, int]
    updated: float = 0.0
    x: float = 0.0
    y: float = 0.0
    health: float = 0.0
    speed: float = 5.0


@dataclass
class GameState:
    players: Optional[Dict[Tuple[str, int], List[PlayerState]]]
    # player_states: List[PlayerState]

    def to_json(self):
        dct = {
            addr: [
                asdict(state) for state in states
            ] for addr, states in self.players
        }

        # dct = dict(
        #     player_states=[
        #         asdict(p) for p in self.player_states
        #     ]
        # )
        return json.dumps(dct)

    def from_json(self, data):
        dct = json.loads(data)

        for addr, states in dct:
            self.players[addr] = [PlayerState(**state) for state in states]

        # for idx, player in enumerate(dct['player_states']):
        #     self.player_states[idx] = PlayerState(**player)
