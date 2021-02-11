import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

import facebook_actions as fb
import instagram_actions as ig
from loggers import chat_logger

from datetime import datetime, timedelta
from copy import deepcopy
from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response
from chatterbot.trainers import ListTrainer
from pyfacebook import Api, IgProApi
from facebook import GraphAPI


# Cruxbot's app ID
APP_ID = "2522931991341291"

APP_SECRET = "9552895069b4d3c2950320c0f06354ff"

USER_ACCESS_TOKEN = ""

PAGE_ACCESS_TOKEN = "EAAj2lZBEi6OsBAKUmb5ZCgYiHrrJzTnfBmUwItETHsrAZC96gnNL0jdhBG31NpFhhZCHTLgmEdCJulQ6S491ZC3QjYiOh9UJjPAFrWFYCzDfZBEwLOEaH5oNwmllruC47SM7PlwycoDgKFLagXfTLHzmZBixziVTdmYX5nnNMqS4AZDZD"

# Cruxbot's user ID
USER_ID = "103684888301061"

# Cruxbot's page ID
PAGE_ID = "102579945106245"

IG_USERNAME = "crux_project"

# Instagram Business Account
INSTAGRAM_BUSINESS_ID = "17841444663784851"

OPTIONS_FOR_EXIT = ["salir", "exit", "quit", "esc"]

OPTIONS_FOR_FACEBOOK = ["facebook", "fb"]

OPTIONS_FOR_INSTAGRAM = ["instagram", "ig"]

KEYWORDS = [
    "opciones", "likear", "publicaciones", 
    "postear", "foto", "actualizar",
    "listar", "amigos", "perfil", 
    "buscar", "seguidores", "habilitar"
]


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


def format_date(str_datetime  # type: str
                ):

    datetime_fixed = ""

    datetime_formatted = (
        datetime.strptime(str_datetime, "%Y-%m-%dT%H:%M:%S+%f") + 
        timedelta(hours=-3)
    )

    datetime_fixed = datetime_formatted.strftime("%d/%m/%Y %H:%M:%S")

    return datetime_fixed


def format_key(key  # type: str
               ):

    key_formatted = ""

    key_formatted = key.capitalize().replace("_", " ")

    return key_formatted


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
    chatbot = ChatBot(
        "Crux",
        response_selection_method = get_random_response
    )

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

    username = request_input(bot, "msgwme")

    while username.isdecimal():
        username = request_input(bot, "msgnameisnum")

    username = username.lower().capitalize()

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


def search_user_by_bot(bot,  # type: ChatBot
                       api,  # type: IgProApi
                       username  # type: str
                       ):                        

    data_list = []

    data = ig.get_ig_user_info(
        api = api,
        username = username
    )

    if "error" in data:
        data_list.append(data)
    else:
        data_list.append(
            filter_data(data, search_user_by_bot.__name__)
        )

    print_data(bot, data_list, search_user_by_bot.__name__)


def get_medias_by_bot(bot,  # type: ChatBot
                      api,  # type: IgProApi
                      username  # type: str
                      ):                     

    data_list = []

    data = ig.get_ig_user_medias(
        api = api,
        username = username
    )

    if "error" in data:
        data_list.append(data)
    else:
        for x in range(len(data)):
            data_list.append(
                filter_data(data[x], get_medias_by_bot.__name__)
            )

    print_data(bot, deepcopy(data_list), get_medias_by_bot.__name__)

    return data_list


def post_ig_photo_by_bot(bot,  # type: ChatBot
                         api,  # type: GraphAPI
                         image_url  # type: str
                         ):
    
    data_list = []

    data = ig.post_ig_photo(
        api = api,
        instagram_business_id = INSTAGRAM_BUSINESS_ID,
        image_url = image_url
    )

    if "error" in data:
        data_list.append(data)
    else:
        data_list.append(
            filter_data(data, post_ig_photo_by_bot.__name__)
        )

    print_data(bot, data_list, post_ig_photo_by_bot.__name__)


def update_media_by_bot(bot,  # type: ChatBot
                        api,  # type: IgProApi
                        media_id,  # type: str
                        comment_enabled  # type: bool
                        ):
    
    data_list = []

    data = ig.put_ig_media(
        api = api,
        media_id = media_id,
        comment_enabled = comment_enabled
    )

    if "error" in data:
        data_list.append(data)
    else:
        data_list.append(filter_data(data, update_media_by_bot.__name__))

    print_data(bot, data_list, update_media_by_bot.__name__)


def get_followers_by_bot(bot,  # type: ChatBot
                         api,  # type: IgProApi
                         username  # type: str
                         ):                        

    data_list = []

    data = ig.get_ig_user_info(
        api = api,
        username = username
    )

    if "error" in data:
        data_list.append(data)
    else:
        data_list.append(
            filter_data(data, get_followers_by_bot.__name__)
        )

    print_data(bot, data_list, get_followers_by_bot.__name__)    


def filter_data(data,  # type: dict
                function_name  # type: str
                ):

    parsed_data = {}

    if function_name == search_user_by_bot.__name__:

        parsed_data = {
            "usuario": data.get("username", IG_USERNAME),
            "biografia": data.get("biography", "Proyecto para facultad"),
            "nombre": data.get("name", "Crux Friend"),
            "cantidad_de_publicaciones": data.get("media_count", 0),
            "cantidad_de_seguidos": data.get("follows_count", 0)
        }

    elif function_name == get_medias_by_bot.__name__:

        parsed_data = {
            "id": data.get("id", 0),
            "cantidad_de_comentarios": data.get("comments_count", 0),
            "usuario": data.get("username", "crux_project"),
            "fecha_y_hora_de_publicacion": data.get(
                "timestamp", 
                (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M:%S+%f")
            ),
            "cantidad_de_likes": data.get("like_count", 0),
            "link": data.get("permalink", "https://www.instagram.com/crux_project")
        }

    elif function_name == get_followers_by_bot.__name__:

        parsed_data = { "cantidad_de_seguidores": data.get("followers_count", 0) }        

    else:
        parsed_data = deepcopy(data)
    
    return parsed_data


def print_data(bot,  # type: ChatBot
               data,  # type: list[dict]
               function_name  # type: str
               ):

    key_error = "error"

    if (function_name == search_user_by_bot.__name__ or 
        function_name == get_followers_by_bot.__name__):

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")

            else:
                for key in data[x]:
                    print(f"[{bot.name}]: {format_key(key)}  :  {data[x].get(key)}")

    elif function_name == get_medias_by_bot.__name__:

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")

            else:
                del data[x]["id"]
                data[x]["fecha_y_hora_de_publicacion"] = format_date(data[x].get("fecha_y_hora_de_publicacion"))

                print(f"\n[{bot.name}]: {x + 1}° - publicación")

                for key in data[x]:
                    print(f"[{bot.name}]: {format_key(key)}  :  {data[x].get(key)}")                       

    elif function_name == post_ig_photo_by_bot.__name__:

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")

            else:
                print_response(bot, "msgpostedphoto")

    elif function_name == update_media_by_bot.__name__:

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")
            else:
                if(data[x].get("success")):
                    print_response(bot, "msgcommenabledsucc")
                else:
                    print_response(bot, "msgcommenablednotsucc")


# ------------------------------------------------------ #
# ----------------- BOT FUNCTIONS ENDS ----------------- #
# ------------------------------------------------------ #


def set_up_username(username  # type: str
                    ):

    filedata = []

    # Read in the file
    with open("data/entrenador.txt", "r", encoding = "utf-8") as file:
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("{nombre}", username)

    # Write the file out again
    with open('data/entrenador.txt', 'w', encoding = "utf-8") as file:
        file.write(filedata)


def request_input(bot,  # type: ChatBot
                  statement  # type: str
                  ):

    response = bot.get_response(statement)
    request = input(f"\n[{bot.name}]: {response}\n")

    return request.lower()


def print_response(bot,  # type: ChatBot
                   statement  # type: str
                   ):

    request = ""

    response = bot.get_response(statement)

    while response.confidence < 0.8:
        request = request_input(bot, "msgforconfidence")

        response = bot.get_response(request)

    print(f"[{bot.name}]: {response}\n")


def are_keywords_in_text(text,  # type: str
                         keywords  # type: list
                         ):

    flag_is_in = False

    for x in range(len(keywords)):
        if keywords[x] in text:
            flag_is_in = True

    return flag_is_in


def main():
    response = ""
    request = ""
    username = ""
    image_url = ""
    posts_list = []
    post_id = 0

    flag_is_valid = False
    comment_enabled = False

    api = Api(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        long_term_token=PAGE_ACCESS_TOKEN,
    )

    igproapi = IgProApi(
        app_id = APP_ID,
        app_secret = APP_SECRET,
        long_term_token = PAGE_ACCESS_TOKEN,
        instagram_business_id = INSTAGRAM_BUSINESS_ID
    )

    graphapi = GraphAPI(
        access_token = PAGE_ACCESS_TOKEN
    )    

    bot = bot_creation()

    bot_training(bot)

    username = bot_greetings(bot)

    set_up_username(username)

    bot_training(bot)

    request = request_input(bot, "descripcion")

    while request not in OPTIONS_FOR_EXIT:

        if "bienvenida" in request:
            print_response(bot, request)

            request = request_input(bot, "continuar")

        elif "opciones" in request:
            request = request_input(bot, request)

            flag_is_valid = False

            while not flag_is_valid:

                if request in OPTIONS_FOR_FACEBOOK:
                    for x in range(7):
                        response = bot.get_response(f"fbopt{x}")
                        print(f"[{bot.name}]: {response}")

                    request = request_input(bot, "msgreqopt")
                    response = bot.get_response(request)

                    while (response.confidence < 0.8 or not are_keywords_in_text(response.text.lower(), KEYWORDS) or 
                           "habilitar" in response.text.lower()):

                        request = request_input(bot, "msgforconfidence")
                        response = bot.get_response(request)

                    print(f"[{bot.name}]: {response}\n")    

                    if "likear" in request and "likear" in response.text.lower():
                        #Llamar a función correspondiente para likear
                        print()

                    elif "publicaciones" in request and "publicaciones" in response.text.lower():
                        #Llamar a función correspondiente para ver publicaciones
                        print()

                    elif "postear" in request and "postear" in response.text.lower():
                        #Llamar a función correspondiente para postear una publicación
                        print()

                    elif "foto" in request and "foto" in response.text.lower():
                        #Llamar a función correspondiente para postear una foto
                        print() 

                    elif "actualizar" in request and "actualizar" in response.text.lower():
                        #Llamar a función correspondiente para actualizar una publicación
                        print()

                    elif "amigos" in request and "amigos" in response.text.lower():
                        #Llamar a función correspondiente para listar los amigos
                        print()

                    elif "perfil" in request and "perfil" in response.text.lower():
                        #Llamar a función correspondiente para actualizar la foto de perfil
                        print()

                    flag_is_valid = True

                elif request in OPTIONS_FOR_INSTAGRAM:
                    for x in range(5):
                        response = bot.get_response(f"igopt{x}")
                        print(f"[{bot.name}]: {response}")

                    request = request_input(bot, "msgreqopt")
                    response = bot.get_response(request)

                    while response.confidence < 0.8 or not are_keywords_in_text(response.text.lower(), KEYWORDS):
                        request = request_input(bot, "msgforconfidence")
                        response = bot.get_response(request)

                    print(f"[{bot.name}]: {response}\n")

                    if "buscar" in request and "buscar" in response.text.lower():
                        username = request_input(bot, "msgrequsername")

                        search_user_by_bot(bot, igproapi, username)

                    elif "publicaciones" in request and "publicaciones" in response.text.lower():
                        username = IG_USERNAME

                        print_response(bot, "msgreqposts")
                        get_medias_by_bot(bot, igproapi, username)

                    elif "foto" in request and "foto" in response.text.lower():
                        # Se debe armar función para validar que se ingrese una URL válida
                        # y que la misma no sea https
                        image_url = request_input(bot, "msgrequrlphoto")
                        post_ig_photo_by_bot(bot, graphapi, image_url)

                    elif "actualizar" in request and "habilitar" in response.text.lower():
                        username = IG_USERNAME

                        posts_list = get_medias_by_bot(bot, igproapi, username)
                        # Se debe armar función para validar el ingreso solamente de números
                        # y que el mismo esté dentro de un rango
                        request = request_input(bot, "msqreqidpostid")

                        post_id = int(request) - 1

                        # Se debe armar función para validar que haya ingresado variantes de
                        # 'habilitar' y 'deshabilitar', y en todo caso armar un while hasta
                        # que ingrese una opción válida. 'habilitar' = True, 'deshabilitar' = False
                        request = request_input(bot, "msgreqcommentenabled")

                        if(request == "habilitar"):
                            comment_enabled = True
                        elif(request == "deshabilitar"):
                            comment_enabled = False

                        update_media_by_bot(bot, igproapi, posts_list[post_id].get("id"), comment_enabled)

                    elif "seguidores" in request and "seguidores" in response.text.lower():
                        username = IG_USERNAME

                        print_response(bot, "msgfollowersok")
                        get_followers_by_bot(bot, igproapi, username)                        

                    flag_is_valid = True

                else:
                    request = request_input(bot, "msgnotfborig")

            request = request_input(bot, "continuar")

        else:
            request = request_input(bot, "msgnotvalidopt")

    else:
        print_response(bot, request)


if __name__ == "__main__":
    main()