import time

from model.generator import TextGenerator
import streamlit as st


def get_api_key():
    try:
        with open('/Users/steve/PycharmProjects/automation_image_generation/model/api_key.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None


def check_for_existing_api_key():
    api_key = get_api_key()
    if api_key:
        return True
    else:
        return False


def generate_text():
    # Replace this with your TextGenerator logic to generate text
    with st.spinner('Wait for it...'):
        time.sleep(5)
        generator = TextGenerator(get_api_key())
        text_data = generator.generate_image_text()

        phrase = text_data['Phrase']
        title = text_data['Title']
        description = text_data['Description']
        tags = text_data['Tags']
        st.success('Done!')

        return phrase, title, description, tags


""" 
TO RUN THE STREAMLIT UI:
python3 -m streamlit run /RelativePath/To/Your/Project/automation_image_generation/model/streamlit_ui/streamlit_ui.py

"""

st.title("Text Generator")

if st.button("Generate Text"):
    phrase, title, description, tags = generate_text()
    st.subheader("Generated Phrase")
    st.write(phrase)
    st.subheader("Generated Title")
    st.write(title)
    st.subheader("Generated Description")
    st.write(description)
    st.subheader('Generated Tags')
    st.write(tags)
