import arcade
import arcade.gui
import csv
import random
import math
import time
import os
from dataclasses import dataclass


@dataclass
class ItemConfig:
    id: str
    name: str
    path: str
    scale: float
    cooldown: float


class Particle(arcade.SpriteSolidColor):
    def __init__(self, x, y, size):
        super().__init__(int(size), int(size), (100, 255, 100))
        self.center_x, self.center_y = x, y
        self.change_x = random.uniform(-0.8, 0.8)
        self.change_y = random.uniform(0.5, 1.5)
        self.life = 1.0

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.life -= delta_time
        self.alpha = int(max(0, self.life) * 255)
        if self.life <= 0:
            self.remove_from_sprite_lists()


class GameItem(arcade.Sprite):
    def __init__(self, config, x, y):
        # Проверка пути, чтобы не поймать PermissionError на папке
        safe_path = config.path if config.path and os.path.isfile(
            config.path) else ":resources:images/items/gemBlue.png"
        super().__init__(safe_path, scale=config.scale)
        self.center_x, self.center_y = x, y
        self.config = config
        self.state = 0  # 0 - скрыт, 1 - найден/камера
        self.spawn_time = time.time()

    def update_logic(self):
        if self.state == 0 and (time.time() - self.spawn_time > self.config.cooldown):
            return False
        return True


class ItemSpawner:
    def __init__(self, window: arcade.Window):
        self.window = window
        self.db = []
        self.items = arcade.SpriteList()
        self.particles = arcade.SpriteList()
        self.camera_active = False
        self.flash = 0
        self.cx = self.cy = 0
        self.cw, self.ch = 300, 200

        self.load_db("resources/items.csv")
        self.ui = arcade.gui.UIManager()
        self.ui.enable()
        self.setup_ui()

    def setup_ui(self):
        box = arcade.gui.UIAnchorLayout()
        btn = arcade.gui.UIFlatButton(text="CLOSE CAMERA", width=150)

        @btn.event("on_click")
        def exit_cam(event):
            self.camera_active = False
            for s in self.items:
                s.state = 0  # Сбрасываем найденный предмет

        box.add(child=btn, anchor_x="right",
                anchor_y="bottom", align_x=-20, align_y=20)
        self.ui.add(box)

    def load_db(self, path):
        if not os.path.exists(path):
            return
        with open(path, mode='r', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                self.db.append(ItemConfig(row['id'], row['name'], row['path'], float(
                    row['scale']), float(row.get('cooldown', 15))))

    def spawn(self):
        if not self.db or self.camera_active:
            return
        cfg = random.choice(self.db)
        self.items.append(GameItem(cfg, random.randint(
            100, self.window.width-100), random.randint(100, self.window.height-100)))

    def update(self, dt):
        if self.flash > 0:
            self.flash = max(0, self.flash - 15)
        if not self.camera_active and random.random() < 0.01:
            self.spawn()

        for item in self.items:
            if not item.update_logic():
                item.remove_from_sprite_lists()
            elif item.state == 0 and random.random() < 0.05:
                self.particles.append(
                    Particle(item.center_x, item.center_y, 4))

        self.particles.update(dt)

    def draw(self):
        self.particles.draw()

        if self.camera_active:
            w, h = self.window.width, self.window.height
            l, r = self.cx - self.cw/2, self.cx + self.cw/2
            b, t = self.cy - self.ch/2, self.cy + self.ch/2

            for s in self.items:
                s.alpha = 255
                # Подсветка если в фокусе
                if l < s.center_x < r and b < s.center_y < t:
                    s.color = (255, 255, 255)
                else:
                    s.color = (30, 30, 30)

            self.items.draw()

            # Маска (безопасные координаты через min/max)
            f_l, f_r = max(0, min(w, l)), max(0, min(w, r))
            f_b, f_t = max(0, min(h, b)), max(0, min(h, t))

            arcade.draw_lrbt_rectangle_filled(
                0, w, f_t, h, (0, 0, 0, 220))  # верх
            arcade.draw_lrbt_rectangle_filled(
                0, w, 0, f_b, (0, 0, 0, 220))  # низ
            arcade.draw_lrbt_rectangle_filled(
                0, f_l, f_b, f_t, (0, 0, 0, 220))  # лево
            arcade.draw_lrbt_rectangle_filled(
                f_r, w, f_b, f_t, (0, 0, 0, 220))  # право
            arcade.draw_rect_outline(arcade.rect.XYWH(
                self.cx, self.cy, self.cw, self.ch), arcade.color.WHITE, 2)
        else:
            for s in self.items:
                s.alpha = 255 if s.state == 1 else 0
            self.items.draw()

        if self.flash > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, self.window.width, 0, self.window.height, (255, 255, 255, self.flash))

        if self.camera_active:
            self.ui.draw()

    def on_mouse_press(self, x, y, button):
        if button == arcade.MOUSE_BUTTON_LEFT and not self.camera_active:
            for item in self.items:
                if math.dist((x, y), (item.center_x, item.center_y)) < 60:
                    item.state = 1
                    self.camera_active = True
                    break
        elif button == arcade.MOUSE_BUTTON_RIGHT and self.camera_active:
            self.flash = 255
            for item in self.items:
                if item.state == 1:
                    l, r = self.cx - self.cw/2, self.cx + self.cw/2
                    b, t = self.cy - self.ch/2, self.cy + self.ch/2
                    if l < item.center_x < r and b < item.center_y < t:
                        item.remove_from_sprite_lists()
                        self.camera_active = False
                        break


if __name__ == "__main__":
    class Win(arcade.Window):
        def __init__(self):
            super().__init__(1280, 720, "Photo Hunt")
            self.s = ItemSpawner(self)

        def on_draw(self):
            self.clear(arcade.color.DARK_SLATE_GRAY)
            self.s.draw()

        def on_update(self, dt): self.s.update(dt)
        def on_mouse_motion(self, x, y, dx, dy): self.s.cx, self.s.cy = x, y

        def on_mouse_press(
            self, x, y, btn, mod): self.s.on_mouse_press(x, y, btn)

    Win()
    arcade.run()
