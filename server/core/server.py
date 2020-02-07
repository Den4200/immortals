import asyncio
import zmq

from .events.states import GameState, PlayerState

async def main():
    future = asyncio.Future()
    app = App(signal=future)

    game_state = GameState(
        player_states=[PlayerState(speed=150)]
    )

    ctx = Context()

    sock_b = ctx.socket(zmq.PULL)
    sock_b.bind('tcp://*25001')
    task_b = asyncio.create_task(
        update_from_client(game_state, sock_b)
    )

    sock_c = ctx.socket(zmq.PUB)
    sock_c.bind('tcp://*25000')
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
