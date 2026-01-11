import arcade
import queue
import threading
import os
import time
from src.registry import reg


class LoadingView(arcade.View):
    def __init__(self, window: arcade.Window, next_view_name: str, load_tag: str):
        super().__init__()
        self.window = window
        self.next_view_name = next_view_name
        self.load_tag = load_tag

        self.total_files = 0
        self.loaded_count = 0
        self.is_finished = False
        self.already_switched = False

    def setup(self):
        self.ui_sprites = arcade.SpriteList()
        self.gif_sprite_list = arcade.SpriteList()

        self.files_to_load = reg.scan_resources(self.load_tag)
        self.total_files = len(self.files_to_load)

        self.bar_bg = arcade.SpriteSolidColor(
            1, 12, color=arcade.color.DARK_GRAY)
        self.bar_fill = arcade.SpriteSolidColor(
            1, 12, color=arcade.color.GREEN)

        self.ui_sprites.extend([self.bar_bg, self.bar_fill])

        self.percent_text = arcade.Text(
            "0%", 0, 0, arcade.color.WHITE, 20, font_name="montserrat", anchor_x="center")

        try:
            self.loading_gif = arcade.load_animated_gif(
                "resources/common/textures/ui/loading.gif")
            self.loading_gif.scale = 2.0
            self.gif_sprite_list.append(self.loading_gif)
        except:
            self.loading_gif = None

        self.setup_positions()

    def setup_positions(self):
        w, h = self.window.width, self.window.height
        cx, cy = w // 2, h // 5

        self.bar_bg.width = int(w * 0.6)
        self.bar_bg.position = (cx, cy)
        self.percent_text.position = (cx, cy + 40)

        if self.loading_gif:
            self.loading_gif.position = (w // 2, h // 2)

        self.refresh_bar_fill()

    def refresh_bar_fill(self):
        if self.total_files > 0:
            progress = self.loaded_count / self.total_files
            new_width = max(1, int(self.bar_bg.width * progress))

            self.bar_fill.width = new_width
            self.bar_fill.left = self.bar_bg.left
            self.bar_fill.center_y = self.bar_bg.center_y

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()
        threading.Thread(target=self.heavy_loader, daemon=True).start()

    def heavy_loader(self):
        for key, path, name in self.files_to_load:
            reg.load_single_resource(key, path, name)
            self.loaded_count += 1
            time.sleep(0.02)

        self.is_finished = True

    def on_update(self, delta_time: float):
        self.gif_sprite_list.update_animation(min(delta_time, 0.03))

        self.refresh_bar_fill()
        if self.total_files > 0:
            self.percent_text.text = f"{int((self.loaded_count / self.total_files) * 100)}%"

        if self.is_finished and not self.already_switched:
            self.already_switched = True
            arcade.schedule_once(
                lambda dt: self.window.switch_view(self.next_view_name), 0.1)

    def on_draw(self):
        self.clear()
        self.ui_sprites.draw()
        self.gif_sprite_list.draw()
        self.percent_text.draw()

    def on_resize(self, width: int, height: int):
        self.setup_positions()


class DemoGameView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.window = window
        self.test_sprite_list = arcade.SpriteList()
        self.phone_sprite = None

    def on_show_view(self):
        self.window.background_color = arcade.color.LION
        self.setup()

    def setup(self):
        self.test_sprite_list.clear()
        texture = reg.get('1episode/textures/ui/buttons/normal/test.png')

        if texture:
            self.phone_sprite = arcade.Sprite(texture)
            self.update_background_position_and_size()
            self.test_sprite_list.append(self.phone_sprite)

    def on_draw(self):
        self.clear()
        self.test_sprite_list.draw()

    def update_background_position_and_size(self):
        if self.phone_sprite:
            self.phone_sprite.width = self.window.width
            self.phone_sprite.height = self.window.height
            self.phone_sprite.position = self.window.width // 2, self.window.height // 2

    def on_resize(self, width, height):
        self.update_background_position_and_size()
