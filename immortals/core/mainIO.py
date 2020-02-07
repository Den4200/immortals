from dataclasses import asdict
import asyncio

import zmq
from pymunk import Vec2d


async def iomain(window, loop):
    ctx = Context()

    sub_sock = ctx.socket(zmq.SUB)
    sub_sock.connect('tcp://localhost:25000')
    sub_sock.subscribe('')

    push_sock = ctx.socket(zmq.PUSH)
    push_sock.connect('tcp://localhost:25001')

    async def send_player_input():
        while True:
            dct = asdict(window.player_input)
            msg = dict(event=d)
            await push_sock.send_json(msg)

    async def receive_game_state():
        while True:
            gs_string = await sub_sock.recv_string()
            window.game_state.from_json(gs_string)
            player_state = window.game_state.player_states[0]
            window.plater.position = Vec2d(player_state.x, player_state.y)

    try:
        await asyncio.gather(send_player_input(), receive_game_state())

    finally:
        sub_sock.close()
        push_sock.close()
