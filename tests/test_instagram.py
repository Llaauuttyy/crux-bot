import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

from pyfacebook import IgProApi
from facebook import GraphAPI
from cruxbot.cruxbot import APP_ID, APP_SECRET, PAGE_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ID

import cruxbot.instagram_actions as ig


def testGetUserInfo():
    data = ig.get_ig_user_info(
        api = api,
        username = username
    )

    assert "ig_id" in data


def testGetUserMedias():
    data = ig.get_ig_user_medias(
        api = api,
        username = username
    )

    assert isinstance(data, list) and len(data) != 0


def testGetMediaInfo():
    data = ig.get_ig_media_info(
        api = api,
        media_id = media_id
    )

    assert "owner" in data


def testPostPhoto():
    data = ig.post_ig_photo(
        api = graphApi,
        instagram_business_id = INSTAGRAM_BUSINESS_ID,
        image_url = image_url
    )

    assert "id" in data


if __name__ == "__main__":

    username = "camilamur_"
    image_url = "https://i.ytimg.com/vi/cn8oF2kRMyY/hqdefault.jpg"
    media_id = "17881781170970625"

    api = IgProApi(
        app_id = APP_ID,
        app_secret = APP_SECRET,
        long_term_token = PAGE_ACCESS_TOKEN,
        instagram_business_id = INSTAGRAM_BUSINESS_ID
    )

    graphApi = GraphAPI(
        access_token = PAGE_ACCESS_TOKEN
    )

    testGetUserInfo()
    testGetUserMedias()
    testGetMediaInfo()
    testPostPhoto()