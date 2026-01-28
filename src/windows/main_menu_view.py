import arcade
from arcade.gui import UIManager, UITextureButton, UIAnchorLayout, UIBoxLayout
from src.settings import settings
from src.registry import reg
from resources.languages import LANGUAGES


class MainMenuView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window

        self.original_width = settings.width
        self.original_height = settings.height

        self.language: int = window.language

        self.timer = 0.0

        self.reg = reg

        self.ui_manager = UIManager()

        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None

        self.hero_sprite = None
        self.hero_textures = {}
        self.hero_direction = 'front'
        self.hero_scale = 0.5
        self.hero_sprite_list = arcade.SpriteList()

        self.keys_pressed = {
            arcade.key.W: False,
            arcade.key.A: False,
            arcade.key.S: False,
            arcade.key.D: False
        }

        self.button_textures = {
            'normal': self.reg.get('common/textures/ui/buttons/normal/main_menu_button.png'),
            'hovered': self.reg.get('common/textures/ui/buttons/hovered/main_menu_button.png'),
            'pressed': self.reg.get('common/textures/ui/buttons/pressed/main_menu_button.png')
        }

        self.button_width = self.button_textures['normal'].width * 2.7
        self.button_height = self.button_textures['normal'].height * 2.7
        self.spacing_between_buttons = 20

        self.original_font_size = 28

        self.ui_buttons = []
        self.hovered_sound = True

        self.fade_in = True
        self.fade_timer = 0.0
        self.fade_duration = 1.0
        self.fade_alpha = 255

        self.transition_to_other = False
        self.transition_timer = 0.0
        self.transition_duration = 1.0
        self.transition_alpha = 0
        self.transition_target = None

    def setup(self):
        self.ui_manager.enable()
        self.language = self.window.language
        self.background_sprite_list.clear()
        self.hero_sprite_list.clear()
        self.load_background()
        self.load_hero()
        self.create_buttons()

        for key in self.keys_pressed:
            self.keys_pressed[key] = False

        self.fade_in = True
        self.fade_timer = 0.0
        self.fade_alpha = 255

        self.transition_to_other = False
        self.transition_timer = 0.0
        self.transition_alpha = 0
        self.transition_target = None

    def on_show_view(self):
        self.setup()
        self.ui_manager.trigger_render()
        self.timer = 0.0

    def on_hide_view(self):
        self.ui_manager.disable()

    def on_draw(self):
        self.clear()

        self.background_sprite_list.draw()

        self.hero_sprite_list.draw()

        self.ui_manager.on_resize(self.window.width, self.window.height)
        self.ui_manager.draw()

        if self.fade_alpha > 0 and not self.transition_to_other:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.window.width,
                bottom=0,
                top=self.window.height,
                color=(0, 0, 0, self.fade_alpha)
            )

        if self.transition_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.window.width,
                bottom=0,
                top=self.window.height,
                color=(0, 0, 0, self.transition_alpha)
            )

    def on_update(self, delta_time):
        if self.transition_to_other:
            self.transition_timer += delta_time
            progress = min(self.transition_timer /
                           self.transition_duration, 1.0)
            self.transition_alpha = int(255 * progress)

            if progress >= 1.0 and self.transition_target:
                self.window.switch_view(self.transition_target)
            return

        self.update_hero_direction()

        if self.fade_in and not self.transition_to_other:
            self.fade_timer += delta_time
            progress = min(self.fade_timer / self.fade_duration, 1.0)
            self.fade_alpha = int(255 * (1 - progress))

            if progress >= 0.5:
                self._start_music_if_needed()

            if progress >= 1.0:
                self.fade_in = False
        else:
            self._start_music_if_needed()

        if any([button.hovered for button in self.ui_buttons]):
            if not self.hovered_sound:
                self.window.play_definite_music(
                    'common/sounds/sfx/ui/on_button_hover.wav')
                self.hovered_sound = True
        elif not all([button.hovered for button in self.ui_buttons]):
            self.hovered_sound = False

    def _start_music_if_needed(self):
        music_key = 'common/sounds/music/main_theme.ogg'

        if music_key not in self.window.music_players.keys():
            self.window.forced_music[music_key] = [{
                'path': music_key,
                'volume': 1.0,
                'isLooping': True
            }, True]

            self.window.play_definite_music(
                path=music_key,
                volume=1.0,
                isLooping=True
            )

    def load_hero(self):
        self.hero_textures = {
            'front': self.reg.get('common/textures/ui/menu_guy/front_side_guy.png'),
            'left': self.reg.get('common/textures/ui/menu_guy/left_side_guy.png'),
            'right': self.reg.get('common/textures/ui/menu_guy/right_side_guy.png'),
            'up': self.reg.get('common/textures/ui/menu_guy/up_side_guy.png'),
            'down': self.reg.get('common/textures/ui/menu_guy/down_side_guy.png'),
        }

        # Создаем спрайт героя
        self.hero_sprite = arcade.Sprite(
            path_or_texture=self.hero_textures['front'],
            center_x=self.window.width * 0.87,
            center_y=self.window.height // 5,
            scale=self.hero_scale
        )

        self.hero_sprite_list.append(self.hero_sprite)
        self.hero_direction = 'front'

    def update_hero_direction(self):
        if self.keys_pressed[arcade.key.W]:
            self.hero_direction = 'up'
        elif self.keys_pressed[arcade.key.S]:
            self.hero_direction = 'down'
        elif self.keys_pressed[arcade.key.A]:
            self.hero_direction = 'left'
        elif self.keys_pressed[arcade.key.D]:
            self.hero_direction = 'right'
        else:
            self.hero_direction = 'front'

        if self.hero_sprite and self.hero_direction in self.hero_textures:
            self.hero_sprite.texture = self.hero_textures[self.hero_direction]

    def on_key_press(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed[key] = True

        if key == arcade.key.ESCAPE:
            arcade.exit()

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed[key] = False

    def on_resize(self, width: float, height: float):
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.update_hero_position()
        self.create_buttons()

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

    def update_hero_position(self):
        if self.hero_sprite:
            self.hero_sprite.center_x = self.window.width // 2
            self.hero_sprite.center_y = self.window.height // 3

    def create_buttons(self):
        self.ui_manager.clear()
        self.ui_buttons.clear()

        win_w = self.window.width
        win_h = self.window.height

        scale_x = win_w / self.original_width
        scale_y = win_h / self.original_height

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
            width=win_w,
            height=win_h
        )
        anchor.add(box, anchor_x='center', anchor_y='center')

        self.ui_manager.add(anchor)

        anchor.do_layout()

        self.ui_buttons.append(play_button)
        self.ui_buttons.append(settings_button)

    def update_background_position_and_size(self):
        if not self.background_sprite:
            return

        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2

    def on_play_click(self, event):
        if not self.transition_to_other:
            self.transition_to_other = True
            self.transition_timer = 0.0
            self.transition_target = 'levels_window'
            self.transition_alpha = 0

    def on_settings_click(self, event):
        if not self.transition_to_other:
            self.transition_to_other = True
            self.transition_timer = 0.0
            self.transition_target = 'settings_window'
            self.transition_alpha = 0
