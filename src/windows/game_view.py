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

        self.intro_images = ["demo1.png", "demo2.png", "room_day.png"]
        self.intro_textures = []
        self.current_slide_idx = 0
        self.slide_time = 0.0
        self.fade_duration = 1.0
        self.slide_duration = 2.0
        self.intro_active = True

        self.bg_list = arcade.SpriteList()
        self.fade_list = arcade.SpriteList()
        self.interactable_sprites = arcade.SpriteList()

        self.bg_sprite = None
        self.fade_sprite = None
        self.phone_base_sprite = None
        self.phone_tube_sprite = None
        self.bed_sprite = None
        self.door_sprite = None

        self.can_interact = False
        self.objects_visible = True
        self.target_bg_tex = None
        self.is_transitioning = False
        self.transition_time = 0.0
        self.is_fading_in_after_door = False

        self.dialog_box = DialogBox(self.window, default_font_name="Arial")
        self.isRinging = False
        self.dialog_finished = False
        self.time_elapsed = 0.0
        self.ring_delay = 5.0

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()

    def setup(self):
        self.intro_textures = [self.reg.get(
            f'1episode/textures/intro/{img}') for img in self.intro_images]
        self.target_bg_tex = self.reg.get(
            '1episode/textures/backgrounds/first_episode_bg.png')

        self.bg_sprite = arcade.Sprite(self.intro_textures[0])
        self.bg_list.append(self.bg_sprite)

        self.fade_sprite = arcade.SpriteSolidColor(
            100, 100, color=arcade.color.BLACK)
        self.fade_sprite.alpha = 255
        self.fade_list.append(self.fade_sprite)

        self.phone_base_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/phone_basel.png'))
        self.phone_tube_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/phone_tubel.png'))

        self.bed_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/bed_day.png'))
        self.bed_sprite.normal_text = self.bed_sprite.texture
        self.bed_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/bed_day_hovered.png')

        self.door_sprite = arcade.Sprite(self.reg.get(
            '1episode/textures/ui/buttons/normal/door_day.png'))
        self.door_sprite.normal_text = self.door_sprite.texture
        self.door_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/door_day_hovered.png')

        self.interactable_sprites.extend(
            [self.bed_sprite, self.door_sprite, self.phone_base_sprite, self.phone_tube_sprite])
        self.update_layout()

    def update_layout(self):
        w, h = self.window.width, self.window.height

        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = w, h
            self.bg_sprite.position = (w / 2, h / 2)
        if self.fade_sprite:
            self.fade_sprite.width, self.fade_sprite.height = w, h
            self.fade_sprite.position = (w / 2, h / 2)

        p_base_w, p_base_h = 0.25, 0.35
        p_base_x, p_base_y = 0.5, 0.25

        p_tube_w, p_tube_h = 0.22, 0.12
        p_tube_offset_y = 0.105

        bed_w, bed_h = 0.35, 0.45
        bed_x, bed_y = 0.18, 0.22

        door_w, door_h = 0.21, 0.6
        door_x, door_y = 0.92, 0.43

        self.phone_base_sprite.width = w * p_base_w
        self.phone_base_sprite.height = h * p_base_h
        self.phone_base_sprite.center_x = w * p_base_x
        self.phone_base_sprite.center_y = h * p_base_y

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

        self.dialog_box._setup_dimensions()

    def on_update(self, delta_time):
        if self.is_transitioning:
            self.transition_time += delta_time
            alpha = int((self.transition_time / 0.8) * 255)
            if alpha >= 255:
                self.fade_sprite.alpha = 255
                self.bg_sprite.texture = self.target_bg_tex
                self.update_layout()
                self.objects_visible = False
                self.is_transitioning = False
                self.is_fading_in_after_door = True
                self.transition_time = 0
            else:
                self.fade_sprite.alpha = alpha
            return

        if self.is_fading_in_after_door:
            self.transition_time += delta_time
            alpha = 255 - int((self.transition_time / 0.8) * 255)
            if alpha <= 0:
                self.fade_sprite.alpha = 0
                self.is_fading_in_after_door = False
            else:
                self.fade_sprite.alpha = alpha
            return

        if self.intro_active:
            self.slide_time += delta_time
            idx = self.current_slide_idx
            is_last = (idx == len(self.intro_textures) - 1)
            self.bg_sprite.texture = self.intro_textures[idx]
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
                    self.intro_active = False

            if is_last:
                self.update_phone_logic(delta_time)
            return

        self.update_phone_logic(delta_time)
        self.dialog_box.update(delta_time)
        if self.dialog_finished and not self.dialog_box.is_active:
            self.can_interact = True

    def update_phone_logic(self, delta_time):
        if not self.dialog_finished:
            self.time_elapsed += delta_time
            if self.time_elapsed > self.ring_delay and not self.isRinging and not self.dialog_box.is_active:
                self.isRinging = True

        if self.isRinging:
            h = self.window.height
            offset = h * 0.105
            shake = math.sin(self.time_elapsed * 60) * (h * 0.003)
            self.phone_tube_sprite.angle = math.sin(self.time_elapsed * 40) * 5
            self.phone_tube_sprite.center_y = self.phone_base_sprite.center_y + offset + shake

    def on_draw(self):
        self.clear()
        self.bg_list.draw()
        if self.current_slide_idx == 2 and self.objects_visible:
            self.interactable_sprites.draw()
            self.dialog_box.draw()
        if self.intro_active or self.is_transitioning or self.is_fading_in_after_door:
            self.fade_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.current_slide_idx < 2 or not self.objects_visible or self.is_transitioning:
            return
        for s in [self.bed_sprite, self.door_sprite]:
            s.texture = s.hover_text if s.collides_with_point(
                (x, y)) else s.normal_text

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_slide_idx < 2 or not self.objects_visible or self.is_transitioning or button != arcade.MOUSE_BUTTON_LEFT:
            return
        if (self.phone_base_sprite.collides_with_point((x, y)) or self.phone_tube_sprite.collides_with_point((x, y))) and not self.dialog_box.is_active:
            if self.isRinging:
                self.isRinging = False
                self.dialog_finished = True
                self.phone_tube_sprite.angle = 0
                self.update_layout()
                self.start_dialog()
                return
        if self.can_interact:
            if self.bed_sprite.collides_with_point((x, y)):
                print("СПАТЬ!")
            elif self.door_sprite.collides_with_point((x, y)):
                self.is_transitioning = True
                self.transition_time = 0

    def start_dialog(self):
        self.dialog_box.start_dialogue([
            DialoguePhrase("** ******* {color:150,75,0}******{/color}!",
                           effect=TextEffect.SHAKE, voice=Voice.GOVERMENT),
            DialoguePhrase("*** *** ******. * ** ****.",
                           voice=Voice.GOVERMENT, effect=TextEffect.RAINBOW),
        ])

    def on_key_press(self, key, modifiers):
        if self.dialog_box.is_active and key in [arcade.key.ENTER, arcade.key.Z]:
            self.dialog_box.next_phrase()

    def on_resize(self, width, height):
        self.update_layout()
