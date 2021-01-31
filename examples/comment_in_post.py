import facebook

# It allows us to log in Facebook, using GraphAPI class
# and It creates an object that we can use later to
# use facebook allowed methods.
graph = facebook.GraphAPI(access_token="PAGE_ACCESS_TOKEN",
                          version="2.12")

# By passing object_id and message.
# It allows us to put a comment in a post.
graph.put_comment(object_id='post_id', message='comment')
