import arcade
from pymunk.vec2d import Vec2d

from .events.movement import KeysPressed, apply_movement


class Immortals(arcade.Window):

    def __init__(
        self, 
        width: int, 
        height: int, 
        title: str = 'Immortals'
    ) -> None:
        super().__init__(width, height)

        self.player_pos = Vec2d(400, 300)
        self.keys_pressed = KeysPressed()

    def update(self, dt) -> None:
        self.player_pos = apply_movement(
            speed=800, dt=dt, 
            current_pos=self.player_pos, 
            kp=self.keys_pressed
        )

    def on_draw(self) -> None:
        arcade.start_render()
        arcade.draw_rectangle_filled(
            center_x=self.player_pos.x, center_y=self.player_pos.y,
            width=50, height=50, color=arcade.color.YELLOW
        )

    def on_key_press(self, key, modifiers) -> None:
        self.keys_pressed.keys[key] = True

    def on_key_release(self, key, modifiers) -> None:
        self.keys_pressed.keys[key] = False
