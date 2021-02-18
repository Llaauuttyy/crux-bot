from typing import Dict, List, Optional, Union, Tuple, Set

from pyfacebook.utils.param_validation import enf_comma_separated

from facebook import GraphAPI, GraphAPIError
from pyfacebook import Api, PyFacebookException


DEFAULT_CONVERSATION_FIELDS = [
    "id", "link", "snippet", "updated_time", "message_count",
    "unread_count", "participants", "senders", "can_reply",
    "is_subscribed"
]

DEFAULT_MESSAGE_FIELDS = [
    "created_time", "from", "id", "message", "tags", "to"
]

DEFAULT_PAGE_FIELDS = [
    "id", "about", "followers_count", "general_info"
]


def path_builder(api,  # type: Api
                 target,  # type: str
                 resource,  # type: str
                 method="GET",  # type: str
                 args=None,  # type: Dict
                 post_args=None,  # type: Dict
                 enforce_auth=True  # type: bool
                 ):

    # PRE: Recibe el objeto api,
    # y target, resource, method,
    # args, post_args, los cuales
    # nos permiten crear el path y los
    # últimos dos, enviar datos necesarios
    # para realizar esas acciones.

    # POST: Crea el path, y permite llamar
    # a _request para llevarle los datos,
    # en fin de recibir la info.

    response = api._request(
        path="{version}/{target}/{resource}".format(
            version=api.version,
            target=target,
            resource=resource
        ),
        method=method,
        args=args,
        post_args=post_args,
        enforce_auth=enforce_auth
    )

    data = api._parse_response(response)

    return data


def page_by_next(api,  # type: Api
                 target,  # type: str
                 resource,  # type: str
                 args,  # type: Dict
                 next_page,  # type: str
                 ):

    # PRE: Recibe el objeto api,
    # target y resource permiten armar
    # el path y los argumentos.

    # POST: Permite obtener información,
    # en caso de ser mucha, de distintas
    # páginas, dentro de un mismo campo.
    # Retorna la siguiente página y la data.

    if next_page is not None:
        response = api._request(
            path=next_page
        )

    else:
        response = api._request(
            path="{version}/{target}/{resource}".format(
                version=api.version,
                target=target,
                resource=resource
            ),
            args=args
        )

    next_page = None
    data = api._parse_response(response)

    if "paging" in data:
        next_page = data["paging"].get("next")

    return next_page, data


def get_posts(api,  # type: Api
              page_id  # type: str
              ):

    # PRE: Recibe el objeto api,
    # y la id de la página.

    # POST: Permite obtener los post
    # y customizar la petición para
    # obtener los que queramos y de
    # la fecha deseada.
    # Retorna la data, sino hay error,
    # contrario, la info del error.

    data = {}

    try:
        data = api.get_page_posts(
            page_id=page_id,
            since_time="2020-05-01",
            count=None,
            limit=100,
            return_json=True
        )

    except PyFacebookException as error:
        data = {"error": error}

    return data


def get_comments(api,  # type: Api
                 object_id  # type: str
                 ):

    # PRE: Recibe el objeto api,
    # y la id del post.

    # POST: Llama a la función necesaria
    # y en caso de error lo retorna, sino,
    # retorna la data.

    data = {}

    try:
        data = api.get_comments_by_object(
            object_id=object_id,
            count=None,
            limit=100,
            return_json=True,
        )

    except PyFacebookException as error:
        data = {"error": error}

    return data


def get_page_conversations(api,  # type: Api
                           page_id,  # type: str
                           fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                           folder="inbox",  # type: str
                           count=10,  # type: Optional[int]
                           limit=200  # type: int
                           ):

    # PRE: Recibe parámetros que nos
    # permiten customizar nuestra petición,
    # tales como fields, folder, count, limit.

    # POST: Llama funciones y controla sus respuestas,
    # para retornar la cantidad de conversaciones que establecimos
    # en caso de que no hayan errores.

    if fields is None:
        fields = DEFAULT_CONVERSATION_FIELDS

    args = {
        "access_token": api._access_token,
        "fields": enf_comma_separated("fields", fields),
        "folder": folder,
        "limit": limit
    }

    conversations = []
    next_page = None

    finish_loop = False
    try:
        while not finish_loop:
            next_page, data = page_by_next(
                api=api,
                target=page_id,
                resource="conversations",
                args=args,
                next_page=next_page
            )

            data = data.get("data", [])

            conversations.extend(data)

            if count is not None:
                conversations = conversations[:count]
                finish_loop = True

            if next_page is None:
                finish_loop = True

    except PyFacebookException as error:
        conversations = {"error": error}

    return conversations


def get_conversation_messages(api,  # type: Api
                              conversation_id,  # type: str
                              fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                              count=10,  # type: Optional[int]
                              limit=200,  # type: int
                              ):

    # PRE: Recibe parámetros que nos
    # permiten customizar nuestra petición,
    # tales como fields, count, limit.

    # POST: Llama funciones y controla sus respuestas,
    # para retornar la cantidad de mensajes que establecimos
    # en caso de que no hayan errores.

    if fields is None:
        fields = DEFAULT_MESSAGE_FIELDS

    args = {
        "access_token": api._access_token,
        "fields": enf_comma_separated("fields", fields),
        "limit": limit
    }

    messages = []
    next_page = None

    finish_loop = False
    try:
        while not finish_loop:
            next_page, data = page_by_next(
                api=api,
                target=conversation_id,
                resource="messages",
                args=args,
                next_page=next_page
            )
            data = data.get("data", [])

            messages.extend(data)

            # Sólo deja la cantidad de mensaje que pedimos.
            messages = messages[:count]

            if count is not None:
                messages = messages[:count]
                finish_loop = True

            if next_page is None:
                finish_loop = True

    except PyFacebookException as error:
        messages = {"error":  error}

    return messages


def post_comment(api,  # type: Api
                 post_id,  # type: str
                 message  # type: str
                 ):

    # PRE: Recibe el objeto api,
    # el id del post y el mensaje.

    # POST: Prepara el diccionario de
    # post_args y llama a la función para
    # crear el path. En caso de error lo
    # capta y retorna info sobre él.

    data = {}

    post_args = {
        "access_token": api._access_token,
        "message": message
    }

    try:
        data = path_builder(
            api=api,
            target=post_id,
            resource="comments",
            post_args=post_args
        )

    except PyFacebookException as error:
        data = {"error": error}

    return data


def post_publication(api,  # type: Api
                     page_id,  # type: str
                     message  # type: str
                     ):

    # PRE: Recibe el objeto api,
    # el id de la página y el mensaje a
    # postear.

    # POST: Prepara el diccionario de
    # post_args y llama a la función para
    # crear el path. En caso de error lo
    # capta y retorna info sobre él.

    data = {}

    post_args = {
        "access_token": api._access_token,
        "message": message
    }

    try:
        data = path_builder(
            api=api,
            target=page_id,
            resource="feed",
            post_args=post_args
        )

    except PyFacebookException as error:
        data = {"error": error}

    return data


def post_like(api,  # type: Api
              object_id  # type: str
              ):

    # PRE: Recibe el objeto api,
    # y la id de lo que se desea likear.

    # POST: Prepara los post_args y
    # llama a la funcion necesaria,
    # en caso de errores prepara un
    # diccionario con el mismo.

    data = {}

    post_args = {
        "access_token": api._access_token
    }

    try:
        data = path_builder(
            api=api,
            target=object_id,
            resource="likes",
            post_args=post_args
        )

    except PyFacebookException as error:
        data = {"error": error}

    return data


def post_photo(api,  # type: GraphAPI
               page_id,  # type: str
               image
               ):

    # PRE: Recibe el objeto api,
    # la id de la página, y la foto.

    # POST: Llama a put_photo para publicar
    # y en caso de error, lo retorna, sino data.

    data = {}

    try:
        data = api.put_photo(
            image=image,
            album_path="{0}/photos/picture".format(page_id)
        )

    except GraphAPIError as error:
        data = {"error": error}

    return data


def post_profile_photo(api,  # type: GraphAPI
                       page_id,  # type: str
                       image
                       ):

    # PRE: Recibe el objeto api,
    # el id de la página y la foto
    # que se desea subir.

    # POST: Llama a la función para
    # publicar la foto y en caso de error,
    # lo retorna, sino data

    data = {}

    try:
        data = api.put_photo(
            image=image,
            album_path="{0}/picture".format(page_id)
        )

    except GraphAPIError as error:
        data = {"error": error}

    return data


def delete_publication(api,  # type: Api
                       post_id  # type: str
                       ):

    # PRE: Recibe el objeto api,
    # el post_id que permite acceder a ese
    # post.

    # POST: Prepara el diccionario args
    # y llama a las funciones necesarias
    # para obtener la data y la retorna.

    data = {}

    args = {
        "access_token": api._access_token,
    }

    try:
        data = path_builder(
            api=api,
            target=post_id,
            resource="",  # Tiene que estar vacío.
            method="DELETE",
            args=args,
            enforce_auth=False
        )

    except PyFacebookException as error:
        data = {"error": error}

    return data


def put_publication(api,  # type: Api
                    post_id,  # type: str
                    message,  # type: str
                    ):

    # PRE: Recibe el objeto api,
    # el post_id permite acceder a ese
    # post y el mensaje a ser publicado.

    # POST: Prepara el diccionario post_args
    # llama a la función para generar los llamados.
    # En caso de error, lo retorna, sino data.

    data = {}

    post_args = {
        "access_token": api._access_token,
        "message": message
    }

    try:
        data = path_builder(
            api=api,
            target=post_id,
            resource="",
            post_args=post_args
        )

    except PyFacebookException as error:
        data = {"error": error}

    return data


def get_page_information(api,  # type: Api
                         page_id,  # type: str
                         fields=None  # type: Optional[Union[str, List, Tuple, Set]]
                         ):

    if fields is None:
        fields = DEFAULT_PAGE_FIELDS

    args = {
        "access_token": api._access_token,
        "fields": enf_comma_separated("fields", fields)
    }

    data = []

    try:
        response = api._request(
            path="{version}/{target}".format(
                version=api.version,
                target=page_id
            ),
            args=args
        )

        data = api._parse_response(response)

    except PyFacebookException as error:
        data = {"error":  error}

    return data
