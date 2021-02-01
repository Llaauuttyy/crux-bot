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
ACCESS_TOKEN = "EAAj2lZBEi6OsBAKUmb5ZCgYiHrrJzTnfBmUwItETHsrAZC96gnNL0jdhBG31NpFhhZCHTLgmEdCJulQ6S491ZC3QjYiOh9UJjPAFrWFYCzDfZBEwLOEaH5oNwmllruC47SM7PlwycoDgKFLagXfTLHzmZBixziVTdmYX5nnNMqS4AZDZD"


def get_posts(user_id):
    # Se crea un objeto Api para la conexión, a partir del contructor, al cual se le
    # pasa por parámetros, las constantes anteriormente definidas.
    api = Api(
        app_id=APP_ID,
        app_secret=APP_SECRET,
        long_term_token=ACCESS_TOKEN,
    )

    # Se llama a un método del objeto Api, el cual nos devuelve los posteos hechos por
    # el usuario, en su muro.
    # Hay algunos filtros que se pueden pasar por parámetro, para manipular que
    # información se desea obtener.
    data = api.get_page_posts(
        page_id=page_username,
        since_time="2020-05-01",
        count=None,
        limit=100,
        return_json=True,
    )

    return data


def processor():
    # En este campo, se debe setear el id de usuario. El mismo se obtiene desde la cuenta
    # normal de Facebook en "Configuración/Integraciones comerciales", y en la aplicación
    # que se creó, dar click en "Ver y editar".
    # También se puede obtener desde Facebook for Developers, haciendo una consulta desde
    # el "Explorador de la API Graph"
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
    user_id = "103684888301061"
    data = get_posts(user_id)

    with open("data/facebook/fb_posts.json", 'w') as f:
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
    page_username = "102579945106245"
    data = get_posts(page_username)

    with open("examples\\data\\fb_get_public_posts.json", 'w') as f:
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
        json.dump(data, f)


if __name__ == "__main__":
    processor()
