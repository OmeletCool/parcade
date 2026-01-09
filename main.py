import arcade
from src.windows.base_window import BaseWindow

if __name__ == "__main__":
    # Создаем главное окно
    window = BaseWindow()

    from src.windows.loading_view import LoadingView

    loading_view = LoadingView(
        window=window,
        next_view_name='start_window',
        load_tag='common'
    )

    # Показываем стартовый экран
    window.show_view(loading_view)

    # Запускаем игровой цикл
    arcade.run()
