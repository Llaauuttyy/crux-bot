# This module contains all of the allowed actions
# for pyfacebook API in order to request Facebook responses

import json

from pyfacebook import Api

from global_constants import APP_ID, APP_SECRET, PAGE_ACCESS_TOKEN, PAGE_ID


def get_posts(page_username):
    # An Api object is created for the connection, from the constructor,
    # to which the constants previously defined are passed through parameters.
    api = Api(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        long_term_token=PAGE_ACCESS_TOKEN,
    )

    # A method of the Api object is called, which returns us the posts made
    # by the user, on his wall. There are some filters that can be passed by parameter,
    # to manipulate what information you want to obtain.
    data = api.get_page_posts(
        page_id=page_username,
        since_time="2020-05-01",
        count=None,
        limit=100,
        return_json=True
    )

    return data


def processor():
    # In this field, the user id must be set. It is obtained from the normal
    # Facebook account in "Configuration / Commercial integrations", and in the
    # application that was created, click on "View and edit".
    # It can also be obtained from Facebook for Developers, by making a query
    # from the "Graph API Explorer"

    page_username = PAGE_ID
    data = get_posts(page_username)

    with open("prototype\\posts_data.json", 'w') as f:
        json.dump(data, f)
