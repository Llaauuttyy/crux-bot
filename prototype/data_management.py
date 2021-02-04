# This module will allow us to control
# the given data from Facebook responses.


import json
import time
import crux


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
                crux.chat_writer("Crux", "Post {post_number}: {post_message}".format(
                    post_number=posts + 1,
                    post_message=posts_info_list[posts]['message']
                ))

            # if key == "like":
            #     print(f"Likes: {posts_info_list[posts]['like']['summary']['total_count']}\n")

            elif key == "picture":
                print(f"Post {posts + 1}: This post is a photo.")
                crux.chat_writer("Crux", "Post {post_number}: {post_message}".format(
                    post_number=posts + 1,
                    post_message="This post is a photo."
                ))


def posts_order(posts_info_list, post_number):

    # PRE: Recieves posts_info_list which is
    # a dictionary list filled up with data, and
    # post_number which is the posts the user wanna
    # interact with.

    # POST: Changes post_number to be an list's index.
    # Then seaches for the post id and returns it.

    post_index = int(post_number) - 1  # Beacuse we're using a list.
    print("[Crux]: Obteniendo datos...")
    crux.chat_writer("Crux", "Obteniendo datos...")

    post_id = posts_info_list[post_index]["id"]

    return post_id


def localdate():
    date = time.asctime(time.localtime())

    return date


def localdate_chat():
    date_and_time = time.localtime()
    # dd/mm/yyyy
    date = "{day}/{month}/{year}".format(
        day=date_and_time[2],
        month=date_and_time[1],
        year=date_and_time[0]
    )

    local_time = time.asctime(date_and_time)
    # hh/mm/ss
    style_time = local_time[11:19:1]

    date_time_styled = "{date}, {time},".format(
        date=date,
        time=style_time
    )

    return date_time_styled
