import arcade
from src.registry import reg
from resources.dialog_box import *
from src.settings import settings


class StartGame(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.window = window
        self.reg = reg

        self.intro_images = ["demo_1.png", "demo_2.png", "room_day.png"]
        self.intro_textures = []
        self.current_slide_idx = 0
        self.slide_time = 0.0
        self.fade_duration = 1.0
        self.slide_duration = 2.0
        self.intro_active = True

        self.bg_sprite = None

        self.bg_list = arcade.SpriteList()
        self.bg_sprite = arcade.Sprite()

        self.fade_list = arcade.SpriteList()

        self.object_list = arcade.SpriteList()

        self.fade_sprite = None

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()

    def setup(self):
        self.phone_base_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/phone_basel.png'))
        self.phone_tube_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/phone_tubel.png'))
        self.bed_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/bed_day.png'))
        self.door_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/door_day.png'))
        self.luke_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/luke_day.png'))
        self.intro_textures = [self.reg.get(
            f'1episode/textures/intro/{img}') for img in self.intro_images]

        w, h = self.window.width, self.window.height

        # ДИМА ЗАДАЙ КООРДИНАТЫ
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_base_w, p_base_h = 0.05, 0.14  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_base_x, p_base_y = 0.5, 0.4  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_tube_w, p_tube_h = 0.11, 0.09  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_tube_offset_y = 0.04  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#
        bed_w, bed_h = 0.36, 0.45  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        bed_x, bed_y = 0.18, 0.24  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        door_w, door_h = 0.19, 0.6  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        door_x, door_y = 0.92, 0.43  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

        luke_w, luke_h = 0.18, 0.18
        luke_x, luke_y = 0.5, 0.91

        self.phone_base_sprite.width = w * p_base_w
        self.phone_base_sprite.height = h * p_base_h
        self.phone_base_sprite.center_x = w * p_base_x
        self.phone_base_sprite.center_y = h * p_base_y
        self.phone_base_sprite.scale_x = 0.15
        self.phone_base_sprite.scale_y = 0.1

        self.phone_tube_sprite.width = w * p_tube_w
        self.phone_tube_sprite.height = h * p_tube_h
        self.phone_tube_sprite.center_x = self.phone_base_sprite.center_x
        self.phone_tube_sprite.center_y = self.phone_base_sprite.center_y + \
            (h * p_tube_offset_y)

        self.bed_sprite.width = w * bed_w
        self.bed_sprite.height = h * bed_h
        self.bed_sprite.center_x = w * bed_x
        self.bed_sprite.center_y = h * bed_y

        self.door_sprite.width = w * door_w
        self.door_sprite.height = h * door_h
        self.door_sprite.center_x = w * door_x
        self.door_sprite.center_y = h * door_y

        self.luke_sprite.width = w * luke_w
        self.luke_sprite.height = h * luke_h
        self.luke_sprite.center_x = w * luke_x
        self.luke_sprite.center_y = h * luke_y

        self.bg_list.append(self.bg_sprite)

        self.fade_sprite = arcade.SpriteSolidColor(100, 100, color=(0, 0, 0))
        self.fade_sprite.alpha = 255
        self.fade_list.append(self.fade_sprite)

        self.object_list.extend(
            [self.phone_base_sprite, self.phone_tube_sprite, self.bed_sprite, self.door_sprite, self.luke_sprite])

        self.intro_active = True
        self.on_resize(self.window.width, self.window.height)

    def on_update(self, delta_time):
        if self.intro_active:
            self.slide_time += delta_time
            is_last = self.current_slide_idx == 2
            self.bg_sprite.texture = self.intro_textures[self.current_slide_idx]
            self.bg_sprite.width, self.bg_sprite.height = self.window.width, self.window.height

            if self.slide_time < self.fade_duration:
                self.fade_sprite.alpha = int(
                    255 * (1 - (self.slide_time / self.fade_duration)))
            elif not is_last and self.slide_time > (self.slide_duration + self.fade_duration):
                el = self.slide_time - \
                    (self.slide_duration + self.fade_duration)
                self.fade_sprite.alpha = int(255 * (el / self.fade_duration))
            else:
                self.fade_sprite.alpha = 0

            if self.slide_time >= (self.slide_duration + self.fade_duration * 2):
                if not is_last:
                    self.current_slide_idx += 1
                    self.slide_time = 0
                else:
                    self.window.switch_view('game_house_view')

    def on_draw(self):
        self.clear()
        self.bg_list.draw()

        if self.current_slide_idx == 2:
            self.object_list.draw()
        if self.intro_active:
            self.fade_list.draw()

    def on_resize(self, width, height):
        w, h = width, height

        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = w, h
            self.bg_sprite.position = (w / 2, h / 2)
        if self.fade_sprite:
            self.fade_sprite.width, self.fade_sprite.height = w, h
            self.fade_sprite.position = (w / 2, h / 2)
