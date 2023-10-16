from PIL import Image, ImageDraw, ImageFont
import numpy as np
from random_generator import RandomGenerator
import textwrap


def draw_multiple_line_text(image, text, font, text_color, text_start_height):
    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    lines = textwrap.wrap(text, width=40)
    total_text_height = (sum(font.getsize(line)[1] for line in lines))

    y_text = text_start_height + (image_height - total_text_height) // 2

    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height


class ImageGeneratorText:
    _generator = RandomGenerator()

    def __init__(self):
        self._width = None
        self._height = None
        self._message = None
        self._color = None
        self._padding = None

    def drawImage(self,
                  width=1024,
                  height=1024,
                  padding=20,
                  message=""
                  ):
        self._width = width
        self._height = height
        self._message = message.upper()
        self._color = self._generator.randomColor()
        self._padding = padding

        image = Image.new('RGB', (self._width, self._height), color=self._color)
        font_size = 40
        font = ImageFont.truetype("Calibri.ttf", font_size)

        text_color = (200, 200, 200)
        text_start_height = 0
        draw_multiple_line_text(image, self._message, font, text_color, text_start_height)

        image.save(
            f'/Users/steve/PycharmProjects/automation_image_generation/data/images_with_text/{self._generator.randomName()}.png')
        return image


generator = ImageGeneratorText()
generator.drawImage(
    message='Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam')
