from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

import facebook_actions
import pyfacebook_actions
import data_management


def bot_creation():

    # POST: Creates the bot object right
    # after deletes all the previous storage.
    # Finally, returns the bot object.

    chatbot = ChatBot("Crux-prototype")
    chatbot.storage.drop()

    return chatbot


def bot_training(bot):

    # PRE: Receives the bot object.

    # POST: Uses it in order to create
    # the trainer object and allows us
    # to train our bot with a string list.

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


def bot_showing_posts():

    # POST: Utilizes modules such as
    # pyfacebook_actions and data_management
    # so that get data from Facebook and enable
    # us to print it out.

    pyfacebook_actions.processor()
    posts_info_list = data_management.posts_reader()
    data_management.posts_printing(posts_info_list)

    return posts_info_list


def bot_liking_posts():

    # POST: Shows all of the posts and then
    # allows the user to enter the one they
    # wanna put a like in. Calls module functions.

    # Shows the post in order to let the user choose.
    posts_info_list = bot_showing_posts()

    post_number = input("Ingrese el numero de la publicacion que quiere likear:\n")
    while not post_number.isdecimal():
        post_number = input("Ingrese el NUMERO de la publicacion que quiere likear:\n")

    post_id = data_management.posts_order(posts_info_list, post_number)
    facebook_actions.put_like(post_id)


def main():

    bot = bot_creation()
    bot_training(bot)

    finish = False
    while not finish:
        message = input("Di algo...\n")

        if message == "salir":
            finish = True
        else:
            response = bot.get_response(message)
            bot_name = bot.name
            response_date = (response.created_at.hour, response.created_at.minute)

            if "Juan" in response.text:
                print(f"({response_date[0]}:{response_date[1]}) {bot_name}: {response.text}")

                if "publicaciones" in response.text:
                    bot_showing_posts()

                elif "likear" in response.text:
                    bot_liking_posts()

            else:
                print(f"({response_date[0]}:{response_date[1]}) {bot_name}: {response.text}")


main()
