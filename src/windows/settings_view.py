# import arcade
# from pyglet.graphics import Batch
# from resources.languages import LANGUAGES
# from arcade.gui import *
# from src.settings import settings
# from src.registry import reg


# class SettingsMenuView(arcade.View):

#     def __init__(self, window: arcade.Window):
#         super().__init__()
#         self.window = window
#         self.language: int = self.window.language

#         self.batch = Batch()

#         self.reg = reg

#         self.texts = {
#             'title': LANGUAGES['settings_button'][self.language],
#             'press_to_return': LANGUAGES['Esc_to_return'][self.language],
#             'change_language': LANGUAGES['change_language'][self.language],
#             'music': LANGUAGES['music'][self.language],
#             'creators': LANGUAGES['creators'][self.language],
#             'glossary': LANGUAGES['Glossary'][self.language]
#         }

#         # Элементы UI
#         self.background_sprite_list = arcade.SpriteList()
#         self.background_sprite = None

#         self.ui_manager = UIManager()
#         self.ui_manager.enable()

#         # Текстовые объекты
#         self.title_text = None
#         self.return_text = None
#         self.change_language_text = None
#         self.language_text = None
#         self.creators_text = None
#         self.glossary_text = None
#         self.music_button = None
#         self.music_button_text = "ON"

#         # Все текстовые объекты будем хранить в списке
#         self.text_objects = []

#     def create_music_button(self):
#         music_x = self.window.width // 3.7
#         music_y = self.window.height * 0.39 - 60

#         style = {
#             "normal": UIFlatButton.UIStyle(
#                 font_name='montserrat',
#                 font_size=16,
#                 font_color=arcade.color.BLACK,
#                 bg=(0, 0, 0, 0),
#             ),
#             "hover": UIFlatButton.UIStyle(
#                 font_name='montserrat',
#                 font_size=16,
#                 font_color=arcade.color.BLACK,
#                 bg=(245, 245, 220, 255),
#             ),
#             "press": UIFlatButton.UIStyle(
#                 font_name='montserrat',
#                 font_size=16,
#                 font_color=arcade.color.BLACK,
#                 bg=(245, 245, 220, 255),
#             )
#         }

#         self.music_button = UIFlatButton(
#             x=music_x,
#             y=music_y,
#             width=80,
#             height=35,
#             text=self.music_button_text,
#             style=style
#         )

#         @self.music_button.event("on_click")
#         def on_music_button_click(event):
#             self.toggle_music()

#         return self.music_button

#     def toggle_music(self):
#         if self.window.music_enabled:
#             self.window.disable_music()
#             self.music_button_text = "OFF"
#         else:
#             self.window.enable_music()
#             self.music_button_text = "ON"

#         if self.music_button:
#             self.music_button.text = self.music_button_text

#     def enable_music(self):
#         # Включить всю музыку в игре
#         if hasattr(self.window, 'main_theme'):
#             self.window.background_music.play()
#             self.window.background_music.volume = 1.0

#         print("Музыка включена")

#     def disable_music(self):
#         # Выключить всю музыку в игре
#         if hasattr(self.window, 'main_theme'):
#             self.window.background_music.pause()
#             self.window.background_music.volume = 0.0

#         print("Музыка выключена")

#     def save_music_setting(self):
#         with open('data/music.txt', 'w') as music_file:
#             music_file.write("ON" if self.music_enabled else "OFF")

#     def load_music_setting(self):
#         try:
#             with open('data/music.txt', 'r') as music_file:
#                 setting = music_file.read().strip()
#                 self.music_enabled = (setting == "ON")
#                 self.music_button_text = "ON" if self.music_enabled else "OFF"
#         except FileNotFoundError:
#             self.music_enabled = True
#             self.music_button_text = "ON"
#             self.save_music_setting()

#     def create_creators_button(self):
#         creators_x = self.window.width // 1.56
#         creators_y = self.window.height * 0.27

#         self.creators_button = UITextureButton(
#             x=creators_x - 75,
#             y=creators_y,
#             width=150,
#             height=45,
#             texture=arcade.Texture.create_empty("transparent", (150, 45)),
#             texture_hovered=arcade.Texture.create_empty(
#                 "transparent_hover", (150, 45)),
#             texture_pressed=arcade.Texture.create_empty(
#                 "transparent_pressed", (150, 45))
#         )

#         @self.creators_button.event("on_click")
#         def on_creators_click(event):
#             self.on_creators_button_clicked()

#         return self.creators_button

#     def on_creators_button_clicked(self):
#         self.window.switch_view('creators_window')

#     def create_lang_button(self):
#         center_x = self.window.width // 5.3
#         center_y = self.window.height * 0.51

#         offset_x = -120
#         offset_y = 80

#         pos_x = center_x + offset_x
#         pos_y = center_y + offset_y

#         # Создаем кнопку для языка
#         self.lang_button = UIFlatButton(
#             x=pos_x,
#             y=pos_y,
#             width=150,
#             height=35,
#             text=LANGUAGES['language'][self.language],
#             style={
#                 "normal": UIFlatButton.UIStyle(
#                     font_name='montserrat',
#                     font_size=16,
#                     font_color=arcade.color.BLACK,
#                     bg=(0, 0, 0, 0),
#                 ),
#                 "hover": UIFlatButton.UIStyle(
#                     font_name='montserrat',
#                     font_size=16,
#                     font_color=arcade.color.BLACK,
#                     bg=(245, 245, 220, 255),
#                 ),
#                 "press": UIFlatButton.UIStyle(
#                     font_name='montserrat',
#                     font_size=16,
#                     font_color=arcade.color.BLACK,
#                     bg=(245, 245, 220, 255),
#                 )
#             }
#         )

#         @self.lang_button.event("on_click")
#         def on_lang_button_click(event):
#             self.language = (self.language + 1) % 3

#             self.lang_button.text = LANGUAGES['language'][self.language]

#             self.window.language = self.language

#             with open('data/language.txt', 'w') as lang:
#                 lang.write(next((key for key, value in settings.lang_dict.items(
#                 ) if value == self.language), 'russian'))

#             self.update_texts()

#         return self.lang_button

#     def create_glossary_button(self):
#         glossary_x = self.window.width // 1.22
#         glossary_y = self.window.height * 0.325

#         self.glossary_button = UITextureButton(
#             x=glossary_x - 75,
#             y=glossary_y,
#             width=150,
#             height=45,
#             texture=arcade.Texture.create_empty("transparent", (150, 45)),
#             texture_hovered=arcade.Texture.create_empty(
#                 "transparent_hover", (150, 45)),
#             texture_pressed=arcade.Texture.create_empty(
#                 "transparent_pressed", (150, 45))
#         )

#         @self.glossary_button.event("on_click")
#         def on_glossary_click(event):
#             self.on_glossary_button_clicked()

#         return self.glossary_button

#     def on_glossary_button_clicked(self):
#         self.window.switch_view('glossary_window')

#     def update_texts(self):
#         self.texts = {
#             'title': LANGUAGES['settings_button'][self.language],
#             'press_to_return': LANGUAGES['Esc_to_return'][self.language],
#             'change_language': LANGUAGES['change_language'][self.language],
#             'music': LANGUAGES['music'][self.language],
#             'creators': LANGUAGES['creators'][self.language],
#             'glossary': LANGUAGES['Glossary'][self.language]
#         }

#         # Обновляем каждый текстовый объект, если он существует
#         if self.title_text:
#             self.title_text.text = self.texts['title']
#         if self.return_text:
#             self.return_text.text = self.texts['press_to_return']
#         if self.change_language_text:
#             self.change_language_text.text = self.texts['change_language']
#         if self.music_text:
#             self.music_text.text = self.texts['music']
#         if self.creators_text:
#             self.creators_text.text = self.texts['creators']
#         if self.glossary_text:
#             self.glossary_text.text = self.texts['glossary']

#     def create_lang_dropdown(self):
#         self.ui_manager.clear()

#         lang_button = self.create_lang_button()
#         self.ui_manager.add(lang_button)

#         creators_button = self.create_creators_button()
#         self.ui_manager.add(creators_button)

#         music_button = self.create_music_button()
#         self.ui_manager.add(music_button)

#         glossary_button = self.create_glossary_button()
#         self.ui_manager.add(glossary_button)

#     def setup(self):
#         self.load_background()

#         self.window.load_music_setting()
#         self.music_button_text = "ON" if self.window.music_enabled else "OFF"

#         self.text_objects.clear()

#         # Создаем UI элементы
#         self.create_lang_dropdown()

#         self.title_text = arcade.Text(
#             text=self.texts['title'],
#             x=self.window.width // 2,
#             y=self.window.height * 0.818,
#             color=arcade.color.BLACK,
#             font_size=30,
#             font_name='Montserrat',
#             anchor_x='center',
#             batch=self.batch
#         )
#         self.text_objects.append(self.title_text)

#         self.return_text = arcade.Text(
#             text=self.texts['press_to_return'],
#             x=self.window.width // 2,
#             y=self.window.height * 0.02,
#             color=arcade.color.WHITE,
#             font_size=18,
#             font_name='Montserrat',
#             anchor_x='center',
#             batch=self.batch
#         )
#         self.text_objects.append(self.return_text)

#         self.change_language_text = arcade.Text(
#             text=self.texts['change_language'],
#             x=self.window.width // 6.45,
#             y=self.window.height * 0.69,
#             color=arcade.color.BLACK,
#             font_size=20,
#             font_name='Montserrat',
#             anchor_x='center',
#             batch=self.batch
#         )
#         self.text_objects.append(self.change_language_text)

#         self.music_text = arcade.Text(
#             text=self.texts['music'],
#             x=self.window.width // 3.353,
#             y=self.window.height * 0.39,
#             color=arcade.color.BLACK,
#             font_size=16,
#             font_name='Montserrat',
#             anchor_x='center',
#             batch=self.batch
#         )
#         self.text_objects.append(self.music_text)

#         self.creators_text = arcade.Text(
#             text=self.texts['creators'],
#             x=self.window.width // 1.56,
#             y=self.window.height * 0.27,
#             color=arcade.color.BLACK,
#             font_size=24,
#             font_name='Montserrat',
#             anchor_x='center',
#             batch=self.batch
#         )
#         self.text_objects.append(self.creators_text)

#         self.glossary_text = arcade.Text(
#             text=self.texts['glossary'],
#             x=self.window.width // 1.22,
#             y=self.window.height * 0.325,
#             color=arcade.color.BLACK,
#             font_size=18,
#             font_name='Montserrat',
#             anchor_x='center',
#             batch=self.batch
#         )

#         self.text_objects.append(self.glossary_text)

#     def on_show_view(self):
#         self.setup()

#     def on_draw(self):
#         self.clear()

#         if self.background_sprite_list:
#             self.background_sprite_list.draw()

#         self.batch.draw()

#         self.ui_manager.draw()

#     def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
#         self.ui_manager.on_mouse_press(x, y, button, modifiers)

#     def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
#         self.ui_manager.on_mouse_release(x, y, button, modifiers)

#     def on_key_press(self, symbol, modifiers):
#         if symbol == arcade.key.ESCAPE:
#             self.window.save_music_setting()
#             self.window.switch_view("main_menu")

#     def on_resize(self, width: float, height: float):
#         super().on_resize(width, height)
#         self.update_background_position_and_size()
#         self.update_text_position_and_size_and_lang()
#         self.create_lang_dropdown()

#     def load_background(self):

#         texture = self.reg.get(
#             'common/textures/backgrounds/settings_background.jpg')
#         self.background_sprite = arcade.Sprite(
#             path_or_texture=texture,
#             center_x=self.window.width // 2,
#             center_y=self.window.height // 2
#         )

#         self.background_sprite.width = self.window.width
#         self.background_sprite.height = self.window.height

#         self.background_sprite_list.append(self.background_sprite)

#     def update_background_position_and_size(self):
#         if not self.background_sprite:
#             return

#         self.background_sprite.width = self.window.width
#         self.background_sprite.height = self.window.height
#         self.background_sprite.center_x = self.window.width // 2
#         self.background_sprite.center_y = self.window.height // 2

#     def update_text_position_and_size_and_lang(self):
#         self.texts = {
#             'title': LANGUAGES['settings_button'][self.language],
#             'press_to_return': LANGUAGES['Esc_to_return'][self.language],
#             'change_language': LANGUAGES['change_language'][self.language],
#             'music': LANGUAGES['music'][self.language],
#             'creators': LANGUAGES['creators'][self.language],
#             'glossary': LANGUAGES['Glossary'][self.language]
#         }

#         self.title_text.text = self.texts['title']
#         self.title_text.x = self.window.width // 2
#         self.title_text.y = self.window.height * 0.818

#         self.return_text.text = self.texts['press_to_return']
#         self.return_text.x = self.window.width // 2
#         self.return_text.y = self.window.height * 0.02

#         self.change_language_text.text = self.texts['change_language']
#         self.change_language_text.x = self.window.width // 6.45
#         self.change_language_text.y = self.window.height * 0.69

#         self.music_text.text = self.texts['music']
#         self.music_text.x = self.window.width // 3.353
#         self.music_text.y = self.window.height * 0.39

#         self.creators_text.text = self.texts['creators']
#         self.creators_text.x = self.window.width // 1.56
#         self.creators_text.y = self.window.height * 0.27

#         self.glossary_text.text = self.texts['glossary']
#         self.glossary_text.x = self.window.width // 1.22
#         self.glossary_text.y = self.window.height * 0.325

# # import arcade
# # import arcade.gui
# # from PIL import Image, ImageFilter  # Нужно для размытия
# # from resources.languages import LANGUAGES
# # from src.settings import settings
# # from src.registry import reg


# # class SettingsMenuView(arcade.View):
# #     def __init__(self, window: arcade.Window, previous_view: arcade.View):
# #         super().__init__()
# #         self.window = window
# #         self.previous_view = previous_view  # Запоминаем, откуда пришли
# #         self.reg = reg

# #         self.language: int = self.window.language

# #         # Менеджер UI
# #         self.ui_manager = arcade.gui.UIManager()
# #         self.ui_manager.enable()

# #         # Спрайт для размытого фона
# #         self.background_texture = self.create_blurred_background()

# #         # Для хранения текстовых объектов (меток)
# #         self.labels = []

# #         self.setup_ui()

# #     def create_blurred_background(self):
# #         """Делает скриншот текущего окна, размывает и затемняет его."""
# #         # 1. Получаем изображение текущего окна
# #         image = arcade.get_image()

# #         # 2. Размываем через Pillow (PIL)
# #         # Radius 5 - сила размытия, можно менять
# #         image = image.filter(ImageFilter.GaussianBlur(radius=5))

# #         # 3. Можно немного затемнить (опционально)
# #         # Но проще рисовать поверх полупрозрачный черный прямоугольник в on_draw

# #         # 4. Превращаем обратно в текстуру Arcade
# #         return arcade.Texture(image)

# #     def get_responsive_font_size(self, base_size=20):
# #         """Возвращает размер шрифта относительно высоты окна"""
# #         # Например, базовый размер рассчитан на высоту 720.
# #         # Если окно 1080, шрифт будет больше.
# #         scale_factor = self.window.height / 720
# #         return int(base_size * scale_factor)

# #     def get_transparent_style(self, font_size=16):
# #         """Стиль для полностью прозрачной кнопки (виден только текст)"""
# #         font_size = self.get_responsive_font_size(font_size)
# #         return {
# #             "normal": arcade.gui.UIFlatButton.UIStyle(
# #                 font_name='montserrat',
# #                 font_size=font_size,
# #                 font_color=arcade.color.BLACK,
# #                 bg=(0, 0, 0, 0),       # Прозрачный
# #                 border=(0, 0, 0, 0)    # Без границ
# #             ),
# #             "hover": arcade.gui.UIFlatButton.UIStyle(
# #                 font_name='montserrat',
# #                 font_size=font_size,
# #                 font_color=(100, 100, 100, 255),  # Серый при наведении
# #                 bg=(0, 0, 0, 0),
# #                 border=(0, 0, 0, 0)
# #             ),
# #             "press": arcade.gui.UIFlatButton.UIStyle(
# #                 font_name='montserrat',
# #                 font_size=font_size,
# #                 font_color=arcade.color.BLACK,
# #                 bg=(0, 0, 0, 0),
# #                 border=(0, 0, 0, 0)
# #             )
# #         }

# #     def setup_ui(self):
# #         self.ui_manager.clear()
# #         self.labels.clear()

# #         # Тексты (берем из словаря)
# #         t_lang = LANGUAGES['language'][self.language]
# #         t_music = "ON" if self.window.music_enabled else "OFF"
# #         # t_creators... и т.д. - для кнопок мы используем их как текст кнопки

# #         # --- 1. КНОПКА ЯЗЫКА ---
# #         lang_btn = arcade.gui.UIFlatButton(
# #             text=t_lang,
# #             width=200,
# #             height=50,
# #             style=self.get_transparent_style(20)
# #         )
# #         # Позиционирование через AnchorLayout или просто перемещение
# #         # В старом коде было абсолютное позиционирование. Повторим его, но адаптивно.
# #         lang_btn.center_x = self.window.width // 5.3 - 120
# #         lang_btn.center_y = self.window.height * 0.51 + 80

# #         @lang_btn.event("on_click")
# #         def on_lang_click(event):
# #             self.toggle_language()
# #             # Пересоздаем UI, чтобы обновить текст везде
# #             self.setup_ui()

# #         self.ui_manager.add(lang_btn)

# #         # --- 2. КНОПКА МУЗЫКИ ---
# #         music_btn = arcade.gui.UIFlatButton(
# #             text=t_music,
# #             width=100,
# #             height=50,
# #             style=self.get_transparent_style(20)
# #         )
# #         music_btn.center_x = self.window.width // 3.7
# #         music_btn.center_y = self.window.height * 0.39 - 60

# #         @music_btn.event("on_click")
# #         def on_music_click(event):
# #             self.toggle_music()
# #             # Обновляем текст только этой кнопки для оптимизации
# #             music_btn.text = "ON" if self.window.music_enabled else "OFF"

# #         self.ui_manager.add(music_btn)

# #         # --- 3. КНОПКА CREATORS (Прозрачная поверх текста или просто текст-кнопка) ---
# #         # Если ты хочешь, чтобы слово "Создатели" само было кнопкой:
# #         creators_btn = arcade.gui.UIFlatButton(
# #             text="",  # Текст нарисуем отдельно, если нужна сложная графика, или используем button text
# #             width=150,
# #             height=50,
# #             style=self.get_transparent_style(20)
# #         )
# #         # Тут я использую невидимую кнопку ПОВЕРХ места, где будет текст,
# #         # или можно просто сделать кнопку с текстом "Creators"
# #         creators_btn.center_x = self.window.width // 1.56 - 75
# #         creators_btn.center_y = self.window.height * 0.27

# #         @creators_btn.event("on_click")
# #         def on_creators_click(event):
# #             # Убедись что там тоже есть возврат
# #             self.window.switch_view('creators_window')

# #         self.ui_manager.add(creators_btn)

# #         # --- 4. КНОПКА GLOSSARY ---
# #         glossary_btn = arcade.gui.UIFlatButton(
# #             text="",
# #             width=150,
# #             height=50,
# #             style=self.get_transparent_style(20)
# #         )
# #         glossary_btn.center_x = self.window.width // 1.22 - 75
# #         glossary_btn.center_y = self.window.height * 0.325

# #         @glossary_btn.event("on_click")
# #         def on_glossary_click(event):
# #             self.window.switch_view('glossary_window')

# #         self.ui_manager.add(glossary_btn)

# #         # --- ДОБАВЛЕНИЕ ПОДПИСЕЙ (LABELS) ---
# #         # Рисуем статический текст, который не является кнопками, или заголовки кнопок

# #         # Заголовок
# #         self.add_label(LANGUAGES['settings_button'][self.language],
# #                        self.window.width // 2,
# #                        self.window.height * 0.818,
# #                        font_size=30, bold=True)

# #         # Подпись "Нажми ESC"
# #         self.add_label(LANGUAGES['Esc_to_return'][self.language],
# #                        self.window.width // 2,
# #                        self.window.height * 0.05,
# #                        font_size=18, color=arcade.color.WHITE)

# #         # Подпись "Сменить язык"
# #         self.add_label(LANGUAGES['change_language'][self.language],
# #                        self.window.width // 6.45,
# #                        self.window.height * 0.69,
# #                        font_size=20)

# #         # Подпись "Музыка"
# #         self.add_label(LANGUAGES['music'][self.language],
# #                        self.window.width // 3.353,
# #                        self.window.height * 0.39,
# #                        font_size=20)

# #         # Подписи для Creators и Glossary (так как кнопки выше были пустыми/прозрачными)
# #         # Если кнопки выше были с текстом, это не нужно.
# #         # Но если ты хочешь текст отдельно, а кликабельную область отдельно:
# #         self.add_label(LANGUAGES['creators'][self.language],
# #                        self.window.width // 1.56,
# #                        self.window.height * 0.27,
# #                        font_size=24)

# #         self.add_label(LANGUAGES['Glossary'][self.language],
# #                        self.window.width // 1.22,
# #                        self.window.height * 0.325,
# #                        font_size=18)

# #     def add_label(self, text, x, y, font_size=20, color=arcade.color.BLACK, bold=False):
# #         """Вспомогательная функция для добавления текста"""
# #         size = self.get_responsive_font_size(font_size)
# #         lbl = arcade.Text(
# #             text=text,
# #             x=x, y=y,
# #             color=color,
# #             font_size=size,
# #             font_name='montserrat',
# #             anchor_x='center',
# #             anchor_y='center',
# #             bold=bold
# #         )
# #         self.labels.append(lbl)

# #     def toggle_language(self):
# #         self.language = (self.language + 1) % 3
# #         self.window.language = self.language

# #         # Сохранение (как у тебя было)
# #         lang_key = next((key for key, value in settings.lang_dict.items(
# #         ) if value == self.language), 'russian')
# #         with open('data/language.txt', 'w') as f:
# #             f.write(lang_key)

# #     def toggle_music(self):
# #         if self.window.music_enabled:
# #             self.window.disable_music()
# #         else:
# #             self.window.enable_music()
# #         self.window.save_music_setting()

# #     def on_draw(self):
# #         self.clear()

# #         # 1. Рисуем размытый фон
# #         arcade.draw_texture_rect(
# #             self.background_texture,
# #             arcade.rect.XYWH(
# #                 self.window.width / 2,
# #                 self.window.height / 2,
# #                 self.window.width,
# #                 self.window.height
# #             )
# #         )

# #         # 2. Рисуем полупрозрачную подложку для красоты (диммер)
# #         arcade.draw_rect_filled(
# #             arcade.rect.XYWH(
# #                 self.window.width / 2,
# #                 self.window.height / 2,
# #                 self.window.width,
# #                 self.window.height
# #             ),
# #             (0, 0, 0, 100)  # Черный с прозрачностью ~40%
# #         )

# #         # 3. Рисуем UI
# #         # Сначала просто текст
# #         for label in self.labels:
# #             label.draw()

# #         # Потом кнопки
# #         self.ui_manager.draw()

# #     def on_resize(self, width, height):
# #         super().on_resize(width, height)
# #         # При изменении размера пересоздаем UI (пересчитываются шрифты и координаты)
# #         self.background_texture = self.create_blurred_background()  # Фон тоже лучше обновить
# #         self.setup_ui()

# #     def on_key_press(self, symbol, modifiers):
# #         if symbol == arcade.key.ESCAPE:
# #             self.close_settings()

# #     def close_settings(self):
# #         # Возвращаемся на предыдущий экран
# #         self.window.show_view(self.previous_view)

# #     def on_show_view(self):
# #         # UI Manager включается
# #         self.ui_manager.enable()

# #     def on_hide_view(self):
# #         # UI Manager выключается
# #         self.ui_manager.disable()
import arcade
from pyglet.graphics import Batch
from arcade.gui import *
from src.settings import settings
from src.registry import reg
from resources.languages import LANGUAGES

class SettingsMenuView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
        self.language: int = self.window.language

        # Параметры для масштабирования (из MainMenu)
        self.original_width = settings.width
        self.original_height = settings.height
        self.original_font_size = 20

        self.reg = reg
        self.ui_manager = UIManager()
        
        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None

        # Состояние музыки для текста на кнопке
        self.music_button_text = "ON" if self.window.music_enabled else "OFF"

    def setup(self):
        """Инициализация представления"""
        self.ui_manager.enable()
        self.load_background()
        self.create_ui()

    def create_ui(self):
        """Создание интерфейса с использованием Layouts и масштабирования"""
        self.ui_manager.clear()

        # 1. Расчет масштаба
        win_w, win_h = self.window.width, self.window.height
        scale_x = win_w / self.original_width
        scale_y = win_h / self.original_height
        scale = min(scale_x, scale_y)

        font_name = 'Montserrat'
        
        # Общий стиль для всех кнопок
        button_style = {
            "normal": UIFlatButton.UIStyle(
                font_name=font_name, font_size=int(18 * scale),
                font_color=arcade.color.BLACK, bg=(0, 0, 0, 0),
            ),
            "hover": UIFlatButton.UIStyle(
                font_name=font_name, font_size=int(18 * scale),
                font_color=arcade.color.BLACK, bg=(245, 245, 220, 0),
            ),
            "press": UIFlatButton.UIStyle(
                font_name=font_name, font_size=int(18 * scale),
                font_color=arcade.color.BLACK, bg=(245, 245, 220, 0),
            )
        }

        # Главный контейнер
        anchor = UIAnchorLayout(width=win_w, height=win_h)

        # --- ЗАГОЛОВОК ---
        title_label = UILabel(
            text=LANGUAGES['settings_button'][self.language],
            font_size=int(35 * scale),
            font_name=font_name,
            text_color=arcade.color.BLACK
        )
        anchor.add(title_label, anchor_x='center', anchor_y='top', align_y=int(-60 * scale))

        # --- ЦЕНТРАЛЬНЫЙ БЛОК (Текст + Кнопки) ---
        v_box = UIBoxLayout(vertical=True, space_between=int(10 * scale))

        # Секция ЯЗЫКА
        lang_header = UILabel(
            text=LANGUAGES['change_language'][self.language],
            font_size=int(22 * scale),
            font_name=font_name,
            text_color=arcade.color.BLACK
        )
        lang_btn = UIFlatButton(
            text=LANGUAGES['language'][self.language], 
            width=int(320 * scale), height=int(50 * scale), style=button_style
        )
        
        @lang_btn.event("on_click")
        def on_lang_click(event):
            self.language = (self.language + 1) % 3
            self.window.language = self.language
            # Сохранение в файл
            with open('data/language.txt', 'w') as lang_file:
                lang_key = next((k for k, v in settings.lang_dict.items() if v == self.language), 'russian')
                lang_file.write(lang_key)
            self.create_ui() # Перерисовка всего UI

        # Секция МУЗЫКИ
        music_header = UILabel(
            text=LANGUAGES['music'][self.language],
            font_size=int(22 * scale),
            font_name=font_name,
            text_color=arcade.color.BLACK
        )
        music_btn = UIFlatButton(
            text=self.music_button_text, 
            width=int(320 * scale), height=int(50 * scale), style=button_style
        )
        
        @music_btn.event("on_click")
        def on_music_click(event):
            self.toggle_music()
            music_btn.text = self.music_button_text

        # Добавляем в вертикальный бокс с отступами (padding)
        v_box.add(lang_header)
        v_box.add(lang_btn)
        # Отступ сверху 30 пикселей для заголовка музыки
        v_box.add(music_header, padding=(0, 0, int(30 * scale), 0))
        v_box.add(music_btn)

        anchor.add(v_box, anchor_x='center', anchor_y='center')

        # --- НИЖНИЙ БЛОК (Авторы и Глоссарий) ---
        h_box = UIBoxLayout(vertical=False, space_between=int(50 * scale))
        
        creators_btn = UIFlatButton(text=LANGUAGES['creators'][self.language], width=int(200 * scale), style=button_style)
        creators_btn.on_click = lambda _: self.window.switch_view('creators_window')
        
        glossary_btn = UIFlatButton(text=LANGUAGES['Glossary'][self.language], width=int(200 * scale), style=button_style)
        glossary_btn.on_click = lambda _: self.window.switch_view('glossary_window')

        h_box.add(creators_btn)
        h_box.add(glossary_btn)
        anchor.add(h_box, anchor_x='center', anchor_y='bottom', align_y=int(120 * scale))

        # Подсказка про ESC в самом низу
        esc_label = UILabel(
            text=LANGUAGES['Esc_to_return'][self.language],
            font_size=int(16 * scale),
            font_name=font_name,
            text_color=(60, 60, 60)
        )
        anchor.add(esc_label, anchor_x='center', anchor_y='bottom', align_y=int(30 * scale))

        self.ui_manager.add(anchor)

    def toggle_music(self):
        """Логика переключения музыки"""
        if self.window.music_enabled:
            self.window.disable_music()
            self.music_button_text = "OFF"
        else:
            self.window.enable_music()
            self.music_button_text = "ON"

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        self.clear()
        if self.background_sprite_list:
            self.background_sprite_list.draw()
        self.ui_manager.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.window.save_music_setting()
            self.window.switch_view("main_menu")

    def on_resize(self, width: float, height: float):
        """Адаптация при изменении размера окна"""
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.create_ui()

    def load_background(self):
        texture = self.reg.get('common/textures/backgrounds/settings_background.jpg')
        self.background_sprite = arcade.Sprite(path_or_texture=texture)
        self.background_sprite_list.clear()
        self.background_sprite_list.append(self.background_sprite)
        self.update_background_position_and_size()

    def update_background_position_and_size(self):
        if self.background_sprite:
            self.background_sprite.width = self.window.width
            self.background_sprite.height = self.window.height
            self.background_sprite.center_x = self.window.width // 2
            self.background_sprite.center_y = self.window.height // 2