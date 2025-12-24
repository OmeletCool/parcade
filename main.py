import arcade
from src.windows.base_window import BaseWindow


if __name__ == "__main__":
    # Создаем главное окно
    window = BaseWindow()
    
    # Загружаем настройки музыки
    window.load_music_setting()
    window.play_background_music() 

    # Показываем стартовый экран
    window.switch_view("start_window")

    # Запускаем игровой цикл
    arcade.run()
