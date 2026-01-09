import arcade
import queue
import threading
import os
import time
from src.registry import reg


class LoadingView(arcade.View):
    def __init__(self, window: arcade.Window, next_view_name: str, load_tag: str):
        super().__init__()
        self.window = window
        self.next_view_name = next_view_name
        self.load_tag = load_tag

    def setup(self):
        self.texture_queue = queue.Queue()
        self.progress_queue = queue.Queue()
        self.total_files = 0
        self.loaded_count = 0
        self.is_finished = False

        self.ui_sprites = arcade.SpriteList()
        self.gif_sprite_list = arcade.SpriteList()

        # Создаем спрайты (в 3.0 они по умолчанию пытаются сглаживаться)
        self.bar_bg = arcade.SpriteSolidColor(
            1, 1, color=arcade.color.DARK_GRAY)
        self.bar_fill = arcade.SpriteSolidColor(1, 1, color=arcade.color.GREEN)
        self.ui_sprites.extend([self.bar_bg, self.bar_fill])

        # Шрифты в 3.0 загружаются так (если нужно из файла)
        # arcade.load_font("resources/fonts/montserrat.ttf")

        self.percent_text = arcade.Text(
            "0%", 0, 0, arcade.color.WHITE, 20,
            font_name="montserrat", anchor_x="center"
        )
        self.file_text = arcade.Text(
            "Scanning...", 0, 0, arcade.color.GRAY, 11,
            font_name="montserrat", anchor_x="center"
        )

        try:
            self.loading_gif = arcade.load_animated_gif(
                "resources/common/textures/ui/loading.gif")
            self.loading_gif.scale = 2.0
            self.gif_sprite_list.append(self.loading_gif)
        except Exception as e:
            print(f"⚠️ GIF Error: {e}")
            self.loading_gif = None

        self.setup_positions()

    def setup_positions(self):
        w, h = self.window.width, self.window.height
        # Используем целочисленное деление // для точности пикселей
        cx, bar_y = w // 2, h // 5
        bar_w = int(w * 0.6)

        # 1. Фиксируем фон
        self.bar_bg.width = bar_w
        self.bar_bg.height = 12
        self.bar_bg.position = (cx, bar_y)

        # 2. Обновляем положение текста относительно нового bar_y
        self.percent_text.position = (cx, bar_y + 40)
        self.file_text.position = (cx, bar_y - 30)

        if self.loading_gif:
            self.loading_gif.position = (cx, h // 2 + 50)

        # 3. ВАЖНО: Принудительно обновляем размер и позицию зеленой полоски при ресайзе
        self.refresh_bar_fill()

    def refresh_bar_fill(self):
        if self.total_files > 0:
            progress = self.loaded_count / self.total_files
            # Считаем актуальную ширину от текущей ширины фона
            fill_w = int(self.bar_bg.width * progress)

            self.bar_fill.width = fill_w
            self.bar_fill.height = self.bar_bg.height
            # Якорим к левому краю фона, чтобы она не «гуляла»
            self.bar_fill.left = self.bar_bg.left
            self.bar_fill.center_y = self.bar_bg.center_y

    def on_update(self, delta_time: float):
        self.gif_sprite_list.update_animation(delta_time)

        # Обработка текстур
        for _ in range(4):
            try:
                key, path, name = self.texture_queue.get_nowait()
                reg.load_single_resource(key, path, name)
                self.update_progress(name)
            except queue.Empty:
                break

        # Обработка прогресса
        try:
            while True:
                msg, _ = self.progress_queue.get_nowait()
                if msg != "THREAD_DONE":
                    self.update_progress(msg)
        except queue.Empty:
            pass

        if self.loaded_count >= self.total_files and not self.is_finished:
            self.is_finished = True
            self.go_next()

    def update_progress(self, name):
        self.loaded_count += 1
        self.current_file_name = name  # Сохраняем имя для on_resize

        # Обновляем визуал через общий метод
        self.refresh_bar_fill()

        # Обновляем тексты
        progress = self.loaded_count / self.total_files
        self.percent_text.text = f"{int(progress * 100)}%"
        self.file_text.text = f"Loading: {name}"

        # Консоль
        bar = "█" * int(progress * 50) + "░" * (50 - int(progress * 50))
        print(f"\r[{bar}] {progress*100:.1f}% | {name[:20]:<20}", end="")

    def on_draw(self):
        self.clear()
        # В 3.0+ это самый быстрый способ отрисовки
        # Передаем фильтр прямо в draw!
        self.ui_sprites.draw(filter=self.window.ctx.NEAREST)
        self.gif_sprite_list.draw(filter=self.window.ctx.NEAREST)

        self.percent_text.draw()
        self.file_text.draw()

    def on_show_view(self):
        self.setup()
        self.window.background_color = arcade.color.BLACK

        self.loaded_count = 0
        self.is_finished = False
        self.current_file_name = "Scanning..."

        self.texture_queue = queue.Queue()
        self.progress_queue = queue.Queue()

        self.percent_text.text = "0%"
        self.file_text.text = "Scanning..."

        self.files_to_load = reg.scan_resources(self.load_tag)
        self.total_files = len(self.files_to_load)

        self.refresh_bar_fill()

        print(
            f"\n🚀 [Registry] Загрузка: '{self.load_tag}' | Файлов: {self.total_files}")
        self.start_time = time.time()

        if self.total_files == 0:
            self.go_next()
            return

        threading.Thread(target=self.background_worker, daemon=True).start()

    def background_worker(self):
        for key, path, name in self.files_to_load:
            ext = os.path.splitext(name)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
                self.texture_queue.put((key, path, name))
            else:
                reg.load_single_resource(key, path, name)
                self.progress_queue.put((name, 1))
        self.progress_queue.put(("THREAD_DONE", 0))

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.setup_positions()

    def go_next(self):
        print(f"\n✅ Загружено за {time.time() - self.start_time:.2f} сек.")
        self.window.switch_view(self.next_view_name)
