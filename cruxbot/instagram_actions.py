import json

from pyfacebook import IgProApi

# El valor de estas variables, se obtienen de la cuenta en Facebook for Developers.
APP_ID = "2522931991341291"
APP_SECRET = "9552895069b4d3c2950320c0f06354ff"

# Se deberá omitir setear ésta variable, por cuestiones de seguridad
ACCESS_TOKEN = "EAAj2lZBEi6OsBAKUmb5ZCgYiHrrJzTnfBmUwItETHsrAZC96gnNL0jdhBG31NpFhhZCHTLgmEdCJulQ6S491ZC3QjYiOh9UJjPAFrWFYCzDfZBEwLOEaH5oNwmllruC47SM7PlwycoDgKFLagXfTLHzmZBixziVTdmYX5nnNMqS4AZDZD"
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


def get_ig_user_medias(username):

    data = api.discovery_user_medias(
        username = username,
        return_json = True
    )

    with open("data/ig_user_medias.json", 'w') as f:
        json.dump(data, f)


def get_ig_media_info(media_id):

    data = api.get_media_info(
        media_id = media_id,
        return_json = True
    )

    with open("data/ig_media_info.json", 'w') as f:
        json.dump(data, f)


class ExtApi(IgProApi):

    def build_path(self,
                        target,
                        resource,
                        args,
                        post_args
                        ):

        resp = self._request(
            path = "{version}/{target}/{resource}".format(
                version = self.version, 
                target = target, 
                resource = resource
            ),
            args = args,
            post_args = post_args
        )

        data = self._parse_response(resp)

        return data


    def post_ig_photo(self,
                     ig_user_id,
                     access_token,
                     args
                     ):

        post_args = {
            "access_token" : access_token,
        }

        data = self.build_path(
            target = ig_user_id, 
            resource = "media",
            args = args,
            post_args = post_args
        )

        with open("data/ig_photo.json", 'w') as f:
            json.dump(data, f) 


    def post_publish_ig_photo(self,
                     ig_user_id,
                     access_token,
                     args
                     ):

        post_args = {
            "access_token" : access_token,
        }

        data = self.build_path(
            target = ig_user_id, 
            resource = "media_publish",
            args = args,
            post_args = post_args
        )

        with open("data/ig_publish_photo.json", 'w') as f:
            json.dump(data, f) 


    def post_enabling_comments(self,
                     ig_media_id,
                     access_token,
                     args
                     ):

        post_args = {
            "access_token" : access_token,
        }

        data = self.build_path(
            target = ig_media_id,
            resource = "",
            args = args,
            post_args = post_args
        )

        with open("data/ig_enabling_comments.json", 'w') as f:
            json.dump(data, f) 
