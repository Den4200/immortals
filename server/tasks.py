from __future__ import annotations

import asyncio
import time

from pymunk import Vec2d

from .events.events import PlayerEvent
from .events.states import GameState


async def update_from_client(game_state: GameState, socket) -> None:
    try:
        while True:
            msg = await sock.recv_json()
            event_dict = msg['event']

            print(f'Recieved: {event_dict}')

            event = PlayerEvent(**event_dict)
            update_game_state(game_state, event)

    except asyncio.CancelledError:
        pass


def update_game_state(
        game_state: GameState,
        event: PlayerEvent
) -> None:
    for ps in game_state.player_states:
        pos = Vec2d(ps.x, ps.y)
        dt = time.time() - ps.updated
        pos = apply_movement(ps.speed, dt, pos, event)
        ps.updated = time.time()


async def push_game_state(game_state: GameState, sock) -> None:
    try:
        while True:
            await sock.send_string(game_state.to_json())
            await asyncio.sleep(1 / SERVER_TICK)

    except asyncio.CancelledError:
        pass
