import unittest
import json

import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

import cruxbot.instagram_actions as ig
import cruxbot.utils.constant as constant


class ApiPostTest(unittest.TestCase):

    def setUp(self):   
        self.ig_media_id = "17903913532690989"

        self.api = ig.ExtApi(
            app_id = constant.APP_ID,
            app_secret = constant.APP_SECRET,         
            long_term_token = constant.PAGE_ACCESS_TOKEN
        )

        self.data = {}


    def testEnablingComments(self):      

        self.api.post_enabling_comments(
            ig_media_id = self.ig_media_id,
            access_token = self.api._access_token,
            args = {
                "comment_enabled": "false"
            }            
        )

        with open("data/instagram/ig_enabling_comments.json", "r") as f:
            self.data = json.load(f)

        self.assertTrue(self.data["success"])       


if __name__ == "__main__":
    unittest.main()