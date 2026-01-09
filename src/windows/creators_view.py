import arcade
from src.registry import reg


class CreatorsView(arcade.View):

    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window

        self.reg = reg

        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None

    def setup(self):
        self.load_background()

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()

        if self.background_sprite_list:
            self.background_sprite_list.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.switch_view("settings_window")

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.update_background_position_and_size()

    def load_background(self):
        texture = self.reg.get(
            'common/textures/backgrounds/creators_background.jpg')
        self.background_sprite = arcade.Sprite(
            path_or_texture=texture,
            center_x=self.window.width // 2,
            center_y=self.window.height // 2
        )

        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height

        self.background_sprite_list.append(self.background_sprite)

    def update_background_position_and_size(self):
        if not self.background_sprite:
            return

        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2
