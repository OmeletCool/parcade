import arcade
import math
from pyglet.graphics import Batch
from src.settings import settings
from src.registry import reg
from resources.languages import LANGUAGES


class MainMenuView(arcade.View):
    """Главное меню игры"""

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно

        self.language = window.language

        self.timer = 0.0

        self.batch = Batch()

        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None
        self.background_image_path = 'resources/textures/backgrounds/main_menu_background.png'

        self.overlay = None
        self.overlay_sprite_list = arcade.SpriteList()

        self.button_textures = {
            'normal': arcade.load_texture('resources/textures/ui/buttons/normal/main_menu_button.png'),
            'hovered': arcade.load_texture('resources/textures/ui/buttons/hovered/main_menu_button.png'),
            'pressed': arcade.load_texture('resources/textures/ui/buttons/pressed/main_menu_button.png')
        }

        self.button_width = self.button_textures['normal'].width * 2.7
        self.button_height = self.button_textures['normal'].height * 2.7
        self.spacing_between_buttons = 20

        self.btn_configs = []

        self.shadow_sprites = arcade.SpriteList()
        self.button_sprites = arcade.SpriteList()

        self.main_theme_audio = arcade.load_sound(
            'resources/sounds/music/main_theme.ogg')
        self.wind_sound = arcade.load_sound(
            'resources/sounds/sfx/ambient/wind.wav')

        self.fade_background_duration = self.wind_sound.get_length()
        self.isFading = True
        self.isTextToContinue = False

        self.isStarted = False
        self.text_to_continue_timer = 0.0
        self.text_to_continue = None
        self.fade_text_to_continue_duration = 1.5
        self.text_to_continue_alpha = 0

        self.click_count = 0

        arcade.load_font('resources/fonts/montserrat.ttf')

        self.create_overlay()
        self.wind_sound_player = self.wind_sound.play()

        self.text_to_continue = arcade.Text(
            text=LANGUAGES['press_for_cont'][self.language],
            x=self.window.width // 2,
            y=self.window.height * 0.15,
            color=(255, 255, 255, self.text_to_continue_alpha),
            font_size=28,
            font_name='montserrat',
            batch=self.batch,
            anchor_x='center'
        )

        self.load_background()
        self.create_button_configs()
        self.create_buttons()

        self.play_button_text = arcade.Text(
            self.btn_configs[0]['text'],
            self.btn_configs[0]['center_x'],
            self.btn_configs[0]['center_y'],
            self.btn_configs[0]['text_color'],
            28,
            anchor_x='center',
            font_name='montserrat',
            batch=self.batch
        )
        self.settings_button_text = arcade.Text(
            self.btn_configs[1]['text'],
            self.btn_configs[1]['center_x'],
            self.btn_configs[1]['center_y'],
            self.btn_configs[1]['text_color'],
            28,
            anchor_x='center',
            font_name='montserrat',
            batch=self.batch
        )

    def setup(self):
        """Инициализация представления"""
        # self.load_background()
        # self.create_button_configs()
        # self.create_buttons()

    def create_button_configs(self):
        total_height = (self.button_height * 2) + self.spacing_between_buttons

        start_y = self.window.height // 2 + \
            (total_height // 2) - (self.button_height // 2)

        btn_play = {
            'center_x': self.window.width // 2,
            'center_y': start_y,
            'state': 'normal',
            'width': self.button_width,
            'height': self.button_height,
            'type': 'play',
            'text': LANGUAGES['play_button'][self.language],
            'text_color': (29, 5, 59, 0)
        }
        btn_settings = {
            'center_x': self.window.width // 2,
            'center_y': start_y - self.button_height - self.spacing_between_buttons,
            'state': 'normal',
            'width': self.button_width,
            'height': self.button_height,
            'type': 'settings',
            'text': LANGUAGES['settings_button'][self.language],
            'text_color': (29, 5, 59, 0)
        }
        self.btn_configs = [
            btn_play,
            btn_settings
        ]

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        self.setup()
        self.timer = 0.0

    def on_draw(self):
        """Рисование"""
        self.clear()

        self.background_sprite_list.draw()
        if self.isFading:
            self.overlay_sprite_list.draw()

        if not self.isFading and self.click_count >= 1:
            self.shadow_sprites.draw()
            self.button_sprites.draw()
            self.batch.draw()

        if self.isTextToContinue:
            self.text_to_continue.color = (
                255, 255, 255, self.text_to_continue_alpha)
            self.batch.draw()

    def on_update(self, delta_time):
        """Обновление логики"""
        self.timer += delta_time

        if self.overlay and self.timer <= self.fade_background_duration:
            progress1 = self.timer / self.fade_background_duration
            eased_progress = 1 - math.pow(1 - progress1, 3)
            alpha = int(255 * (1.0 - eased_progress))
            alpha = max(0, min(255, alpha))
            self.overlay.color = (0, 0, 0, alpha)

        if self.text_to_continue_timer <= self.fade_text_to_continue_duration and self.isTextToContinue:
            progress2 = self.text_to_continue_timer / self.fade_text_to_continue_duration
            self.text_to_continue_alpha = int(255 * progress2)
        elif self.text_to_continue_timer >= self.fade_text_to_continue_duration and self.isTextToContinue:
            self.text_to_continue_alpha = 255

        if self.timer >= self.fade_background_duration:
            self.isFading = False

        if self.click_count == 0 and self.timer >= self.fade_background_duration + 2.0:
            self.isTextToContinue = True
            self.text_to_continue_timer += delta_time
        elif self.click_count > 0 and not self.isStarted:
            self.isStarted = True
            self.text_to_continue.color = (255, 255, 255, 0)
            self.isTextToContinue = False
            self.btn_configs[0]['text_color'] = (29, 5, 59, 255)
            self.btn_configs[1]['text_color'] = (29, 5, 59, 255)
            self.update_button_text()

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.update_buttons_position_and_size()
        self.update_button_text()

    def on_mouse_motion(self, x, y, dx, dy):
        for i in range(len(self.button_sprites)):
            if self.button_sprites[i].collides_with_point((x, y)):
                if self.btn_configs[i]['state'] != 'pressed':
                    self.btn_configs[i]['state'] = 'hovered'
            else:
                if self.btn_configs[i]['state'] == 'hovered':
                    self.btn_configs[i]['state'] = 'normal'

        self.update_button_textures()

    def on_mouse_press(self, x, y, button, modifiers):
        self.click_count += 1
        if self.click_count == 1:
            arcade.play_sound(self.main_theme_audio, loop=True, volume=1.7)
        if self.isFading:
            self.timer = self.fade_background_duration
            self.wind_sound.stop(self.wind_sound_player)
            self.overlay.color = (0, 0, 0, 0)
            self.isFading = False
        else:
            if button == arcade.MOUSE_BUTTON_LEFT:
                for i in range(len(self.button_sprites)):
                    if self.button_sprites[i].collides_with_point((x, y)):
                        self.btn_configs[i]['state'] = 'pressed'
                self.update_button_textures()

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for i in range(len(self.button_sprites)):
                if self.btn_configs[i]['state'] == 'pressed':
                    self.btn_configs[i]['state'] = 'normal'

                    if self.button_sprites[i].collides_with_point((x, y)):
                        self.on_button_click(self.btn_configs[i])
            self.update_button_textures()

    def on_button_click(self, button):
        if button['type'] == 'play':
            print('play')
        elif button['type'] == 'settings':
            print('settings')
            self.window.switch_view('settings_window')

    def on_key_press(self, symbol, modifiers):
        self.click_count += 1
        if self.click_count == 1:
            arcade.play_sound(self.main_theme_audio, loop=True)
        if self.isFading:
            self.timer = self.fade_background_duration
            self.wind_sound.stop(self.wind_sound_player)
            self.overlay.color = (0, 0, 0, 0)
            self.isFading = False

    def load_background(self):
        texture = arcade.load_texture(self.background_image_path)

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

    def create_buttons(self):
        shadow_btn_play = arcade.SpriteSolidColor(
            self.btn_configs[0]['width'],
            self.btn_configs[0]['height'],
            self.btn_configs[0]['center_x'],
            self.btn_configs[0]['center_y'] - 2,
            (0, 0, 0, 90)
        )
        self.shadow_sprites.append(shadow_btn_play)

        btn_play = arcade.Sprite(
            path_or_texture=self.button_textures[self.btn_configs[0]['state']],
            center_x=self.btn_configs[0]['center_x'],
            center_y=self.btn_configs[0]['center_y']
        )
        btn_play.width = self.btn_configs[0]['width']
        btn_play.height = self.btn_configs[0]['height']

        self.button_sprites.append(btn_play)

        shadow_btn_settings = arcade.SpriteSolidColor(
            self.btn_configs[1]['width'],
            self.btn_configs[1]['height'],
            self.btn_configs[1]['center_x'],
            self.btn_configs[1]['center_y'] - 2,
            (0, 0, 0, 90)
        )
        self.shadow_sprites.append(shadow_btn_settings)

        btn_settings = arcade.Sprite(
            path_or_texture=self.button_textures[self.btn_configs[1]['state']],
            center_x=self.btn_configs[1]['center_x'],
            center_y=self.btn_configs[1]['center_y']
        )
        btn_settings.width = self.btn_configs[1]['width']
        btn_settings.height = self.btn_configs[1]['height']

        self.button_sprites.append(btn_settings)

    def update_button_textures(self):
        for i in range(len(self.button_sprites)):
            state = self.btn_configs[i]['state']
            if state == 'normal':
                self.button_sprites[i].texture = self.button_textures['normal']
                if self.isStarted:
                    self.btn_configs[i]['text_color'] = (29, 5, 59, 255)
            elif state == 'hovered':
                self.button_sprites[i].texture = self.button_textures['hovered']
                if self.isStarted:
                    self.btn_configs[i]['text_color'] = (45, 16, 82, 255)
            elif state == 'pressed':
                self.button_sprites[i].texture = self.button_textures['pressed']
                if self.isStarted:
                    self.btn_configs[i]['text_color'] = (62, 10, 130, 255)
        self.update_button_text()

    def update_background_position_and_size(self):
        # это было растягивание при сохранениях пропорций

        # if not self.background_sprite or not self.background_sprite.texture:
        #     return

        # texture = self.background_sprite.texture
        # orig_width = texture.width
        # orig_height = texture.height

        # window_ratio = self.window.width / self.window.height
        # background_image_ratio = orig_width / orig_height

        # if window_ratio > background_image_ratio:
        #     scale = self.window.height / orig_height
        # else:
        #     scale = self.window.width / orig_width

        # self.background_sprite.width = orig_width * scale
        # self.background_sprite.height = orig_height * scale

        # self.background_sprite.center_x = self.window.width // 2
        # self.background_sprite.center_y = self.window.height // 2

        # а это просто растягивание

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

    def update_buttons_position_and_size(self):
        center_x = self.window.width // 2
        center_y = self.window.height // 2

        total_height = (self.button_height * 2) + self.spacing_between_buttons
        start_y = center_y + (total_height // 2) - (self.button_height // 2)

        self.btn_configs[0]['center_x'] = center_x
        self.btn_configs[0]['center_y'] = start_y

        self.button_sprites[0].center_x = self.btn_configs[0]['center_x']
        self.button_sprites[0].center_y = self.btn_configs[0]['center_y']

        self.shadow_sprites[0].center_x = self.btn_configs[0]['center_x']
        self.shadow_sprites[0].center_y = self.btn_configs[0]['center_y'] - 2

        self.btn_configs[1]['center_x'] = center_x
        self.btn_configs[1]['center_y'] = start_y - \
            self.button_height - self.spacing_between_buttons

        self.button_sprites[1].center_x = self.btn_configs[1]['center_x']
        self.button_sprites[1].center_y = self.btn_configs[1]['center_y']

        self.shadow_sprites[1].center_x = self.btn_configs[1]['center_x']
        self.shadow_sprites[1].center_y = self.btn_configs[1]['center_y'] - 2

    def update_button_text(self):
        self.play_button_text.x = self.btn_configs[0]['center_x']
        self.play_button_text.y = self.btn_configs[0]['center_y']
        self.play_button_text.color = self.btn_configs[0]['text_color']

        self.settings_button_text.x = self.btn_configs[1]['center_x']
        self.settings_button_text.y = self.btn_configs[1]['center_y']
        self.settings_button_text.color = self.btn_configs[1]['text_color']
