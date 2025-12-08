import arcade
from arcade.gui import *
import random


class Button(UITextureButton):
    def __init__(self, game, x=0, y=0, width=100, height=50):
        self.game = game
        texture = arcade.load_texture(
            "resources/camera_button_pro_version.png")

        super().__init__(texture=texture, x=x, y=y,
                         text='папер2', width=width, height=height)

    def on_click(self, event):
        self.booyah()

    def booyah(self):

        self.game.background_color = (random.randint(
            0, 255), random.randint(0, 255), random.randint(0, 255))


class MainMenu(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.w = width
        self.h = height
        self.texture = arcade.load_texture(
            "resources/camera_button_pro_version.png")
        arcade.set_background_color(arcade.color.BABY_BLUE_EYES)
        self.gui_manager = UIManager()
        self.gui_manager.enable()
        anchor_layout = UIAnchorLayout()
        self.button = Button(self, self.w // 2, self.h // 2)
        anchor_layout.add(self.button)
        self.gui_manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        # arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(
        #     self.w // 2, self.h // 2, self.w - 40, self.w - 40))
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(random.randint(0, self.w), random.randint(
            0, self.h), random.randint(0, self.w // 2), random.randint(0, self.h // 2)))
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(random.randint(0, self.w), random.randint(
            0, self.h), random.randint(0, self.w // 2), random.randint(0, self.h // 2)))
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(random.randint(0, self.w), random.randint(
            0, self.h), random.randint(0, self.w // 2), random.randint(0, self.h // 2)))
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(random.randint(0, self.w), random.randint(
            0, self.h), random.randint(0, self.w // 2), random.randint(0, self.h // 2)))
        self.gui_manager.draw()
