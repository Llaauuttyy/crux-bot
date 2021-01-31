# This module will allow us to control
# the given data from Facebook responses.

import json


def posts_reader():

    # POST: Loads the information into the json and returns it.

    # wto_posts.json would contain all the information needed.
    with open("prototype\\posts_data.json", "r") as posts:

        # json.load loads information and creates
        # a dictionary list, which is
        # trapped in posts_info_list.

        posts_info_list = json.load(posts)

        return posts_info_list


def posts_printing(posts_info_list):

    # PRE: Receives posts_info_list which is
    # a dictionary list (filled up).

    # POST: Goes through such list and print the requested data
    # from those dictionaries.

    for posts in range(len(posts_info_list)):

        for key in posts_info_list[posts]:

            if key == "message":
                print(f"Post {posts + 1}: {posts_info_list[posts]['message']}\n")

            # if key == "like":
            #     print(f"Likes: {posts_info_list[posts]['like']['summary']['total_count']}\n")

            elif key == "picture":
                print(f"Post {posts + 1}: This post is a photo.")


def posts_order(posts_info_list, post_number):

    # PRE: Recieves posts_info_list which is
    # a dictionary list filled up with data, and
    # post_number which is the posts the user wanna
    # interact with.

    # POST: Changes post_number to be an list's index.
    # Then seaches for the post id and returns it.

    post_index = int(post_number) - 1  # Beacuse we're using a list.
    print("Obteniendo datos...")
    post_id = posts_info_list[post_index]["id"]

    return post_id
