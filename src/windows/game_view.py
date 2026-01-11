import arcade
import math
from src.registry import reg
from resources.dialog_box import *
from src.settings import settings


class DemoGameView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.window = window
        self.reg = reg
        self.test_sprite_list = arcade.SpriteList()
        self.phone_base_sprite = None
        self.phone_tube_sprite = None
        self.dialog_box = DialogBox(self.window, default_font_name="Arial")
        self.isRinging = False
        self.dialog_finished = False
        self.time_elapsed = 0.0
        self.ring_delay = 5.0
        self.tube_offset_y = 0

    def on_show_view(self):
        self.window.background_color = arcade.color.LION
        self.setup()

    def setup(self):
        self.test_sprite_list.clear()
        phone_base_texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/phone_basel.png')
        phone_tube_texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/phone_tubel.png')

        self.phone_base_sprite = arcade.Sprite(phone_base_texture)
        self.phone_tube_sprite = arcade.Sprite(phone_tube_texture)

        self.test_sprite_list.extend(
            [self.phone_base_sprite, self.phone_tube_sprite])
        self.update_background_position_and_size()

    def update_background_position_and_size(self):
        win_w, win_h = self.window.width, self.window.height

        base_sc = (win_h * 0.25) / self.phone_base_sprite.texture.height
        tube_sc = (win_h * 0.1) / self.phone_tube_sprite.texture.height

        self.phone_base_sprite.scale = base_sc
        self.phone_tube_sprite.scale = tube_sc

        self.phone_tube_sprite.scale_x *= 1.17

        self.phone_base_sprite.center_x = win_w * 0.2
        self.phone_base_sprite.center_y = win_h * 0.35

        self.tube_offset_y = self.phone_base_sprite.width / 3

        self.phone_tube_sprite.center_x = self.phone_base_sprite.center_x
        self.phone_tube_sprite.center_y = self.phone_base_sprite.center_y + self.tube_offset_y
        self.phone_tube_sprite.angle = 0

    def on_update(self, delta_time):
        self.dialog_box.update(delta_time)

        if not self.dialog_finished:
            self.time_elapsed += delta_time
            if self.time_elapsed > self.ring_delay and not self.isRinging and not self.dialog_box.is_active:
                self.isRinging = True

        if self.isRinging:
            self.phone_tube_sprite.angle = math.sin(self.time_elapsed * 40) * 5
            self.phone_tube_sprite.center_y = (
                self.phone_base_sprite.center_y + self.tube_offset_y) + math.sin(self.time_elapsed * 60) * 2

    def stop_ringing(self):
        self.isRinging = False
        self.dialog_finished = True
        self.phone_tube_sprite.angle = 0
        self.phone_tube_sprite.center_y = self.phone_base_sprite.center_y + self.tube_offset_y

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if (self.phone_base_sprite.collides_with_point((x, y)) or self.phone_tube_sprite.collides_with_point((x, y))) and not self.dialog_box.is_active:
                if self.isRinging:
                    self.stop_ringing()
                    self.start_dialog()

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.ENTER, arcade.key.Z]:
            if self.dialog_box.is_active:
                self.dialog_box.next_phrase()

    def start_dialog(self):
        phrases = [
            DialoguePhrase("ТЫ ваняеш {color:150,75,0}КАЛЛОМ{/color}!", effect=TextEffect.SHAKE,
                           voice=Voice.GOVERMENT, speed=10, skippable=False, font_name='Montserrat', pitch=0.5),
            DialoguePhrase("Лан это прикол. Я за лгбт.", voice=Voice.GOVERMENT,
                           font_name="Comic Sans MS", effect=TextEffect.RAINBOW),
            DialoguePhrase("{color:170,100,0}Грязные дети{/color} VS {color:252,249,227}Чистые джигиты{/color}",
                           voice=Voice.GOVERMENT, font_name="Impact", effect=TextEffect.WAVE),
            DialoguePhrase("872345 als\njklhdsfalhjka\n\n. . .", 15,
                           font_name='Wingdings', voice=Voice.GOVERMENT, pitch=2)
        ]
        self.dialog_box.start_dialogue(phrases)

    def on_draw(self):
        self.clear()
        self.test_sprite_list.draw()
        self.dialog_box.draw()

    def on_resize(self, width, height):
        self.update_background_position_and_size()
        self.dialog_box._setup_dimensions()
