from time import sleep
from instapy import InstaPy

session = InstaPy(username="technovisualartisty", password="Waschbaer4203").login()
session.login()
session.like_by_tags(["bmw", "mercedes"], amount=5)
session.set_dont_like(["naked", "nsfw"])
session.set_do_follow(True, percentage=50)
session.set_do_comment(True, percentage=50)
session.set_comments(["Nice!", "Sweet!", "Beautiful :heart_eyes:"])
session.end()
