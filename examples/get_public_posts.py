"""
    This show how to get facebook page public posts.
"""

import json

from pyfacebook import Api

# Use version 5+, Call API need app secret proof. So need provide your app secret.
# If not have, you can just use version 4.0.
# El valor de estas variables, se obtienen de la cuenta en Facebook for Developers.
APP_ID = "2522931991341291"
APP_SECRET = "9552895069b4d3c2950320c0f06354ff"

# Se deberá omitir setear ésta variable, por cuestiones de seguridad
ACCESS_TOKEN = "Your Access Token"


def get_posts(user_id):
    # Se crea un objeto Api para la conexión, a partir del contructor, al cual se le
    # pasa por parámetros, las constantes anteriormente definidas.
    api = Api(
        app_id = APP_ID,
        app_secret = APP_SECRET,
        long_term_token = ACCESS_TOKEN,
    )

    # Se llama a un método del objeto Api, el cual nos devuelve los posteos hechos por
    # el usuario, en su muro.
    # Hay algunos filtros que se pueden pasar por parámetro, para manipular que
    # información se desea obtener.
    data = api.get_page_posts(
        page_id = user_id,
        since_time = "2020-05-01",
        count = None,
        limit = 100,
        return_json = True,
    )

    return data


def processor():
    # En este campo, se debe setear el id de usuario. El mismo se obtiene desde la cuenta
    # normal de Facebook en "Configuración/Integraciones comerciales", y en la aplicación
    # que se creó, dar click en "Ver y editar".
    # También se puede obtener desde Facebook for Developers, haciendo una consulta desde
    # el "Explorador de la API Graph"
    user_id = "103684888301061"
    data = get_posts(user_id)
    
    with open("data/facebook/fb_posts.json", 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    processor()