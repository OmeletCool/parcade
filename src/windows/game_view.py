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
        
        # --- Настройки интро ---
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
        
        # Объекты
        self.phone_base_sprite = None
        self.phone_tube_sprite = None
        self.bed_sprite = None
        self.door_sprite = None
        
        self.can_interact = False   
        self.objects_visible = True 
        self.target_bg_tex = None
        self.is_transitioning = False
        self.transition_time = 0.0
        
        self.dialog_box = DialogBox(self.window, default_font_name="Arial")
        self.isRinging = False
        self.dialog_finished = False
        self.time_elapsed = 0.0
        self.ring_delay = 5.0
        self.tube_offset_y = 0

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()

    def setup(self):
        self.intro_textures = [self.reg.get(f'1episode/textures/intro/{img}') for img in self.intro_images]
        self.target_bg_tex = self.reg.get('1episode/textures/backgrounds/first_episode_bg.png')

        self.bg_list.clear()
        self.bg_sprite = arcade.Sprite(self.intro_textures[0])
        self.bg_list.append(self.bg_sprite)
        
        self.fade_list.clear()
        self.fade_sprite = arcade.SpriteSolidColor(100, 100, color=arcade.color.BLACK)
        self.fade_sprite.alpha = 255
        self.fade_list.append(self.fade_sprite)

        self.interactable_sprites.clear()
        self.phone_base_sprite = arcade.Sprite(self.reg.get('1episode/textures/ui/buttons/normal/phone_basel.png'))
        self.phone_tube_sprite = arcade.Sprite(self.reg.get('1episode/textures/ui/buttons/normal/phone_tubel.png'))
        
        self.bed_sprite = arcade.Sprite(self.reg.get('1episode/textures/ui/buttons/normal/bed_day.png'))
        self.bed_sprite.normal_tex = self.bed_sprite.texture
        self.bed_sprite.hover_tex = self.reg.get('1episode/textures/ui/buttons/hovered/bed_day_hovered.png')
        
        self.door_sprite = arcade.Sprite(self.reg.get('1episode/textures/ui/buttons/normal/door_day.png'))
        self.door_sprite.normal_tex = self.door_sprite.texture
        self.door_sprite.hover_tex = self.reg.get('1episode/textures/ui/buttons/hovered/door_day_hovered.png')

        self.interactable_sprites.extend([self.bed_sprite, self.door_sprite, self.phone_base_sprite, self.phone_tube_sprite])
        self.update_background_position_and_size()

    def update_background_position_and_size(self):
        win_w, win_h = self.window.width, self.window.height
        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = win_w, win_h
            self.bg_sprite.position = (win_w / 2, win_h / 2)
        if self.fade_sprite:
            self.fade_sprite.width, self.fade_sprite.height = win_w, win_h
            self.fade_sprite.position = (win_w / 2, win_h / 2)

        self.phone_base_sprite.scale = (win_h * 0.22) / self.phone_base_sprite.texture.height
        self.phone_base_sprite.center_x, self.phone_base_sprite.center_y = win_w * 0.45, win_h * 0.3
        
        self.phone_tube_sprite.scale = (win_h * 0.09) / self.phone_tube_sprite.texture.height
        self.phone_tube_sprite.scale_x *= 1.17
        self.tube_offset_y = self.phone_base_sprite.width / 3.2
        self.phone_tube_sprite.center_x = self.phone_base_sprite.center_x
        self.phone_tube_sprite.center_y = self.phone_base_sprite.center_y + self.tube_offset_y

        self.bed_sprite.scale = (win_h * 0.8) / self.bed_sprite.texture.height
        self.bed_sprite.center_x, self.bed_sprite.center_y = win_w * 0.18, win_h * 0.15

        self.door_sprite.scale = (win_h * 0.8) / self.door_sprite.texture.height
        self.door_sprite.center_x, self.door_sprite.center_y = win_w * 0.92, win_h * 0.52

    def on_update(self, delta_time):
        if self.is_transitioning:
            self.transition_time += delta_time
            alpha = int((self.transition_time / 0.8) * 255)
            if alpha <= 255:
                self.fade_sprite.alpha = alpha
            else:
                self.fade_sprite.alpha = 255
                self.bg_sprite.texture = self.target_bg_tex
                self.objects_visible = False
                self.is_transitioning = False
                self.is_fading_in_after_door = True
                self.transition_time = 0
            return

        if getattr(self, 'is_fading_in_after_door', False):
            self.transition_time += delta_time
            alpha = 255 - int((self.transition_time / 0.8) * 255)
            if alpha >= 0:
                self.fade_sprite.alpha = alpha
            else:
                self.fade_sprite.alpha = 0
                self.is_fading_in_after_door = False
            return

        if self.intro_active:
            self.slide_time += delta_time
            is_last_slide = (self.current_slide_idx == len(self.intro_textures) - 1)
            self.bg_sprite.texture = self.intro_textures[self.current_slide_idx]

            if self.slide_time < self.fade_duration:
                self.fade_sprite.alpha = int(255 * (1 - (self.slide_time / self.fade_duration)))
            elif not is_last_slide and self.slide_time > (self.slide_duration + self.fade_duration):
                elapsed = self.slide_time - (self.slide_duration + self.fade_duration)
                self.fade_sprite.alpha = int(255 * (elapsed / self.fade_duration))
            else:
                self.fade_sprite.alpha = 0

            if self.slide_time >= (self.slide_duration + self.fade_duration * 2):
                if not is_last_slide:
                    self.current_slide_idx += 1
                    self.slide_time = 0
                else:
                    self.intro_active = False
            
            if is_last_slide: self.update_phone_logic(delta_time)
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
            self.phone_tube_sprite.angle = math.sin(self.time_elapsed * 40) * 5
            self.phone_tube_sprite.center_y = (self.phone_base_sprite.center_y + self.tube_offset_y) + math.sin(self.time_elapsed * 60) * 2

    def on_draw(self):
        self.clear()
        self.bg_list.draw()

        if self.current_slide_idx == 2 and self.objects_visible:
            self.interactable_sprites.draw()
            self.dialog_box.draw()

        if self.intro_active or self.is_transitioning or getattr(self, 'is_fading_in_after_door', False):
            self.fade_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if self.current_slide_idx < 2 or not self.objects_visible or self.is_transitioning: return
        for sprite in [self.bed_sprite, self.door_sprite]:
            if hasattr(sprite, 'hover_tex') and sprite.hover_tex:
                sprite.texture = sprite.hover_tex if sprite.collides_with_point((x, y)) else sprite.normal_tex

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_slide_idx < 2 or not self.objects_visible or self.is_transitioning: 
            return
        if button != arcade.MOUSE_BUTTON_LEFT: 
            return

        if (self.phone_base_sprite.collides_with_point((x, y)) or 
            self.phone_tube_sprite.collides_with_point((x, y))) and not self.dialog_box.is_active:
            if self.isRinging:
                self.isRinging = False
                self.dialog_finished = True
                self.phone_tube_sprite.angle = 0
                self.phone_tube_sprite.center_y = self.phone_base_sprite.center_y + self.tube_offset_y
                self.start_dialog()
                return

        if self.can_interact:
            if self.bed_sprite.collides_with_point((x, y)):
                print("СПАТЬ!")
            
            elif self.door_sprite.collides_with_point((x, y)):
                music_path = 'common/sounds/music/main_theme.ogg'
                if music_path in self.window.music_players:
                    self.window.stop_definite_music(music_path)

                # --- ЗАПУСКАЕМ ПЛАВНЫЙ ПЕРЕХОД ---
                self.is_transitioning = True 
                self.transition_time = 0

    def start_dialog(self):
        self.dialog_box.start_dialogue([
            DialoguePhrase("** ******* {color:150,75,0}******{/color}!", effect=TextEffect.SHAKE, voice=Voice.GOVERMENT),
            DialoguePhrase("*** *** ******. * ** ****.", voice=Voice.GOVERMENT, effect=TextEffect.RAINBOW),
        ])

    def on_key_press(self, key, modifiers):
        if self.dialog_box.is_active and key in [arcade.key.ENTER, arcade.key.Z]:
            self.dialog_box.next_phrase()

    def on_resize(self, width, height):
        self.update_background_position_and_size()
        self.dialog_box._setup_dimensions()