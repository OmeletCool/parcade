import arcade
from src.settings import settings
from src.registry import reg


class BaseWindow(arcade.Window):

    def __init__(self):
        super().__init__(settings.width, settings.height, settings.title,
                         resizable=settings.resizable, fullscreen=settings.fullscreen)
        self.set_minimum_size(settings.width_min,
                              settings.height_min)
        self.center_window()
        self.background_color = arcade.color.BLACK
        self.language = settings.language

        self.reg = reg

        self.background_music = None
        self.music_player = None
        self.is_music_playing = False
        self.music_enabled = True

        # Храним представления
        self.views = {}

    def get_view(self, view_name):

        if view_name not in self.views:
            if view_name == "main_menu":
                from src.windows.main_menu_view import MainMenuView
                self.views[view_name] = MainMenuView(self)
            elif view_name == 'settings_window':
                from src.windows.settings_window import SettingsMenuView
                self.views[view_name] = SettingsMenuView(self)
            elif view_name == 'levels_window':
                from src.windows.levels_window import LevelsView
                self.views[view_name] = LevelsView(self)
            elif view_name == 'start_window':
                from src.windows.start_window import StartView
                self.views[view_name] = StartView(self)
            elif view_name == 'creators_window':
                from src.windows.creators_window import CreatorsView
                self.views[view_name] = CreatorsView(self)

        return self.views[view_name]

    def switch_view(self, view_name):
        view = self.get_view(view_name)

        self.show_view(view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.close()

    def play_background_music(self):
        if not self.is_music_playing and self.music_enabled:
            self.background_music = self.reg.get(
                'sounds/music/main_theme.ogg')
            self.music_player = arcade.play_sound(
                self.background_music, loop=True, volume=1.0)
            self.is_music_playing = True

    def stop_background_music(self):
        if self.music_player:
            arcade.stop_sound(self.music_player)
            self.is_music_playing = False
            self.music_player = None
    def enable_music(self):
        self.music_enabled = True
        self.play_background_music()

    def disable_music(self):
        self.music_enabled = False
        self.stop_background_music()

    def load_music_setting(self):
        try:
            with open('data/music.txt', 'r') as music_file:
                setting = music_file.read().strip()
                self.music_enabled = (setting == "ON")
                print(f"Загружена настройка музыки: {setting}")
        except FileNotFoundError:
            self.music_enabled = True
            print("Файл настроек музыки не найден, использую настройки по умолчанию (ON)")
            self.save_music_setting()

    def save_music_setting(self):
        with open('data/music.txt', 'w') as music_file:
            music_file.write("ON" if self.music_enabled else "OFF")
            print(f"Сохранена настройка музыки: {'ON' if self.music_enabled else 'OFF'}")