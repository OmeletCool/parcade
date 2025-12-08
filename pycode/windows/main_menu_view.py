import arcade


class MainMenu(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.w = width
        self.h = height
        self.texture = arcade.load_texture(
            "resources/camera_button_pro_version.png")
        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(
            self.w // 2, self.h // 2, self.w - 40, self.w - 40))
