import arcade
import random
import csv
import math

MARKER_COLOR = arcade.color.ELECTRIC_PURPLE
MARKER_TYPE = 'orbit'
MARKER_SOUND = "ANOMALY_DETECTION_STATIC"


class RippleEffect(arcade.SpriteCircle):
    def __init__(self, x, y):
        super().__init__(30, (255, 255, 255))
        self.center_x, self.center_y = x, y
        self.life = 1.0
        self.growth = 3.5

    def update(self, delta_time=1/60):
        self.life -= delta_time * 1.2
        self.width += self.growth
        self.height += self.growth
        self.alpha = int(max(0, self.life) * 150)
        if self.life <= 0:
            self.remove_from_sprite_lists()


class VisualEffect(arcade.SpriteCircle):
    def __init__(self, x, y, color, mode):
        super().__init__(random.randint(10, 18), color)
        self.center_x, self.center_y = x, y
        self.mode = mode
        self.life = 1.0
        self.angle = random.random() * math.pi * 2

    def update(self, delta_time=1/60):
        self.life -= delta_time
        if self.mode == 'orbit':
            self.center_x += math.cos(self.angle) * 6
            self.center_y += math.sin(self.angle) * 6
            self.angle += 0.2
        else:
            self.center_y += 0.8
        self.alpha = int(max(0, self.life) * 255)
        if self.life <= 0:
            self.remove_from_sprite_lists()


class GameItem(arcade.Sprite):
    def __init__(self, config, is_anomaly):
        scale_val = float(config['scale'])
        super().__init__(config['path'].replace('\\', '/'), scale_val)
        self.id = config['id']
        self.is_anomaly = is_anomaly
        self.stage = 0
        self.timer = 0.0
        # Относительные координаты для ресайза в лесу
        self.rel_x = 0.0
        self.rel_y = 0.0

    def start_inspection(self, sw, sh):
        self.stage = 1
        self.alpha = 255
        self.scale_x *= 1.8
        self.scale_y *= 1.8
        self.center_x, self.center_y = sw / 2, sh / 2


class ItemSpawner:
    def __init__(self, window):
        self.window = window
        self.active_item = None
        self.item_list = arcade.SpriteList()
        self.effects_list = arcade.SpriteList()
        self.particles = arcade.SpriteList()
        self.ripples = arcade.SpriteList()
        self.items_to_spawn = 10
        self.spawn_timer = 0
        self.spawn_interval = 12.0
        self.stats = {"found": 0, "anomalies_caught": 0, "failed_shots": 0}
        self.anchors = {
            'forest': [(420, 245), (680, 310), (950, 215)],
            'edge':   [(380, 275), (710, 240), (1050, 320)],
            'rocks':  [(480, 420), (620, 340), (980, 460)]
        }

    def update(self, delta_time, current_loc, camera_on, mouse_pos):
        self.effects_list.update()
        self.particles.update()
        self.ripples.update()

        is_night = self.window.night_data.get("is_night_active", False)

        # Если 6 утра уже наступило — ничего не делаем
        if self.window.night_data.get("hours", 0) >= 6:
            return

        # Динамическое обновление времени в зависимости от прогресса (декоративно)
        # 10 предметов -> распределяем на 5 часов (с 1 AM до 6 AM)
        progress = (10 - self.items_to_spawn) / 10
        current_hour = 1 + int(progress * 4)  # Будет идти от 1 до 5
        self.window.night_data["hours"] = current_hour
        self.window.night_data["current_time"] = f"{current_hour} AM"

        # Проверка завершения смены
        if self.items_to_spawn <= 0 and not self.active_item:
            self.spawn_timer += delta_time
            if self.spawn_timer >= 3.0:  # Задержка 3 секунды после крайнего предмета
                self.window.night_data["hours"] = 6
                self.window.night_data["current_time"] = "6:00 AM"
            return

        # Спавн предметов
        if is_night and not self.active_item and self.items_to_spawn > 0:
            self.spawn_timer += delta_time
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                self.spawn_random_item(current_loc)

        if self.active_item:
            # ... (логика эффектов Stage 0 и Stage 1 остается без изменений) ...
            self.active_item.timer += delta_time
            # Stage 0:
            if self.active_item.stage == 0:
                if random.random() < 0.03:
                    self.particles.append(VisualEffect(
                        self.active_item.center_x, self.active_item.center_y, arcade.color.WHITE, 'float'))
                if random.random() < 0.01:
                    self.ripples.append(RippleEffect(
                        self.active_item.center_x, self.active_item.center_y))
            # Stage 1:
            elif self.active_item.stage == 1 and camera_on:
                dist = math.dist(
                    mouse_pos, (self.active_item.center_x, self.active_item.center_y))
                if dist < 150:
                    if random.random() < 0.04:
                        self.effects_list.append(VisualEffect(
                            self.active_item.center_x, self.active_item.center_y, arcade.color.GRAY, 'float'))
                    if self.active_item.is_anomaly and random.random() < 0.03:
                        if random.random() < 0.5:
                            print(f"🔊 {MARKER_SOUND}")
                        else:
                            self.effects_list.append(VisualEffect(
                                self.active_item.center_x, self.active_item.center_y, MARKER_COLOR, MARKER_TYPE))

            # Авто-пропуск предмета по таймеру
            if self.active_item.timer > (15.0 if self.active_item.stage == 0 else 10.0):
                self.resolve_item()

    def spawn_random_item(self, loc):
        try:
            with open('resources/items.csv', mode='r', encoding='utf-8') as f:
                valid = [r for r in csv.DictReader(
                    f) if loc in r['tags'].split(';')]
            if valid and loc in self.anchors:
                cfg = random.choice(valid)
                pos = random.choice(self.anchors[loc])
                self.active_item = GameItem(
                    cfg, is_anomaly=(random.random() < 0.5))
                self.active_item.position = pos
                self.active_item.rel_x = pos[0] / self.window.width
                self.active_item.rel_y = pos[1] / self.window.height
                self.active_item.alpha = 0
                self.item_list.clear()
                self.item_list.append(self.active_item)
                self.items_to_spawn -= 1
        except Exception as e:
            print(f"Spawn Error: {e}")

    def resolve_item(self, photographed=False):
        if not self.active_item:
            return
        if photographed:
            if self.active_item.is_anomaly:
                self.stats["anomalies_caught"] += 1
            else:
                self.stats["failed_shots"] += 1
            self.stats["found"] += 1
        self.active_item.remove_from_sprite_lists()
        self.active_item = None
        self.item_list.clear()
