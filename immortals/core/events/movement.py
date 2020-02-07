from __future__ import annotations

import arcade
from pymunk import Vec2d

MOVE_MAP = {
    arcade.key.UP: Vec2d(0, 1),
    arcade.key.DOWN: Vec2d(0, -1),
    arcade.key.LEFT: Vec2d(-1, 0),
    arcade.key.RIGHT: Vec2d(1, 0)
}

class KeysPressed:
    
    def __init__(self) -> None:
        self.keys = {
            key: False for key in MOVE_MAP
        }


def apply_movement(
    speed,
    dt,
    current_pos: Vec2d,
    kp: KeysPressed
) -> Vec2d:

    delta_pos = sum(kp.keys[k] * MOVE_MAP[k] for k in kp.keys)
    return (delta_pos.normalized() * speed * dt) + current_pos
