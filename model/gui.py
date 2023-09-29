import tkinter as tk
from tkinter import ttk
import clipboard
# from data.CONSTANTS import API_KEY
from model.generator import TextGenerator


def get_api_key():
    try:
        with open('api_key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None



def save_api_key():
    api_key = api_key_entry.get()
    if api_key != "":
        with open('api_key.txt', 'w') as file:
            file.write(api_key)
        message_label.config(text="API Key saved successfully!")
        open_text_generator_window()
    else:
        style = ttk.Style()
        style.configure('Red')
        error_label.config(text="Error saving APIKEY, field can not be empty!", foreground='RED')
        error_label.pack()


def check_for_existing_api_key():
    api_key = get_api_key()
    if api_key:
        return True
    else:
        return False


def open_text_generator_window():
    text_generator_window = tk.Tk()
    text_generator_window.title("Text Generator")

    # Function to generate text
    def generate_text():
        text_generator = TextGenerator(get_api_key())
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

    # Function to copy text to clipboard
    def copy_text(text):
        clipboard.copy(text)
        text_generator_window.clipboard_clear()
        text_generator_window.clipboard_append(text)
        text_generator_window.update()

    # Create labels for displaying text
    title_label = ttk.Label(text_generator_window, text="", wraplength=700)
    title_label.pack_forget()
    description_label = ttk.Label(text_generator_window, text="", wraplength=700)
    description_label.pack_forget()
    tags_label = ttk.Label(text_generator_window, text="", wraplength=700)
    tags_label.pack_forget()

    # Create "Copy" buttons for Title, Description, and Tags
    copy_title_button = ttk.Button(text_generator_window, text="Copy Title",
                                   command=lambda: copy_text(title_label.cget("text")))
    copy_title_button.pack(pady=5)
    copy_description_button = ttk.Button(text_generator_window, text="Copy Description",
                                         command=lambda: copy_text(description_label.cget("text")))
    copy_description_button.pack(pady=5)
    copy_tags_button = ttk.Button(text_generator_window, text="Copy Tags",
                                  command=lambda: copy_text(tags_label.cget("text")))
    copy_tags_button.pack(pady=5)

    # Create a vertical scrollbar
    scrollbar = ttk.Scrollbar(text_generator_window, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Create a Text widget to display the generated text
    result_text = tk.Text(text_generator_window, wrap=tk.WORD, width=100, height=30, yscrollcommand=scrollbar.set)
    result_text.pack(pady=10, expand=True, fill="both")

    # Create a "Generate Text" button
    generate_button = ttk.Button(text_generator_window, text="Generate Text", command=generate_text)
    generate_button.pack(pady=10)

    # Start the Tkinter event loop for the text generator window
    text_generator_window.mainloop()

if not check_for_existing_api_key():
    # Create the main window for entering the API key
    api_key_window = tk.Tk()
    api_key_window.geometry("300x200")
    api_key_window.title("API Key Setup")

    # Create a label with a message
    message_label = ttk.Label(api_key_window, text="Type your API Key:")
    message_label.pack(pady=30)

    # Create an entry widget for entering the API key
    api_key_entry = ttk.Entry(api_key_window)
    api_key_entry.pack()

    # Error Label
    error_label = ttk.Label(api_key_window, text="Error saving API Key")
    error_label.pack_forget()

    # Create a button to save the API key
    save_button = ttk.Button(api_key_window, text="Save API Key", command=save_api_key)
    save_button.pack()

    # Start the Tkinter event loop for the API key window
    api_key_window.mainloop()
else:
    open_text_generator_window()