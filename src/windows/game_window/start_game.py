import arcade
from src.registry import reg
from resources.dialog_box import *
from src.settings import settings


class StartGame(arcade.View):
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

        self.bg_sprite = None

        self.bg_list = arcade.SpriteList()
        self.bg_sprite = arcade.Sprite()

        self.fade_list = arcade.SpriteList()

        self.fade_sprite = None

    def on_show_view(self):
        self.window.background_color = arcade.color.BLACK
        self.setup()

    def setup(self):
        self.intro_textures = [self.reg.get(
            f'1episode/textures/intro/{img}') for img in self.intro_images]

        self.bg_list.append(self.bg_sprite)

        self.fade_sprite = arcade.SpriteSolidColor(100, 100, color=(0, 0, 0))
        self.fade_sprite.alpha = 255
        self.fade_list.append(self.fade_sprite)

        self.intro_active = True
        self.on_resize(self.window.width, self.window.height)

    def on_update(self, delta_time):
        if self.intro_active:
            self.slide_time += delta_time
            is_last = self.current_slide_idx == 2
            self.bg_sprite.texture = self.intro_textures[self.current_slide_idx]
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
                    self.window.switch_view('game_house_view')

    def on_draw(self):
        self.clear()
        self.bg_list.draw()

        if self.intro_active:
            self.fade_list.draw()

    def on_resize(self, width, height):
        w, h = width, height

        if self.bg_sprite:
            self.bg_sprite.width, self.bg_sprite.height = w, h
            self.bg_sprite.position = (w / 2, h / 2)
        if self.fade_sprite:
            self.fade_sprite.width, self.fade_sprite.height = w, h
            self.fade_sprite.position = (w / 2, h / 2)
