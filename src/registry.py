import arcade
import os
import json
import gc


class Registry:
    def __init__(self, base_path="resources"):
        self.base_path = base_path
        self.registry = {}

    def scan_resources(self, tag: str):
        """Только ищет файлы, не загружая их."""
        files_to_load = []
        for root, dirs, files in os.walk(self.base_path):
            dirs[:] = [d for d in dirs if not d.startswith(
                '.') and d != '__pycache__']

            normalized_root = root.replace('\\', '/')
            if tag not in normalized_root:
                continue

            for file in files:
                if file.startswith('.') or file.endswith(('.py', '.pyc')):
                    continue

                file_path = os.path.join(root, file)
                key = os.path.relpath(
                    file_path, self.base_path).replace('\\', '/')

                if key not in self.registry:
                    files_to_load.append((key, file_path, file))

        return files_to_load

    def load_single_resource(self, key, file_path, file_name):
        """Загружает один конкретный файл."""
        try:
            ext = os.path.splitext(file_name)[1].lower()

            if ext == '.gif':
                self.registry[key] = arcade.load_animated_gif(file_path)
            elif ext in ['.png', '.jpg', '.jpeg', '.bmp']:
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
            return True
        except Exception as e:
            print(f"\n❌ Ошибка загрузки {file_name}: {e}")
            self.registry[key] = None
            return False

    def get(self, path, default=None):
        return self.registry.get(path, default)

    def unload_resources(self, tag: str):
        print(f"\n🗑️ [Registry] Выгрузка пакета: '{tag}'...")
        keys_to_remove = [k for k in self.registry if tag in k]
        for k in keys_to_remove:
            del self.registry[k]
        gc.collect()
        print(
            f"🧹 Удалено объектов: {len(keys_to_remove)}. Осталось: {len(self.registry)}")


reg = Registry()
