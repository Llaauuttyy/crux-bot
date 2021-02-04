from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import facebook_actions
import pyfacebook_actions
import data_management


def debug_writer(function_name):
    with open("prototype\\log\\debug.log", "a") as debug:
        date = data_management.localdate()
        debug.write(f"[{date}]: {function_name} function has been executed\n")


def errors_writer(single_error):
    with open("prototype\\log\\erros.log", "a") as errors:
        date = data_management.localdate()
        errors.write(f"[{date}]: {single_error}\n")


def chat_writer(sender_name, message):
    with open("prototype\\log\\chat.log", "a") as chat:
        date_chat = data_management.localdate_chat()
        chat.write(f"{date_chat} {sender_name}, {message}\n")


def bot_creation():

    # POST: Creates the bot object right
    # after deletes all the previous storage.
    # Finally, returns the bot object.
    try:
        chatbot = ChatBot("Crux")
        chatbot.storage.drop()

    except:
        raise Exception("Something went wrong while creating bot.")
        errors_writer("bot_creation failed")

    else:
        return chatbot


def bot_training(bot):

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
        raise Exception("Something went wrong while training bot")
        errors_writer("bot_training failed")


def bot_greetings():
    greeting_message = "Bienvenido. Me llamo Crux. ¿Cuál es tu nombre? (Sólo escribe tu nombre)"
    with open("prototype\\log\\chat.log", "w") as chat:
        date_chat = data_management.localdate_chat()
        chat.write(f"{date_chat} Crux, {greeting_message}\n")

    user_name = input(f"[Crux]: {greeting_message}\n")
    chat_writer(user_name, user_name)

    return user_name


def bot_showing_posts():

    # POST: Utilizes modules such as
    # pyfacebook_actions and data_management
    # so that get data from Facebook and enable
    # us to print it out.

    posts_info_list = list()

    try:
        debug_writer("From pyfacebook_actions module, processor")
        pyfacebook_actions.processor()

    except:
        print("Something went wrong with Facebook connection. Check your internet")
        with open("prototype\\log\\errors.log", "w") as errors:
            date = data_management.localdate()
            errors.write(f"[{date}]: From pyfacebook_actions module, processor failed\n")

    else:
        debug_writer("From data_management module, posts_reader")
        posts_info_list = data_management.posts_reader()
        debug_writer("From data_management module, posts_printing")
        data_management.posts_printing(posts_info_list)

        return posts_info_list

    return posts_info_list


def bot_liking_posts(user_name):

    # POST: Shows all of the posts and then
    # allows the user to enter the one they
    # wanna put a like in. Calls module functions.

    # Shows the post in order to let the user choose.

    posts_info_list = bot_showing_posts()
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

        post_id = data_management.posts_order(posts_info_list, post_number)

    try:
        facebook_actions.put_like(post_id)

    except:
        print("Try rebooting your connection")
        return False

    return True


def main():
    date = data_management.localdate()
    with open("prototype\\log\\debug.log", "w") as debug:
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
                    bot_showing_posts()

                elif "likear" in response.in_response_to:
                    debug_writer("bot_liking_posts")
                    liked = bot_liking_posts(user_name)

                    if liked is True:
                        success_message = "Post likeado con exito!"
                        print(f"[Crux]: {success_message}\n")
                        chat_writer("Crux", success_message)

            else:
                print(f"[{bot_name}]: {response.text}")
                chat_writer("Crux", response.text)


main()
