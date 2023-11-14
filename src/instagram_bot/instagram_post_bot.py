import requests
import json
import boto3
import os
from time import sleep


GRAPH_URL = "https://graph.facebook.com"
username = ""
client_id = ""
INSTAGRAM_ACCOUNT_ID = ""
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""
JPEG_IMAGES_DIRECTORY = ""
BUCKET_NAME = "technovisualartisty"
TEXT_DIRECTORY = ""
CAPTION = '#DigitalArt #TraditionalArt #GraphicDesign #Painting #Drawing #Illustration #Sculpture #Photography #ArtificialIntelligence #CreativeCoding #GenerativeArt #DesignInspiration #ConceptArt #UIUX #WebDesign #VRDesign #3DArt #Animation #TechArt #CodeArt #DataVisualization #GameDesign #AugmentedReality #VirtualReality #ArtTech #ComputerGraphics'


def format_tags_for_url(tags):
    """
    FUNCTION TO FORMAT THE CAPTION FOR URL
    :param tags:
    :return:
    """

    formatted_tags = tags.replace(' ', '%20').replace('#', '%23')
    return formatted_tags


# MARK: S3 FUNCTIONS
def upload_to_s3_bucket(image_directory = ""):
    """
    UPLOADS DIRECTORY TO S3 BUCKET
    :return:
    """

    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY)

    for root, dirs, files in os.walk(image_directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                s3_client.upload_file(file_path, BUCKET_NAME, filename)
                print(f"{filename} uploaded to S3")
            except Exception as e:
                print(f"Failed to upload {filename} to S3: {e}")


def delete_files_from_s3(bucket_name, files_to_delete):
    """
    DELETE FILES IN S3
    :param bucket_name: <YOUR BUCKET NAME>
    :param files_to_delete: <LIST OF FILES TO DELETE>
    :return:
    """

    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_ACCESS_KEY,
                             aws_secret_access_key=AWS_SECRET_KEY)

    for file_key in files_to_delete:
        s3_client.delete_object(Bucket=bucket_name, Key=file_key)
        print(f"SUCCSSFULLY DELETED {file_key} FROM S3 BUCKET.")



def retrieve_all_images_from_s3(bucket_name=""):
    """
    :params:
    bucket_name = Name of the bucket.

    :return:
    Response list with all keys.
    """

    responses_list = []
    s3_client = boto3.client('s3',
                            aws_access_key_id =AWS_ACCESS_KEY,
                            aws_secret_access_key =AWS_SECRET_KEY)

    for key in s3_client.list_objects(Bucket=bucket_name)['Contents']:
        response = key['Key']
        responses_list.append(response)

    return responses_list


#MARK: INSTAGRAM GRAPH API
def create_container(instagram_account_id = "",
                     image_name = "",
                     access_token = "",
                     caption = ""):
    """
    URL:
    graph.facebook.com/instagram_account_id/media?image_url= {s3 bucket url} & access_token= {access token}

    FUNCTION TO CREATE INSTAGRAM CONTAINER
    *** ONLY USE JPEG, MAX 8MB SIZE ***

        :param instagram_account_id: <YOUR INSTAGRAM ACCOUNT ID>
        :param image_url: <IMAGE URL>
        :param access_token: <INSTAGRAM ACCESS TOKEN>

    :return:
    response
    """

    container_ids = []
    image_url = f"https://technovisualartisty.s3.eu-west-1.amazonaws.com/{image_name}"


    url = f"{GRAPH_URL}/{instagram_account_id}/media?image_url={image_url}&access_token={access_token}&caption={caption}"
    payload = {}
    headers = {}
    response = requests.request("POST", url, headers=headers, data=payload)

    response_dict = json.loads(response.text)
    print(response_dict)
    container_ids.append(response_dict['id'])

    return container_ids


def publish_container(instagram_account_id="",
                      creation_id=0,
                      access_token=""):
    """
    FUNCTION TO PUBLISH THE CONTAINER ON INSTAGRAM

    :param instagram_account_id: <YOUR INSTAGRAM ACCOUNT ID>
    :param creation_id: <CONTAINER ID>
    :param access_token: <ACCESS TOKEN GENERATED IN THE FACEBOOK APP>

    :return:
    response
    """

    url = f"{GRAPH_URL}/v18.0/{instagram_account_id}/media_publish?creation_id={creation_id}&access_token={access_token}"

    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def publish_x_instagram(instagram_account_id, access_token, image_names, X, should_remove=False):
    """
    FUNCTION TO CREATE AND PUBLISH X CONTAINERS, E.G. 10 POSTS

    :param instagram_account_id: <YOUR INSTAGRAM ACCOUNT ID>
    :param access_token: <YOUR FACEBOOK ACCESS TOKEN>
    :param image_names: <ARRAY OF IMAGES>
    :param X: <THE VALUE HOW MANY IMAGES YOU WANT TO POST>
    :param should_remove: <BOOL VALUE RATHER IMAGES SHOULD GET DELETED OR NOT>
    :return:
    """

    FORMATTED_CAPTION = format_tags_for_url(CAPTION)

    container_count = 0
    files_to_delete = []

    for name in image_names:
        if container_count >= X:
            break

        creation_ids = create_container(instagram_account_id, name, access_token, FORMATTED_CAPTION)

        for creation_id in creation_ids:
            publish_container(instagram_account_id, creation_id, access_token)
            container_count += 1

            print("****************************")
            print("SUCCESSFULLY UPLOADED IMAGE ON INSTAGRAM")
            print("****************************")

            files_to_delete.append(name)

    if should_remove:
        delete_files_from_s3(BUCKET_NAME, files_to_delete)
    else:
        print("REMOVING DISABLED.\n")



if __name__ == "__main__":
    image_names = retrieve_all_images_from_s3(bucket_name='technovisualartisty')
    create_publish_X_containers(INSTAGRAM_ACCOUNT_ID, ACCESS_TOKEN, image_names, 3)