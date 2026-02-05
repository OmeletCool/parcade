import arcade
import math
from resources.items_spawning import ItemSpawner
from resources.dialog_box import DialoguePhrase, Voice, TextEffect, DialogBox


class NavigationSprite(arcade.SpriteCircle):
    def __init__(self, radius, color, target_location):
        super().__init__(radius, color)
        self.target_location = target_location
        self.alpha = 150
        self.rel_x = 0.0
        self.rel_y = 0.0


class GameFieldView(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.spawner = ItemSpawner(self.window)

        # Инициализация текстов
        self.debug_label = arcade.Text("", 0, 0, arcade.color.YELLOW, 11)
        self.stats_label = arcade.Text("", 0, 0, arcade.color.NEON_GREEN, 11)
        self.time_label = arcade.Text("", 30, 0, arcade.color.WHITE, 20)
        self.morning_msg = arcade.Text(
            "6:00 AM\nПОРА ДОМОЙ", 0, 0, arcade.color.WHITE, 30, align="center", anchor_x="center")

        self.current_location = 'forest'
        self.bg_list = arcade.SpriteList()
        self.navigation_sprites = arcade.SpriteList()

        self.camera_on = False
        self.flash_alpha = 0
        self.fade_alpha = 0
        self.is_fading = False
        self.next_location = None
        self.fade_speed = 600
        self.night_timer = 0
        self.hour_duration = 30.0

        self.cam_btn_x, self.cam_btn_y = 100, 100
        self.cam_btn_radius = 40

        self.dialog_box = DialogBox(window)
        self.end_sequence_triggered = False
        self.dialogue_started = False

    def on_show_view(self):
        self.setup()

    def setup(self):
        self.update_location_visuals()
        # Принудительно вызываем ресайз при старте, чтобы всё встало на места
        self.on_resize(self.window.width, self.window.height)

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        # 1. Фон
        for bg in self.bg_list:
            bg.width, bg.height = width, height
            bg.position = (width / 2, height / 2)

        # 2. ПРЕДМЕТЫ (Stage 0 и Stage 1)
        item = self.spawner.active_item
        if item:
            if item.stage == 1:
                item.center_x, item.center_y = width / 2, height / 2
            else:
                # Stage 0: двигаем предмет за экраном
                item.center_x = item.rel_x * width
                item.center_y = item.rel_y * height

        # 3. НАВИГАЦИЯ (теперь всегда)
        for s in self.navigation_sprites:
            s.center_x = s.rel_x * width
            s.center_y = s.rel_y * height

        # 4. ТЕКСТЫ И ИНТЕРФЕЙС
        self.time_label.y = height - 50
        self.debug_label.position = (width - 250, height - 40)
        self.stats_label.position = (width - 250, height - 60)
        self.cam_btn_y = 100

    def register_miss(self):
        pass

    def update_location_visuals(self):
        self.bg_list.clear()
        self.navigation_sprites.clear()

        is_night = self.window.night_data.get("is_night_active", False)
        suffix = "night" if is_night else "day"

        # СТРОГО ТВОЙ ПУТЬ
        path = f'1episode/textures/backgrounds/{self.current_location}_{suffix}.png'
        bg_tex = self.window.reg.get(path)

        if bg_tex:
            bg = arcade.Sprite(bg_tex)
            bg.width, bg.height = self.window.width, self.window.height
            bg.position = (self.window.width / 2, self.window.height / 2)
            self.bg_list.append(bg)
        else:
            print(f"ОШИБКА: Не найден фон {path}")

        # Навигация
        locs = ['forest', 'edge', 'rocks']
        idx = locs.index(self.current_location)
        w, h = self.window.width, self.window.height

        if idx > 0:
            n = NavigationSprite(30, arcade.color.WHITE, locs[idx-1])
            n.rel_x, n.rel_y = 60/w, 0.5
            self.navigation_sprites.append(n)
        if idx < len(locs) - 1:
            n = NavigationSprite(30, arcade.color.WHITE, locs[idx+1])
            n.rel_x, n.rel_y = (w-60)/w, 0.5
            self.navigation_sprites.append(n)

        # Обновляем их позиции сразу
        for s in self.navigation_sprites:
            s.center_x = s.rel_x * w
            s.center_y = s.rel_y * h

    def draw_camera_viewfinder(self, width, height):
        cx, cy = self.window._mouse_x, self.window._mouse_y
        sw = width * 0.2
        sh = height * 0.2
        w, h = width, height

        # Безопасные границы для LRBT
        l, r = max(0, cx - sw), min(w, cx + sw)
        b, t = max(0, cy - sh), min(h, cy + sh)

        # Рамка
        arcade.draw_rect_outline(arcade.rect.XYWH(
            cx, cy, sw*2, sh*2), arcade.color.WHITE, 2)

        # Шторы (проверка l < r и b < t обязательна)
        if 0 < l:
            arcade.draw_lrbt_rectangle_filled(0, l, 0, h, (0, 0, 0, 230))
        if r < w:
            arcade.draw_lrbt_rectangle_filled(r, w, 0, h, (0, 0, 0, 230))
        if l < r:
            if t < h:
                arcade.draw_lrbt_rectangle_filled(l, r, t, h, (0, 0, 0, 230))
            if 0 < b:
                arcade.draw_lrbt_rectangle_filled(l, r, 0, b, (0, 0, 0, 230))

    def on_draw(self):
        self.clear()
        self.bg_list.draw()

        # Если 6 утра, рисуем только фон и диалог (убираем интерфейс камеры и навигацию)
        if self.window.night_data.get("hours") < 6:
            self.navigation_sprites.draw()
            self.spawner.ripples.draw()
            self.spawner.particles.draw()
            self.spawner.item_list.draw()
            self.spawner.effects_list.draw()

            if self.camera_on and self.window.night_data.get("is_night_active"):
                self.draw_camera_viewfinder(self.window.width, self.window.height)

            # Рисуем часы и кнопку только ночью
            if self.window.night_data.get("is_night_active"):
                self.time_label.text = f"TIME: {self.window.night_data['current_time']}"
                self.time_label.draw()

        # 4. Интерфейс (только ночью)
        if self.window.night_data.get("is_night_active"):
            self.time_label.text = f"TIME: {self.window.night_data['current_time']}"
            self.time_label.draw()

            self.debug_label.text = f"ITEMS LEFT: {self.spawner.items_to_spawn}"
            self.stats_label.text = f"CAUGHT: {self.spawner.stats['anomalies_caught']}"
            self.debug_label.draw()
            self.stats_label.draw()

            # Кнопка камеры
            c = arcade.color.GRAY if self.camera_on else arcade.color.WHITE
            arcade.draw_circle_filled(
                self.cam_btn_x, self.cam_btn_y, self.cam_btn_radius, c)
            arcade.draw_circle_outline(
                self.cam_btn_x, self.cam_btn_y, self.cam_btn_radius, arcade.color.BLACK, 2)

        # 5. Эффекты переходов
        if self.flash_alpha > 0:
            arcade.draw_rect_filled(arcade.rect.XYWH(self.window.width/2, self.window.height/2,
                                    self.window.width, self.window.height), (255, 255, 255, int(self.flash_alpha)))

        if self.dialog_box.is_active:
            self.dialog_box.draw()

        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, self.window.width, 0, self.window.height, (0, 0, 0, int(self.fade_alpha)))

    def on_update(self, delta_time):
        if self.dialog_box.is_active:
            self.dialog_box.update(delta_time)
            return  # Стопим остальную логику, если идет диалог

        # 2. Стандартный флеш (вспышка камеры)
        if self.flash_alpha > 0:
            self.flash_alpha -= delta_time * 600

        # 3. Логика спавнера и времени
        # Она сама переключит hours на 6 через 3 секунды после последнего предмета
        self.spawner.update(delta_time, self.current_location,
                            self.camera_on, (self.window._mouse_x, self.window._mouse_y))

        # 4. Проверка наступления 6 утра
        if self.window.night_data.get("hours") >= 6 and not self.end_sequence_triggered:
            self.trigger_end_of_night()

        # 5. Логика фейда (Затемнение/Осветление)
        if self.is_fading:
            # Затемняемся
            if self.next_location:
                self.fade_alpha += self.fade_speed * delta_time
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.current_location = self.next_location
                    self.next_location = None
                    self.update_location_visuals()  # Теперь загрузит дневные текстуры
            # Осветляемся
            else:
                self.fade_alpha -= self.fade_speed * delta_time
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.is_fading = False
                    # Когда экран полностью осветлился и наступило утро — запускаем монолог
                    if self.end_sequence_triggered and not self.dialogue_started:
                        self.start_end_monologue()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.N:
            self.window.night_data["is_night_active"] = not self.window.night_data["is_night_active"]
            self.update_location_visuals()
        if key == arcade.key.C:
            self.camera_on = not self.camera_on

        if key in (arcade.key.ENTER, arcade.key.Z):
            self.dialog_box.next_phrase()

    def on_mouse_press(self, x, y, button, modifiers):
        if math.dist((x, y), (self.cam_btn_x, self.cam_btn_y)) < self.cam_btn_radius:
            self.camera_on = not self.camera_on
            return

        item = self.spawner.active_item

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.camera_on or self.window.night_data.get("hours", 0) >= 6:
                return

            if item and item.stage == 0 and math.dist((x, y), item.position) < 70:
                item.start_inspection(self.window.width, self.window.height)
            elif not item and not self.is_fading:
                for s in self.navigation_sprites:
                    if s.collides_with_point((x, y)):
                        self.next_location = s.target_location
                        self.is_fading = True

        if button == arcade.MOUSE_BUTTON_RIGHT and self.camera_on:
            if self.window.night_data.get("hours", 0) >= 6:
                return

            # Вспышка и звук только при наличии цели в Stage 1
            if item and item.stage == 1:
                if math.dist((x, y), (item.center_x, item.center_y)) < 150:
                    self.flash_alpha = 255  # Вспышка ТЕПЕРЬ ТОЛЬКО ЗДЕСЬ
                    print("📸 CLICK! Попадание!")
                    self.spawner.resolve_item(photographed=True)
                else:
                    # Промах — вспышки нет, просто принт для дебага
                    print("☁️ Мимо, вспышка не сработала")

    def trigger_end_of_night(self):
        """Запускает процесс перехода в утро"""
        self.end_sequence_triggered = True
        # Перезагружаем текущую локу, но уже 'day'
        self.next_location = self.current_location
        self.is_fading = True
        # Важно: принудительно ставим ночь в False, чтобы update_location_visuals выбрал 'day'
        self.window.night_data["is_night_active"] = False

    def start_end_monologue(self):
        """Запускает финальный текст"""
        phrases = [
            DialoguePhrase(
                text="Всё, вроде всё... | Пора домой.",
                speed=20,
                voice=Voice.PLAYER,
                effect=TextEffect.NORMAL
            )
        ]
        self.dialog_box.start_dialogue(phrases)
        self.dialogue_started = True
