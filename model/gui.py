from model.generator import TextGenerator
import tkinter as tk
from tkinter import ttk
import clipboard
from data.CONSTANTS import API_KEY


text_generator = TextGenerator(API_KEY)


# Function to be called when the button is clicked
def generate_text():
    image_data = text_generator.generate_image_text()
    # Create a formatted text with labels
    title_label.config(text=f"{image_data['Title']}")
    description_label.config(text=f"{image_data['Description']}")

    original_tags = ", ".join(image_data['Tags'])

    tags_label.config(text=original_tags)

    generated_text = (
        f'\n{image_data["Title"]}\n'
        f'\n'
        f'\n{image_data["Description"]}\n'
        f'\n'
        f'\n{original_tags}\n'
    )

    # Clear previous text and insert the new generated text
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, generated_text)


def generate_formatted_text(image_data):
    formatted_text = (
        f"{image_data['Title']}\n\n"
        f"{image_data['Description']}\n\n"
        f"\n{image_data['Tags']}"
    )

    return formatted_text


# Function to copy text to clipboard
def copy_text(text):
    clipboard.copy(text)
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()


# Create a Tkinter window
root = tk.Tk()
root.title("Text Generator")
root.geometry("800x750")  # Set the size of the GUI window

# Create labels for displaying text
title_label = ttk.Label(root, text="", wraplength=700)
title_label.pack_forget()
description_label = ttk.Label(root, text="", wraplength=700,)
description_label.pack_forget()
tags_label = ttk.Label(root, text="", wraplength=700)
tags_label.pack_forget()


# Create "Copy" buttons for Title, Description, and Tags
copy_title_button = ttk.Button(root, text="Copy Title", command=lambda: copy_text(title_label.cget("text")))
copy_title_button.pack(pady=5)
copy_description_button = ttk.Button(root, text="Copy Description",
                                     command=lambda: copy_text(description_label.cget("text")))
copy_description_button.pack(pady=5)
copy_tags_button = ttk.Button(root, text="Copy Tags", command=lambda: copy_text(tags_label.cget("text")))
copy_tags_button.pack(pady=5)

# Create a vertical scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical")
scrollbar.pack(side="right", fill="y")


# Create a Text widget to display the generated text
result_text = tk.Text(root, wrap=tk.WORD, width=100, height=30, yscrollcommand=scrollbar.set)
result_text.pack(pady=10, expand=True, fill="both")

# Create a "Generate Text" button
generate_button = ttk.Button(root, text="Generate Text", command=generate_text)
generate_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
