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

    # Add the last line
    if current_line:
        lines.append(" ".join(current_line))

    # Join the lines to form the text with a maximum of max_words_per_line words per line
    formatted_text = "\n".join(lines)

    return formatted_text
