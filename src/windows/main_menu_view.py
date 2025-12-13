import arcade
import math
from pyglet.graphics import Batch
from src.settings import settings
from src.registry import reg


class MainMenuView(arcade.View):
    """Главное меню игры"""

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.timer = 0.0
        self.batch = Batch()
        self.shape_list = arcade.shape_list.ShapeElementList()
        self.sprite_list = arcade.SpriteList()
        self.background_sprite = None
        self.overlay = None
        self.overlay_sprite_list = arcade.SpriteList()
        self.wind_sound = arcade.load_sound(
            'resources/sounds/sfx/ambient/wind.wav')
        self.fade_duration = self.wind_sound.get_length()
        self.display_duration = 3.0
        self.background_image_path = 'resources/textures/backgrounds/main_menu_background.png'
        self.isFading = False

    def setup(self):
        """Инициализация представления"""
        self.load_background()
        self.create_overlay()
        self.isFading = True
        self.wind_sound_player = self.wind_sound.play()

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        self.setup()
        self.timer = 0.0

    def on_draw(self):
        """Рисование"""
        self.clear()

        self.sprite_list.draw()

        self.overlay_sprite_list.draw()

    def on_update(self, delta_time):
        """Обновление логики"""
        self.timer += delta_time

        if self.overlay and self.timer <= self.fade_duration:
            progress = self.timer / self.fade_duration
            eased_progress = 1 - math.pow(1 - progress, 3)
            alpha = int(255 * (1.0 - eased_progress))
            alpha = max(0, min(255, alpha))
            self.overlay.color = (0, 0, 0, alpha)

        if self.timer >= self.fade_duration:
            self.isFading = False

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        self.update_background_position_and_size()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.timer < self.fade_duration:
            self.timer = self.fade_duration
            self.wind_sound.stop(self.wind_sound_player)
            self.overlay.color = (0, 0, 0, 0)

    def on_key_press(self, symbol, modifiers):
        if self.timer < self.fade_duration:
            self.timer = self.fade_duration
            self.wind_sound.stop(self.wind_sound_player)
            self.overlay.color = (0, 0, 0, 0)

    def load_background(self):
        texture = arcade.load_texture(self.background_image_path)

        self.background_sprite = arcade.Sprite(
            path_or_texture=texture,
            center_x=self.window.width // 2,
            center_y=self.window.height // 2
        )

        self.sprite_list.append(self.background_sprite)

        self.update_background_position_and_size()

    def create_overlay(self):
        self.overlay = arcade.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height,
            color=(0, 0, 0, 255)
        )
        self.overlay.center_x = self.window.width // 2
        self.overlay.center_y = self.window.height // 2
        self.overlay_sprite_list.append(self.overlay)

    def update_background_position_and_size(self):
        # это было растягивание при сохранениях пропорций

        # if not self.background_sprite or not self.background_sprite.texture:
        #     return

        # texture = self.background_sprite.texture
        # orig_width = texture.width
        # orig_height = texture.height

        # window_ratio = self.window.width / self.window.height
        # background_image_ratio = orig_width / orig_height

        # if window_ratio > background_image_ratio:
        #     scale = self.window.height / orig_height
        # else:
        #     scale = self.window.width / orig_width

        # self.background_sprite.width = orig_width * scale
        # self.background_sprite.height = orig_height * scale

        # self.background_sprite.center_x = self.window.width // 2
        # self.background_sprite.center_y = self.window.height // 2

        # а это просто растягивание

        if not self.background_sprite:
            return

        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2

        if self.overlay:
            self.overlay.width = self.window.width
            self.overlay.height = self.window.height
            self.overlay.center_x = self.window.width // 2
            self.overlay.center_y = self.window.height // 2
