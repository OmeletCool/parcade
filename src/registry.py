import arcade
import os
import time
import json


class Registry:

    def __init__(self, base_path="resources"):
        self.base_path = base_path
        self.registry = {}
        self._load_with_progress()

    def _load_with_progress(self):
        print("🚀 Начинаю загрузку ресурсов...")

        # Сначала считаем общее количество файлов
        total_files = 0
        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if not d.startswith(
                '.') and d != '__pycache__']
            total_files += len([f for f in files if not f.startswith('.')
                               and not f.endswith(('.py', '.pyc'))])

        print(f"📊 Найдено файлов: {total_files}")

        # Загружаем с прогрессом
        loaded = 0
        start_time = time.time()

        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if not d.startswith(
                '.') and d != '__pycache__']

            for file in files:
                if file.startswith('.') or file.endswith(('.py', '.pyc')):
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, self.base_path)
                key = relative_path.replace('\\', '/')

                # Выводим прогресс
                loaded += 1
                percent = (loaded / total_files) * 100
                bar = "█" * int(percent / 2) + "░" * (50 - int(percent / 2))

                print(
                    f"\r[{bar}] {percent:.1f}% | {loaded}/{total_files} | {file[:20]:<20}", end="")

                # Загружаем файл
                try:
                    ext = os.path.splitext(file)[1].lower()

                    if ext == '.gif':
                        self.registry[key] = arcade.load_animated_gif(
                            file_path)
                    elif ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tga']:
                        self.registry[key] = arcade.load_texture(file_path)
                    elif ext in ['.wav', '.mp3', '.ogg']:
                        self.registry[key] = arcade.load_sound(file_path)
                    elif ext in ['.ttf', '.otf']:
                        self.registry[key] = arcade.load_font(file_path)
                    elif ext == '.json':
                        with open(file_path, 'r', encoding='utf-8') as f:
                            self.registry[key] = json.load(f)
                    else:
                        self.registry[key] = file_path

                except Exception as e:
                    print(f"\n❌ Ошибка: {file} - {e}")
                    self.registry[key] = None

        # Завершение
        elapsed = time.time() - start_time
        print(f"\n✅ Загрузка завершена за {elapsed:.2f} секунд")
        print(f"📦 Загружено ресурсов: {len(self.registry)}")

    def get(self, path, default=None):
        return self.registry.get(path, default)


reg = Registry()
