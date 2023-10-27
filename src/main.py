from PIL import Image
from tqdm import tqdm
import os


# Path for original_images
original_image_path = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/original_images"
resized_images_path = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/resized_images"

original_image_files = [
    filename for filename in os.listdir(original_image_path) if filename.lower().endswith((".png", ".jpg", ".jpeg"))
]
resized_image_files = [
    filename for filename in os.listdir(resized_images_path) if filename.lower().endswith((".png", ".jpg", ".jpeg"))
]

resized_width = 6000
resized_height = 6000

original_image_files.sort()

for file in original_image_files:
    if file.startswith('.'):
        new_name = file[1:]  # Remove the first dot
        old_path = os.path.join(original_image_path, file)
        new_path = os.path.join(original_image_path, new_name)
        os.rename(old_path, new_path)

for filename in tqdm(original_image_files):
    resized_filename = f'{filename.split(".")[0]}_RESIZED.{filename.split(".")[-1]}'
    resized_file_path = os.path.join(resized_images_path, resized_filename)

    if os.path.exists(resized_file_path):
        print(f"Resized image {resized_filename} already exists.. Skipping {filename}...")
        continue

    original_image = Image.open(os.path.join(original_image_path, filename))
    resized_image = original_image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)

    resized_image.save(os.path.join(resized_images_path, resized_filename), quality=100)
    print(f"Resized and saved {filename} as {resized_filename}")

print("images saved.")
