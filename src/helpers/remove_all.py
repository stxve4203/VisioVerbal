import os

ORIGINAL_IMAGES_PATH = '/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/original_images'
RESIZED_IMAGES_PATH = '/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/resized_images'
RECENT_TEXT_FILES = '/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/recent_text_files'

directories_to_clear = [ORIGINAL_IMAGES_PATH, RESIZED_IMAGES_PATH, RECENT_TEXT_FILES]

def remove_all_files_in_directories(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

for directory in directories_to_clear:
    remove_all_files_in_directories(directory)
