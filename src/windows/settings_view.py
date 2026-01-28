import arcade
from arcade.gui import *
from src.settings import settings
from src.registry import reg
from resources.languages import LANGUAGES


class SettingsMenuView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
        self.language: int = self.window.language

        self.original_width = settings.width
        self.original_height = settings.height

        self.reg = reg
        self.ui_manager = UIManager()
        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None

        self.fade_in = True
        self.fade_timer = 0.0
        self.fade_duration = 1.0
        self.fade_alpha = 255

        self.transition_to_menu = False
        self.transition_timer = 0.0
        self.transition_duration = 1.0
        self.transition_alpha = 0

        self.transition_to_other = False
        self.other_target = None

        self.music_button_text = "ON" if self.window.music_enabled else "OFF"

    def setup(self):
        self.ui_manager.enable()
        self.load_background()
        self.create_ui()

        self.fade_in = True
        self.fade_timer = 0.0
        self.fade_alpha = 255
        self.transition_to_menu = False
        self.transition_timer = 0.0
        self.transition_alpha = 0
        self.transition_to_other = False
        self.other_target = None

    def create_ui(self):
        self.ui_manager.clear()

        win_w, win_h = self.window.width, self.window.height
        sw = win_w / self.original_width
        sh = win_h / self.original_height
        m_scale = min(sw, sh)

        font_name = 'Montserrat'

        invisible_style = {
            "normal": UIFlatButton.UIStyle(font_name=font_name, font_color=arcade.color.BLACK, bg=(0, 0, 0, 0), font_size=16),
            "hover": UIFlatButton.UIStyle(font_name=font_name, font_color=arcade.color.BLACK, bg=(0, 0, 0, 0), font_size=17),
            "press": UIFlatButton.UIStyle(font_name=font_name, font_color=arcade.color.BLACK, bg=(0, 0, 0, 0), font_size=16)
        }

        title_label = UILabel(
            text=LANGUAGES['settings_button'][self.language],
            x=win_w * 0.5 - (100 * sw),
            y=win_h * 0.8,
            width=200 * sw,
            font_size=int(28 * m_scale),
            font_name=font_name,
            text_color=(0, 0, 0),
            align="center"
        )
        self.ui_manager.add(title_label)

        lang_header = UILabel(
            text=LANGUAGES['change_language'][self.language],
            x=win_w * 0.085,
            y=win_h * 0.68,
            width=200 * sw,
            font_size=int(18 * m_scale),
            font_name=font_name,
            text_color=(0, 0, 0),
            align="center"
        )
        lang_btn = UIFlatButton(
            x=win_w * 0.11, y=win_h * 0.61,
            width=int(140 * sw), height=int(50 * sh),
            text=LANGUAGES['language'][self.language],
            style=invisible_style
        )

        @lang_btn.event("on_click")
        def on_lang_click(event):
            self.language = (self.language + 1) % 3
            self.window.language = self.language
            lang_dict = {
                0: 'english',
                1: 'russian',
                2: 'albanian'
            }
            with open('data/language.txt', 'w') as lang:
                lang.write(lang_dict[self.language])
            self.create_ui()

        self.ui_manager.add(lang_header)
        self.ui_manager.add(lang_btn)

        music_header = UILabel(
            text=LANGUAGES['music'][self.language],
            x=win_w * 0.243,
            y=win_h * 0.37,
            width=150 * sw,
            font_size=int(17 * m_scale),
            font_name=font_name,
            text_color=(0, 0, 0),
            align="center"
        )
        music_btn = UIFlatButton(
            x=win_w * 0.26, y=win_h * 0.3,
            width=int(100 * sw), height=int(40 * sh),
            text=self.music_button_text,
            style=invisible_style
        )

        @music_btn.event("on_click")
        def on_music_click(event):
            self.toggle_music()
            music_btn.text = self.music_button_text

        self.ui_manager.add(music_header)
        self.ui_manager.add(music_btn)

        creators_btn = UIFlatButton(
            x=win_w * 0.58, y=win_h * 0.25,
            width=int(170 * sw), height=int(60 * sh),
            text=LANGUAGES['creators'][self.language],
            style=invisible_style
        )
        creators_btn.on_click = lambda _: self._go_to_creators()
        self.ui_manager.add(creators_btn)

        glossary_btn = UIFlatButton(
            x=win_w * 0.76, y=win_h * 0.3,
            width=int(160 * sw), height=int(55 * sh),
            text=LANGUAGES['Glossary'][self.language],
            style=invisible_style
        )
        glossary_btn.on_click = lambda _: self._go_to_glossary()
        self.ui_manager.add(glossary_btn)

        esc_label = UILabel(
            text=LANGUAGES['Esc_to_return'][self.language],
            x=win_w * 0.4,
            y=win_h * 0.03,
            width=200 * sw,
            font_size=int(16 * m_scale),
            font_name=font_name,
            text_color=arcade.color.WHITE,
            align="center"
        )
        self.ui_manager.add(esc_label)

    def _go_to_creators(self):
        if not self.transition_to_other:
            self.transition_to_other = True
            self.transition_timer = 0.0
            self.other_target = 'creators_window'
            self.transition_alpha = 0

    def _go_to_glossary(self):
        if not self.transition_to_other:
            self.transition_to_other = True
            self.transition_timer = 0.0
            self.other_target = 'glossary_window'
            self.transition_alpha = 0

    def toggle_music(self):
        if self.window.music_enabled:
            self.window.disable_music()
            self.music_button_text = "OFF"
        else:
            self.window.enable_music()
            self.music_button_text = "ON"

        self.create_ui()

    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw()
        self.ui_manager.draw()

        # Рисуем затемнение для плавного появления
        if self.fade_alpha > 0 and not self.transition_to_menu and not self.transition_to_other:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.window.width,
                bottom=0,
                top=self.window.height,
                color=(0, 0, 0, self.fade_alpha)
            )

        # Рисуем затемнение для плавного ухода
        if self.transition_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.window.width,
                bottom=0,
                top=self.window.height,
                color=(0, 0, 0, self.transition_alpha)
            )

    def on_show_view(self):
        self.setup()

    def on_update(self, delta_time):
        if self.transition_to_menu:
            self.transition_timer += delta_time
            progress = min(self.transition_timer /
                           self.transition_duration, 1.0)
            self.transition_alpha = int(255 * progress)

            if progress >= 1.0:
                self.window.save_music_setting()
                self.window.switch_view("main_menu")
            return

        if self.transition_to_other and self.other_target:
            self.transition_timer += delta_time
            progress = min(self.transition_timer /
                           self.transition_duration, 1.0)
            self.transition_alpha = int(255 * progress)

            if progress >= 1.0:
                self.window.switch_view(self.other_target)
            return

        # Плавное появление
        if self.fade_in and not self.transition_to_menu and not self.transition_to_other:
            self.fade_timer += delta_time
            progress = min(self.fade_timer / self.fade_duration, 1.0)
            self.fade_alpha = int(255 * (1 - progress))

            if progress >= 1.0:
                self.fade_in = False

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE and not self.transition_to_menu and not self.transition_to_other:
            self.transition_to_menu = True
            self.transition_timer = 0.0
            self.transition_alpha = 0

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.create_ui()

    def load_background(self):
        texture = self.reg.get(
            'common/textures/backgrounds/settings_background.jpg')
        self.background_sprite = arcade.Sprite(path_or_texture=texture)
        self.background_sprite_list.clear()
        self.background_sprite_list.append(self.background_sprite)
        self.update_background_position_and_size()

    def update_background_position_and_size(self):
        """Обновляет позицию и размер фонового изображения"""
        if self.background_sprite:
            self.background_sprite.width = self.window.width
            self.background_sprite.height = self.window.height
            self.background_sprite.center_x = self.window.width // 2
            self.background_sprite.center_y = self.window.height // 2
