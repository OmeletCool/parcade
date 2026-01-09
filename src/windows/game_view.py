import arcade
from src.registry import reg


class DemoGameView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        arcade.set_background_color(arcade.color.LION)

        self.window = window

        self.reg = reg
