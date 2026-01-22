import arcade
import random


class NewspaperSystem:
    def __init__(self, window: arcade.Window):
        self.window = window
        self.visible = False
        self.aspect_ratio = 0.75

        self.text_objects = []
        self.line_points = []

        # Хранилище данных
        self.current_title = "УШИ ЛЕСА"
        self.current_headline = ""
        self.current_body = ""
        self.current_ads = []
        self.current_issue_num = random.randint(100, 999)
        self.current_day = random.randint(1, 31)

        # ОГРОМНЫЙ ПУЛ ВАРИАНТОВ
        self.anomaly_templates = [
            "КОШМАР НА ОКРАИНЕ: {prop}!",
            "УЧЕНЫЕ БЕССИЛЬНЫ: В ТАЙГЕ {prop}.",
            "НЕ ПУСКАЙТЕ ДЕТЕЙ В ЛЕС, ПОКА ТАМ {prop}.",
            "АНОМАЛИЯ ИЛИ ЗАГОВОР? ОЧЕВИДЦЫ ВИДЕЛИ, КАК {prop}.",
            "ПОТЕРЯННЫЙ ОТРЯД: ПЕРЕД ИСЧЕЗНОВЕНИЕМ ОНИ СООБЩИЛИ, ЧТО {prop}.",
            "СТРАННЫЙ ГУЛ ИЗ ПУСТОТЫ: {prop}.",
            "МЕСТНЫЙ ОХОТНИК В ШОКЕ: 'Я ВИДЕЛ, КАК {prop}'."
        ]

        self.anomaly_properties = [
            "деревья начинают кровоточить густой смолой",
            "камни взлетают на высоту человеческого роста",
            "воздух застывает, превращаясь в стекло",
            "тени отделяются от своих владельцев",
            "птицы начинают имитировать голоса умерших",
            "снег горит фиолетовым пламенем",
            "время замедляется до полной остановки",
            "почва под ногами пульсирует, как живое сердце",
            "радиоприемники ловят сигналы из 1945 года",
            "вода в ручьях течет вверх по склону",
            "звери выходят к людям и просят уйти"
        ]

        self.flavor_ads = [
            "ПРОДАМ ТРАКТОР. Почти на ходу. Или обменяю на мешок тушенки.",
            "ПОТЕРЯН КЛЮЧ от сейфа. Просьба вернуть за вознаграждение в литрах.",
            "ИЩУ ЖЕНУ. Умение готовить из хвои приветствуется.",
            "ПРОДАМ ДРОВА. Сухие, как горло после вчерашнего.",
            "КУПЛЮ ИКОНУ. Можно реставрированную. Срочно.",
            "ВНИМАНИЕ! Сосед с 4-го этажа — не человек. Я видел его глаза.",
            "ПОЗДРАВЛЯЕМ бабушку Маню со 105-летием. Снова жива!",
            "АНЕКДОТ: Идет медведь по лесу, видит — машина горит. Сел в неё и сгорел.",
            "УСЛУГИ: Заточка топоров, снятие венца безбрачия, настройка антенн.",
            "ПРОДАМ ГРИБЫ. Очень странные. Есть только один раз.",
            "ИЩУ ПОПУТЧИКА до Большой Земли. Свои патроны обязательно.",
            "НАЙДЕНО: Левая калоша у болота. Верну за честное 'спасибо'.",
            "ОБЪЯВЛЕНИЕ: Группа энтузиастов ищет вход в Шамбалу через подвал сельпо.",
            "ТРЕБУЕТСЯ: Сторож на склад №8. Желательно глухой."
        ]

        self.generate_content()

    def generate_content(self):
        prop = random.choice(self.anomaly_properties)
        template = random.choice(self.anomaly_templates)

        self.current_headline = template.format(prop=prop).upper()
        self.current_body = (
            "Местные власти продолжают замалчивать инцидент, списывая всё на испытания метеозондов. "
            "Однако в редакцию продолжают поступать звонки. Жители сообщают о странных изменениях в ландшафте. "
            "Старожилы вспоминают пророчества деда Пахома, который предсказывал, что 'земля разверзнется и выдаст всё накопленное'. "
            "Мы призываем читателей сохранять бдительность и не вступать в контакт с объектами, природа которых не ясна."
        )

        self.current_ads = random.sample(
            self.flavor_ads, k=len(self.flavor_ads))
        self.current_issue_num = random.randint(100, 999)
        self.update_layout()

    def update_layout(self):
        self.text_objects.clear()
        self.line_points.clear()

        w, h = self.window.width, self.window.height
        self.p_h = h * 0.9
        self.p_w = self.p_h * self.aspect_ratio

        if self.p_w > w * 0.95:
            self.p_w = w * 0.95
            self.p_h = self.p_w / self.aspect_ratio

        self.cx, self.cy = w / 2, h / 2
        scale = self.p_h / 800
        margin = 35 * scale

        left_x = self.cx - self.p_w / 2 + margin
        right_x = self.cx + self.p_w / 2 - margin
        top_y = self.cy + self.p_h / 2 - (40 * scale)

        # Название газеты
        self.text_objects.append(arcade.Text(
            self.current_title, self.cx, top_y, arcade.color.BLACK,
            font_size=int(44 * scale), font_name="Times New Roman", bold=True, anchor_x="center", anchor_y="top"
        ))

        line_y = top_y - (65 * scale)
        self.line_points.append(
            ((left_x, line_y), (right_x, line_y), max(1, int(4 * scale))))

        # Информация о выпуске (ВНИЗУ СПРАВА)
        info_text = f"Выпуск №{self.current_issue_num} | {self.current_day} окт."
        self.text_objects.append(arcade.Text(
            info_text, right_x, self.cy - self.p_h / 2 + (15 * scale),
            arcade.color.DARK_GRAY, font_size=int(9 * scale), anchor_x="right"
        ))

        # Колонки
        col_gap = 25 * scale
        main_w = (self.p_w - margin * 2 - col_gap) * 0.68
        side_w = (self.p_w - margin * 2 - col_gap) * 0.32
        side_x = left_x + main_w + col_gap

        # Заголовок статьи
        title_obj = arcade.Text(self.current_headline, left_x, line_y - (20 * scale), arcade.color.BLACK,
                                font_size=int(19 * scale), bold=True, width=int(main_w), multiline=True, anchor_y="top")
        self.text_objects.append(title_obj)

        # Текст статьи
        body_y = line_y - (25 * scale) - \
            title_obj.content_height - (10 * scale)
        self.text_objects.append(arcade.Text(self.current_body, left_x, body_y,
                                             arcade.color.BLACK, font_size=int(13 * scale), width=int(main_w), multiline=True, anchor_y="top"))

        # Объявления
        curr_ad_y = line_y - (20 * scale)
        for ad in self.current_ads:
            if curr_ad_y < (self.cy - self.p_h/2) + (40 * scale):
                break

            ad_obj = arcade.Text(ad, side_x, curr_ad_y, arcade.color.DARK_SLATE_GRAY,
                                 font_size=int(10 * scale), width=int(side_w), multiline=True, anchor_y="top")
            self.text_objects.append(ad_obj)
            curr_ad_y -= (ad_obj.content_height + (15 * scale))
            self.line_points.append(
                ((side_x, curr_ad_y + (8 * scale)), (side_x + side_w, curr_ad_y + (8 * scale)), 1))

    def draw(self):
        if not self.visible:
            return
        arcade.draw_rect_filled(arcade.rect.XYWH(
            self.cx, self.cy, self.p_w, self.p_h), color=(240, 235, 215))
        arcade.draw_rect_outline(arcade.rect.XYWH(
            self.cx, self.cy, self.p_w - 6, self.p_h - 6), color=arcade.color.BLACK, border_width=1)

        for p1, p2, width in self.line_points:
            arcade.draw_line(p1[0], p1[1], p2[0], p2[1],
                             arcade.color.BLACK, width)
        for t in self.text_objects:
            t.draw()


if __name__ == "__main__":
    class DebugWindow(arcade.Window):
        def __init__(self):
            super().__init__(1280, 720, "Газета: Тест", resizable=True)
            # ЖЕСТКИЙ МИНИМУМ
            self.set_minimum_size(800, 600)

            self.news = NewspaperSystem(self)
            self.news.visible = True

        def on_draw(self):
            self.clear(arcade.color.DARK_BLUE_GRAY)
            self.news.draw()
            arcade.draw_text("E: НОВЫЙ ВЫПУСК | ESC: ВЫХОД",
                             20, 20, arcade.color.WHITE, 10)

        def on_key_press(self, key, modifiers):
            if key == arcade.key.E:
                self.news.generate_content()
            if key == arcade.key.ESCAPE:
                self.close()

        def on_resize(self, width, height):
            super().on_resize(width, height)
            self.news.update_layout()

    window = DebugWindow()
    arcade.run()
