import streamlit as st
from PIL import Image
import os
import io
import random
import zipfile
import tempfile
import shutil
from time import sleep


TEMP_PATH = '/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/src/streamlit_ui/temp'

def resize_images(uploaded_images_temp="",
                  resized_width=600,
                  resized_height=600):
    resized_images = []

    original_image_path = 'original_images'
    resized_images_path = 'resized_images'

    if not os.path.exists(original_image_path):
        os.makedirs(original_image_path)

    if not os.path.exists(resized_images_path):
        os.makedirs(resized_images_path)

    resized_image_names = []

    for uploaded_image in uploaded_images:
        resized_image_name = f'{random.randint(10000, 99999)}.png'
        resized_image = uploaded_image.resize((resized_width, resized_height), Image.LANCZOS)
        resized_image.save(os.path.join(TEMP_PATH), quality=100)
        resized_image_names.append(resized_image_name)

    return resized_images

st.markdown('# Image Converter')

original_images = []
column1_images = []
column2_images = []
column3_images = []
uploaded_files = st.file_uploader("Choose Images to Convert", accept_multiple_files=True)

for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    original_images.append(uploaded_file)
    images_per_sublist = len(original_images) // 3
    column1_images = original_images[:images_per_sublist]
    column2_images = original_images[images_per_sublist:2 * images_per_sublist]
    column3_images = original_images[2 * images_per_sublist:]

col1, col2, col3 = st.columns(3)

with col1:
    for i in range(len(column1_images)):
        image = Image.open(column1_images[i])
        st.image(image, use_column_width=True)
with col2:
    for i in range(len(column2_images)):
        image = Image.open(column2_images[i])
        st.image(image, use_column_width=True)
with col3:
    for i in range(len(column3_images)):
        image = Image.open(column3_images[i])
        st.image(image, use_column_width=True)


if st.button("Convert Images 📸"):
    images = []
    with tempfile.TemporaryDirectory() as workdir:
        image = open(os.path.join(workdir, 'images.png'), 'w')
        image = Image.open(column1_images[i])
        images.append(image)
        resized_images = resize_images(images, resized_width=6000, resized_height=6000)

    st.write("Converting completed !")

