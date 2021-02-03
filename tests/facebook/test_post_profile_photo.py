import unittest
import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

import cruxbot.facebook_actions as fb
import cruxbot.utils.constant as constant


class ConversationMessagesTest(unittest.TestCase):

    def setUp(self):
        self.page_id = constant.PAGE_ID
        self.page_access_token = constant.PAGE_ACCESS_TOKEN

        self.api = fb.ExtApi(long_term_token = "long-term-token")


    def testPostProfilePhoto(self):

        exception_error = self.api.post_profile_photo(
            page_id = self.page_id,
            access_token = self.page_access_token,
            files = open("images.jpg", 'rb'),
            return_json = True
        )
        # Expected error, code=100
        self.assertIs(100, exception_error.code, msg = "FAILED")


if __name__ == "__main__":
    unittest.main()