from PIL import Image
import os


""" 
********* CONFIG *********
"""
DIRECTORY_PATH = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/original_images"
OUTPUT_DIRECTORY_PATH = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/src/instagram_bot/data/posts/jpeg_images"


"""
********* FUNCTIONS *******
"""

def convert_png_to_jpeg(png_image_path, jpeg_image_path):
    try:
        with Image.open(png_image_path) as img:
            img = img.convert("RGB")
            img.save(jpeg_image_path, "JPEG")
        print(f"Conversion successful. Image saved as {jpeg_image_path}")
    except Exception as e:
        print(f"Conversion failed for {png_image_path}: {e}")

for filename in os.listdir(DIRECTORY_PATH):
    if filename.endswith(".png"):
        png_path = os.path.join(DIRECTORY_PATH, filename)
        jpeg_path = os.path.join(OUTPUT_DIRECTORY_PATH, filename.replace(".png", ".jpeg"))
        convert_png_to_jpeg(png_path, jpeg_path)
