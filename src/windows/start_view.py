import math
import arcade
from pyglet.graphics import Batch
from src.settings import settings
from src.registry import reg
from resources.languages import LANGUAGES


class StartView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window

        self.language: int = self.window.language

        self.timer = 0.0

        self.reg = reg

        self.original_width = settings.width
        self.original_height = settings.height

        self.batch = Batch()

        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None

        self.overlay = None
        self.overlay_sprite_list = arcade.SpriteList()

        self.wind_sound: arcade.Sound = self.reg.get(
            'common/sounds/sfx/ambient/wind.wav')

        self.fade_background_duration = self.wind_sound.get_length()

        self.isTextToContinue = False
        self.fade_text_to_continue_duration = 1.5
        self.text_to_continue_timer = 0.0

        self.click_count = 0

        self.text_to_continue = arcade.Text(
            text=LANGUAGES['press_for_cont'][self.language],
            x=self.window.width // 2,
            y=self.window.height * 0.15,
            color=(255, 255, 255, 0),
            font_size=28,
            font_name='Montserrat',
            batch=self.batch,
            anchor_x='center'
        )

        self.original_font_size_text_to_continue = 28

    def setup(self):
        """Инициализация представления"""
        self.language = self.window.language
        self.create_overlay()
        self.load_background()
        self.wind_sound_player = self.wind_sound.play()

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        self.setup()
        self.timer = 0.0
        self.text_to_continue_timer = 0.0
        self.click_count = 0
        self.isTextToContinue = False

    def on_draw(self):
        """Рисование"""
        self.clear()

        self.background_sprite_list.draw()
        self.overlay_sprite_list.draw()

        self.batch.draw()

    def on_update(self, delta_time):
        """Обновление логики"""
        self.timer += delta_time

        if self.overlay and self.timer <= self.fade_background_duration:
            pr1 = self.timer / self.fade_background_duration
            eased_pr1 = 1 - math.pow(1 - pr1, 3)
            alpha1 = int(255 * (1.0 - eased_pr1))
            alpha1 = max(0, min(255, alpha1))
            self.overlay.color = (0, 0, 0, alpha1)

        if self.isTextToContinue:
            self.text_to_continue_timer += delta_time
            pr2 = self.text_to_continue_timer / self.fade_text_to_continue_duration
            alpha2 = int(255 * pr2)
            self.text_to_continue.color = (
                255, 255, 255, max(0, min(255, alpha2)))

        if self.timer >= self.fade_background_duration + 2.0 and not self.isTextToContinue:
            self.isTextToContinue = True

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        self.update_overlay_position_and_size()
        self.update_background_position_and_size()
        self.update_text_to_continue_position_and_size()

    def on_mouse_press(self, x, y, button, modifiers):
        self.wind_sound.stop(self.wind_sound_player)
        self.window.switch_view('main_menu')

    def on_key_press(self, symbol, modifiers):
        self.wind_sound.stop(self.wind_sound_player)
        self.window.switch_view('main_menu')

    def load_background(self):
        texture = self.reg.get(
            'common/textures/backgrounds/main_menu_background.png')
        self.background_sprite = arcade.Sprite(
            path_or_texture=texture,
            center_x=self.window.width // 2,
            center_y=self.window.height // 2
        )

        self.background_sprite_list.append(self.background_sprite)

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

    def update_overlay_position_and_size(self):
        if not self.overlay:
            return

        self.overlay.width = self.window.width
        self.overlay.height = self.window.height
        self.overlay.center_x = self.window.width // 2
        self.overlay.center_y = self.window.height // 2

    def update_background_position_and_size(self):
        if not self.background_sprite:
            return

        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2

    def update_text_to_continue_position_and_size(self):
        self.text_to_continue.x = self.window.width // 2
        self.text_to_continue.y = self.window.height * 0.15

        width_scale = self.window.width / self.original_width
        height_scale = self.window.height / self.original_height
        scale_factor = min(width_scale, height_scale)

        new_font_size = int(
            self.original_font_size_text_to_continue * scale_factor)
        new_font_size = max(12, min(new_font_size, 48))
        self.text_to_continue.font_size = new_font_size
