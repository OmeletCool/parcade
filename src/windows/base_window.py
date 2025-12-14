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

        return self.views[view_name]

    def switch_view(self, view_name):
        view = self.get_view(view_name)

        self.show_view(view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.Q:
            self.close()
