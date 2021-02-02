import unittest
import json

import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

import cruxbot.instagram_actions as ig
import cruxbot.utils.constant as constant


class ApiPhotoTest(unittest.TestCase):

    def setUp(self):
        self.instagram_business_id = constant.INSTAGRAM_BUSINESS_ID

        self.api = ig.ExtApi(
            app_id = constant.APP_ID,
            app_secret = constant.APP_SECRET,         
            long_term_token = constant.PAGE_ACCESS_TOKEN
        )
        
        self.data = {}


    def testPostPhoto(self):

        self.api.post_ig_photo(
            ig_user_id = self.instagram_business_id,
            access_token = self.api._access_token,
            args = {
                "image_url": "https://i.ytimg.com/vi/cn8oF2kRMyY/hqdefault.jpg"
            }
        )

        with open("data/instagram/ig_photo.json", "r") as f:
            self.data = json.load(f)

        self.assertTrue("id" in self.data)


    def testPublishPhoto(self):

        with open("data/instagram/ig_photo.json", "r") as f:
            self.data = json.load(f)        

        self.api.post_publish_ig_photo(
            ig_user_id = self.instagram_business_id,
            access_token = self.api._access_token,
            args = {
                "creation_id": self.data["id"]
            }            
        )

        with open("data/instagram/ig_publish_photo.json", "r") as f:
            self.data = json.load(f)

        self.assertTrue("id" in self.data)       


if __name__ == "__main__":
    unittest.main()