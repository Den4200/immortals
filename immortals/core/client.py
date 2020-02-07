import arcade
from pymunk import Vec2d

from .events.events import PlayerEvent
from .events.states import GameState, PlayerState
from .events.movement import KeysPressed, apply_movement


class Player:

    def __init__(self, x, y, color, filled=True):
        self.pos = Vec2d(x, y)
        self.color = color
        self.filled = filled

    def draw(self):
        if self.filled:
            arcade.draw_rectangle_fille(
                self.pos.x, self.pos.y,
                50, 50,
                self.color
            )d
        else:
            arcade.draw_rectangle_outline(
                self.pos.x, self.pos.y,
                50, 50,
                self.color,
                border_width=4
            )


class Immortals(arcade.Window):

    def __init__(
        self, 
        width: int, 
        height: int, 
        title: str = 'Immortals'
    ) -> None:
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.WHITE)
        
        self.game_state = GameState(player_states=[PlayerState()])
        self.player = Player(0, 0, arcade.color.GREEN_YELLOW, filled=False)
        self.player_input = PlayerEvent()

    def update(self, dt) -> None:
        self.player_pos = apply_movement(
            speed=800, dt=dt, 
            current_pos=self.player_pos, 
            kp=self.keys_pressed
        )

    def on_draw(self) -> None:
        arcade.start_render()
        self.player.draw()

    def on_key_press(self, key, modifiers) -> None:
        self.keys_pressed.keys[key] = True

    def on_key_release(self, key, modifiers) -> None:
        self.keys_pressed.keys[key] = False
