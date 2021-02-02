import unittest
import json
import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

import cruxbot.facebook_actions as fb
import cruxbot.utils.constant as constant


class ConversationMessagesTest(unittest.TestCase):

    def setUp(self):
        self.object_id = "102579945106245_117019143662325"
        self.page_access_token = constant.PAGE_ACCESS_TOKEN

        self.api = fb.ExtApi(long_term_token = "long-term-token")


    def testPutLike(self):

        self.api.put_like(
            object_id = self.object_id,
            access_token = self.page_access_token,
            return_json = True
        )

        data = []

        with open("data\\facebook\\fb_put_like.json") as file:
            data = json.load(file)

        self.assertTrue("success" in data)


if __name__ == "__main__":
    unittest.main()