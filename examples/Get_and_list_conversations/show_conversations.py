from extended_api import ExtApi


def show_conversations(conversation):

    # PRE: Recieves conversation parameter
    # which is a dict list (full).

    # POST: Goes through the dict list and
    # shows every message after the name sender.

    for data in reversed(conversation):
        message = data["message"]
        sender = data["from"]["name"]
        print(f"{sender}: {message}")

    print("\n")


def get_every_chat(conversations, api):

    # PRE: Recieves conversations parameter which is a
    # dict list (full) containing every single chat, also
    # revieces api parameter which is an object created at main.

    # POST: Goes through conversations and gets every id from them,
    # uses get_conversation_messages and then calls show_conversations.

    for conversation in range(len(conversations)):

        for info in conversations[conversation]:

            if info == "id":
                conversation_id = conversations[conversation]["id"]

                messages_info = api.get_conversation_messages(
                    conversation_id=conversation_id,
                    access_token="ACCESS_TOKEN",
                    fields=["message", "from", "to", "created_time"], count=100, limit=200, return_json=True
                )

                show_conversations(messages_info)


def main():
    api = ExtApi(long_term_token="long-term-token")

    conversations = api.get_page_conversations(
        page_id="102579945106245",
        access_token="ACCESS_TOKEN",
        fields=None, folder="inbox", count=10, limit=20, return_json=True
    )

    get_every_chat(conversations, api)


main()
