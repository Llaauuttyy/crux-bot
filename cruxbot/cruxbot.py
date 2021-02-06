import time
import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from pyfacebook import Api

import cruxbot.facebook_actions as fb

#Cruxbot's app ID
APP_ID = "2522931991341291"

APP_SECRET = "9552895069b4d3c2950320c0f06354ff"

USER_ACCESS_TOKEN = ""

PAGE_ACCESS_TOKEN = "EAAj2lZBEi6OsBAKUmb5ZCgYiHrrJzTnfBmUwItETHsrAZC96gnNL0jdhBG31NpFhhZCHTLgmEdCJulQ6S491ZC3QjYiOh9UJjPAFrWFYCzDfZBEwLOEaH5oNwmllruC47SM7PlwycoDgKFLagXfTLHzmZBixziVTdmYX5nnNMqS4AZDZD"

#Cruxbot's user ID
USER_ID = "103684888301061"

#Cruxbot's page ID
PAGE_ID = "102579945106245"

#Instagram Business Account
INSTAGRAM_BUSINESS_ID = "17841444663784851"


#-----------------------------------------------------#
#------------ START DATA MANAGEMENT UTILS ------------#
#-----------------------------------------------------#

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
                chat_writer("Crux", "Post {post_number}: {post_message}".format(
                    post_number=posts + 1,
                    post_message=posts_info_list[posts]['message']
                ))

            # if key == "like":
            #     print(f"Likes: {posts_info_list[posts]['like']['summary']['total_count']}\n")

            elif key == "picture":
                print(f"Post {posts + 1}: This post is a photo.")
                chat_writer("Crux", "Post {post_number}: {post_message}".format(
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
    print("[Crux]: Obteniendo datos...")
    chat_writer("Crux", "Obteniendo datos...")

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

                # Time's been caught from Facebook servers (Different than ours).    

#-----------------------------------------------------#
#------------- END DATA MANAGEMENT UTILS -------------#
#-----------------------------------------------------#

#-----------------------------------------------------#
#------------------- START LOGGERS -------------------#
#-----------------------------------------------------#

def debug_writer(function_name):
    with open("logs\\debug.log", "a") as debug:
        date = localdate()
        debug.write(f"[{date}]: {function_name} function has been executed\n")


def errors_writer(single_error):
    with open("logs\\error.log", "a") as errors:
        date = localdate()
        errors.write(f"[{date}]: {single_error}\n")


def chat_writer(sender_name, message):
    with open("logs\\chat.log", "a") as chat:
        date_chat = localdate_chat()
        chat.write(f"{date_chat} {sender_name}, {message}\n")

#-----------------------------------------------------#
#-------------------- END LOGGERS --------------------#
#-----------------------------------------------------#        

#-----------------------------------------------------#
#---------------- START BOT FUNCTIONS ----------------#
#-----------------------------------------------------#

def bot_creation():

    # POST: Creates the bot object right
    # after deletes all the previous storage.
    # Finally, returns the bot object.
    try:
        chatbot = ChatBot("Crux")
        chatbot.storage.drop()

    except:
        errors_writer("bot_creation failed")
        raise Exception("Something went wrong while creating bot.")

    else:
        return chatbot


def bot_training(bot  # type: ChatBot
                ):

    # PRE: Receives the bot object.

    # POST: Uses it in order to create
    # the trainer object and allows us
    # to train our bot with a string list.

    try:
        trainer = ListTrainer(bot)

        trainer.train([
            "Hola, soy Juan",
            "Hola, bienvenido. Mi nombre es Crux",
            "Quiero ver mis publicaciones",
            "Perfecto, Juan. Aqui estan tus publicaciones:",
            "Quiero likear una publicacion",
            "Excelente, Juan. Vamos a likear la publicacion",
            "Quiero comentar la ultima publicacion",
            "Maravilloso, Juan. Aqui vamos"
        ])

    except:
        errors_writer("bot_training failed")
        raise Exception("Something went wrong while training bot")


def bot_greetings():
    greeting_message = "Bienvenido. Me llamo Crux. ¿Cuál es tu nombre? (Sólo escribe tu nombre)"
    with open("logs\\chat.log", "w") as chat:
        date_chat = localdate_chat()
        chat.write(f"{date_chat} Crux, {greeting_message}\n")

    user_name = input(f"[Crux]: {greeting_message}\n")
    chat_writer(user_name, user_name)

    return user_name


def bot_showing_posts(api  # type: Api
                      ):

    # POST: Utilizes modules such as
    # pyfacebook_actions and data_management
    # so that get data from Facebook and enable
    # us to print it out.

    posts_info_list = list()

    try:
        debug_writer("From pyfacebook_actions module, processor")

    except:
        print("Something went wrong with Facebook connection. Check your internet")
        with open("logs\\errors.log", "w") as errors:
            date = localdate()
            errors.write(f"[{date}]: From pyfacebook_actions module, processor failed\n")

    else:
        debug_writer("From data_management module, posts_reader")
        posts_info_list = fb.get_posts(
            api = api,
            page_id = PAGE_ID
        )
        debug_writer("From data_management module, posts_printing")
        posts_printing(posts_info_list)

        return posts_info_list

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
        chat_writer("Crux", bot_input_message)
        post_number = input(f"[Crux]: {bot_input_message}\n")
        chat_writer(user_name, post_number)

        while not post_number.isdecimal():
            chat_writer("Crux", bot_input_message)
            post_number = input(f"{bot_input_message}\n")
            chat_writer(user_name, post_number)

        post_id = posts_order(posts_info_list, post_number)

    try:
        fb.post_like(api, post_id)

    except:
        print("Try rebooting your connection")
        return False

    return True

#-----------------------------------------------------#
#----------------- END BOT FUNCTIONS -----------------#
#-----------------------------------------------------#

def main():
    api = Api(
        app_id = APP_ID,
        app_secret = APP_SECRET,
        long_term_token = PAGE_ACCESS_TOKEN,
    )


    date = localdate()
    with open("logs\\debug.log", "w") as debug:
        debug.write(f"[{date}]: The program has just started...\n\n")
        debug.write(f"[{date}]: bot_creation function has been executed\n")

    bot = bot_creation()

    debug_writer("bot_training")
    bot_training(bot)

    debug_writer("bot_greetings")
    user_name = bot_greetings()

    finish = False
    while not finish:
        motivation = "Di algo..."
        chat_writer("Crux", motivation)
        user_message = input(f"[Crux]: {motivation}\n")
        chat_writer(user_name, user_message)

        if user_message == "salir":
            finish = True
        else:
            response = bot.get_response(user_message)
            bot_name = bot.name
            response_date = (response.created_at.hour, response.created_at.minute)

            if "Juan" in response.text:
                print(f"[{bot_name}]: {response.text}")
                chat_writer("Crux", response.text)

                if "publicaciones" in response.text:
                    debug_writer("bot_showing_posts")
                    bot_showing_posts(api)

                elif "likear" in response.in_response_to:
                    debug_writer("bot_liking_posts")
                    liked = bot_liking_posts(api, user_name)

                    if liked is True:
                        success_message = "Post likeado con exito!"
                        print(f"[Crux]: {success_message}\n")
                        chat_writer("Crux", success_message)

            else:
                print(f"[{bot_name}]: {response.text}")
                chat_writer("Crux", response.text)


if __name__ == "__main__":
    main()