import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

import facebook_actions as fb
import instagram_actions as ig
from loggers import chat_logger

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pyfacebook import Api, IgProApi


# Cruxbot's app ID
APP_ID = "2522931991341291"

APP_SECRET = "9552895069b4d3c2950320c0f06354ff"

USER_ACCESS_TOKEN = ""

PAGE_ACCESS_TOKEN = "EAAj2lZBEi6OsBAKUmb5ZCgYiHrrJzTnfBmUwItETHsrAZC96gnNL0jdhBG31NpFhhZCHTLgmEdCJulQ6S491ZC3QjYiOh9UJjPAFrWFYCzDfZBEwLOEaH5oNwmllruC47SM7PlwycoDgKFLagXfTLHzmZBixziVTdmYX5nnNMqS4AZDZD"

# Cruxbot's user ID
USER_ID = "103684888301061"

# Cruxbot's page ID
PAGE_ID = "102579945106245"

# Instagram Business Account
INSTAGRAM_BUSINESS_ID = "17841444663784851"


# ------------------------------------------------------ #
# ------------ DATA MANAGEMENT UTILS STARTS ------------ #
# ------------------------------------------------------ #


def posts_printing(posts_info_list  # type: dict
                   ):

    # PRE: Receives posts_info_list which is
    # a dictionary list (filled up).

    # POST: Goes through such list and print the requested data
    # from those dictionaries.

    for posts in range(len(posts_info_list)):

        for key in posts_info_list[posts]:

            if key == "message":
                print(f"Post {posts + 1}: {posts_info_list[posts]['message']}\n")
                chat_logger.info("Crux, Post {post_number}: {post_message}".format(
                    post_number=posts + 1,
                    post_message=posts_info_list[posts]['message']
                ))

            # if key == "like":
            #     print(f"Likes: {posts_info_list[posts]['like']['summary']['total_count']}\n")

            elif key == "picture":
                print(f"Post {posts + 1}: This post is a photo.")
                chat_logger.info("Crux, Post {post_number}: {post_message}".format(
                    post_number=posts + 1,
                    post_message="This post is a photo."
                ))


def posts_order(posts_info_list,  # type: dict
                post_number  # type: str
                ):

    # PRE: Recieves posts_info_list which is
    # a dictionary list filled up with data, and
    # post_number which is the posts the user wanna
    # interact with.

    # POST: Changes post_number to be an list's index.
    # Then seaches for the post id and returns it.

    post_index = int(post_number) - 1  # Beacuse we're using a list.



    post_id = posts_info_list[post_index]["id"]

    return post_id


def date_transforming(posts_info_list):

    # PRE: Receives posts_info_list which is
    # a dictionary list filled up with posts data.

    # POST: Seaches the date and time and transforms them
    # in order to print them right after.

    for post in range(len(posts_info_list)):

        for key in posts_info_list[post]:

            if key == "updated_time":
                date_and_time = posts_info_list[post]["created_time"]
                used_date, complete_hour = date_and_time.split("T")
                splitted_hour = complete_hour.split("+")
                used_time = splitted_hour[0]
                print(f"Date: {used_date}. Time: {used_time}.")

                # Time's been caught from Facebook servers (Different than ours)


# ------------------------------------------------------ #
# ------------- DATA MANAGEMENT UTILS ENDS ------------- #
# ------------------------------------------------------ #

# ------------------------------------------------------ #
# ---------------- BOT FUNCTIONS STARTS ---------------- #
# ------------------------------------------------------ #


def bot_creation():

    # POST: Creates the bot object right
    # after deletes all the previous storage.
    # Finally, returns the bot object.
    chatbot = ChatBot("Crux")

    return chatbot


def bot_training(bot  # type: ChatBot
                 ):

    # PRE: Receives the bot object.

    # POST: Uses it in order to create
    # the trainer object and allows us
    # to train our bot with a string list.
    datos = []
    bot.storage.drop()
    trainer = ListTrainer(bot)

    with open("data/entrenador.txt", "r", encoding = "utf-8") as f:
        datos = f.read().splitlines()

    trainer.train(datos)


def bot_greetings(bot  # type: ChatBot
                 ):

    response = bot.get_response("msgwme")

    username = input(f"[{bot.name}]: {response}\n")

    return username


def bot_showing_posts(api  # type: Api
                      ):

    # POST: Utilizes modules such as
    # pyfacebook_actions and data_management
    # so that get data from Facebook and enable
    # us to print it out.

    posts_info_list = list()


    posts_info_list = fb.get_posts(
        api=api,
        page_id=PAGE_ID
    )

    posts_printing(posts_info_list)

    return posts_info_list


def bot_liking_posts(api,  # type: Api
                     user_name  # type: str
                     ):

    # POST: Shows all of the posts and then
    # allows the user to enter the one they
    # wanna put a like in. Calls module functions.

    # Shows the post in order to let the user choose.

    posts_info_list = bot_showing_posts(api)
    if posts_info_list == []:
        print("Try rebooting your connection")

    else:
        bot_input_message = "Ingrese el numero de la publicacion que quiere likear:"

        post_number = input(f"[Crux]: {bot_input_message}\n")


        while not post_number.isdecimal():

            post_number = input(f"[Crux]: {bot_input_message}\n")


        post_id = posts_order(posts_info_list, post_number)

        fb.post_like(api, post_id)
        

    return True


def search_user_by_bot(api,  # type: IgProApi
                       username  # type: str
                       ):                        

    data = ig.get_ig_user_info(
        api = api,
        username = username
    )


# ------------------------------------------------------ #
# ----------------- BOT FUNCTIONS ENDS ----------------- #
# ------------------------------------------------------ #


def set_up_username(username # type: str
                    ):

    # Read in the file
    with open("data/entrenador.txt", "r", encoding = "utf-8") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("{nombre}", username)

    # Write the file out again
    with open('data/entrenador.txt', 'w', encoding = "utf-8") as file:
        file.write(filedata)


def main():
    response = ""
    request = ""

    api = Api(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        long_term_token=PAGE_ACCESS_TOKEN,
    )

    bot = bot_creation()

    bot_training(bot)

    username = bot_greetings(bot)

    set_up_username(username)

    bot_training(bot)

    response = bot.get_response("Descripcion")
    request = input(f"[{bot.name}]: {response}\n")

    while request not in ["Salir", "salir", "Exit", "exit"]:

        if "bienvenida" in request:
            response = bot.get_response(request)
            print(f"[{bot.name}]: {response}\n")            

        if "opciones" in request:
            response = bot.get_response(request)
            request = input(f"[{bot.name}]: {response}\n")

            if request in ["Facebook", "facebook", "fb"]:
                for x in range(7):
                    response = bot.get_response(f"fbopt{x}")
                    print(f"[{bot.name}]: {response}")

                request = input("\nEscribe la opción: ")

            elif request in ["Instagram", "instagram", "ig"]:
                for x in range(5):
                    response = bot.get_response(f"igopt{x}")
                    print(f"[{bot.name}]: {response}")

                request = input("\nEscribe la opción: ")

            else:
                print("Ingresó una opción no valida")

        response = bot.get_response("Continuar")
        request = input(f"[{bot.name}]: {response}\n")        

    else:
        response = bot.get_response(request)
        print(f"[{bot.name}]: {response}\n")


if __name__ == "__main__":
    main()