import json

from pyfacebook import IgProApi

# El valor de estas variables, se obtienen de la cuenta en Facebook for Developers.
APP_ID = "2522931991341291"
APP_SECRET = "9552895069b4d3c2950320c0f06354ff"

# Se deberá omitir setear ésta variable, por cuestiones de seguridad
ACCESS_TOKEN = ""
INSTAGRAM_ID = "17841444663784851"

api = IgProApi(
    app_id = APP_ID,
    app_secret = APP_SECRET,
    long_term_token = ACCESS_TOKEN,
    instagram_business_id = INSTAGRAM_ID
)


def get_ig_user_info(username):

    data = api.discovery_user(
        username = username,
        return_json = True
    )

    with open("data/ig_user_info.json", 'w') as f:
        json.dump(data, f)

