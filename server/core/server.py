import asyncio
import time

import zmq
import zmq.asyncio
from pymunk import Vec2d
from zmq import Socket

from .constants import SERVER_TICK
from .events.events import PlayerEvent
from .events.movement import apply_movement
from .events.states import GameState, PlayerState


async def main():
    future = asyncio.Future()
    game_state = GameState(
        player_states=[PlayerState()]
    )
    ctx = zmq.asyncio.Context()

    sock_b = ctx.socket(zmq.PULL)
    sock_b.bind('tcp://*:25001')
    task_b = asyncio.create_task(
        update_from_client(game_state, sock_b)
    )

    sock_c = ctx.socket(zmq.PUB)
    sock_c.bind('tcp://*:25000')
    task_c = asyncio.create_task(
        push_game_state(game_state, sock_c)
    )

    try:
        await asyncio.wait(
            [task_b, task_c, future],
            return_when=asyncio.FIRST_COMPLETED
        )

    except asyncio.CancelledError:
        print('Cancelled')

    finally:
        sock_b.close()
        sock_c.close()
        ctx.destroy(linger=1)


async def update_from_client(game_state: GameState, sock: Socket) -> None:
    try:
        while True:
            msg = dict(await sock.recv_json())
            event_dict = msg['event']
            print(f'Received {event_dict}')

            event = PlayerEvent(**event_dict)
            update_game_state(game_state, event)

    except asyncio.CancelledError:
        print("Cancelled")
        pass


def update_game_state(game_state: GameState, event: PlayerEvent) -> None:
    for ps in game_state.player_states:
        pos = Vec2d(ps.x, ps.y)
        dt = time.time() - ps.updated

        new_pos = apply_movement(ps.speed, dt, pos, event)
        ps.x, ps.y = new_pos.x, new_pos.y

        ps.updated = time.time()


async def push_game_state(game_state: GameState, sock: Socket) -> None:
    try:
        while True:
            sock.send_string(game_state.to_json())
            await asyncio.sleep(1 / SERVER_TICK)

    except asyncio.CancelledError:
        pass
