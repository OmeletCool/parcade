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
            'music': LANGUAGES['music'][self.language],
            'creators': LANGUAGES['creators'][self.language],
            'glossary': LANGUAGES['Glossary'][self.language]
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
        self.creators_text = None
        self.glossary_text = None
        self.music_button = None
        self.music_button_text = "ON" 

        # Все текстовые объекты будем хранить в списке
        self.text_objects = []
        
    def create_music_button(self):
        music_x = self.window.width // 3.7
        music_y = self.window.height * 0.39 - 60
        
        style = {
            "normal": UIFlatButton.UIStyle(
                font_name='montserrat',
                font_size=16,
                font_color=arcade.color.BLACK,
                bg=(0, 0, 0, 0),
            ),
            "hover": UIFlatButton.UIStyle(
                font_name='montserrat',
                font_size=16,
                font_color=arcade.color.BLACK,
                bg=(245, 245, 220, 255),
            ),
            "press": UIFlatButton.UIStyle(
                font_name='montserrat',
                font_size=16,
                font_color=arcade.color.BLACK,
                bg=(245, 245, 220, 255),
            )
        }
        
        self.music_button = UIFlatButton(
            x=music_x,
            y=music_y,
            width=80,
            height=35,
            text=self.music_button_text,
            style=style
        )
        
        @self.music_button.event("on_click")
        def on_music_button_click(event):
            self.toggle_music()
        
        return self.music_button

    def toggle_music(self):
        if self.window.music_enabled:
            self.window.disable_music()
            self.music_button_text = "OFF"
        else:
            self.window.enable_music()
            self.music_button_text = "ON"
        
        if self.music_button:
            self.music_button.text = self.music_button_text
        
        self.window.save_music_setting()

    def enable_music(self):
        # Включить всю музыку в игре
        if hasattr(self.window, 'main_theme'):
            self.window.background_music.play()
            self.window.background_music.volume = 1.0
        
        print("Музыка включена")

    def disable_music(self):
        # Выключить всю музыку в игре
        if hasattr(self.window, 'main_theme'):
            self.window.background_music.pause()
            self.window.background_music.volume = 0.0

        
        print("Музыка выключена")

    def save_music_setting(self):
        with open('data/music.txt', 'w') as music_file:
            music_file.write("ON" if self.music_enabled else "OFF")

    def load_music_setting(self):
        try:
            with open('data/music.txt', 'r') as music_file:
                setting = music_file.read().strip()
                self.music_enabled = (setting == "ON")
                self.music_button_text = "ON" if self.music_enabled else "OFF"
        except FileNotFoundError:
            self.music_enabled = True
            self.music_button_text = "ON"
            self.save_music_setting()

    def create_creators_button(self):
        creators_x = self.window.width // 1.56
        creators_y = self.window.height * 0.27
        
        self.creators_button = UITextureButton(
            x=creators_x - 75,
            y=creators_y,
            width=150,
            height=45,
            texture=arcade.Texture.create_empty("transparent", (150, 45)),
            texture_hovered=arcade.Texture.create_empty("transparent_hover", (150, 45)),
            texture_pressed=arcade.Texture.create_empty("transparent_pressed", (150, 45))
        )
        
        @self.creators_button.event("on_click")
        def on_creators_click(event):
            self.on_creators_button_clicked()
        
        return self.creators_button

    def on_creators_button_clicked(self):
        self.window.switch_view('creators_window')
        
    def create_lang_button(self):
        center_x = self.window.width // 5.3
        center_y = self.window.height * 0.51

        offset_x = -120
        offset_y = 80

        pos_x = center_x + offset_x
        pos_y = center_y + offset_y

        # Создаем кнопку для языка
        self.lang_button = UIFlatButton(
            x=pos_x,
            y=pos_y,
            width=150,
            height=35,
            text=LANGUAGES['language'][self.language],
            style={
                "normal": UIFlatButton.UIStyle(
                    font_name='montserrat',
                    font_size=16,
                    font_color=arcade.color.BLACK,
                    bg=(0, 0, 0, 0),
                ),
                "hover": UIFlatButton.UIStyle(
                    font_name='montserrat',
                    font_size=16,
                    font_color=arcade.color.BLACK,
                    bg=(245, 245, 220, 255),
                ),
                "press": UIFlatButton.UIStyle(
                    font_name='montserrat',
                    font_size=16,
                    font_color=arcade.color.BLACK,
                    bg=(245, 245, 220, 255),
                )
            }
        )
        
        @self.lang_button.event("on_click")
        def on_lang_button_click(event):
            self.language = (self.language + 1) % 3
            
            self.lang_button.text = LANGUAGES['language'][self.language]
            
            self.window.language = self.language
            
            with open('data/language.txt', 'w') as lang:
                lang.write(next((key for key, value in settings.lang_dict.items(
                ) if value == self.language), 'russian'))
            
            self.update_texts()
        
        return self.lang_button
    
    def create_glossary_button(self):
        glossary_x = self.window.width // 1.22
        glossary_y = self.window.height * 0.325
        
        self.glossary_button = UITextureButton(
            x=glossary_x - 75,
            y=glossary_y,
            width=150,
            height=45,
            texture=arcade.Texture.create_empty("transparent", (150, 45)),
            texture_hovered=arcade.Texture.create_empty("transparent_hover", (150, 45)),
            texture_pressed=arcade.Texture.create_empty("transparent_pressed", (150, 45))
        )
        
        @self.glossary_button.event("on_click")
        def on_glossary_click(event):
            self.on_glossary_button_clicked()
        
        return self.glossary_button

    def on_glossary_button_clicked(self):
        self.window.switch_view('glossary_window')

    def update_texts(self):
        self.texts = {
            'title': LANGUAGES['settings_button'][self.language],
            'press_to_return': LANGUAGES['Esc_to_return'][self.language],
            'change_language': LANGUAGES['change_language'][self.language],
            'music': LANGUAGES['music'][self.language],
            'creators': LANGUAGES['creators'][self.language],
            'glossary': LANGUAGES['Glossary'][self.language]
        }
        
        # Обновляем каждый текстовый объект, если он существует
        if self.title_text:
            self.title_text.text = self.texts['title']
        if self.return_text:
            self.return_text.text = self.texts['press_to_return']
        if self.change_language_text:
            self.change_language_text.text = self.texts['change_language']
        if self.music_text:
            self.music_text.text = self.texts['music']
        if self.creators_text:
            self.creators_text.text = self.texts['creators']
        if self.glossary_text:
            self.glossary_text.text = self.texts['glossary']


    def create_lang_dropdown(self):
        self.ui_manager.clear()
        
        lang_button = self.create_lang_button()
        self.ui_manager.add(lang_button)
        
        creators_button = self.create_creators_button()
        self.ui_manager.add(creators_button)
        
        music_button = self.create_music_button()
        self.ui_manager.add(music_button)
        
        glossary_button = self.create_glossary_button()
        self.ui_manager.add(glossary_button) 

    def setup(self):
        self.load_background()
        
        self.window.load_music_setting()
        self.music_button_text = "ON" if self.window.music_enabled else "OFF"

        self.text_objects.clear()
        
        # Создаем UI элементы
        self.create_lang_dropdown()

        self.title_text = arcade.Text(
            text=self.texts['title'],
            x=self.window.width // 2,
            y=self.window.height * 0.818,
            color=arcade.color.BLACK,
            font_size=30,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.title_text)

        self.return_text = arcade.Text(
            text=self.texts['press_to_return'],
            x=self.window.width // 2,
            y=self.window.height * 0.02,
            color=arcade.color.WHITE,
            font_size=18,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.return_text)

        self.change_language_text = arcade.Text(
            text=self.texts['change_language'],
            x=self.window.width // 6.45,
            y=self.window.height * 0.69,
            color=arcade.color.BLACK,
            font_size=20,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.change_language_text)

        self.music_text = arcade.Text(
            text=self.texts['music'],
            x=self.window.width // 3.353,
            y=self.window.height * 0.39,
            color=arcade.color.BLACK,
            font_size=16,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.music_text)
        
        self.creators_text = arcade.Text(
            text=self.texts['creators'],
            x=self.window.width // 1.56,
            y=self.window.height * 0.27,
            color=arcade.color.BLACK,
            font_size=24,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        self.text_objects.append(self.creators_text)
        
        self.glossary_text = arcade.Text(
            text=self.texts['glossary'],
            x=self.window.width // 1.22,
            y=self.window.height * 0.325,
            color=arcade.color.BLACK,
            font_size=18,
            font_name='montserrat',
            anchor_x='center',
            batch=self.batch
        )
        
        self.text_objects.append(self.glossary_text)
        

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()

        if self.background_sprite_list:
            self.background_sprite_list.draw()

        self.batch.draw()

        self.ui_manager.draw()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.ui_manager.on_mouse_press(x, y, button, modifiers)
        
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.ui_manager.on_mouse_release(x, y, button, modifiers)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.save_music_setting()
            self.window.switch_view("main_menu")

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.update_text_position_and_size_and_lang()
        self.create_lang_dropdown()

    def load_background(self):

        texture = self.reg.get(
            'textures/backgrounds/settings_background.jpg')
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
            'music': LANGUAGES['music'][self.language],
            'creators': LANGUAGES['creators'][self.language],
            'glossary': LANGUAGES['Glossary'][self.language]
        }

        self.title_text.text = self.texts['title']
        self.title_text.x = self.window.width // 2
        self.title_text.y = self.window.height * 0.818

        self.return_text.text = self.texts['press_to_return']
        self.return_text.x = self.window.width // 2
        self.return_text.y = self.window.height * 0.02

        self.change_language_text.text = self.texts['change_language']
        self.change_language_text.x = self.window.width // 6.45
        self.change_language_text.y = self.window.height * 0.69

        self.music_text.text = self.texts['music']
        self.music_text.x = self.window.width // 3.353
        self.music_text.y = self.window.height * 0.39

        self.creators_text.text = self.texts['creators']
        self.creators_text.x = self.window.width // 1.56
        self.creators_text.y = self.window.height * 0.27
    
        self.glossary_text.text = self.texts['glossary']
        self.glossary_text.x = self.window.width // 1.22
        self.glossary_text.y = self.window.height * 0.325
