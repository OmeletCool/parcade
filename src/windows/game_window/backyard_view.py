import arcade
from src.registry import reg
from resources.dialog_box import *
from src.settings import settings
from resources.languages import LANGUAGES


class BackyardView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.reg = reg
        self.language = self.window.language

        self.bg_list = arcade.SpriteList()
        self.interactable_sprites = arcade.SpriteList()
        self.character_sprites = arcade.SpriteList()

        self.bg_sprite = None
        self.gate_sprite = None
        self.postman_sprite = None

        self.locker_texture_hovered = None
        self.locker_texture = None

        self.dialog_box = DialogBox(
            self.window, default_font_name="Montserrat")
        
        self.is_night = self.window.night_data['is_night_active']

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.is_night = self.window.night_data['is_night_active']
        self.setup()

    def setup(self):
        self.bg_list = arcade.SpriteList()
        self.interactable_sprites = arcade.SpriteList()
        self.character_sprites = arcade.SpriteList()

        if self.is_night:
            bg_tex = self.reg.get('1episode/textures/backgrounds/backjard_night.png')
            self.locker_texture = self.reg.get('1episode/textures/ui/buttons/normal/locker_night.png')
            self.locker_texture_hovered = self.reg.get('1episode/textures/ui/buttons/hovered/locker_night_hovered.png')
        else:
            bg_tex = self.reg.get('1episode/textures/backgrounds/backjard_day.png')
            self.locker_texture = self.reg.get('1episode/textures/ui/buttons/normal/locker_day.png')
            self.locker_texture_hovered = self.reg.get(
            '1episode/textures/ui/buttons/hovered/locker_day_hovered.png')
            
        self.bg_sprite = arcade.Sprite(bg_tex)
        self.bg_sprite.position = (
            self.window.width / 2, self.window.height / 2)
        self.bg_sprite.width = self.window.width
        self.bg_sprite.height = self.window.height
        self.bg_list.append(self.bg_sprite)
        
        is_open = self.window.game_state.get("is_gate_open", False)
        current_tex = self.locker_texture_hovered if is_open else self.locker_texture
        self.gate_sprite = arcade.Sprite(current_tex)
        self.gate_sprite.center_x = self.window.width * 0.51
        self.gate_sprite.center_y = self.window.height * 0.337
        self.gate_sprite.scale_x *= 1.3
        self.gate_sprite.scale_y *= 1.3
        self.interactable_sprites.append(self.gate_sprite)

        if self.window.game_state.get("postman_in_backyard", False):
            if self.is_night:
                postman_tex = self.reg.get('1episode/textures/npc/postman_night.png')
            else:
                postman_tex = self.reg.get('1episode/textures/npc/postman_day.png')
            self.postman_sprite = arcade.Sprite(postman_tex)
            self.postman_sprite.center_x = self.gate_sprite.center_x - 100
            self.postman_sprite.center_y = self.gate_sprite.center_y + 15
            self.postman_sprite.scale_x *= 3
            self.postman_sprite.scale_y *= 3
            self.character_sprites.append(self.postman_sprite)

        self.dialog_box._setup_dimensions()
    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.gate_sprite.center_x = self.window.width * 0.51
        self.gate_sprite.center_y = self.window.height * 0.337
        
        self.bg_sprite.position = (
            self.window.width / 2, self.window.height / 2)
        self.bg_sprite.width = self.window.width
        self.bg_sprite.height = self.window.height
        
        self.postman_sprite.center_x = self.gate_sprite.center_x - 100
        self.postman_sprite.center_y = self.gate_sprite.center_y + 15

    def on_draw(self):
        self.clear()
        self.bg_list.draw()
        self.interactable_sprites.draw()
        self.character_sprites.draw()
        self.dialog_box.draw()

    def on_update(self, delta_time):
        self.dialog_box.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.dialog_box.is_active:
            self.dialog_box.next_phrase()
            return

        if self.gate_sprite.collides_with_point((x, y)):
            self._handle_gate_click()
            return

        if self.postman_sprite and self.postman_sprite.collides_with_point((x, y)):
            self.dialog_box.start_dialogue([
                DialoguePhrase(". . .", voice=Voice.NONE, speed=10)
            ])
            return

        if x < 100:
            self.window.switch_view('game_house_view')

    def _handle_gate_click(self):
        if self.window.game_state["is_gate_locked"]:
            if "gate_key" in self.window.inventory:
                self.window.game_state["is_gate_locked"] = False
                self.window.inventory.remove("gate_key")
                self.dialog_box.start_dialogue([
                    DialoguePhrase(
                        LANGUAGES['dialogues']['items']['key_used'][self.language], voice=Voice.DEFAULT)
                ])
                self.window.play_definite_music(
                    'common/sounds/sfx/items/unlock.wav')
            else:
                self.dialog_box.start_dialogue([
                    DialoguePhrase(
                        LANGUAGES['dialogues']['items']['gate_locked'][self.language], voice=Voice.PLAYER)
                ])
            return
        is_open = self.window.game_state['is_gate_open']

        if not is_open:
            self.window.game_state["is_gate_open"] = True
            self.gate_sprite.texture = self.locker_texture_hovered
            self.window.play_definite_music(
                'common/sounds/sfx/doors/door_open.wav')

        else:
            self.window.switch_view('game_field_view')

    def on_key_press(self, key, modifiers):
        if self.dialog_box.is_active and key in [arcade.key.ENTER, arcade.key.Z]:
            self.dialog_box.next_phrase()
