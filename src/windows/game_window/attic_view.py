import arcade
from src.registry import reg


class AtticView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.reg = reg

        self.bg_list = arcade.SpriteList()
        self.interactable_sprites = arcade.SpriteList()

        self.bg_sprite = None

        # Кнопки

        # Диалоги

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
        if not self.window.game_state.get("key_picked_up", False):
            self.key_sprite = arcade.Sprite(
                self.reg.get('1episode/textures/items/key.png'))
            self.key_sprite.center_x = 300  # Поставь координаты где он спрятан
            self.key_sprite.center_y = 200
            self.interactable_sprites.append(self.key_sprite)

        self.update_layout()

    def _init_buttons(self):
        pass

    def _init_dialog_box(self):
        pass

    def update_layout(self):
        w, h = self.window.width, self.window.height

        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = w, h
            self.bg_sprite.position = (w / 2, h / 2)

    def on_update(self, delta_time):
        if self.fade_in:
            self.fade_timer += delta_time
            progress = min(self.fade_timer / self.fade_duration, 1.0)
            self.fade_alpha = int(255 * (1 - progress))

            if progress >= 1.0:
                self.fade_in = False

    def on_draw(self):
        self.clear()
        self.bg_list.draw()

        if self.interactable_sprites:
            self.interactable_sprites.draw()

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
        if not self.window.game_state.get("key_picked_up", False):
            if self.key_sprite and self.key_sprite.collides_with_point((x, y)):
                self.window.inventory.append("gate_key")
                self.window.game_state["key_picked_up"] = True
                self.key_sprite.remove_from_sprite_lists()
                # Тут можно вызвать диалог "Я нашел ключ"

    def on_key_press(self, key, modifiers):
        pass

    def on_resize(self, width, height):
        self.update_layout()
