import arcade
import arcade.gui
import csv
import random
import math
from dataclasses import dataclass
from typing import List, Optional, Dict

DB_PATH = "resources/items.csv"
BG_PATH = "resources/1episode/textures/backgrounds/first_episode_bg.png"

SPAWN_RATIOS = [
    (0.25, 0.30, "ground"),
    (0.50, 0.45, "tree"),
    (0.75, 0.25, "mud"),
    (0.40, 0.15, "ground")
]


@dataclass
class ItemConfig:
    id: str
    name: str
    desc: str
    tags: List[str]
    path: str
    scale: float


class ActiveItem(arcade.Sprite):
    def __init__(self, config: ItemConfig, x_ratio: float, y_ratio: float, window_w: int, window_h: int):
        tex = arcade.load_texture(config.path)
        super().__init__(tex)
        self.config = config
        self.x_ratio = x_ratio
        self.y_ratio = y_ratio
        self.scale = config.scale
        self.is_revealed = False
        self.anim_timer = random.uniform(0, 10)
        self.update_position(window_w, window_h)

    def update_position(self, w, h):
        self.center_x = self.x_ratio * w
        self.base_y = self.y_ratio * h
        self.center_y = self.base_y

    def update(self, delta_time: float):
        if not self.is_revealed:
            self.anim_timer += delta_time * 5
            self.center_y = self.base_y + math.sin(self.anim_timer) * 3
            self.alpha = 100
        else:
            self.alpha, self.center_y = 255, self.base_y


class InspectionUI(arcade.gui.UIManager):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.enable()
        self.visible = False
        self.active_item: Optional[ItemConfig] = None
        self._name_text = None
        self._desc_text = None

    def show(self, item: ItemConfig):
        self.clear()
        self.active_item, self.visible = item, True

        # 1. Готовим текст заранее
        cx, cy = self.window.width // 2, self.window.height // 2

        # Поднимаем текст названия чуть выше центра
        self._name_text = arcade.Text(
            item.name, cx, cy + 20, arcade.color.WHITE,
            font_size=22, bold=True, anchor_x="center"
        )

        # Описание чуть ниже названия
        self._desc_text = arcade.Text(
            item.desc, cx, cy - 30, arcade.color.LIGHT_GRAY,
            font_size=14, anchor_x="center", multiline=True, width=380, align="center"
        )

        # 2. Создаем контейнер для кнопки
        v_box = arcade.gui.UIBoxLayout()
        # Увеличиваем пустой отступ сверху до 280, чтобы кнопка не «подпирала» текст
        v_box.add(arcade.gui.UISpace(height=280))

        btn = arcade.gui.UIFlatButton(text="ВЗЯТЬ", width=140)
        btn.on_click = self._hide
        v_box.add(btn)

        anchor = arcade.gui.UIAnchorLayout()
        # Увеличиваем высоту самого окна до 420, чтобы всё влезло
        anchor.add(arcade.gui.UIWidget(
            child=v_box, width=500, height=420,
            style={"bg_color": (20, 20, 30, 250), "border_radius": 30}
        ), anchor_x="center", anchor_y="center")
        self.add(anchor)

    def draw_custom(self):
        if not self.visible or not self.active_item:
            return

        # 1. Рисуем темную вуаль на весь экран
        arcade.draw_lrbt_rectangle_filled(
            0, self.window.width, 0, self.window.height, (0, 0, 0, 180))

        # 2. Рисуем саму плашку меню и кнопку
        self.draw()

        cx, cy = self.window.width // 2, self.window.height // 2

        # 3. Рисуем текст (теперь он точно поверх плашки)
        if self._name_text:
            self._name_text.x, self._name_text.y = cx, cy + 35
            self._name_text.draw()
        if self._desc_text:
            self._desc_text.x, self._desc_text.y = cx, cy - 25
            self._desc_text.draw()

        # 4. РИСУЕМ ИКОНКУ (Ботинок) — теперь он на самом верху (cy + 150)
        tex = arcade.load_texture(self.active_item.path)

        # Динамический скейл: берем базу из CSV и адаптируем под экран
        s = self.active_item.scale * (self.window.width / 1280)

        # Рисуем иконку ВЫШЕ текста названия
        target_w = tex.width * s
        target_h = tex.height * s

        # Ограничиваем размер иконки, чтобы она не сошла с ума
        if target_h > 120:
            target_w *= (120 / target_h)
            target_h = 120

        arcade.draw_texture_rect(
            tex,
            arcade.XYWH(cx, cy + 150, target_w, target_h),
            color=arcade.color.WHITE
        )

    def _hide(self, _=None):
        self.visible = False
        self.active_item = None
        self.clear()


class GameView(arcade.Window):
    def __init__(self):
        super().__init__(1280, 720, "Forest Search", resizable=True)
        self.sprites = arcade.SpriteList()
        self.db: Dict[str, ItemConfig] = {}
        self.background = None
        try:
            self.background = arcade.load_texture(BG_PATH)
        except:
            pass

        self._load_csv(DB_PATH)
        self.ui = InspectionUI(self)
        self.reload_level()

    def _load_csv(self, path):
        try:
            with open(path, mode='r', encoding='utf-8') as f:
                for r in csv.DictReader(f):
                    self.db[r['id']] = ItemConfig(r['id'], r['name'], r['desc'],
                                                  r['tags'].split(';'), r['path'], float(r['scale']))
        except:
            print("CSV Error")

    def reload_level(self):
        # ОЧЕНЬ ВАЖНО: сначала закрываем UI, потом чистим спрайты
        self.ui._hide()
        self.sprites.clear()

        for x_rat, y_rat, tag in SPAWN_RATIOS:
            possible = [c for c in self.db.values() if tag in c.tags]
            if possible:
                cfg = random.choice(possible)
                self.sprites.append(ActiveItem(
                    cfg, x_rat, y_rat, self.width, self.height))

    def on_resize(self, width, height):
        super().on_resize(width, height)
        for sprite in self.sprites:
            if isinstance(sprite, ActiveItem):
                sprite.update_position(width, height)

    def on_key_press(self, key, modifiers):
        # Теперь E работает всегда
        if key == arcade.key.E:
            self.reload_level()

    def on_draw(self):
        self.clear()
        if self.background:
            arcade.draw_texture_rect(self.background, arcade.XYWH(
                self.width//2, self.height//2, self.width, self.height))
        self.sprites.draw()
        self.ui.draw_custom()

    def on_update(self, delta_time):
        if not self.ui.visible:
            self.sprites.update(delta_time)

    def on_mouse_press(self, x, y, btn, mod):
        if self.ui.visible:
            self.ui.on_mouse_press(x, y, btn, mod)
            return
        hit = arcade.get_sprites_at_point((x, y), self.sprites)
        if hit:
            item = hit[0]
            if not item.is_revealed:
                item.is_revealed = True
            else:
                self.ui.show(item.config)


if __name__ == "__main__":
    GameView().run()
