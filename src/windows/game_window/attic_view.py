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

        self.fade_in = True
        self.fade_timer = 0.0
        self.fade_duration = 1.0
        self.fade_alpha = 255

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()

    def setup(self):
        zzz_texture = self.reg.get('1episode/textures/backgrounds/attic.png')
        self.bg_sprite = arcade.Sprite(zzz_texture)
        self.bg_list.append(self.bg_sprite)

        # Загружаем ключ только если он еще не подобран
        if not self.window.game_state.get("key_picked_up", False):
            self.load_key()

        self.update_layout()

    def load_key(self):
        """Загружает спрайт ключа"""
        self.key_sprite = arcade.Sprite(
            self.reg.get('1episode/textures/ui/buttons/key.png'))
        # Устанавливаем позицию в правой части окна посередине
        self.key_sprite.center_x = self.window.width * 0.85
        self.key_sprite.center_y = self.window.height * 0.5
        # Опционально: масштабируем ключ относительно размера окна
        self.key_sprite.scale = min(self.window.width / 1920, self.window.height / 1080) * 0.8
        self.interactable_sprites.append(self.key_sprite)

    def _init_buttons(self):
        pass

    def _init_dialog_box(self):
        pass

    def update_layout(self):
        w, h = self.window.width, self.window.height

        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = w, h
            self.bg_sprite.position = (w / 2, h / 2)

        if not self.window.game_state.get("key_picked_up", False) and self.key_sprite:
            self.key_sprite.center_x = w * 0.82
            self.key_sprite.center_y = h * 0.37
            self.key_sprite.scale = min(w / 1920, h / 1080) * 0.8

        # Обновляем размеры диалогового окна
        self.dialog_box._setup_dimensions()

    def on_update(self, delta_time):
        # Обновляем анимацию появления
        if self.fade_in:
            self.fade_timer += delta_time
            progress = min(self.fade_timer / self.fade_duration, 1.0)
            self.fade_alpha = int(255 * (1 - progress))

            if progress >= 1.0:
                self.fade_in = False

        # Обновляем диалоговое окно
        self.dialog_box.update(delta_time)

    def on_draw(self):
        self.clear()
        self.bg_list.draw()

        if self.interactable_sprites:
            self.interactable_sprites.draw()

        self.dialog_box.draw()

        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.window.width,
                bottom=0,
                top=self.window.height,
                color=(0, 0, 0, self.fade_alpha)
            )

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.window.game_state.get("key_picked_up", False) and self.key_sprite:
            if self.key_sprite.collides_with_point((x, y)):
                # Добавляем ключ в инвентарь
                self.window.inventory.append("gate_key")
                self.window.game_state["key_picked_up"] = True
                
                self.key_sprite.remove_from_sprite_lists()
                
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
        if self.dialog_box.is_active and key in [arcade.key.ENTER]:
            self.dialog_box.next_phrase()

    def on_resize(self, width, height):
        self.update_layout()