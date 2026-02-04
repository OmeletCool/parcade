import arcade
import math
from src.registry import reg
from resources.dialog_box import *
from src.windows.game_window.attic_view import AtticView
from src.settings import settings
from resources.languages import LANGUAGES


class HouseView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.reg = reg
        self.language: int = self.window.language

        self.bg_list = arcade.SpriteList()
        self.fade_list = arcade.SpriteList()
        self.interactable_sprites = arcade.SpriteList()

        self.bg_sprite = None
        self.fade_sprite = None
        self.phone_base_sprite = None
        self.phone_tube_sprite = None
        self.bed_sprite = None
        self.door_sprite = None
        self.luke_sprite = None

        self.can_interact = False
        self.postman_interaction_finished = False

        self.dialog_box = DialogBox(
            self.window, default_font_name="Montserrat")
        self.isRinging = False
        self.isStartedToRing = False
        self.dialog_finished = False
        self.time_elapsed = 0.0
        self.ring_delay = 5.0

        self.sequence_step = 0
        self.sequence_timer = 0.0
        self.can_open_door = False

        self.transition_to_attic = False
        self.transition_timer = 0.0
        self.transition_duration = 1.0
        self.fade_alpha = 0

        self.transition_to_night = False
        self.night_transition_timer = 0.0
        self.night_transition_duration = 3.0
        self.night_fade_alpha = 0
        self.is_night = False
        self.textures_changed = False

        self.day_counter = 0
        self.max_days = 4
        self.phone_after_days_called = False
        self.dialogue_after_4days_shown = False

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()

    def setup(self):
        bg_texture = self.reg.get('1episode/textures/intro/room_day.png')

        self.bg_sprite = arcade.Sprite(bg_texture)
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

        self.luke_sprite = arcade.Sprite(
            self.reg.get('1episode/textures/ui/buttons/normal/luke_day.png'))
        self.luke_sprite.normal_text = self.luke_sprite.texture
        self.luke_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/luke_day_hovered.png')

        self.interactable_sprites.extend(
            [self.bed_sprite, self.door_sprite, self.luke_sprite, self.phone_base_sprite, self.phone_tube_sprite])
        self.update_layout()

    def update_layout(self):
        w, h = self.window.width, self.window.height

        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = w, h
            self.bg_sprite.position = (w / 2, h / 2)
        if self.fade_sprite:
            self.fade_sprite.width, self.fade_sprite.height = w, h
            self.fade_sprite.position = (w / 2, h / 2)

        p_base_w, p_base_h = 0.05, 0.14
        p_base_x, p_base_y = 0.5, 0.4
        p_tube_w, p_tube_h = 0.11, 0.09
        p_tube_offset_y = 0.04
        bed_w, bed_h = 0.36, 0.45
        bed_x, bed_y = 0.18, 0.24
        door_w, door_h = 0.19, 0.6
        door_x, door_y = 0.92, 0.43

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

        self.dialog_box._setup_dimensions()

    def on_update(self, delta_time):
        self.time_elapsed += delta_time

        if self.transition_to_night:
            self.night_transition_timer += delta_time
            progress = min(self.night_transition_timer /
                           self.night_transition_duration, 1.0)
            if progress < 0.5:
                self.night_fade_alpha = int(510 * progress)
            else:
                self.night_fade_alpha = int(510 * (1 - progress))
            if progress >= 0.5 and not self.textures_changed:
                if not self.is_night:
                    self._switch_to_night_textures()
                else:
                    self._switch_to_day_textures()
                self.textures_changed = True
            if progress >= 1.0:
                self.transition_to_night = False
                self.night_fade_alpha = 0
                self.textures_changed = False
                if not self.is_night:
                    self.day_counter += 1
                    if self.day_counter >= self.max_days and not self.dialogue_after_4days_shown:
                        self._trigger_phone_after_days()
            return

        if self.transition_to_attic:
            self.transition_timer += delta_time
            progress = min(self.transition_timer /
                           self.transition_duration, 1.0)
            self.fade_alpha = int(255 * progress)
            if progress >= 1.0:
                self.window.switch_view('game_attic_view')
                return

        self.update_phone_logic(delta_time)
        self.dialog_box.update(delta_time)

        if not self.dialog_box.is_active:
            if self.day_counter >= self.max_days and self.sequence_step == 5:
                self.start_dialog(5)
                self.sequence_step = -1
                return

            if self.sequence_step == 0:
                self.sequence_timer += delta_time
                if self.sequence_timer >= 1.0:
                    self.isRinging = True
                    self.start_dialog(0)
                    self.sequence_timer = 0
                    self.sequence_step = -1
            elif self.sequence_step == 0.2:
                self.sequence_timer += delta_time
                if self.sequence_timer >= 0.2:
                    self.sequence_timer = 0
                    self.sequence_step = -1
                    self.dialog_finished = True
                    self.start_dialog(1)
            elif self.sequence_step == 1.5:
                self.sequence_timer += delta_time
                if self.sequence_timer >= 0.5:
                    self.sequence_timer = 0
                    self.sequence_step = -1
                    self.start_dialog(1.5)
            elif self.sequence_step == 1:
                self.sequence_timer += delta_time
                if self.sequence_timer >= 1.0:
                    self.sequence_timer = 0
                    self.sequence_step = 0
                    self.start_dialog(2)
            elif self.sequence_step == 2:
                self.window.play_definite_music(
                    'common/sounds/sfx/ambient/door_knocking.wav')
                self.start_dialog(2.5)
                self.sequence_step = -1
            elif self.sequence_step == 3:
                self.sequence_timer += delta_time
                if self.sequence_timer >= 0.2:
                    self.sequence_timer = 0
                    self.sequence_step = -1
                    self.start_dialog(3)

        if self.dialog_finished and not self.dialog_box.is_active:
            if self.can_open_door:
                self.can_interact = True

    def update_phone_logic(self, delta_time):
        if self.sequence_step == 0.2:
            return
        if not self.dialog_finished and not self.isRinging and not self.dialog_box.is_active:
            if self.time_elapsed > self.ring_delay:
                self.isRinging = True
        if self.isRinging:
            if not self.isStartedToRing:
                self.window.play_definite_music(
                    '1episode/sounds/sfx/ambient/bringing_phone.wav', isLooping=True)
                self.isStartedToRing = True
            h = self.window.height
            offset = h * 0.052
            shake = math.sin(self.time_elapsed * 60) * (h * 0.003)
            self.phone_tube_sprite.angle = math.sin(self.time_elapsed * 40) * 5
            self.phone_tube_sprite.center_y = self.phone_base_sprite.center_y + offset + shake

    def _switch_to_night_textures(self):
        self.bg_sprite.texture = self.reg.get(
            '1episode/textures/backgrounds/room_night.png')

        # Кровать ночь
        self.bed_sprite.texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/bed_night.png')
        self.bed_sprite.normal_text = self.bed_sprite.texture
        self.bed_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/bed_hovered.png')

        # Дверь ночь
        self.door_sprite.texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/door_night.png')
        self.door_sprite.normal_text = self.door_sprite.texture
        self.door_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/door_night_hovered.png')

        # Люк ночь
        self.luke_sprite.texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/luke_night.png')
        self.luke_sprite.normal_text = self.luke_sprite.texture
        self.luke_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/luke_night_hovered.png')

        self.is_night = True

    def _switch_to_day_textures(self):
        self.bg_sprite.texture = self.reg.get(
            '1episode/textures/intro/room_day.png')

        # Кровать день
        self.bed_sprite.texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/bed_day.png')
        self.bed_sprite.normal_text = self.bed_sprite.texture
        self.bed_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/bed_day_hovered.png')

        # Дверь день
        self.door_sprite.texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/door_day.png')
        self.door_sprite.normal_text = self.door_sprite.texture
        self.door_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/door_day_hovered.png')

        # Люк день
        self.luke_sprite.texture = self.reg.get(
            '1episode/textures/ui/buttons/normal/luke_day.png')
        self.luke_sprite.normal_text = self.luke_sprite.texture
        self.luke_sprite.hover_text = self.reg.get(
            '1episode/textures/ui/buttons/hovered/luke_day_hovered.png')

        self.is_night = False

    def _trigger_phone_after_days(self):
        self.isRinging, self.isStartedToRing, self.time_elapsed, self.ring_delay = True, False, 0, 0

    def _start_4days_phone_dialog(self):
        self.phone_after_days_called, self.sequence_step = True, 5

    def _on_phone_end(self): self.sequence_step = 1.5
    def _on_hanging_up_end(self): self.sequence_step = 1
    def _on_monologue1_end(self): self.sequence_step = 2
    def _on_knocking_end(self): self.sequence_step = 3

    def _on_4days_procrastinating(self):
        self.dialogue_after_4days_shown = True
        arcade.exit()

    def _on_t3_end(self): self.can_open_door, self.dialog_finished = True, True

    def _on_postman_dialogue_end(self):
        self.postman_interaction_finished, self.can_interact, self.can_open_door = True, True, False

    def on_draw(self):
        self.clear()
        self.bg_list.draw()
        self.interactable_sprites.draw()
        self.dialog_box.draw()
        if self.night_fade_alpha > 0:
            arcade.draw_lbwh_rectangle_filled(
                0, 0, self.window.width, self.window.height, (0, 0, 0, self.night_fade_alpha))
        if self.fade_alpha > 0:
            arcade.draw_lbwh_rectangle_filled(
                0, 0, self.window.width, self.window.height, (0, 0, 0, self.fade_alpha))

    def on_mouse_motion(self, x, y, dx, dy):
        if self.transition_to_attic or self.transition_to_night or self.isRinging or self.dialog_box.is_active:
            return
        for s in [self.bed_sprite, self.door_sprite, self.luke_sprite]:
            s.texture = s.hover_text if s.collides_with_point(
                (x, y)) else s.normal_text

    def on_mouse_press(self, x, y, button, modifiers):
        if self.transition_to_attic or self.transition_to_night or self.dialog_box.is_active:
            return
        if (self.phone_base_sprite.collides_with_point((x, y)) or self.phone_tube_sprite.collides_with_point((x, y))) and self.sequence_step != 0.2:
            if self.isRinging:
                self.isRinging = False
                self.window.stop_definite_music(
                    '1episode/sounds/sfx/ambient/bringing_phone.wav')
                self.phone_tube_sprite.angle = 0
                self.window.play_definite_music(
                    '1episode/sounds/sfx/ambient/picking_up_the_phone.wav')
                if self.day_counter >= self.max_days:
                    self._start_4days_phone_dialog()
                else:
                    self.sequence_step, self.sequence_timer = 0.2, 0.0
            return
        if self.can_interact:
            if self.bed_sprite.collides_with_point((x, y)):
                if not self.postman_interaction_finished and self.day_counter == 0:
                    return
                self.transition_to_night, self.night_transition_timer, self.textures_changed = True, 0.0, False
            elif self.door_sprite.collides_with_point((x, y)):
                if self.postman_interaction_finished:
                    self.window.switch_view('game_backyard_view')
                elif self.can_open_door:
                    self.can_open_door = False
                    self.start_dialog(4)
            elif self.luke_sprite.collides_with_point((x, y)):
                if not self.postman_interaction_finished and self.day_counter == 0:
                    return
                self.transition_to_attic, self.transition_timer = True, 0.0

    def start_dialog(self, t):
        if t != 5 and (self.transition_to_attic or self.transition_to_night or self.isRinging):
            return
        if t == 0:
            self.dialog_box.start_dialogue([DialoguePhrase(
                LANGUAGES['dialogues']['phone_talkings']['calling'][self.language], voice=Voice.DEFAULT, speed=30)])
        elif t == 1:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['1'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['2'][self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['3'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['4'][self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['5'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['6'][self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['7'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['8'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['9'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['10'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['11'][self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['12']
                               [self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE, skippable=False, speed=10),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['13'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['14'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['15'][self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['16'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['17'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']
                               ['18'][self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['19']
                               [self.language], voice=Voice.GOVERMENT, logo=Icon.PHONE, skippable=False),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['20'][self.language],
                               voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT, callback=self._on_phone_end)
            ])
        elif t == 1.5:
            self.dialog_box.start_dialogue([DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['hanging_up']
                                           [self.language], speed=30, voice=Voice.DEFAULT, callback=self._on_hanging_up_end)])
        elif t == 2:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['monologues']['1'][self.language],
                               voice=Voice.PLAYER, logo=Icon.PLAYER_ANGRY),
                DialoguePhrase(LANGUAGES['monologues']['2'][self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT, callback=self._on_monologue1_end)])
        elif t == 2.5:
            self.dialog_box.start_dialogue([DialoguePhrase(LANGUAGES['dialogues']['ui_sound_desc']['knocking']
                                           [self.language], voice=Voice.DEFAULT, speed=30, callback=self._on_knocking_end)])
        elif t == 3:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['monologues']['3'][self.language],
                               voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT),
                DialoguePhrase(LANGUAGES['monologues']['4'][self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT, callback=self._on_t3_end)])
        elif t == 4:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['dialogues']['postman_talkings']['1']
                               [self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['postman_talkings']['2']
                               [self.language], voice=Voice.PLAYER, logo=Icon.PLAYER_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['postman_talkings']['3']
                               [self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['postman_talkings']['4']
                               [self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN_DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['postman_talkings']['5'][self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN_DEFAULT, callback=self._on_postman_dialogue_end)])
        elif t == 5:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['21'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE, callback=self._on_4days_procrastinating)])

    def on_key_press(self, key, modifiers):
        if self.dialog_box.is_active and key in [arcade.key.ENTER, arcade.key.Z, arcade.key.SPACE]:
            self.dialog_box.next_phrase()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.update_layout()

    def on_hide_view(self):
        self.window.stop_definite_music(
            '1episode/sounds/sfx/ambient/bringing_phone.wav')
