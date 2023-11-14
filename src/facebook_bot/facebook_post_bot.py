import requests
import urllib3
import json
import facebook
import boto3
#from src.instagram_bot.instagram_post_bot import retrieve_all_images_from_s3, format_tags_for_url
import os

CAPTION = '#DigitalArt #TraditionalArt #GraphicDesign #Painting #Drawing #Illustration #Sculpture #Photography #ArtificialIntelligence #CreativeCoding #GenerativeArt #DesignInspiration #ConceptArt #UIUX #WebDesign #VRDesign #3DArt #Animation #TechArt #CodeArt #DataVisualization #GameDesign #AugmentedReality #VirtualReality #ArtTech #ComputerGraphics'
TOKEN = ""
FACEBOOK_PAGE_ID = ""
url = f'https://graph.facebook.com/{FACEBOOK_PAGE_ID}/photos'
GRAPH_URL = "https://graph.facebook.com"
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
DATA_DIR = ""


def remove_files_from_directory(directory_path):
    try:
        file_list = os.listdir(directory_path)
        for file_name in file_list:
            file_path = os.path.join(directory_path, file_name)
            os.remove(file_path)
            print(f"File {file_name} removed successfully.")
        print("All files removed successfully.")
    except Exception as e:
        print(f"Error removing files: {e}")


def retrieve_image_path_from_dir(image_dir):
    local_paths = []
    count = 0

    for key in image_dir:
        try:
            file_list = sorted(os.listdir(image_dir))
            for file_name in file_list:
                file_path = os.path.join(image_dir, file_name)
                count += 1
                local_paths.append(file_name)
            return local_paths

        except Exception as e:
            print(f'Images not found. {e}')



def publish_x_facebook(
        access_token,
        data_path,
        X,
        should_remove=False):

    """
    PUBLISHING X IMAGES TO FACEBOOK

    :param data_path:
    :param X:
    :return:
    """

    graph = facebook.GraphAPI(access_token=access_token)

    local_images_list = retrieve_image_path_from_dir(DATA_DIR)
    container_count = 0

    for image_name in local_images_list:
        if container_count >= X:
            break

        try:
            image_path = os.path.join(DATA_DIR, image_name)
            with open(image_path, 'rb') as image_file:
                response = graph.put_photo(image=image_file, message=CAPTION)

                if should_remove:
                    os.remove(image_path)
                    print(f"Successfully removed {image_path} from directory.")
                else:
                    print("Removing image disabled.\n")

            if 'id' in response:
                container_count += 1
                print("****************************")
                print(f"SUCCESSFULLY UPLOADED IMAGE {image_name}")
                print(f"Facebook Post ID: {response['id']}")
                print("****************************")
            else:
                print(f"Failed to upload image: {response}")
        except Exception as e:
            print(f"Error uploading image: {e}")
