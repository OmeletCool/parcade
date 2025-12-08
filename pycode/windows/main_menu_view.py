import arcade


class MainMenu(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.w = width
        self.h = height
        # Загружаем текстуру (изображение)
        self.texture = arcade.load_texture(
            ":resources:/images/backgrounds/abstract_2.jpg")

    def on_draw(self):
        self.clear()

        # Отрисовываем изображение во весь экран
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(
            self.w // 2, self.h // 2, self.w, self.h))
