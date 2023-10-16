from PIL import ImageDraw
import textwrap


def limit_words_per_line(text, max_words_per_line=20):
    # Split the text into words
    words = text.split()

    # Initialize variables
    lines = []
    current_line = []

    for word in words:
        if len(current_line) + len(word) + 1 <= max_words_per_line:
            # Add the word to the current line
            current_line.append(word)
        else:
            # Start a new line
            lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    formatted_text = "\n".join(lines)

    return formatted_text


def draw_multiple_line_text(image, text, font, text_color, text_start_height):

    draw = ImageDraw.Draw(image)
    image_width, image_height = image.size
    y_text = text_start_height
    lines = textwrap.wrap(text, width=40)
    for line in lines:
        line_width, line_height = font.getsize(line)
        draw.text(((image_width - line_width) / 2, y_text),
                  line, font=font, fill=text_color)
        y_text += line_height
