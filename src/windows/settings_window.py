import arcade
from resources.languages import LANGUAGES


class SettingsMenuView(arcade.View):

    def __init__(self, window):
        super().__init__()
        self.window = window  # Ссылка на главное окно
        self.language = window.language

        # Загрузка текстов
        self.texts = {
            'title': LANGUAGES.get('settings_title', {}).get(self.language, 'Settings'),
            'back': LANGUAGES.get('back', {}).get(self.language, 'Back'),
            'press_to_return': LANGUAGES.get('press_to_return', {}).get(self.language, 'Press ESC to return')
        }

        # Элементы UI
        self.background_sprite_list = arcade.SpriteList()
        self.background_sprite = None
        
        self.title_text = None
        self.return_text = None
        
        # Фон
        self.background_image_path = 'resources/textures/backgrounds/settings_background.png'
        
        arcade.load_font('resources/fonts/montserrat.ttf')

    def setup(self):
        """Инициализация представления"""
        self.load_background()
        
        # Создание заголовка
        self.title_text = arcade.Text(
            text=self.texts['title'],
            x=self.window.width // 2,
            y=self.window.height * 0.8,
            color=arcade.color.WHITE,
            font_size=48,
            font_name='montserrat',
            anchor_x='center'
        )
        
        # Текст для возврата
        self.return_text = arcade.Text(
            text=self.texts['press_to_return'],
            x=self.window.width // 2,
            y=self.window.height * 0.1,
            color=arcade.color.WHITE,
            font_size=24,
            font_name='montserrat',
            anchor_x='center'
        )

    def on_show_view(self):
        """Вызывается при показе этого представления"""
        self.setup()

    def on_draw(self):
        """Отрисовка"""
        self.clear()

        # Фон
        if self.background_sprite_list:
            self.background_sprite_list.draw()

        # Заголовок
        if self.title_text:
            self.title_text.draw()
            
        # Текст для возврата
        if self.return_text:
            self.return_text.draw()

    def on_key_press(self, symbol, modifiers):
        """Обработка нажатия клавиш"""
        # ESC для возврата в главное меню
        if symbol == arcade.key.ESCAPE:
            self.window.switch_view("main_window")

    def on_resize(self, width: float, height: float):
        """Обработка изменения размера окна"""
        super().on_resize(width, height)
        self.update_background_position_and_size()
        self.update_text_position()

    def load_background(self):
        """Загрузка фона"""
        texture = arcade.load_texture(self.background_image_path)
        self.background_sprite = arcade.Sprite(
            path_or_texture=texture,
            center_x=self.window.width // 2,
            center_y=self.window.height // 2
        )
        
        # Растягиваем фон на весь экран
        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        
        self.background_sprite_list.append(self.background_sprite)

    def update_background_position_and_size(self):
        """Обновление позиции и размера фона"""
        if not self.background_sprite:
            return

        self.background_sprite.width = self.window.width
        self.background_sprite.height = self.window.height
        self.background_sprite.center_x = self.window.width // 2
        self.background_sprite.center_y = self.window.height // 2

    def update_text_position(self):
        """Обновление позиции текста"""
        if self.title_text:
            self.title_text.x = self.window.width // 2
            self.title_text.y = self.window.height * 0.8
            
        if self.return_text:
            self.return_text.x = self.window.width // 2
            self.return_text.y = self.window.height * 0.1

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мыши - возврат в главное меню по любому клику"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.window.switch_view("main_menu")