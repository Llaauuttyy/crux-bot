import os
import sys
sys.path.append("C://Users//Leonel//Documents//crux-bot")

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

import re


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

KEYWORDS_ENABLE = [
    "habilitar", "habilita", "habilitalo"
]

KEYWORDS_DISABLE = [
    "deshabilitar", "deshabilita", "deshabilitalo"
]

MIN_CONFIDENCE = 0.8

# ------------------------------------------------------ #
# ------------ DATA MANAGEMENT UTILS STARTS ------------ #
# ------------------------------------------------------ #


def validate_url(bot  # type: ChatBot
                 ):

    # PRE: Recibe el objeto bot
    # POST: Valida la url y la retorna

    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    url = request_input(bot, "msgrequrlphoto")
    acepted = re.match(regex, url) is not None

    while not acepted:
        url = request_input(bot, "urlgeterror")

    return url


def validate_enable_disable(bot  # type: ChatBot
                            ):

    # PRE: Recibe el objeto bot
    # POST: Pregunta al usuario si quiero habilitar o deshabilitar
    # la publicacion

    enable_or_not = request_input(bot, "msgreqcommentenabled")
    while (enable_or_not not in KEYWORDS_ENABLE and
           enable_or_not not in KEYWORDS_DISABLE):
        enable_or_not = request_input(bot, "msgerrorenable")

    return enable_or_not


def validate_number_in_range(bot,  # type: ChatBot
                             range  # type: list[dict]
                             ):

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'range', debe ser una variable de tipo list
    # POST: Devuelve un número de tipo int, el cuál es ingresado por
    #       el usuario, para posteriormente validar, que es un número y
    #       que se encuentra dentro del rango de la cantidad de elementos
    #       de la lista indicada anteriormente

    request = ""
    flag_is_valid_number = False
    number = 0

    request = request_input(bot, "msgreqobjectid")

    while not flag_is_valid_number:

        if request.isdecimal():
            number = int(request) - 1

            if number >= 0 and number <= len(range) - 1:
                flag_is_valid_number = True
            else:
                request = request_input(bot, "msgerrornotinrange")

        else:
            request = request_input(bot, "msgerrornotnumber")

    return number


def posts_or_convo_order(object_info_list,  # type: list
                         object_number  # type: str
                         ):

    # PRE: Recibe posts_info_list que
    # una lista de diccionarios lleno de data, y
    # object_number que es el post que
    # al que el usuario quiere acceder.

    # POST: Cambia object_number para ser
    # el índice de una lista, luego busca
    # al post y lo retorna (su ID).

    object_index = int(object_number) - 1  # Beacuse we're using a list.

    object_id = object_info_list[object_index]["id"]

    return object_id


def fb_error_checking(data  # type: dict
                      ):

    # PRE: Recibe data de todo tipo
    # de acciones.

    # POST: Chequea si hay error, si lo
    # hay, lo printea y devuelve True, sino
    # False.

    if "error" in data:
        text = "Un error ha ocurrido: {error}".format(
            error=data["error"]
            )

        print(text)
        chat_logger.info(text)

        return True

    else:
        return False


def fb_error_checking_profile_photo(data  # type: dict
                                    ):

    # PRE: Recibe data de foto de perfil.

    # POST: Chequea si hay error, si lo
    # hay, printea y devuelve True, sino
    # False.

    if data["error"].result["error"]["code"] == 100:
        return False

    else:
        print("Ha ocurrido un error inesperado.")
        chat_logger.info("[Crux]: Ha ocurrido un error inesperado")

        return True


def format_date(str_datetime  # type: str
                ):

    # PRE: 'str_datetime', debe ser una variable de tipo str
    # POST: Devuelve un string que representa la fecha y hora, la cual
    #       deriva de la fecha y hora ingresada anteriormente, a esa
    #       se le dió un formato local y se corrigió la diferencia de
    #       horas

    datetime_fixed = ""

    # El string pasado por parámetro, es necesario parsearlo/convertirlo
    # a una variable de tipo datetime e indicar el tipo de formato de fecha
    # y hora con el que viene, para recién poder realizar alguna operación
    # con la misma, como por ej. la resta de horas
    datetime_formatted = (
        datetime.strptime(str_datetime, "%Y-%m-%dT%H:%M:%S+%f") +
        timedelta(hours=-3)
    )

    # Una vez corregido la diferencia de horas, a la hora y fecha, se le da
    # un formato local, para luego parsearlo/convertirlo a string
    datetime_fixed = datetime_formatted.strftime("%d/%m/%Y %H:%M:%S")

    return datetime_fixed


def format_key(key  # type: str
               ):

    # PRE: 'key', debe ser una variable de tipo str
    # POST: Devuelve un string que representa una llave de diccionario, dicha
    #       llave ingresda anteriormente, se la capitalizó y se reemplazó los
    #       guiones bajos por un espacio

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

    # POST: Crea el objeto bot y lo retorna.

    chatbot = ChatBot(
        "Crux",
        response_selection_method = get_random_response,
        preprocessors = [
            "chatterbot.preprocessors.clean_whitespace",
            #"chatterbot.preprocessors.convert_to_ascii"
        ]
    )

    return chatbot


def bot_training(bot  # type: ChatBot
                 ):

    # PRE: Recibe el objeto bot.

    # POST: Lo usa para crear
    # el objeto trainer que nos permite
    # entrenar al bot con lista de strings,
    # provenientes del archivo trainer.

    datos = []
    bot.storage.drop()
    trainer = ListTrainer(bot)
    trainer.show_training_progress = False

    with open("data/entrenador.txt", "r", encoding="utf-8") as f:
        datos = f.read().splitlines()

    trainer.train(datos)


def bot_greetings(bot  # type: ChatBot
                  ):

    # PRE: Recibe el objeto bot.

    # POST: Da la bienvenida al usuario,
    # valida su nombre y lo devuelve.

    username = request_input(bot, "msgwme")

    while username.isdecimal():
        username = request_input(bot, "msgnameisnum")

    username = username.lower().capitalize()

    return username


def information_followers(api,  # type: Api
                          bot  # type: ChatBot
                          ):

    # PRE: Recibe el objeto api y bot.
    # POST: Obtiene la data,
    # y si todo sale bien, imprime los seguidores
    print_response(bot, "fbopt9msg0")

    data = fb.get_page_information(
        api=api,
        page_id=PAGE_ID
    )

    if not fb_error_checking(data):
        followers_count(data)

    else:
        print_response(bot, "fbopt5msg5")


def followers_count(data  # type: list[dict]
                    ):

    # PRE: Obtiene la data
    # POST: Accede a la cantidad de seguidores, y la imprime
    text = (
        '''
        Bien, entonces la cantidad de seguidores que tenes es: {}.
        Sos famosito eh!
        '''.format(
            data["followers_count"]
        )
    )

    print(text)
    chat_logger.info(text)


def bot_shows_posts(api,  # type: Api
                    bot  # type: ChatBot
                    ):

    # PRE: Recibe el objeto api y bot.

    # POST: Obtiene los posts, en caso de
    # que no haya error, returna los mismos,
    # sino una lista vacía.

    print_response(bot, "fbopt1msg0")

    posts_info_list = fb.get_posts(
        api=api,
        page_id=PAGE_ID
    )

    if not fb_error_checking(posts_info_list):
        print_data(bot, posts_info_list, bot_shows_posts.__name__)

        return posts_info_list

    else:
        posts_info_list = list()

        return posts_info_list


def bot_shows_conversations(api,  # type: Api
                              bot  # type: ChatBot
                              ):

    # PRE: Recibe el objeto api y bot.

    # POST: Obtiene las convers, en caso de
    # que no haya error, returna las mismas
    # en una lista, sino una lista vacía.

    print_response(bot, "fbopt7msg0")
    # calls conversations
    convers_info_list = fb.get_page_conversations(
        api=api,
        page_id=PAGE_ID
    )

    # looks for errors
    if not fb_error_checking(convers_info_list):
        # if there's not, print conversations
        print_data(bot, convers_info_list, bot_shows_conversations.__name__)
        # lets the user choose and print all
        # of the mssages from that convo.
        return convers_info_list

    else:
        posts_info_list = list()

        return posts_info_list


def bot_object_chooser(api,  # type: Api
                       bot,  # type: ChatBot
                       type_object  # type: str  # Values: posts_fb, convo_fb (else)
                       ):

    # PRE: Recibe el objeto api, bot y
    # la str type_object que determina
    # qué objetos mostrar.

    # POST: Printea la informacion,
    # dependiendo del caso y valida
    # el numero que elija el usuario.

    if type_object == "posts_fb":
        object_info_list = bot_shows_posts(api, bot)

    else:
        object_info_list = bot_shows_conversations(api, bot)

    if object_info_list == []:
        print("Try rebooting your connection")

    else:
        object_number = request_input(bot, "fbchr0")

        while not object_number.isdecimal() or int(object_number) > len(object_info_list) or int(object_number) < 1:

            object_number = request_input(bot, "fbchr5")

        object_id = posts_or_convo_order(object_info_list, object_number)

        return object_id


def bot_shows_convers_msg(api,  # type: Api
                          bot  # type: ChatBot
                          ):

    # PRE: Recibe el objeto api y bot.

    # POST: Permite recibir info de mensajes
    # y si no hay errores, llama para printearlos.

    convo_id = bot_object_chooser(api, bot, "convo")

    messages_info_list = fb.get_conversation_messages(
        api=api,
        conversation_id=convo_id
    )

    if not fb_error_checking(messages_info_list):
        print_data(bot, messages_info_list, bot_shows_convers_msg.__name__)


def bot_likes_posts(api,  # type: Api
                    bot  # type: ChatBot
                    ):

    # PRE: Recibe el objeto api y bot.

    # POST: Llama a método para likear post,
    # si no hay error, avisa que se ha likeado.

    post_id = bot_object_chooser(api, bot, "posts")

    data = fb.post_like(api, post_id)

    if not fb_error_checking(data):
        print_response(bot, "fbopt0msg0")


def bot_post_publication(api,  # type: Api
                         bot  # type: ChatBot
                         ):

    # PRE: Recibe el objeto api y bot.

    # POST: Permite publicar llamando
    # a un método de fb y chequea si hay
    # algún error al hacerlo, sino hay,
    # avisa al usuario que todo salió bien.

    post_message = request_input(bot, "fbopt2msg0")

    data = fb.post_publication(
        api,
        page_id=PAGE_ID,
        message=post_message
    )

    if not fb_error_checking(data):

        print_response(bot, "fbopt2msg10")


def bot_put_publication(api,  # type: Api
                        bot  # type: ChatBot
                        ):

    # PRE: Recibe el objeto api y bot.

    # POST: Permite al usuario editar un post,
    # llama al método necesario y si no hay
    # error, muestra mensaje de éxito.

    post_id = bot_object_chooser(api, bot, "posts")

    user_edit = request_input(bot, "fbopt4msg10")
    data = fb.put_publication(api, post_id, user_edit)

    if not fb_error_checking(data):
        print_response(bot, "fbopt4msg15")


def bot_comments_posts(api,  # type: Api
                       bot  # type: ChatBot
                       ):

    # PRE: Recibe el objeto api y bot.

    # POST: Permite comentar, llamándo a método
    # de fb, si sale bien, printea mensaje.

    post_id = bot_object_chooser(api, bot, "posts")

    comment_message = request_input(bot, "fbopt2msg0")

    data = fb.post_comment(
        api=api,
        post_id=post_id,
        message=comment_message
    )

    if not fb_error_checking(data):

        print_response(bot, "fbopt2msg15")


def bot_checks_photo_is_in_path(bot   # type: ChatBot
                                ):

    # PRE: Recibe el objeto bot.

    # POST: Crea la carpeta para subir
    # fotos, si ya está creada avisa,
    # y luego revisa que la foto esté
    # localizada dentro de la carpeta.
    # Una vez que todo está en order,
    # retorna la foto.

    try:
        os.mkdir("images")

    except FileExistsError:
        photo_path = request_input(bot, "fbopt3msg1")

    else:
        photo_path = request_input(bot, "fbopt3msg0")

    photo_is_ready = False

    while not photo_is_ready:
        try:
            photo = open("images//{photo_path}".format(photo_path=photo_path), "rb")

            photo_is_ready = True

        except FileNotFoundError:
            photo_path = request_input(bot, "fbopt3msg5")

    return photo


def bot_uploads_feed_photo(graphapi,  # type: GraphAPI
                           bot  # type: ChatBot
                           ):

    # PRE: Recibe objeto graphapi y bot.

    # POST: Llama al método para subir la
    # foto y recibe la data, si no tiene error,
    # le avisa al usuario que todo salió bien.
    photo = bot_checks_photo_is_in_path(bot)

    data = fb.post_photo(
        api=graphapi,
        page_id=PAGE_ID,
        image=photo
    )

    if not fb_error_checking(data):
        print_response(bot, "fbopt3msg20")


def bot_uploads_profile_photo(graphapi,  # type: GraphAPI
                              bot  # type: ChatBot
                              ):

    # PRE: Recibe objeto graphapi y bot.

    # POST: Llama al método para subir la
    # foto de perfil y recibe la data, si
    # no tiene error, le avisa al usuario
    # que todo salió bien.

    photo = bot_checks_photo_is_in_path(bot)

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

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'api', debe ser una variable de tipo IgProApi
    #      'username', debe ser una variable de tipo str
    # POST: Hace el llamado a la API de Facebook, haciendo uso de api, con
    #       el fin de buscar al usuario indicado anteriormente, y de este
    #       modo, obtener sus datos

    data_list = []

    data = ig.get_ig_user_info(
        api=api,
        username=username
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

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'api', debe ser una variable de tipo IgProApi
    #      'username', debe ser una variable de tipo str
    # POST: Hace el llamado a la API de Facebook, haciendo uso de api, con
    #       el fin de obtener las publicaciones/medias del usuario indicado
    #       anteriormente, y de este modo, obtener la información de cada una

    data_list = []

    data = ig.get_ig_user_medias(
        api=api,
        username=username
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

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'api', debe ser una variable de tipo GraphAPI
    #      'image_url', debe ser una variable de tipo str
    # POST: Hace el llamado a la API de Facebook, haciendo uso de api, con
    #       el fin de postear una foto en el muro/feed. Dicha foto, se
    #       encuentra en la url, indicada anteriormente

    data_list = []

    data = ig.post_ig_photo(
        api=api,
        instagram_business_id=INSTAGRAM_BUSINESS_ID,
        image_url=image_url
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

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'api', debe ser una variable de tipo IgProApi
    #      'media_id', debe ser una variable de tipo str
    #      'comment_enabled', debe ser una variable de tipo bool
    # POST: Hace el llamado a la API de Facebook, haciendo uso de api, con
    #       el fin de actualizar la publicacion/media indicada
    #       anteriormente. Dicha actualización se basa en la habilitación
    #       o no, de los comentarios

    data_list = []

    data = ig.put_ig_media(
        api=api,
        media_id=media_id,
        comment_enabled=comment_enabled
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

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'api', debe ser una variable de tipo IgProApi
    #      'username', debe ser una variable de tipo str
    # POST: Hace el llamado a la API de Facebook, haciendo uso de api, con
    #       el fin de obtener los seguidores del usuario indicado
    #       anteriormente. No se puede listar, sólo se los cuenta

    data_list = []

    data = ig.get_ig_user_info(
        api=api,
        username=username
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

    # PRE: 'data', debe ser una variable de tipo dict
    #      'function_name', debe ser una variable de tipo str
    # POST: Devuelve un diccionario, el cual deriva de la data pasada
    #       por parámetro, a la misma se la filtra y se asignan las
    #       llaves en español. La filtración varia de acuerdo a la
    #       función que llame a ésta

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

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'data', debe ser una variable de tipo dict
    #      'function_name', debe ser una variable de tipo str
    # POST: Imprime el error que ocurrió, al hacer la petición a la API
    #       de Facebook, de lo contrario, de acuerdo a que función llame
    #       a ésta, imprimirá la información/respuesta que se recibió de
    #       Facebook

    key_error = "error"

    if (function_name == search_user_by_bot.__name__ or function_name == get_followers_by_bot.__name__):

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")

                chat_logger.info(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}")

            else:
                for key in data[x]:
                    print(f"[{bot.name}]: {format_key(key)}  :  {data[x].get(key)}")

                    chat_logger.info(f"[{bot.name}]: {format_key(key)}  :  {data[x].get(key)}")

    elif function_name == get_medias_by_bot.__name__:

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")

                chat_logger.info(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}")

            else:
                del data[x]["id"]
                data[x]["fecha_y_hora_de_publicacion"] = format_date(data[x].get("fecha_y_hora_de_publicacion"))

                print(f"\n[{bot.name}]: {x + 1}° - publicación")

                chat_logger.info(f"[{bot.name}]: {x + 1}° - publicación")

                for key in data[x]:
                    print(f"[{bot.name}]: {format_key(key)}  :  {data[x].get(key)}")

                    chat_logger.info(f"[{bot.name}]: {format_key(key)}  :  {data[x].get(key)}")

    elif function_name == post_ig_photo_by_bot.__name__:

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")

                chat_logger.info(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}")

            else:
                print_response(bot, "msgpostedphoto")

    elif function_name == update_media_by_bot.__name__:

        for x in range(len(data)):

            if key_error in data[x]:
                print_response(bot, "msgerrorconn")
                print(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}\n")

                chat_logger.info(f"[{bot.name}]: {key_error.capitalize()}  :  {data[x].get(key_error).message}")
            else:
                if(data[x].get("success")):
                    print_response(bot, "msgcommenabledsucc")
                else:
                    print_response(bot, "msgcommenablednotsucc")

    elif function_name == bot_shows_posts.__name__:

        for posts in range(len(data)):

            for key in data[posts]:

                if key == "message":
                    print(f"Post {posts + 1}: {data[posts]['message']}\n")
                    chat_logger.info("[Crux]: Post {post_number} - {post_message}".format(
                            post_number=posts + 1,
                            post_message=data[posts]['message']
                        )
                    )

                elif key == "picture":
                    print(f"Post {posts + 1}: This post is a photo.")
                    chat_logger.info("[Crux]: Post {post_number} - {post_message}".format(
                            post_number=posts + 1,
                            post_message="This post is a photo."
                        )
                    )

    elif function_name == bot_shows_conversations.__name__:

        for snippet in range(len(data)):

            print(
                '''
                [Crux]:
                Follower: {follower}
                Last message: {last_message}
                Conversation: {snippet}
                '''.format(
                    follower=data[snippet]["participants"]["data"][0]["name"],
                    last_message=data[snippet]["snippet"],
                    snippet=snippet + 1
                )
            )

            chat_logger.info("[Crux]: Follower: {follower} | Last message: {last_message} | Conversation: {snippet}".format(
                    follower=data[snippet]["participants"]["data"][0]["name"],
                    last_message=data[snippet]["snippet"],
                    snippet=snippet + 1
                )
            )

    elif function_name == bot_shows_convers_msg.__name__:

        for message in range(len(data)):
            print(
                '''
                [Crux]:
                Sender: {sender}
                Message: {message}
                '''.format(
                    sender=data[message]["from"]["name"],
                    message=data[message]["message"]
                )
            )

            chat_logger.info("[Crux]: Sender: {sender} | Message: {message}".format(
                    sender=data[message]["from"]["name"],
                    message=data[message]["message"]
                )
            )


# ------------------------------------------------------ #
# ----------------- BOT FUNCTIONS ENDS ----------------- #
# ------------------------------------------------------ #


def set_up_file(from_filepath,  # type: str
                to_filepath,  # type: str
                enforce_username=False,  # type: bool
                username=None  # type: str
                ):

    # PRE: 'from_filepath', debe ser una variable de tipo str
    #      'to_filepath', debe ser una variable de tipo str
    #      'enforce_username', debe ser una variable de tipo bool
    #      'username', debe ser una variable de tipo str
    # POST: Reemplaza una palabra clave, por el nombre del usuario pasado
    #       por parámetro, de acuerdo a si se desea forzar el cambio,
    #       desde el archivo deseado, hacia el archivo indicado

    filedata = []

    with open(from_filepath, "r", encoding="utf-8") as file:
        filedata = file.read()

    if enforce_username:
        filedata = filedata.replace("{nombre}", username)

    with open(to_filepath, 'w', encoding="utf-8") as file:
        file.write(filedata)


def request_input(bot,  # type: ChatBot
                  statement  # type: str
                  ):

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'statement', debe ser una variable de tipo str
    # POST: Devuelve un string que representa una petición hecha por
    #       el usuario. Dicha petición se parsea a minúsculas

    response = bot.get_response(statement)
    chat_logger.info(f"[{bot.name}]: {response}")

    request = input(f"\n[{bot.name}]: {response}\n")
    chat_logger.info(f"[Usuario]: {request}")

    return request.lower()


def print_response(bot,  # type: ChatBot
                   statement  # type: str
                   ):

    # PRE: 'bot', debe ser una variable de tipo ChatBot
    #      'statement', debe ser una variable de tipo str
    # POST: Imprime la respuesta que se recibe por parte del bot,
    #       en función del statement

    request = ""

    response = bot.get_response(statement)

    while response.confidence < MIN_CONFIDENCE:
        request = request_input(bot, "msgforconfidence")

        response = bot.get_response(request)

    print(f"[{bot.name}]: {response}\n")

    chat_logger.info(f"[{bot.name}]: {response}")


def are_keywords_in_text(text,  # type: str
                         keywords  # type: list
                         ):

    # PRE: 'text', debe ser una variable de tipo str
    #      'keywords', debe ser una variable de tipo list
    # POST: Retorna un boolean, que representa la ocurrencia de
    #       una palabra de la lista 'keywords', en el texto
    #       ingresado anteriormente

    flag_is_in = False

    for x in range(len(keywords)):
        if keywords[x] in text:
            flag_is_in = True

    return flag_is_in


def init_main_options(request,  # type: str
                      bot,  # type: ChatBot
                      api,  # type: Api
                      igproapi,  # type: IgProApi
                      graphapi  # type: GraphAPI
                      ):

    # PRE: 'request', debe ser una variable de tipo str
    #      'bot', debe ser una variable de tipo ChatBot
    #      'api', debe ser una variable de tipo Api
    #      'igproapi', debe ser una variable de tipo IgProApi
    #      'graphapi', debe ser una variable de tipo GraphAPI
    # POST: Retorna un string, que representa una petición
    #       solicitada por el usuario

    response = ""
    image_url = ""
    posts_list = []
    post_id = 0

    comment_enabled = False

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

                    chat_logger.info(f"[{bot.name}]: {response}")

                request = request_input(bot, "msgreqopt")
                response = bot.get_response(request)

                while (response.confidence < MIN_CONFIDENCE or not are_keywords_in_text(response.text.lower(), KEYWORDS) or
                        "habilitar" in response.text.lower()):

                    request = request_input(bot, "msgforconfidence")
                    response = bot.get_response(request)

                print(f"[{bot.name}]: {response}\n")

                chat_logger.info(f"[{bot.name}]: {response}")

                if "likear" in request and "likear" in response.text.lower():
                    bot_likes_posts(api, bot)

                elif "publicaciones" in request and "publicaciones" in response.text.lower():
                    bot_shows_posts(api, bot)

                elif "postear" in request and "postear" in response.text.lower():
                    bot_post_publication(api, bot)

                elif "foto" in request and "foto" in response.text.lower():
                    bot_uploads_feed_photo(graphapi, bot)

                elif "actualizar" in request and "actualizar" in response.text.lower():
                    bot_put_publication(api, bot)

                elif "seguidores" in request and "seguidores" in response.text.lower():
                    information_followers(api, bot)

                elif "perfil" in request and "perfil" in response.text.lower():
                    bot_uploads_profile_photo(graphapi, bot)

                elif "conversaciones" in request and "conversaciones" in response.text.lower():
                    bot_shows_convers_msg(api, bot)

                elif "comentar" in request and "comentar" in response.text.lower():
                    bot_comments_posts(api, bot)

                flag_is_valid = True

            elif request in OPTIONS_FOR_INSTAGRAM:
                for x in range(5):
                    response = bot.get_response(f"igopt{x}")
                    print(f"[{bot.name}]: {response}")

                    chat_logger.info(f"[{bot.name}]: {response}")

                request = request_input(bot, "msgreqopt")
                response = bot.get_response(request)

                while response.confidence < MIN_CONFIDENCE or not are_keywords_in_text(response.text.lower(), KEYWORDS):
                    request = request_input(bot, "msgforconfidence")
                    response = bot.get_response(request)

                print(f"[{bot.name}]: {response}\n")

                chat_logger.info(f"[{bot.name}]: {response}")

                if "buscar" in request and "buscar" in response.text.lower():
                    username = request_input(bot, "msgrequsername")

                    search_user_by_bot(bot, igproapi, username)

                elif "publicaciones" in request and "publicaciones" in response.text.lower():
                    username = IG_USERNAME

                    print_response(bot, "msgreqposts")
                    get_medias_by_bot(bot, igproapi, username)

                elif "foto" in request and "foto" in response.text.lower():

                    image_url = validate_url(bot)
                    post_ig_photo_by_bot(bot, graphapi, image_url)

                elif "actualizar" in request and "habilitar" in response.text.lower():
                    username = IG_USERNAME

                    posts_list = get_medias_by_bot(bot, igproapi, username)

                    post_id = validate_number_in_range(bot, posts_list)

                    request = validate_enable_disable(bot)

                    if request in KEYWORDS_ENABLE:
                        comment_enabled = True
                    elif request in KEYWORDS_DISABLE:
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

    return request


def main():
    request = ""
    username = ""

    api = Api(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        long_term_token=PAGE_ACCESS_TOKEN,
    )

    igproapi = IgProApi(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        long_term_token=PAGE_ACCESS_TOKEN,
        instagram_business_id=INSTAGRAM_BUSINESS_ID
    )

    graphapi = GraphAPI(
        access_token=PAGE_ACCESS_TOKEN
    )

    bot = bot_creation()

    bot_training(bot)

    username = bot_greetings(bot)

    set_up_file("data/entrenador.txt", "data/entrenador.txt", True, username)

    bot_training(bot)

    request = request_input(bot, "descripcion")

    while request not in OPTIONS_FOR_EXIT:

        request = init_main_options(request, bot, api, igproapi, graphapi)

    else:
        print_response(bot, request)

    set_up_file("data/entrenador.bak", "data/entrenador.txt")


if __name__ == "__main__":
    main()
