import time
import asyncio
from random import randrange

import zmq
from zmq import Socket
from pymunk import Vec2d
from connectIO import Server, threaded

from .constants import SERVER_TICK
from .events.events import PlayerEvent
from .events.states import GameState, PlayerState
from .events.movement import apply_movement


class ImmortalsServer(Server):

    def __init__(self, ip='127.0.01.', port=5555) -> None:
        super().__init__(ip, port)
        self.func = self.player_conn

        self.game_state = GameState(None)

    def player_conn(self, conn, addr) -> None:
        raddr = conn.getpeername()

        color = (
            randrange(0, 256, 15),
            randrange(0, 256, 15),
            randrange(0, 256, 15)
        )

        if len(self.game_state.players) == 0:
            self.game_state.players[raddr] = (
                PlayerState(
                    color,
                    x=600, 
                    y=50
                )
            )

        else:
            prev = list(self.game_state.players.values())

            self.game_state.players[raddr] = (
                PlayerState(
                    color,
                    x=prev[-1][-1].x + 100,
                    y=prev[-1][-1].y
                )
            )


        self.send(conn, (raddr, self.game_state.players[raddr]))

        self.main_loop(conn, raddr)

    
    def main_loop(self, conn, raddr) -> None:
        while True:
            try:
                data = self.recieve(conn)

                if not data:
                    print(f'Disconnected from player {raddr}')
                    break

                else:
                    self.send(conn, self.game_state)

                self.update_game_state(data)

            except Exception:
                break

    def update_game_state(self, data) -> None:
        for addr, player_states in self.game_state.players.items():
            
            for ps in player_states:
                pos = Vec2d(ps.x, ps.y)
                dt = time.time() - ps.updated

                # TODO: finish this function


async def main():
    future = asyncio.Future()

    game_state = GameState(
        player_states=[PlayerState()]
    )

    ctx = zmq.Context()

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
            msg = sock.recv_json()

            event_dict = msg['event']
            print(f'Received {event_dict}')

            event = PlayerEvent(**event_dict)
            update_game_state(game_state, event)

    except asyncio.CancelledError:
        pass

def update_game_state(game_state: GameState, event: PlayerEvent) -> None:
    for ps in game_state.player_states:
        pos = Vec2d(ps.x, ps.y)
        dt = time.time() - ps.updated

        new_pos = apply_movement(ps.speed, dt, pos, event)

        # modifies values in place (ps: PlayerState)
        ps.x, ps.y = new_pos.x, new_pos.y
        ps.updated = time.time()

async def push_game_state(game_state: GameState, sock: Socket) -> None:
    try:
        while True:
            await sock.send_string(game_state.to_json())
            await asyncio.sleep(1 / SERVER_TICK)

    except asyncio.CancelledError:
        pass
