import unittest
import json
import sys
sys.path.append("ALTERNATIVE PATH")

import cruxbot.facebook_actions as fb


class ConversationMessagesTest(unittest.TestCase):

    def setUp(self):
        self.conversation_id = "t_3858840557530603"
        self.page_access_token = "PAGE_aCCESS_TOKEN"

        self.api = fb.ExtApi(long_term_token="long-term-token")

    def testConversationMessages(self):

        messages = self.api.get_conversation_messages(
            conversation_id=self.conversation_id,
            access_token=self.page_access_token,
            fields=["id", "message", "from", "to"],
            count=10,
            limit=100,
            return_json=True
        )

        data = []

        with open("data\\facebook\\fb_get_conversation_messages.json") as file:
            data = json.load(file)

        self.assertTrue("id" in data[0])
        self.assertTrue("message" in data[0])


if __name__ == "__main__":
    unittest.main()
