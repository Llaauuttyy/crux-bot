import json

# This module will allow the user sees which posts
# they want to comment in, like, edit, etc. 

def posts_reader():

    # POST: Loads the information into the json and returns it.

    # wto_posts.json would contain all the information needed.
    with open("wto_posts.json", "r") as posts:

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
                print(f"Post: {posts_info_list[posts]['message']}")

            if key == "like":
                print(f"Likes: {posts_info_list[posts]['like']['summary']['total_count']}\n")

            elif key == "picture":
                print("This post is a photo.")


def main():
    posts_printing(posts_reader())


main()
