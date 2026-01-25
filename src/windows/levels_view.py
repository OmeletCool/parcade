import arcade
from src.registry import reg
from resources.languages import LANGUAGES


class LevelsView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window
        self.reg = reg
        self.language: int = self.window.language

        self.current_episode = 0
        self.target_offset = 0.0
        self.current_offset = 0.0
        self.scroll_speed = 0.15

        self.background_sprite_list = arcade.SpriteList()
        self.episode_buttons = arcade.SpriteList()
        self.background_sprite = None

        self.texts = []

        self.ui_text_left = arcade.Text(
            "<", 0, 0, arcade.color.WHITE, font_size=60, anchor_y="center", font_name='MS PGothic')
        self.ui_text_right = arcade.Text(
            ">", 0, 0, arcade.color.WHITE, font_size=60, anchor_y="center", font_name='MS PGothic')

    def setup(self):
        self.language = self.window.language

        self.episode_buttons.clear()
        self.background_sprite_list.clear()
        self.texts.clear()

        texture = self.reg.get(
            'common/textures/backgrounds/main_menu_background.png')
        self.background_sprite = arcade.Sprite(texture)
        self.background_sprite.width = float(self.window.width)
        self.background_sprite.height = float(self.window.height)
        self.background_sprite.position = self.window.width / 2, self.window.height / 2
        self.background_sprite_list.append(self.background_sprite)

        for i in range(3):
            if i == 0:
                btn = arcade.Sprite(self.reg.get(
                    'common/textures/backgrounds/st_episode.png'))
                btn.width = int(self.window.width * 0.6)
                btn.height = int(self.window.height * 0.6)
                btn.episode_index = 0
                btn.center_x = float(self.window.width / 2)
                btn.center_y = float(self.window.height / 2)
            else:
                btn = arcade.SpriteSolidColor(
                    int(self.window.width * 0.6),
                    int(self.window.height * 0.6),
                    (60, 60, 60, 255)
                )
                btn.episode_index = i
                btn.center_x = float(self.window.width / 2 +
                                     (i * self.window.width))
                btn.center_y = float(self.window.height / 2)

            self.episode_buttons.append(btn)

            label_text = f"{LANGUAGES['episodes'][self.language]} {i + 1}"

            label = arcade.Text(
                label_text,
                0, 0,
                arcade.color.WHITE,
                font_size=30,
                anchor_x="center",
                font_name='Montserrat'
            )
            self.texts.append(label)

        self._update_ui_positions()
        self.target_offset = float(-(self.current_episode * self.window.width))
        self.current_offset = self.target_offset

    def _update_ui_positions(self):
        self.ui_text_left.position = (50, self.window.height / 2)
        self.ui_text_right.position = (
            self.window.width - 80, self.window.height / 2)

    def on_show_view(self):
        self.setup()

    def on_update(self, delta_time: float):
        diff = self.target_offset - self.current_offset
        if abs(diff) < 0.1:
            self.current_offset = self.target_offset
        else:
            self.current_offset += diff * self.scroll_speed

        for i, (btn, label) in enumerate(zip(self.episode_buttons, self.texts)):
            base_x = (self.window.width / 2) + (i * self.window.width)
            btn.center_x = base_x + self.current_offset
            btn.center_y = self.window.height / 2
            label.x = btn.center_x
            label.y = btn.center_y - (btn.height / 2) - 50

    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw()
        self.episode_buttons.draw()

        for label in self.texts:
            if -500 < label.x < self.window.width + 500:
                label.draw()

        is_moving = abs(self.target_offset - self.current_offset) > 1.0

        if not is_moving:
            if self.current_episode > 0:
                self.ui_text_left.draw()
            if self.current_episode < 2:
                self.ui_text_right.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        is_moving = abs(self.target_offset - self.current_offset) > 1.0
        if is_moving:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            if x < 150 and self.current_episode > 0:
                self.change_episode(self.current_episode - 1)
            elif x > self.window.width - 150 and self.current_episode < 2:
                self.change_episode(self.current_episode + 1)

            for btn in self.episode_buttons:
                if btn.collides_with_point((x, y)):
                    print(f"Выбран эпизод {btn.episode_index + 1}")
                    if 'common/sounds/music/main_theme.ogg' in self.window.music_players.keys():
                        self.window.stop_definite_music(
                            'common/sounds/music/main_theme.ogg')
                    self.window.forced_music['common/sounds/music/main_theme.ogg'][1] = False
                    self.window.switch_view(
                        ['loading_view', 'game_house_view', f'{btn.episode_index + 1}episode'])

    def change_episode(self, index):
        self.current_episode = index
        self.target_offset = float(-(self.current_episode * self.window.width))

    def on_key_press(self, symbol, modifiers):
        is_moving = abs(self.target_offset - self.current_offset) > 1.0
        if is_moving:
            return

        if symbol == arcade.key.ESCAPE:
            self.window.switch_view("main_menu")
        elif symbol == arcade.key.LEFT and self.current_episode > 0:
            self.change_episode(self.current_episode - 1)
        elif symbol == arcade.key.RIGHT and self.current_episode < 2:
            self.change_episode(self.current_episode + 1)

    def on_resize(self, width: float, height: float):
        if self.background_sprite:
            self.background_sprite.width = width
            self.background_sprite.height = height
            self.background_sprite.position = width / 2, height / 2

        for btn in self.episode_buttons:
            btn.width = width * 0.6
            btn.height = height * 0.6

        self._update_ui_positions()
        self.target_offset = float(-(self.current_episode * width))
        self.current_offset = self.target_offset
