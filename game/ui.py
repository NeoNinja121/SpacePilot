# ui.py – PIL-based Display Rewrite for Display HAT Mini
import time
import random
from PIL import ImageFont, ImageDraw
from game.constants import *

class StatusBar:
    def __init__(self, display_config, speed, boost_active, boost_points, repair_points, damaged_systems, distance):
        self.display_config = display_config
        self.speed = speed
        self.boost_active = boost_active
        self.boost_points = boost_points
        self.repair_points = repair_points
        self.damaged_systems = damaged_systems
        self.distance_convered = distance


        self.messages = [
            "Systems OK", "DM collector on", "Dest: Unknown",
            "Mission: Explore", "Temp: OK", "Life sup: OK"
        ] if display_config.is_display_hat_mini else [
            "Systems nominal", "Dark matter collector active",
            "Destination: The unknown", "Current mission: Go further than anyone before",
            "Ship temperature: Cozy", "Life support: Operational"
        ]

        self.message_index = 0
        self.last_message_change = time.time()
        self.flicker = False
        self.last_flicker_time = time.time()

        self.font = ImageFont.load_default()
        self.height = MINI_STATUS_BAR_HEIGHT if display_config.is_display_hat_mini else STATUS_BAR_HEIGHT

    def update(self, speed, boost_active, boost_points, repair_points, damaged_systems, distance):
        self.speed = speed
        self.boost_active = boost_active
        self.boost_points = boost_points
        self.repair_points = repair_points
        self.damaged_systems = damaged_systems
        self.distance = distance
        now = time.time()
        if now - self.last_message_change > 5:
            self.message_index = (self.message_index + 1) % len(self.messages)
            self.last_message_change = now
        if damaged_systems and now - self.last_flicker_time > (0.5 + random.random() * 0.5):
            self.flicker = not self.flicker
            self.last_flicker_time = now

    def draw(self, draw):
        width = self.display_config.width
        height = self.height
        y_pos = self.display_config.height - height

        bg_color = (50, 0, 0) if self.damaged_systems and self.flicker else (0, 0, 0)
        draw.rectangle([0, y_pos, width, y_pos + height], fill=bg_color)

        draw.line([0, y_pos, width, y_pos], fill=COLOR_GREEN_DARK, width=1)
        draw.text((5, y_pos + 2), f"SPD: {self.speed * 2 if self.boost_active else self.speed} mi/s", font=self.font, fill=COLOR_YELLOW if self.boost_active else COLOR_GREEN)

        if self.damaged_systems:
            sys_text = f"SYS: {len(self.damaged_systems)} DMG"
            sys_color = COLOR_RED
        else:
            sys_text = "SYS: OK"
            sys_color = COLOR_GREEN

        text_width = draw.textlength(sys_text, font=self.font)
        draw.text((width - text_width - 5, y_pos + 2), sys_text, font=self.font, fill=sys_color)


        draw.text((5, y_pos + 14), f"DST: {self.distance}", font=self.font, fill=COLOR_GREEN)


        if self.display_config.is_display_hat_mini:
            draw.text(((width - 60) // 2, y_pos + 14), self.messages[self.message_index][:8], font=self.font, fill=COLOR_GREEN)


class ButtonBar:
    def __init__(self, display_config, boost_points, boost_active, repair_points, damaged_count, event_active):
        self.display_config = display_config
        self.boost_points = boost_points
        self.boost_active = boost_active
        self.repair_points = repair_points
        self.damaged_count = damaged_count
        self.event_active = event_active
        self.height = MINI_BUTTON_HEIGHT if display_config.is_display_hat_mini else BUTTON_HEIGHT
        self.font = ImageFont.load_default()

    def update(self, boost_points, boost_active, repair_points, damaged_count, event_active):
        self.boost_points = boost_points
        self.boost_active = boost_active
        self.repair_points = repair_points
        self.damaged_count = damaged_count
        self.event_active = event_active

    def draw(self, draw):
        pass


class EventDisplay:
    def __init__(self, display_config, event):
        self.display_config = display_config
        self.event = event
        self.create_time = time.time()
        self.title_font = ImageFont.load_default()
        self.text_font = ImageFont.load_default()
        self.option_font = ImageFont.load_default()

    def wrap_text(self, draw, text, max_width):
        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if draw.textlength(test_line, font=self.text_font) < max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.strip())

        return lines

    def draw(self, draw):
        width = self.display_config.width
        height = self.display_config.height

        # Draw event box
        margin = 10
        card_width = width - 2 * margin
        card_height = height - 2 * margin
        card_x = margin
        card_y = margin

        draw.rectangle([card_x, card_y, card_x + card_width, card_y + card_height], outline=COLOR_PURPLE, width=2)

        # Draw title
        title = self.event.title
        title_w = draw.textlength(title, font=self.title_font)
        draw.text((card_x + (card_width - title_w) // 2, card_y + 10), title, font=self.title_font, fill=COLOR_GREEN)

        # Draw description
        description_lines = self.wrap_text(draw, self.event.description, card_width - 20)
        y_offset = card_y + 30
        for line in description_lines:
            draw.text((card_x + 10, y_offset), line, font=self.text_font, fill=COLOR_WHITE)
            y_offset += 14

        # Draw options
        if self.event.options:
            draw.text((card_x + 10, y_offset + 10), f"A: {self.event.options[0]['text']}", font=self.option_font, fill=COLOR_YELLOW)
            if len(self.event.options) > 1:
                draw.text((card_x + 10, y_offset + 30), f"X: {self.event.options[1]['text']}", font=self.option_font, fill=COLOR_YELLOW)


class MilestoneDisplay:
    # Placeholder for future PIL version
    ...
