import arcade
from pyglet.graphics import Batch
from resources.languages import LANGUAGES
from arcade.gui import *
from src.settings import settings
from src.registry import reg


class SettingsMenuView(arcade.View):

    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
        self.language: int = self.window.language

        self.batch = Batch()

        self.reg = reg

        self.texts = {
            'title': LANGUAGES['settings_button'][self.language],
            'press_to_return': LANGUAGES['Esc_to_return'][self.language],
            'change_language': LANGUAGES['change_language'][self.language],
            'music': LANGUAGES['music'][self.language]
        }

        # Элементы UI
        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None

        self.ui_manager = UIManager()
        self.ui_manager.enable()

        # Текстовые объекты
        self.title_text = None
        self.return_text = None
        self.change_language_text = None
        self.language_text = None

        # Все текстовые объекты будем хранить в списке
        self.text_objects = []

    def create_lang_dropdown(self):
        self.ui_manager.clear()

        center_x = self.window.width // 2
        center_y = self.window.height // 2

        offset_x = -120
        offset_y = 80

        pos_x = center_x + offset_x
        pos_y = center_y + offset_y

        options = [
            LANGUAGES['language'][0],
            LANGUAGES['language'][1],
            LANGUAGES['language'][2]
        ]

        self.lang_dropdown = UIDropdown(
            x=pos_x,
            y=pos_y,
            default=LANGUAGES['language'][self.language],
            options=options,
            width=200,
            height=45,
        )

        self.ui_manager.add(self.lang_dropdown)

        @self.lang_dropdown.event('on_change')
        def on_language_change(event: UIOnChangeEvent):
            if event.new_value == LANGUAGES['language'][0]:
                self.language = 0
            elif event.new_value == LANGUAGES['language'][1]:
                self.language = 1
            elif event.new_value == LANGUAGES['language'][2]:
                self.language = 2

            self.window.language = self.language

            with open('data/language.txt', 'w') as lang:
                lang.write(next((key for key, value in settings.lang_dict.items(
                ) if value == self.language), 'russian'))

            self.update_text_position_and_size_and_lang()

    def setup(self):
        self.load_background()

        self.text_objects.clear()

        self.create_lang_dropdown()

        self.title_text = arcade.Text(
            text=self.texts['title'],
            x=self.window.width // 1.4,
            y=self.window.height * 0.8,
            color=arcade.color.BLACK,
            font_size=32,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.title_text)

        self.return_text = arcade.Text(
            text=self.texts['press_to_return'],
            x=self.window.width // 2,
            y=self.window.height * 0.02,
            color=arcade.color.BLACK,
            font_size=18,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.return_text)

        self.change_language_text = arcade.Text(
            text=self.texts['change_language'],
            x=self.window.width // 4.1,
            y=self.window.height * 0.71,
            color=arcade.color.BLACK,
            font_size=28,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.change_language_text)

        self.music_text = arcade.Text(
            text=self.texts['music'],
            x=self.window.width // 3.15,
            y=self.window.height * 0.51,
            color=arcade.color.BLACK,
            font_size=18,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.music_text)

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()

        if self.background_sprite_list:
            self.background_sprite_list.draw()

        self.batch.draw()

        self.ui_manager.draw()

    def on_key_press(self, symbol, modifiers):
        """Обработка нажатия клавиш"""
        if symbol == arcade.key.ESCAPE:
            self.window.switch_view("main_menu")

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.update_text_position_and_size_and_lang()
        self.create_lang_dropdown()

    def load_background(self):
        """Загрузка фона"""

        texture = self.reg.get(
            'textures/backgrounds/settings_background.png')
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

    def update_text_position_and_size_and_lang(self):
        self.texts = {
            'title': LANGUAGES['settings_button'][self.language],
            'press_to_return': LANGUAGES['Esc_to_return'][self.language],
            'change_language': LANGUAGES['change_language'][self.language],
            'music': LANGUAGES['music'][self.language]
        }

        self.title_text.text = self.texts['title']
        self.title_text.x = self.window.width // 1.4
        self.title_text.y = self.window.height * 0.8

        self.return_text.text = self.texts['press_to_return']
        self.return_text.x = self.window.width // 2
        self.return_text.y = self.window.height * 0.02

        self.change_language_text.text = self.texts['change_language']
        self.change_language_text.x = self.window.width // 4.1
        self.change_language_text.y = self.window.height * 0.71

        self.music_text.text = self.texts['music']
        self.music_text.x = self.window.width // 3.15
        self.music_text.y = self.window.height * 0.51
