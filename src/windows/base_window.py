import arcade
from src.settings import settings


class BaseWindow(arcade.Window):

    def __init__(self):
        super().__init__(settings.width, settings.height, settings.title,
                         resizable=settings.resizable, fullscreen=settings.fullscreen)
        self.set_minimum_size(settings.width_min,
                              settings.height_min)
        self.center_window()
        self.background_color = arcade.color.BLACK
        self.language = settings.language

        self.background_music = None
        self.music_player = None
        self.is_music_playing = False

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

        return self.views[view_name]

    def switch_view(self, view_name):
        view = self.get_view(view_name)

        self.show_view(view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.close()

    def play_background_music(self):
        if not self.is_music_playing:
            self.background_music = arcade.load_sound(
                'resources/sounds/music/main_theme.ogg')
            self.music_player = arcade.play_sound(
                self.background_music, loop=True)
            self.is_music_playing = True

    def stop_background_music(self):
        if self.music_player:
            arcade.stop_sound(self.music_player)
            self.is_music_playing = False
            self.music_player = None
