import os
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
    "buscar", "seguidores", "habilitar",
    "conversaciones", "chats", "comentar"
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


def posts_or_convo_order(object_info_list,  # type: dict
                         object_number  # type: str
                         ):

    # PRE: Recieves posts_info_list which is
    # a dictionary list filled up with data, and
    # object_number which is the posts the user wanna
    # interact with.

    # POST: Changes object_number to be an list's index.
    # Then seaches for the post id and returns it.

    object_index = int(object_number) - 1  # Beacuse we're using a list.

    object_id = object_info_list[object_index]["id"]

    return object_id


def convers_snippet_printing(convers_info_list):

    for snippet in range(len(convers_info_list)):

        print(
            '''
            Follower: {follower}
            Last message: {last_message}
            Conversation: {snippet}
            '''.format(
                follower=convers_info_list[snippet]["participants"]["data"][0]["name"],
                last_message=convers_info_list[snippet]["snippet"],
                snippet=snippet + 1
            )
        )


def convers_messages_printing(message_info_list):

    for message in range(len(message_info_list)):
        print(
            '''
            Sender: {sender}
            Message: {message}
            '''.format(
                sender=message_info_list[message]["from"]["name"],
                message=message_info_list[message]["message"]
            )
        )


def printing_friend_list(bot, data):

    print_response(bot, "fbopt5msg5")

    for friend in data["data"]:
        print("Nombre: {name}\n".format(
                name=friend["name"]
            )
        )

    print("Total de amigos: {friends}".format(
            friends=data["summary"]["total_count"]
        )
    )


def fb_error_checking(data):

    if "error" in data:
        print("Un error ha ocurrido: {error}".format(
            error=data["error"]
            )
        )

        return True

    else:
        return False


def fb_error_checking_profile_photo(data):

    if data["error"].result["error"]["code"] == 100:
        return False

    else:
        print("Ha ocurrido un error inesperado.")
        return True



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


def bot_showing_posts(api,  # type: Api
                      bot
                      ):

    # POST: Utilizes modules such as
    # pyfacebook_actions and data_management
    # so that get data from Facebook and enable
    # us to print it out.

    print_response(bot, "fbopt1msg0")

    posts_info_list = fb.get_posts(
        api=api,
        page_id=PAGE_ID
    )

    if not fb_error_checking(posts_info_list):
        posts_printing(posts_info_list)

        return posts_info_list

    else:
        posts_info_list = list()

        return posts_info_list


def bot_showing_conversations(api, bot):

    print_response(bot, "fbopt7msg0")
    # calls conversations
    convers_info_list = fb.get_page_conversations(
        api=api,
        page_id=PAGE_ID
    )

    # looks for errors
    if not fb_error_checking(convers_info_list):
        # if there's not, print conversations
        convers_snippet_printing(convers_info_list)
        # lets the user choose and print all
        # of the mssages from that convo.
        return convers_info_list

    else:
        posts_info_list = list()

        return posts_info_list


def bot_object_chooser(api,
                       bot,
                       type_object  # type: str
                                    # Values: convo, posts_fb, posts_ig
                       ):

    if type_object == "posts":
        object_info_list = bot_showing_posts(api, bot)

    else:
        object_info_list = bot_showing_conversations(api, bot)

    if object_info_list == []:
        print("Try rebooting your connection")

    else:
        object_number = request_input(bot, "fbchr0")

        while not object_number.isdecimal() or int(object_number) > len(object_info_list) or int(object_number) < 1:

            object_number = request_input(bot, "fbchr5")

        object_id = posts_or_convo_order(object_info_list, object_number)

        return object_id

    
def bot_showing_convers_msg(api, bot):

    convo_id = bot_object_chooser(api, bot, "convo")

    messages_info_list = fb.get_conversation_messages(
        api=api,
        conversation_id=convo_id
    )

    if not fb_error_checking(messages_info_list):
        convers_messages_printing(messages_info_list)


def bot_liking_posts(api,  # type: Api
                     bot
                     ):

    # POST: Shows all of the posts and then
    # allows the user to enter the one they
    # wanna put a like in. Calls module functions.

    # Shows the post in order to let the user choose.

    post_id = bot_object_chooser(api, bot, "posts")

    data = fb.post_like(api, post_id)

    if not fb_error_checking(data):
        print_response(bot, "fbopt0msg0")


def bot_post_publication(api,
                         bot
                         ):

    post_message = request_input(bot, "fbopt2msg0")

    data = fb.post_publication(
        api,
        page_id=PAGE_ID,
        message=post_message
    )

    # fbopt2msg5

    if not fb_error_checking(data):

        print_response(bot, "fbopt2msg10")


def bot_put_publication(api,
                        bot
                        ):

    post_id = bot_object_chooser(api, bot, "posts")

    user_edit = request_input(bot, "fbopt4msg10")
    data = fb.put_publication(api, post_id, user_edit)

    if not fb_error_checking(data):
        print_response(bot, "fbopt4msg15")


def bot_commenting_posts(api, bot):

    post_id = bot_object_chooser(api, bot, "posts")

    comment_message = request_input(bot, "fbopt2msg0")

    data = fb.post_comment(
        api=api,
        post_id=post_id,
        message=comment_message
    )

    if not fb_error_checking(data):

        print_response(bot, "fbopt2msg15")


def bot_checking_photo_in_path(bot):

    try:
        os.mkdir("images")

    except FileExistsError:
        user_ready = request_input(bot, "fbopt3msg1")

    else:
        user_ready = request_input(bot, "fbopt3msg0")

    photo_is_ready = False

    while not photo_is_ready:
        try:
            photo = open("images//image.jpeg", "rb")

            photo_is_ready = True

        except FileNotFoundError:
            user_ready = request_input(bot, "fbopt3msg5")

    return photo


def bot_uploading_feed_photo(graphapi, bot):
    photo = bot_checking_photo_in_path(bot)

    data = fb.post_photo(
        api=graphapi,
        page_id=PAGE_ID,
        image=photo
    )

    if not fb_error_checking(data):
        print_response(bot, "fbopt3msg20")


def bot_uploading_profile_photo(graphapi, bot):
    photo = bot_checking_photo_in_path(bot)

    data = fb.post_profile_photo(
        api=graphapi,
        page_id=PAGE_ID,
        image=photo
    )

    if not fb_error_checking_profile_photo(data):
        print_response(bot, "fbopt6msg0")


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
                    for x in range(9):
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
                        bot_liking_posts(api, bot)

                    elif "publicaciones" in request and "publicaciones" in response.text.lower():
                        bot_showing_posts(api, bot)

                    elif "postear" in request and "postear" in response.text.lower():
                        bot_post_publication(api, bot)
                        print()

                    elif "foto" in request and "foto" in response.text.lower():
                        bot_uploading_feed_photo(graphapi, bot)
                        print() 

                    elif "actualizar" in request and "actualizar" in response.text.lower():
                        bot_put_publication(api, bot)
                        print()

                    elif "amigos" in request and "amigos" in response.text.lower():
                        #Llamar a función correspondiente para listar los amigos
                        print()

                    elif "perfil" in request and "perfil" in response.text.lower():
                        bot_uploading_profile_photo(graphapi, bot)
                        print()

                    elif "conversaciones" in request and "conversaciones" in response.text.lower():
                        bot_showing_convers_msg(api, bot)

                    elif "comentar" in request and "comentar" in response.text.lower():
                        bot_commenting_posts(api, bot)

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