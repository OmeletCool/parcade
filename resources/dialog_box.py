import arcade
import math
import random
import re
from enum import Enum
from typing import List, Optional, Callable, Tuple, Dict
from dataclasses import dataclass
from src.registry import reg


class TextEffect(Enum):
    NORMAL = "normal"
    SHAKE = "shake"
    WAVE = "wave"
    RAINBOW = "rainbow"


class Voice(Enum):
    DEFAULT = "default"
    PLAYER = 'player'
    NONE = 'none'
    GOVERMENT = "government"
    CIVILIAN = "civilian"
    POSTMAN = 'postman'
    FEAR = "fear"


class Icon(Enum):
    NONE = None
    DEVELOPER = 'common/textures/icons/test_icon.png'
    PHONE = 'common/textures/icons/phone_icon.png'

    class POSTMAN(Enum):
        DEFAULT = 'common/textures/icons/postman/default.png'
        THINKING = 'common/textures/icons/postman/thinking.png'
        SAD = 'common/textures/icons/postman/sad.png'
        ANGRY = 'common/textures/icons/postman/angry.png'

    class PLAYER(Enum):
        DEFAULT = 'common/textures/icons/main_character/default.png'
        ANGRY = 'common/textures/icons/main_character/angry.png'


@dataclass
class DialoguePhrase:
    text: str
    speed: float = 25.0
    effect: TextEffect = TextEffect.NORMAL
    voice: Voice = Voice.DEFAULT
    font_name: Optional[str] = None
    callback: Optional[Callable] = None
    skippable: bool = True
    pitch: float = 1.0
    logo: any = None


class DialogBox:
    def __init__(self, window: arcade.Window, default_font_name: str = "Montserrat"):
        self.window = window
        self.reg = reg
        self.default_font_name = default_font_name
        self.base_width = 1376
        self.base_height = 768
        self.bg_color = (0, 0, 0, 245)
        self.border_color = (255, 255, 255, 255)
        self.border_thickness = 3
        self._measure_text = arcade.Text("", 0, 0)
        self.sound_interval = 0.06
        self.time_since_last_sound = 0.0
        self.char_timer = 0.0
        self.visible_chars_count = 0
        self.seconds_per_char = 0.0
        self._last_w = window.width
        self._last_h = window.height
        self._resize_threshold = 5
        try:
            v_snd = self.reg.get(
                'common/sounds/sfx/voices/goverment_voice.wav')
            self.voices = {v: v_snd for v in Voice}
            self.voices[Voice.NONE] = None
        except:
            self.voices = {v: None for v in Voice}
        self.phrases: List[DialoguePhrase] = []
        self.current_idx = -1
        self.is_active = False
        self.waiting_for_input = False
        self.callback_fired = False
        self.portrait_list = arcade.SpriteList()
        self.char_sprites: List[arcade.Text] = []
        self.char_positions: List[Tuple[float, float]] = []
        self._update_layout(force=True)

    def _setup_dimensions(self):
        dw = abs(self.window.width - self._last_w)
        dh = abs(self.window.height - self._last_h)
        if dw > self._resize_threshold or dh > self._resize_threshold:
            self._update_layout()

    def _update_layout(self, force=False):
        self._last_w = self.window.width
        self._last_h = self.window.height
        self.scale = self.window.width / self.base_width
        self.height = self.window.height * 0.28
        self.width = self.window.width * 0.94
        self.x = self.window.width / 2
        self.y = self.height / 2 + (45 * self.scale)
        self.padding = 40 * self.scale
        self.base_font_size = int(36 * self.scale)
        if self.is_active and 0 <= self.current_idx < len(self.phrases):
            prog = self.visible_chars_count
            self._load_phrase(self.current_idx)
            self.visible_chars_count = min(prog, len(self.char_sprites))

    def start_dialogue(self, phrases: List[DialoguePhrase]):
        self.phrases = phrases
        self.current_idx = 0
        self.is_active = True
        self.visible_chars_count = 0
        self.char_timer = 0.0
        self._load_phrase(0)

    def _load_phrase(self, idx: int):
        self.current_phrase = self.phrases[idx]
        self.callback_fired = False
        self.seconds_per_char = 1.0 / \
            self.current_phrase.speed if self.current_phrase.speed > 0 else 0
        if self.current_idx != idx:
            self.char_timer = 0.0
            self.visible_chars_count = 0
        self.waiting_for_input = False
        self.portrait_list.clear()
        indent_x = 0
        logo_val = self.current_phrase.logo
        if logo_val and hasattr(logo_val, 'value'):
            logo_val = logo_val.value
        if logo_val:
            tex = self.reg.get(logo_val)
            if tex:
                s = arcade.Sprite(tex)
                s.scale = (self.height - self.padding * 1.2) / s.height
                s.left = self.x - self.width / 2 + self.padding
                s.center_y = self.y
                self.portrait_list.append(s)
                indent_x = s.width + self.padding
        max_w = self.width - (self.padding * 2) - indent_x
        max_h = self.height - (self.padding * 1.5)
        lines, final_size = self._wrap_and_fit(
            self.current_phrase.text, self.base_font_size, max_w, max_h)
        self.char_sprites = []
        self.char_positions = []
        start_x = self.x - self.width / 2 + self.padding + indent_x
        line_step = final_size * 1.4
        total_h = len(lines) * line_step
        curr_y = self.y + (total_h / 2) - (line_step / 2)
        for line in lines:
            curr_x = start_x
            for char, color in line:
                t = arcade.Text(char, curr_x, curr_y, color, font_size=final_size,
                                font_name=self.current_phrase.font_name or self.default_font_name, anchor_y="center")
                self.char_sprites.append(t)
                self.char_positions.append((curr_x, curr_y))
                curr_x += t.content_width
            curr_y -= line_step

    def _wrap_and_fit(self, text, start_size, max_w, max_h):
        curr_size = start_size
        raw_tokens = re.findall(
            r"(\{color:\d+,\d+,\d+\}.*?\{/color\}|\s+|\S+)", text)
        processed_tokens = []
        for token in raw_tokens:
            match = re.match(r"\{color:(\d+,\d+,\d+)\}(.*?)\{/color\}", token)
            if match:
                color_str, content = match.group(1), match.group(2)
                sub_tokens = re.findall(r"(\s+|\S+)", content)
                for st in sub_tokens:
                    processed_tokens.append(
                        (st, tuple(map(int, color_str.split(','))) + (255,)))
            else:
                processed_tokens.append((token, (255, 255, 255, 255)))
        while curr_size > 8:
            lines, curr_line, curr_line_w = [], [], 0
            self._measure_text.font_size = curr_size
            self._measure_text.font_name = self.default_font_name
            for content, color in processed_tokens:
                self._measure_text.text = content
                w = self._measure_text.content_width
                if not content.isspace() and curr_line_w + w > max_w:
                    if curr_line:
                        lines.append(curr_line)
                        curr_line, curr_line_w = [], 0
                for c in content:
                    self._measure_text.text = c
                    curr_line.append((c, color))
                    curr_line_w += self._measure_text.content_width
            if curr_line:
                lines.append(curr_line)
            if len(lines) * (curr_size * 1.5) <= max_h:
                return lines, curr_size
            curr_size -= 2
        return lines, curr_size

    def update(self, delta_time: float):
        if not self.is_active:
            return
        if self.waiting_for_input:
            if self.current_phrase.callback and not self.callback_fired:
                self.current_phrase.callback()
                self.callback_fired = True
            return
        self.char_timer += delta_time
        self.time_since_last_sound += delta_time
        while self.char_timer >= self.seconds_per_char and self.visible_chars_count < len(self.char_sprites):
            self.char_timer -= self.seconds_per_char
            self.visible_chars_count += 1
            idx = self.visible_chars_count - 1
            if idx < len(self.char_sprites):
                char = self.char_sprites[idx].text
                if char.strip() and self.voices.get(self.current_phrase.voice):
                    if self.time_since_last_sound >= self.sound_interval:
                        p = random.uniform(0.9, 1.1) * \
                            self.current_phrase.pitch
                        arcade.play_sound(
                            self.voices[self.current_phrase.voice], volume=0.3, speed=p)
                        self.time_since_last_sound = 0.0
        if self.visible_chars_count >= len(self.char_sprites):
            self.waiting_for_input = True

    def draw(self):
        if not self.is_active:
            return
        arcade.draw_rect_filled(arcade.rect.XYWH(
            self.x, self.y, self.width, self.height), self.bg_color)
        arcade.draw_rect_outline(arcade.rect.XYWH(
            self.x, self.y, self.width, self.height), self.border_color, self.border_thickness)
        self.portrait_list.draw(pixelated=True)
        t_now = arcade.get_window().time
        limit = min(self.visible_chars_count, len(
            self.char_sprites), len(self.char_positions))
        for i in range(limit):
            obj = self.char_sprites[i]
            ox, oy = self.char_positions[i]
            nx, ny = ox, oy
            if self.current_phrase.effect == TextEffect.SHAKE:
                nx += random.uniform(-1.2, 1.2)
                ny += random.uniform(-1.2, 1.2)
            elif self.current_phrase.effect == TextEffect.WAVE:
                ny += math.sin(t_now * 8 + i * 0.4) * (4 * self.scale)
            obj.x, obj.y = nx, ny
            obj.draw()

    def next_phrase(self):
        if not self.is_active:
            return
        if not self.waiting_for_input:
            if self.current_phrase.skippable:
                self.visible_chars_count = len(self.char_sprites)
                self.waiting_for_input = True
        else:
            self.current_idx += 1
            if self.current_idx < len(self.phrases):
                self.visible_chars_count = 0
                self.char_timer = 0.0
                self._load_phrase(self.current_idx)
            else:
                self.is_active = False
