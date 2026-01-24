import arcade
from src.registry import reg
from resources.dialog_box import *
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

        self.can_interact = False

        self.dialog_box = DialogBox(
            self.window, default_font_name="Montserrat")
        self.isRinging = False
        self.dialog_finished = False
        self.time_elapsed = 0.0
        self.ring_delay = 5.0

        self.sequence_step = 0
        self.sequence_timer = 0.0
        self.can_open_door = False

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

        # ДИМА ЗАДАЙ КООРДИНАТЫ
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_base_w, p_base_h = 0.25, 0.35  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_base_x, p_base_y = 0.5, 0.25  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_tube_w, p_tube_h = 0.22, 0.12  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        p_tube_offset_y = 0.105  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
#
        bed_w, bed_h = 0.35, 0.45  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        bed_x, bed_y = 0.18, 0.22  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        door_w, door_h = 0.21, 0.6  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        door_x, door_y = 0.92, 0.43  # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

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
        self.update_phone_logic(delta_time)
        self.dialog_box.update(delta_time)

        if not self.dialog_box.is_active:
            if self.sequence_step == 1:
                self.sequence_timer += delta_time
                if self.sequence_timer >= 1.0:
                    self.sequence_timer = 0
                    self.sequence_step = 0
                    self.start_dialog(2)

            elif self.sequence_step == 2:
                # Проигрываем звук стука (замени путь на свой из реестра)
                # arcade.play_sound(self.reg.get('common/sounds/sfx/world/door_knock.wav'))
                self.sequence_step = 0
                self.start_dialog(3)

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

    def _on_phone_end(self):
        self.sequence_step = 1

    def _on_t2_end(self):
        self.sequence_step = 2

    def _on_t3_end(self):
        self.can_open_door = True

    def on_draw(self):
        self.clear()
        self.bg_list.draw()
        self.interactable_sprites.draw()
        self.dialog_box.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for s in [self.bed_sprite, self.door_sprite]:
            s.texture = s.hover_text if s.collides_with_point(
                (x, y)) else s.normal_text

    def on_mouse_press(self, x, y, button, modifiers):
        if (self.phone_base_sprite.collides_with_point((x, y)) or self.phone_tube_sprite.collides_with_point((x, y))) and not self.dialog_box.is_active:
            if self.isRinging:
                self.isRinging = False
                self.dialog_finished = True
                self.phone_tube_sprite.angle = 0
                self.update_layout()
                self.start_dialog(1)
                return
        if self.can_interact:
            if self.bed_sprite.collides_with_point((x, y)):
                print("СПАТЬ!")
            elif self.door_sprite.collides_with_point((x, y)):
                if self.can_open_door:
                    self.can_open_door = False
                    self.postman_here = True
                    self.start_dialog(4)
                else:
                    pass

    def start_dialog(self, t: int):
        if t == 1:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['1'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['2'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['3'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['4'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['5'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['6'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['7'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['8'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['9'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['10'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['11'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['12'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['13'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['14'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['15'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['16'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['17'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['18'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['19'][self.language],
                               voice=Voice.GOVERMENT, logo=Icon.PHONE),
                DialoguePhrase(LANGUAGES['dialogues']['phone_talkings']['1episode']['20'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT, callback=self._on_phone_end)
            ])
        if t == 2:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['monologues']['1'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(LANGUAGES['monologues']['2'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT, callback=self._on_t2_end),
            ])
        if t == 3:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['monologues']['3'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(LANGUAGES['monologues']['4'][self.language],
                               voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT, callback=self._on_t3_end),
            ])
        if t == 4:
            self.dialog_box.start_dialogue([
                DialoguePhrase(LANGUAGES['dialogues']['postman_talkings']['1']
                               [self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN.DEFAULT),
                DialoguePhrase(LANGUAGES['dialogues']['postman_talkings']['2']
                               [self.language], voice=Voice.DEFAULT, logo=Icon.PLAYER.DEFAULT),
                DialoguePhrase(
                    LANGUAGES['dialogues']['postman_talkings']['3'][self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN.DEFAULT),
                DialoguePhrase(
                    LANGUAGES['dialogues']['postman_talkings']['4'][self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN.DEFAULT),
                DialoguePhrase(
                    LANGUAGES['dialogues']['postman_talkings']['5'][self.language], voice=Voice.POSTMAN, logo=Icon.POSTMAN.DEFAULT),
            ])

    def on_key_press(self, key, modifiers):
        if self.dialog_box.is_active and key in [arcade.key.ENTER, arcade.key.Z]:
            self.dialog_box.next_phrase()

    def on_resize(self, width, height):
        self.update_layout()
