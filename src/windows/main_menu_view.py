import arcade
import math
from pyglet.graphics import Batch
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout
from src.settings import settings
from src.registry import reg
from resources.languages import LANGUAGES


class MainMenuView(arcade.View):
    """Главное меню игры"""

    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window  # Ссылка на главное окно

        self.original_width = settings.width
        self.original_height = settings.height

        self.language: int = window.language

        self.timer = 0.0

        self.reg = reg

        self.batch = Batch()

        self.ui_manager = UIManager()

        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None

        self.button_textures = {
            'normal': self.reg.get('textures/ui/buttons/normal/main_menu_button.png'),
            'hovered': self.reg.get('textures/ui/buttons/hovered/main_menu_button.png'),
            'pressed': self.reg.get('textures/ui/buttons/pressed/main_menu_button.png')
        }

        self.button_width = self.button_textures['normal'].width * 2.7
        self.button_height = self.button_textures['normal'].height * 2.7
        self.spacing_between_buttons = 20

        self.original_font_size = 28

        self.ui_buttons = []
        self.hovered_sound = False

        self.window.forced_music['sounds/music/main_theme.ogg'] = {
            'path': 'sounds/music/main_theme.ogg',
            'volume': 1.0,
            'isLooping': True
        }

        self.window.play_definite_music(
            self.window.forced_music['sounds/music/main_theme.ogg']['path'],
            self.window.forced_music['sounds/music/main_theme.ogg']['volume'],
            self.window.forced_music['sounds/music/main_theme.ogg']['isLooping']
        )

    def setup(self):
        """Инициализация представления"""
        self.language = self.window.language
        self.load_background()
        self.ui_manager.enable()
        self.create_buttons()

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        self.setup()
        self.timer = 0.0

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        """Рисование"""
        self.clear()

        self.background_sprite_list.draw()

        self.ui_manager.draw()

    def on_update(self, delta_time):
        """Обновление логики"""
        self.timer += delta_time

        if any([button.hovered for button in self.ui_buttons]):
            if not self.hovered_sound:
                self.window.play_definite_music(
                    'sounds/sfx/ui/on_button_hover.wav')
                self.hovered_sound = True
        elif not all([button.hovered for button in self.ui_buttons]):
            self.hovered_sound = False

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.create_buttons()

    def load_background(self):
        texture = self.reg.get('textures/backgrounds/main_menu_background.png')

        self.background_sprite = arcade.Sprite(
            path_or_texture=texture,
            center_x=self.window.width // 2,
            center_y=self.window.height // 2
        )

        self.background_sprite_list.append(self.background_sprite)

        self.update_background_position_and_size()

    def create_buttons(self):
        self.ui_manager.clear()
        self.ui_buttons.clear()

        scale_x = self.window.width / self.original_width
        scale_y = self.window.height / self.original_height

        scale = min(scale_x, scale_y)

        button_width = int(self.button_width * scale)
        button_height = int(self.button_height * scale)
        spacing = int(self.spacing_between_buttons * scale)

        font_size = int(self.original_font_size * scale)
        font_size = max(20, min(40, font_size))

        font_name = 'montserrat'
        normal_color = (29, 5, 59, 255)
        hover_color = (45, 16, 82, 255)

        button_style = {
            "normal": UITextureButton.UIStyle(
                font_name=font_name,
                font_size=font_size,
                font_color=normal_color
            ),
            "hover": UITextureButton.UIStyle(
                font_name=font_name,
                font_size=font_size,
                font_color=hover_color
            ),
            "press": UITextureButton.UIStyle(
                font_name=font_name,
                font_size=font_size,
                font_color=normal_color
            ),
            "disabled": UITextureButton.UIStyle(
                font_name=font_name,
                font_size=font_size,
                font_color=(128, 128, 128, 255)
            )
        }

        box = UIBoxLayout(
            vertical=True,
            align='center',
            space_between=spacing)

        play_button = UITextureButton(
            texture=self.button_textures['normal'],
            texture_hovered=self.button_textures['hovered'],
            texture_pressed=self.button_textures['pressed'],
            width=button_width,
            height=button_height,
            text=LANGUAGES['play_button'][self.language],
            style=button_style
        )

        settings_button = UITextureButton(
            texture=self.button_textures['normal'],
            texture_hovered=self.button_textures['hovered'],
            texture_pressed=self.button_textures['pressed'],
            width=button_width,
            height=button_height,
            text=LANGUAGES['settings_button'][self.language],
            style=button_style
        )

        play_button.on_click = self.on_play_click
        settings_button.on_click = self.on_settings_click

        box.add(play_button)
        box.add(settings_button)

        anchor = UIAnchorLayout(
            width=self.window.width,
            height=self.window.height
        )
        anchor.add(box, anchor_x='center', anchor_y='center')

        self.ui_manager.add(anchor)

        self.ui_buttons.append(play_button)
        self.ui_buttons.append(settings_button)

    def on_play_click(self, event):
        print('play')
        self.window.switch_view('levels_window')

    def on_settings_click(self, event):
        print('settings')
        self.window.switch_view('settings_window')

    def update_background_position_and_size(self):
        if not self.background_sprite:
            return

        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2
