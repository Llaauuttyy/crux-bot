# This module contains all of the constants we need
# in order to send request to facebook.

import facebook

APP_ID = "2522931991341291"

APP_SECRET = ""

PAGE_ACCESS_TOKEN = ""

PAGE_ID = "102579945106245"

graph = facebook.GraphAPI(access_token=PAGE_ACCESS_TOKEN, version="2.12")
