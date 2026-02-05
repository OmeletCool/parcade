import arcade
from src.registry import reg
from resources.dialog_box import *
from resources.languages import LANGUAGES


class AtticView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.reg = reg
        self.language: int = self.window.language

        self.bg_list = arcade.SpriteList()
        self.interactable_sprites = arcade.SpriteList()

        self.bg_sprite = None
        self.key_sprite = None

        # Диалоговое окно
        self.dialog_box = DialogBox(
            self.window, default_font_name="Montserrat")

        self.transition_to_house = False
        self.transition_timer = 0.0
        self.transition_duration = 1.0
        self.fade_alpha = 0
        
        self.fade_in = True
        self.fade_in_timer = 0.0
        self.fade_in_duration = 1.0
        self.fade_in_alpha = 255

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()

    def setup(self):
        # Загружаем фон если еще не загружен
        if not self.bg_sprite:
            attic_texture = self.reg.get('1episode/textures/backgrounds/attic.png')
            self.bg_sprite = arcade.Sprite(attic_texture)
            self.bg_list.append(self.bg_sprite)

        # Загружаем ключ только если он еще не подобран
        if (not self.window.game_state.get("key_picked_up", False) 
                and not self.key_sprite):
            self.key_sprite = arcade.Sprite(
                self.reg.get('1episode/textures/ui/buttons/key.png'))
            self.interactable_sprites.append(self.key_sprite)

        self.update_layout()

    def update_layout(self):
        w, h = self.window.width, self.window.height

        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = w, h
            self.bg_sprite.position = (w / 2, h / 2)

        if not self.window.game_state.get("key_picked_up", False) and self.key_sprite:
            self.key_sprite.center_x = w * 0.82
            self.key_sprite.center_y = h * 0.37
            self.key_sprite.scale = min(w / 1920, h / 1080) * 0.8

        self.dialog_box._setup_dimensions()

    def on_update(self, delta_time):
        # Fade-in при входе
        if self.fade_in:
            self.fade_in_timer += delta_time
            progress = min(self.fade_in_timer / self.fade_in_duration, 1.0)
            self.fade_in_alpha = int(255 * (1 - progress))
            if progress >= 1.0:
                self.fade_in = False
                self.fade_in_alpha = 0

        # Переход обратно в дом
        if self.transition_to_house:
            self.transition_timer += delta_time
            progress = min(self.transition_timer / self.transition_duration, 1.0)
            self.fade_alpha = int(255 * progress)
            
            if progress >= 1.0:
                # Полностью затемнили - переключаемся
                self.transition_to_house = False
                self.fade_alpha = 0
                # Используем switch_view который должен сохранять состояние
                self.window.switch_view('game_house_view')
                return

        self.dialog_box.update(delta_time)

    def on_draw(self):
        self.clear()
        self.bg_list.draw()
        
        if self.interactable_sprites:
            self.interactable_sprites.draw()
        
        self.dialog_box.draw()
        
        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, self.window.width, 0, self.window.height,
                color=(0, 0, 0, self.fade_alpha)
            )
        
        if self.fade_in_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, self.window.width, 0, self.window.height,
                color=(0, 0, 0, self.fade_in_alpha)
            )

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if self.transition_to_house or self.fade_in or self.dialog_box.is_active:
            return
            
        if not self.window.game_state.get("key_picked_up", False) and self.key_sprite:
            if self.key_sprite.collides_with_point((x, y)):
                self.window.inventory.append("gate_key")
                self.window.game_state["key_picked_up"] = True
                
                self.key_sprite.remove_from_sprite_lists()
                self.key_sprite = None
                
                self.show_key_dialog()

    def show_key_dialog(self):
        key_message = LANGUAGES['dialogues']['items']['key_found'][self.language]
        
        self.dialog_box.start_dialogue([
            DialoguePhrase(
                text=key_message,
                voice=Voice.DEFAULT,
                speed=30,
                skippable=True
            )
        ])

    def on_key_press(self, key, modifiers):
        if self.transition_to_house:
            return
            
        if self.dialog_box.is_active and key in [arcade.key.ENTER, arcade.key.Z, arcade.key.SPACE]:
            self.dialog_box.next_phrase()
        
        elif key == arcade.key.ESCAPE:
            if not self.transition_to_house and not self.fade_in:
                self.transition_to_house = True
                self.transition_timer = 0.0

    def on_resize(self, width, height):
        self.update_layout()