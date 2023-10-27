import json
import time
import sys
from VisioVerbal.src.generator import TextGenerator
import streamlit as st
import os

# RUNNING STREAMLIT UI ON LOCALHOST
# python3 -m streamlit run /RelativePath/To/Your/Project/automation_image_generation/src/streamlit_ui/streamlit_ui.py

SECRETS_PATH = 'VisioVerbal/secrets/api_key.txt'

def get_api_key():
    try:
        with open(SECRETS_PATH, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def check_for_existing_api_key():
    api_key = get_api_key()
    if api_key:
        return True
    else:
        return False


def generate_text(num_texts):
    with st.spinner('Wait for it...'):
        time.sleep(5)
        generator = TextGenerator(get_api_key())
        generated_texts = []
        for i in range(num_texts):
            text_data = generator.generate_image_text()
            generated_texts.append(text_data)

        phrase = text_data['Phrase']
        title = text_data['Title']
        description = text_data['Description']
        tags = text_data['Tags']
        st.success('Done!')

        return generated_texts

@st.cache_data
def load_data(file_path):
    with open(file_path, 'r') as file:
        file_contents = file.read()
        return json.loads(file_contents)

text_directory = 'VisioVerbal/data/recent_text_files'
text_files = os.listdir(text_directory)
file_info_list = []

for file_name in text_files:
    file_path = os.path.join(text_directory, file_name)
    modification_time = os.path.getmtime(file_path)
    file_info = {'file_name': file_name, 'modification_time': modification_time}
    file_info_list.append(file_info)

# Sort the list of dictionaries by modification time (latest first)
file_info_list.sort(key=lambda x: x['modification_time'], reverse=False)

st.title("Text Generator")
selected_file = "New Text.."
text_files.append("New Text..")
selected_file = st.sidebar.selectbox('Select a Text', text_files, index=text_files.index("New Text.."))

text_generator = TextGenerator(get_api_key())
text_input = st.text_input(label="Put in your custom text")

num_texts_to_generate = st.number_input("Choose the number of texts to generate", min_value=1, max_value=10, value=1, step=1)

if st.button('Generate own custom text.'):
    phrase = text_generator.generate_custom_text(text_input)
    st.write(phrase)

if st.sidebar.button('Generate New Text'):
    generated_text_data = generate_text(num_texts_to_generate)

    for idx, text_data in enumerate(generated_text_data):
        st.subheader(f"Generated Text {idx + 1}")
        st.write(f"Phrase: {text_data['Phrase']}")
        st.write(f"Title: {text_data['Title']}")
        st.write(f"Description: {text_data['Description']}")
        st.write(f"Tags: {', '.join(text_data['Tags'])}")


if selected_file == "New Text..":
    st.write('OR')
    st.write("Create new text!")
    if st.button("Generate Text.."):
        generated_text_data = generate_text(num_texts_to_generate)

        for idx, text_data in enumerate(generated_text_data):
            st.subheader(f"Generated Text {idx + 1}")
            st.write(f"Phrase: {text_data['Phrase']}")
            st.write(f"Title: {text_data['Title']}")
            st.write(f"Description: {text_data['Description']}")
            st.write(f"Tags: {', '.join(text_data['Tags'])}")

else:
    if selected_file:
        file_path = os.path.join(text_directory, selected_file)
        data_dict = load_data(file_path)
        st.subheader("Generated Phrase")
        st.write(data_dict['Phrase'])
        st.subheader("Generated Title")
        st.write(data_dict['Title'])
        st.subheader("Generated Description")
        st.write(data_dict['Description'])
        st.subheader('Generated Tags')
        st.write(data_dict['Tags'])

