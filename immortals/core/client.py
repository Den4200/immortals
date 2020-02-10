import arcade
from pymunk import Vec2d

from .events.events import PlayerEvent
from .events.states import GameState, PlayerState


class Player:

    def __init__(self, x, y, color, filled=True):
        self.pos = Vec2d(x, y)
        self.color = color
        self.filled = filled
        self.size = 50

    def draw(self):
        if self.filled:
            arcade.draw_rectangle_filled(
                self.pos.x, self.pos.y,
                self.size, self.size,
                self.colorDamn
            )
        else:
            arcade.draw_rectangle_outline(
                self.pos.x, self.pos.y,
                self.size, self.size,
                self.color,
                border_width=4
            )


class Immortals(arcade.Window):

    def __init__(
        self, 
        width: int, 
        height: int,
            title: str = "Immortal"
    ) -> None:
        super().__init__(width, height, title=title)

        arcade.set_background_color(arcade.color.WHITE)
        
        self.game_state = GameState(player_states=[PlayerState()])
        self.player = Player(0, 0, arcade.color.GREEN_YELLOW, filled=False)
        self.player_input = PlayerEvent()
        self.keys_pressed = dict()

    def on_draw(self) -> None:
        arcade.start_render()
        self.player.draw()

    def on_key_press(self, key, modifiers) -> None:
        self.keys_pressed[key] = True
        self.player_input.keys = self.keys_pressed

    def on_key_release(self, key, modifiers) -> None:
        self.keys_pressed[key] = False
        self.player_input.keys = self.keys_pressed
