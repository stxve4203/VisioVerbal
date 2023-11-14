from PIL import Image
from tqdm import tqdm
import os
from src.instagram_bot.instagram_post_bot import upload_to_s3_bucket
from time import sleep
from tqdm import tqdm

ORIGINAL_IMAGE_PATH = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/original_images"
RESIZED_IMAGE_PATH = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/resized_images"


def reformat_file_name(image_files = []):
    for file in image_files:
        if file.startswith('.'):
            new_name = file[1:]  # Remove the first dot
            old_path = os.path.join(ORIGINAL_IMAGE_PATH, file)
            new_path = os.path.join(ORIGINAL_IMAGE_PATH, new_name)
            os.rename(old_path, new_path)


def remove_png_file(png_image_path):
    try:
        os.remove(png_image_path)
        print(f"Removed {png_image_path}")
    except Exception as e:
        print(f"Failed to remove {png_image_path}: {e}")


def convert_png_to_jpeg(png_image_path, jpeg_image_path):
    try:
        with Image.open(png_image_path) as img:
            img = img.convert("RGB")
            img.save(jpeg_image_path, "JPEG")
        print(f"Conversion successful. Image saved as {jpeg_image_path}")
    except Exception as e:
        print(f"Conversion failed for {png_image_path}: {e}")


def reformat_files(original_image_path, resized_image_path):
    for filename in os.listdir(ORIGINAL_IMAGE_PATH):
        if filename.endswith(".png"):
            png_path = os.path.join(original_image_path, filename)
            jpeg_path = os.path.join(original_image_path, filename.replace(".png", ".jpeg"))

            convert_png_to_jpeg(png_path, jpeg_path)
            remove_png_file(png_path)

    original_image_files = [
        filename for filename in os.listdir(original_image_path) if filename.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    resized_image_files = [
        filename for filename in os.listdir(resized_image_path) if filename.lower().endswith((".png", ".jpg", ".jpeg"))
    ]

    reformat_file_name(original_image_files)

    new_image_files = [
        filename for filename in os.listdir(original_image_path) if filename.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    resized_width = 6000
    resized_height = 6000

    for filename in tqdm(new_image_files):
        resized_filename = f'{filename.split(".")[0]}_RESIZED.{filename.split("_")[-1]}'
        resized_file_path = os.path.join(resized_image_path, resized_filename)

        if os.path.exists(resized_file_path):
            print(f"Resized image {resized_filename} already exists.. Skipping {filename}..")
            continue

        original_image = Image.open(os.path.join(original_image_path, filename))
        resized_image = original_image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)

        resized_image.save(os.path.join(resized_image_path, resized_filename), quality=100)
        print(f"Resized and saved {filename} as {resized_filename}")

    upload_to_s3_bucket(ORIGINAL_IMAGE_PATH)
    print("++++++ SUCCESSFULLY UPLOADED IMAGES ++++++++")

    print("images saved.")