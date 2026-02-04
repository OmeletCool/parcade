import arcade
from src.registry import reg
from src.settings import settings


class NavigationSprite(arcade.SpriteCircle):
    def __init__(self, radius, color, target_location):
        super().__init__(radius, color)
        self.target_location = target_location
        self.alpha = 100


class GameFieldView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.reg = reg

        self.location_order = ['forest', 'edge', 'rocks']
        self.current_location = 'forest'

        self.bg_list = arcade.SpriteList()
        self.ui_list = arcade.SpriteList()
        self.navigation_sprites = arcade.SpriteList()

        self.bg_sprite = None

        self.fade_alpha = 0
        self.is_fading = False
        self.next_location = None
        self.fade_speed = 600

    def on_show_view(self):
        self.setup()

    def setup(self):
        self.update_location_visuals()

    def update_location_visuals(self):
        self.bg_list.clear()
        self.navigation_sprites.clear()

        w, h = self.window.width, self.window.height

        bg_texture_path = f'1episode/textures/backgrounds/{self.current_location}.png'
        bg_tex = self.reg.get(bg_texture_path)

        if bg_tex:
            self.bg_sprite = arcade.Sprite(bg_tex)
            self.bg_sprite.position = (w / 2, h / 2)
            self.bg_sprite.width = w
            self.bg_sprite.height = h
            self.bg_list.append(self.bg_sprite)

        self._setup_navigation()

    def _setup_navigation(self):
        w, h = self.window.width, self.window.height
        radius = 40
        padding = 60
        color = arcade.color.WHITE

        if self.current_location == 'forest':
            back_btn = NavigationSprite(radius, color, 'yard')
            back_btn.position = (padding, padding)
            self.navigation_sprites.append(back_btn)

            next_btn = NavigationSprite(radius, color, 'edge')
            next_btn.position = (w - padding, padding)
            self.navigation_sprites.append(next_btn)

        elif self.current_location == 'edge':
            back_btn = NavigationSprite(radius, color, 'forest')
            back_btn.position = (padding, padding)
            self.navigation_sprites.append(back_btn)

            next_btn = NavigationSprite(radius, color, 'rocks')
            next_btn.position = (w - padding, padding)
            self.navigation_sprites.append(next_btn)

        elif self.current_location == 'rocks':
            back_btn = NavigationSprite(radius, color, 'edge')
            back_btn.position = (padding, padding)
            self.navigation_sprites.append(back_btn)

    def on_draw(self):
        self.clear()

        self.bg_list.draw()
        self.navigation_sprites.draw()

        if self.fade_alpha > 0:
            arcade.draw_lbwh_rectangle_filled(
                left=0, bottom=0,
                width=self.window.width, height=self.window.height,
                color=(0, 0, 0, int(self.fade_alpha))
            )

    def on_update(self, delta_time):
        if self.is_fading:
            if self.next_location:
                self.fade_alpha += self.fade_speed * delta_time
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.change_location_data()
            else:
                self.fade_alpha -= self.fade_speed * delta_time
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.is_fading = False

    def change_location_data(self):
        if self.next_location == 'yard':
            self.window.switch_view('game_backyard_view')
            return

        self.current_location = self.next_location
        self.next_location = None
        self.update_location_visuals()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_fading:
            return

        for sprite in self.navigation_sprites:
            if sprite.collides_with_point((x, y)):
                if isinstance(sprite, NavigationSprite):
                    self.start_transition(sprite.target_location)

    def start_transition(self, target_loc):
        self.is_fading = True
        self.next_location = target_loc
