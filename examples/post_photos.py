import facebook

# It allows us to log in Facebook, using GraphAPI class
# and It creates an object that we can use later to
# use facebook allowed methods.
graph = facebook.GraphAPI(access_token="PAGE_ACCESS_TOKEN",
                          version="2.12")

# It posts a photo in an album which is /me/photos.
graph.put_photo(image=open("IMG.jpg", 'rb'),
                album_path="/me/photos" + "/picture")

# It posts a photo in the feed with a message.
graph.put_photo(image=open('IMG.jpg', 'rb'),
                message='message')
