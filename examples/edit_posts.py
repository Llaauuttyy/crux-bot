import facebook

# It allows us to log in Facebook, using GraphAPI class
# and It creates an object that we can use later to
# use facebook allowed methods.
graph = facebook.GraphAPI(access_token="PAGE_ACCESS_TOKEN",
                          version="2.12")

# Allows us to edit a post by passing its post id
# Parameter connection_name gotta be empty in order to work.
# It can be used whether for posts or comments.
data = graph.put_object(parent_object="post_id", connection_name="", message="edit")
