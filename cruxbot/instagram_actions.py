from facebook import GraphAPI, GraphAPIError
from pyfacebook import IgProApi, PyFacebookException

from loggers import error_logger


def get_ig_user_info(api,  # type: IgProApi
                     username  # type: str
                     ):

    # PRE: 'api', debe ser una variable de tipo IgProApi
    #      'username', debe ser una variable de tipo str
    # POST: Devuelve los datos del usuario indicado anteriormente,
    #       en un diccionario

    data = {}

    try:
        data = api.discovery_user(
            username=username,
            return_json=True
        )

    except PyFacebookException as error:
        data = {"error": error}

        error_logger.error(error, exc_info=True)

    return data


def get_ig_user_medias(api,  # type: IgProApi
                       username  # type: str
                       ):

    # PRE: 'api', debe ser una variable de tipo IgProApi
    #      'username', debe ser una variable de tipo str
    # POST: Devuelve las publicaciones/medias del usuario indicado
    #       anteriormente, en una lista de diccionarios

    data = {}

    try:
        data = api.discovery_user_medias(
            username=username,
            return_json=True
        )

    except PyFacebookException as error:
        data = {"error": error}

        error_logger.error(error, exc_info=True)

    return data


def get_ig_media_info(api,  # type: IgProApi
                      media_id  # type: str
                      ):

    # PRE: 'api', debe ser una variable de tipo IgProApi
    #      'media_id', debe ser una variable de tipo str
    # POST: Devuelve los datos de la publicacion/media indicado
    #       anteriormente, en un diccionario

    data = {}

    try:
        data = api.get_media_info(
            media_id=media_id,
            return_json=True
        )

    except PyFacebookException as error:
        data = {"error": error}

        error_logger.error(error, exc_info=True)

    return data


def post_ig_photo(api,  # type: GraphAPI
                  instagram_business_id,  # type: str
                  image_url  # type: str
                  ):

    # PRE: 'api', debe ser una variable de tipo GraphAPI
    #      'instagram_business_id', debe ser una variable de tipo str
    #      'image_url', debe ser una variable de tipo str
    # POST: Devuelve el 'id' de la publicacion de la foto indicada
    #       anteriormente, en un diccionario

    response = {}
    data = {}

    try:
        # Al tratarse de una funcionalidad que no es contemplada, por ninguna
        # de las API's, es necesario armar la petición manualmente
        response = api.request(
            # v9.0/{object-id}/resource?args={arg1,arg2...}
            path="{0}/{1}/{2}".format("v9.0", instagram_business_id, "media"),
            args={
                "image_url": image_url
            },
            post_args={
                "access_token": api.access_token
            },
            method="POST"
        )

    except GraphAPIError as error:
        response = {"error": error}

        error_logger.error(error, exc_info=True)

    if "error" not in response:
        try:
            # La primera petición, se encarga de subir la foto a Instagram, donde
            # quedará almacenada.
            # Ésta segunda petición, se encarga de publicar la foto en el feed/muro
            # de la cuenta de Instagram
            data = api.request(
                path="{0}/{1}/{2}".format("v9.0", instagram_business_id, "media_publish"),
                args={
                    "creation_id": response["id"]
                },
                post_args={
                    "access_token": api.access_token
                },
                method="POST"
            )

        except GraphAPIError as error:
            data = {"error": error}

            error_logger.error(error, exc_info=True)

    else:
        data = response.copy()

    return data


def put_ig_media(api,  # type: IgProApi
                 media_id,  # type: str
                 comment_enabled  # type: bool
                 ):
    
    # PRE: 'api', debe ser una variable de tipo IgProApi
    #      'media_id', debe ser una variable de tipo str
    #      'comment_enabled', debe ser una variable de tipo bool
    # POST: Devuelve el estado de la actualización de la publicacion/media
    #       indicada anteriormente, en un diccionario

    data = {}

    try:
        response = api._request(
            path="{0}/{1}".format(api.version, media_id),
            method="POST",
            args={
                "comment_enabled": comment_enabled
            },
            post_args={
                "access_token": api._access_token
            }
        )

        # Ésta función se encarga de convertir en un diccionario
        # la respuesta que se recibió de la API
        data = api._parse_response(response)

    except PyFacebookException as error:
        data = {"error": error}

        error_logger.error(error, exc_info=True)

    return data
