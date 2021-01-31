import facebook

# It allows us to log in Facebook, using GraphAPI class
# and It creates an object that we can use later to
# use facebook allowed methods.
graph = facebook.GraphAPI(access_token="PAGE_ACCESS_TOKEN",
                          version="2.12")

# It gets the comments from post given by id.
data = graph.get_object(id="POST_ID", fields="comments")
