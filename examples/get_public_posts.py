import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

from pyfacebook import Api

from cruxbot.cruxbot import APP_ID, APP_SECRET, PAGE_ACCESS_TOKEN, PAGE_ID


def get_posts(page_id):
    # Se crea un objeto Api para la conexión, a partir del contructor, al cual se le
    # pasa por parámetros, las constantes anteriormente definidas.
    api = Api(
        app_id = APP_ID,
        app_secret = APP_SECRET,
        long_term_token = PAGE_ACCESS_TOKEN,
    )

    # Se llama a un método del objeto Api, el cual nos devuelve los posteos hechos por
    # el usuario, en su muro.
    # Hay algunos filtros que se pueden pasar por parámetro, para manipular que
    # información se desea obtener.
    data = api.get_page_posts(
        page_id = page_id,
        since_time = "2020-05-01",
        count = None,
        limit = 100,
        return_json = True
    )

    return data


def processor():
    # En este campo, se debe setear el id de usuario. El mismo se obtiene desde la cuenta
    # normal de Facebook en "Configuración/Integraciones comerciales", y en la aplicación
    # que se creó, dar click en "Ver y editar".
    # También se puede obtener desde Facebook for Developers, haciendo una consulta desde
    # el "Explorador de la API Graph"
    user_id = PAGE_ID
    data = get_posts(user_id)

    return data


if __name__ == "__main__":
    processor()