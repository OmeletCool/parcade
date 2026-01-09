import arcade
from src.registry import reg


class DemoGameView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        arcade.set_background_color(arcade.color.LION)

        self.window = window

        self.reg = reg

        self.test_sprite_list = arcade.SpriteList()

    def setup(self):
        self.load_phone()

    def load_phone(self):
        texture = self.reg.get('1episode/textures/ui/buttons/normal/test.png')
        self.phone_sprite = arcade.Sprite(path_or_texture=texture)
        self.test_sprite_list.clear()
        self.test_sprite_list.append(self.phone_sprite)

    def update_background_position_and_size(self):
        if self.phone_sprite:
            self.phone_sprite.width = self.window.width
            self.phone_sprite.height = self.window.height
            self.phone_sprite.center_x = self.window.width // 2
            self.phone_sprite.center_y = self.window.height // 2

    def on_draw(self):
        self.test_sprite_list.draw()
