import unittest
import json
import sys
sys.path.append("ALTERNATIVE PATH")

import examples.extended_api as extended_api


class ConversationMessagesTest(unittest.TestCase):

    def setUp(self):
        self.post_id = "102579945106245_116774450353461"
        self.page_access_token = "PAGE_ACCESS_TOKEN"

        self.api = extended_api.ExtApi(long_term_token="long-term-token")

    def testPostComment(self):

        self.api.post_comment(
            post_id=self.post_id,
            access_token=self.page_access_token,
            message="Looking good, son",
            return_json=True
        )

        data = []

        with open("data\\facebook\\fb_post_comment.json") as file:
            data = json.load(file)

        self.assertTrue("id" in data)


if __name__ == "__main__":
    unittest.main()
