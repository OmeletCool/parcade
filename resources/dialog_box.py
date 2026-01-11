import arcade
import math
import random
import re
from enum import Enum
from typing import List, Optional, Callable, Tuple, Dict
from dataclasses import dataclass


class TextEffect(Enum):
    NORMAL = "normal"
    SHAKE = "shake"
    WAVE = "wave"
    RAINBOW = "rainbow"


class Voice(Enum):
    DEFAULT = "default"
    GOVERMENT = "goverment"
    CIVILIAN = "civilian"
    FEAR = "fear"


@dataclass
class DialoguePhrase:
    text: str
    speed: float = 20.0
    effect: TextEffect = TextEffect.NORMAL
    voice: Voice = Voice.DEFAULT
    font_name: Optional[str] = None
    callback: Optional[Callable] = None
    skippable: bool = True
    pitch: float = 1


class DialogBox:
    def __init__(self, window: arcade.Window, default_font_name: str = "Arial"):
        self.window = window
        self.default_font_name = default_font_name
        self.base_width = 1376
        self.base_height = 768

        self.bg_color = (0, 0, 0, 255)
        self.border_color = (255, 255, 255, 255)
        self.default_text_color = (255, 255, 255, 255)
        self.border_thickness = 4

        # Звуки
        self.voices: Dict[Voice, Optional[arcade.Sound]] = {
            Voice.DEFAULT: None,
            Voice.GOVERMENT: arcade.load_sound('resources/common/sounds/sfx/voices/goverment_voice.wav'),
            Voice.CIVILIAN: None,
            Voice.FEAR: None,
        }

        self.phrases: List[DialoguePhrase] = []
        self.current_idx = -1
        self.visible_chars_count = 0
        self.char_timer = 0.0
        self.seconds_per_char = 0.0
        self.is_active = False
        self.waiting_for_input = False
        self.indicator_blink = 0.0

        # Список для оптимизированных объектов текста
        self.text_objects: List[arcade.Text] = []
        self._setup_dimensions()

    def _setup_dimensions(self):
        scale = max(self.window.width / self.base_width,
                    self.window.height / self.base_height)
        self.width = self.window.width * 0.85
        self.height = self.window.height * 0.28
        self.x = self.window.width / 2
        self.y = self.height / 2 + (40 * scale)
        self.font_size = int(24 * scale)
        self.padding = int(35 * scale)
        self.line_height = self.font_size * 1.5

    def _parse_tags(self, raw_text: str) -> List[Tuple[str, tuple]]:
        pattern = r"\{color:(\d+,\d+,\d+)\}(.*?)\{/color\}|([^{]+)"
        matches = re.findall(pattern, raw_text)
        parsed_chars = []
        for match in matches:
            color_str, tagged_text, plain_text = match
            if color_str:
                r, g, b = map(int, color_str.split(','))
                for char in tagged_text:
                    parsed_chars.append((char, (r, g, b, 255)))
            else:
                for char in plain_text:
                    parsed_chars.append((char, self.default_text_color))
        return parsed_chars

    def start_dialogue(self, phrases: List[DialoguePhrase]):
        self._setup_dimensions()
        self.phrases = phrases
        self.current_idx = 0
        self.is_active = True
        self._load_phrase(self.current_idx)

    def _load_phrase(self, idx: int):
        self.current_phrase = self.phrases[idx]
        self.current_phrase.pitch = max(0.4, min(2, self.current_phrase.pitch))
        self.parsed_data = self._parse_tags(self.current_phrase.text)
        self.visible_chars_count = 0
        self.char_timer = 0.0
        self.seconds_per_char = 1.0 / \
            self.current_phrase.speed if self.current_phrase.speed > 0 else 0
        self.waiting_for_input = False

        current_font = self.current_phrase.font_name or self.default_font_name

        # ОПТИМИЗАЦИЯ: Создаем объекты заранее
        self.text_objects = []
        for char, color in self.parsed_data:
            obj = arcade.Text(
                char, 0, 0, color,
                font_size=self.font_size,
                font_name=current_font,
                anchor_y="top"
            )
            self.text_objects.append(obj)

    def update(self, delta_time: float):
        if not self.is_active:
            return

        if self.waiting_for_input:
            self.indicator_blink += delta_time
            return

        self.char_timer += delta_time

        while self.char_timer >= self.seconds_per_char and self.visible_chars_count < len(self.parsed_data):
            self.char_timer -= self.seconds_per_char
            self.visible_chars_count += 1

            current_char = self.parsed_data[self.visible_chars_count - 1][0]

            if current_char not in [" ", "\n"]:
                sound = self.voices.get(self.current_phrase.voice)
                should_play = (self.visible_chars_count %
                               2 == 1) or (self.current_phrase.speed <= 15)

                if sound and should_play:
                    pitch = random.uniform(
                        0.9 * self.current_phrase.pitch, 1 * self.current_phrase.pitch)
                    arcade.play_sound(sound, volume=0.3, speed=pitch)

        if self.visible_chars_count >= len(self.parsed_data):
            self.waiting_for_input = True
            if self.current_phrase.callback:
                self.current_phrase.callback()

    def draw(self):
        if not self.is_active:
            return

        # Фон и рамка
        arcade.draw_rect_filled(arcade.rect.XYWH(
            self.x, self.y, self.width, self.height), self.bg_color)
        arcade.draw_rect_outline(arcade.rect.XYWH(self.x, self.y, self.width, self.height),
                                 self.border_color, border_width=self.border_thickness)

        start_x = self.x - self.width/2 + self.padding
        start_y = self.y + self.height/2 - self.padding
        current_x, current_y = start_x, start_y
        time_ref = self.window.time

        for i in range(self.visible_chars_count):
            char = self.parsed_data[i][0]
            text_obj = self.text_objects[i]

            if char == '\n':
                current_x = start_x
                current_y -= self.line_height
                continue

            cw = text_obj.content_width
            if current_x + cw > self.x + self.width/2 - self.padding:
                current_x = start_x
                current_y -= self.line_height

            dx, dy = current_x, current_y

            if self.current_phrase.effect == TextEffect.SHAKE:
                dx += random.uniform(-math.sqrt(2), math.sqrt(2))
                dy += random.uniform(-2, 2)
            elif self.current_phrase.effect == TextEffect.WAVE:
                dy += math.sin(time_ref * 8 + i * 0.6) * 6
            elif self.current_phrase.effect == TextEffect.RAINBOW:
                phase = time_ref * 5 + i * 0.5
                r = int(math.sin(phase) * 127 + 128)
                g = int(math.sin(phase + 2) * 127 + 128)
                b = int(math.sin(phase + 4) * 127 + 128)
                text_obj.color = (r, g, b, 255)

            text_obj.x = dx
            text_obj.y = dy
            text_obj.draw()
            current_x += cw

        if self.waiting_for_input and int(self.indicator_blink * 4) % 2 == 0:
            ix, iy = self.x + self.width/2 - 40, self.y - self.height/2 + 30
            arcade.draw_triangle_filled(
                ix-10, iy+7,
                ix+10, iy,
                ix-10, iy-7,
                self.border_color
            )

    def next_phrase(self):
        if not self.is_active:
            return
        if self.waiting_for_input:
            self.current_idx += 1
            if self.current_idx < len(self.phrases):
                self._load_phrase(self.current_idx)
            else:
                self.is_active = False
        else:
            # ПРОВЕРКА НА ПРОПУСК
            if self.current_phrase.skippable:
                self.visible_chars_count = len(self.parsed_data)
                self.waiting_for_input = True


class DebugWindow(arcade.Window):
    def __init__(self):
        super().__init__(1376, 768, "Final Dialog System", resizable=True)
        self.dialog_box = DialogBox(self, default_font_name="Arial")
        self.start_test()

    def start_test(self):
        phrases = [
            DialoguePhrase("Эта фраза трясется {color:125,222,198}ВЕЧНО{/color}!",
                           effect=TextEffect.SHAKE, voice=Voice.GOVERMENT, speed=7, skippable=False),
            DialoguePhrase("Я санс. и я говорю своим шрифтом.",
                           voice=Voice.GOVERMENT, font_name="Montserrat"),
            DialoguePhrase("А Я ПАПАЙРУС! И Я ТОЖЕ ТРЯСУСЬ!",
                           voice=Voice.GOVERMENT, font_name="Impact", effect=TextEffect.SHAKE),
            DialoguePhrase("Радужная волна для завершения теста.",
                           effect=TextEffect.RAINBOW, voice=Voice.GOVERMENT)
        ]
        self.dialog_box.start_dialogue(phrases)

    def on_draw(self):
        self.clear()
        self.dialog_box.draw()

    def on_update(self, delta_time):
        self.dialog_box.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.ENTER, arcade.key.Z]:
            if self.dialog_box.is_active:
                self.dialog_box.next_phrase()
            else:
                self.start_test()

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        self.dialog_box._setup_dimensions()


if __name__ == "__main__":
    window = DebugWindow()
    arcade.run()

    # def on_draw(self):
    #     self.clear()
    #     self.dialog_box.draw()

    # def on_update(self, delta_time):
    #     self.dialog_box.update(delta_time)

    # def on_key_press(self, key, modifiers):
    #     if key in [arcade.key.ENTER, arcade.key.Z]:
    #         if self.dialog_box.is_active:
    #             self.dialog_box.next_phrase()
    #         else:
    #             self.start_test()

    # def on_resize(self, width: int, height: int):
    #     super().on_resize(width, height)
    #     self.dialog_box._setup_dimensions()
