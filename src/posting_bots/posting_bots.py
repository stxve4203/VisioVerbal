from src.instagram_bot.instagram_post_bot import publish_x_instagram, retrieve_all_images_from_s3
from src.facebook_bot.facebook_post_bot import publish_x_facebook, retrieve_image_path_from_dir
from src.main import reformat_files
from time import sleep


INSTAGRAM_ACCOUNT_ID = ""
INSTAGRAM_ACCESS_TOKEN = ''

FACEBOOK_ACCESS_TOKEN = ''
FACEBOOK_PAGE_ID = ""

AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""

ORIGINAL_IMAGE_PATH = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/original_images"
RESIZED_IMAGE_PATH = "/Users/steve/PycharmProjects/VisioVerbal_Project/VisioVerbal/data/resized_images"


def publish_posts(X, upload_files=True):

    if upload_files:
        reformat_files(ORIGINAL_IMAGE_PATH, RESIZED_IMAGE_PATH)
    else:
        print("UPLOADING FILES DISABLED.\n")

    image_names = retrieve_all_images_from_s3(bucket_name='technovisualartisty')

    print("Publishing on Instagram..\n")
    publish_x_instagram(instagram_account_id=INSTAGRAM_ACCOUNT_ID,
                                access_token=INSTAGRAM_ACCESS_TOKEN,
                                image_names=image_names,
                                X=X
                        )

    print("Publishing on Facebook..\n")
    publish_x_facebook(access_token=FACEBOOK_ACCESS_TOKEN,
                              data_path=RESIZED_IMAGE_PATH,
                              X=X
                        )

publish_posts(2, upload_files=False)
