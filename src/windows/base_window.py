import arcade
from src.settings import settings
from src.registry import reg
import pyglet


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

        self.set_icon(pyglet.image.load(
            "resources/common/textures/ui/icons/icon.jpg"))

        self.background_music = None
        self.music_players = {}
        self.forced_music = {}
        self.is_music_playing = False
        self.music_enabled = False
        self.load_music_setting()

        # Храним представления
        self.views = {}

    def get_view(self, view_name):

        if view_name not in self.views:
            if view_name == "main_menu":
                from src.windows.main_menu_view import MainMenuView
                self.views[view_name] = MainMenuView(self)
            elif view_name == 'levels_window':
                from src.windows.levels_view import LevelsView
                self.views[view_name] = LevelsView(self)
            elif view_name == 'start_window':
                from src.windows.start_view import StartView
                self.views[view_name] = StartView(self)
            elif view_name == 'creators_window':
                from src.windows.creators_view import CreatorsView
                self.views[view_name] = CreatorsView(self)
            elif view_name == 'glossary_window':
                from src.windows.glossary_view import GlossaryView
                self.views[view_name] = GlossaryView(self)
            elif view_name == 'settings_window':
                from src.windows.settings_view import SettingsMenuView
                self.views[view_name] = SettingsMenuView(self)
            elif view_name == 'demo_game_view':
                from src.windows.game_view import DemoGameView
                self.views[view_name] = DemoGameView(self)

        return self.views[view_name]

    def switch_view(self, view_name):
        # if view_name == 'settings_window':
        #     from src.windows.settings_view import SettingsMenuView
        #     current_view = self.current_view
        #     view = SettingsMenuView(self, current_view)
        #     self.show_view(view)
        #     return

        if type(view_name) == list and view_name[0] == 'loading_view':
            from src.windows.loading_view import LoadingView
            loading_view = LoadingView(
                window=self,
                next_view_name=view_name[1],
                load_tag=view_name[2]
            )
            self.show_view(loading_view)
            return

        view = self.get_view(view_name)

        self.show_view(view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.close()

    def play_definite_music(self, path: str, volume=1.0, isLooping=False):
        if self.music_enabled:
            self.music_players[path] = arcade.play_sound(
                self.reg.get(path), volume, isLooping)

    def stop_definite_music(self, path: str):
        if self.music_players[path]:
            arcade.stop_sound(self.music_players[path])
            self.music_players.pop(path)

    def disable_music(self):
        if self.music_enabled:
            for player in self.music_players.values():
                arcade.stop_sound(player)

            self.music_players.clear()
            self.music_enabled = False

    def enable_music(self):
        if not self.music_enabled:
            self.music_enabled = True
            if self.forced_music:
                for music in self.forced_music.values():
                    self.music_players[music['path']] = arcade.play_sound(
                        self.reg.get(music['path']), music['volume'], loop=music['isLooping'])

    def load_music_setting(self):
        with open('data/music.txt', 'r') as music_file:
            setting = music_file.read().strip()
            self.music_enabled = (setting == "ON")
        self.save_music_setting()

    def save_music_setting(self):
        with open('data/music.txt', 'w') as music_file:
            music_file.write("ON" if self.music_enabled else "OFF")
