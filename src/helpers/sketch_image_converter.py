import cv2
from random_generator import RandomGenerator
import os
from tqdm import tqdm

random_generator = RandomGenerator()
LOGO_IMAGE_DIR = '/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/test_images/'
LOGO_OUTPUT_DIR = '/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/test_images/'

class ImageConverter:

    def image_to_sketch(self, input_image_path, output_directory):
        with os.scandir(input_image_path) as entries:
            for entry in tqdm(entries):
                if entry.is_file() and entry.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = entry.path

                    image = cv2.imread(image_path)

                    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    alpha = 1.5
                    enhanced_gray = cv2.convertScaleAbs(gray_image, alpha=alpha, beta=0)

                    blurred_image = cv2.GaussianBlur(enhanced_gray, (5, 5), 0)

                    sketch = cv2.adaptiveThreshold(
                        blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2
                    )

                    output_path = os.path.join(output_directory, entry.name)
                    cv2.imwrite(output_path, sketch)

converter = ImageConverter()
converter.image_to_sketch(LOGO_IMAGE_DIR, LOGO_OUTPUT_DIR)
