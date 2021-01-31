# This module contains all of the functions
# we will use in order to manage facebook with Crux.

from global_constants import graph


def put_like(object_id):

    # PRE: Recieves object_id which is the
    # post or comment id we need in
    # order to like the post.

    # POST: Calls the put_like method which
    # generates and send the request to Facebook
    # for liking the post or comment.

    graph.put_like(object_id=object_id)

    print("Post likeado con exito!")
