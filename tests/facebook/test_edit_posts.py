import unittest
import json
import sys
sys.path.append("ALTERNATIVE PATH")

import examples.extended_api as extended_api


class ConversationMessagesTest(unittest.TestCase):

    def setUp(self):
        self.post_id = "102579945106245_117019143662325"
        self.page_access_token = "PAGE_ACCESS_TOKEN"

        self.api = extended_api.ExtApi(long_term_token="long-term-token")

    def testEditPosts(self):

        self.api.edit_posts(
            post_id=self.post_id,
            access_token=self.page_access_token,
            message="CHANGINNG TESTING POST",
            return_json=True
        )

        data = []

        with open("data\\facebook\\fb_edit_posts.json") as file:
            data = json.load(file)

        self.assertTrue("success" in data)


if __name__ == "__main__":
    unittest.main()
