import json

from pyfacebook import IgProApi


def get_ig_user_info(api, username):

    data = api.discovery_user(
        username = username,
        return_json = True
    )

    with open("data/instagram/ig_user_info.json", 'w') as f:
        json.dump(data, f)


def get_ig_user_medias(api, username):

    data = api.discovery_user_medias(
        username = username,
        return_json = True
    )

    with open("data/instagram/ig_user_medias.json", 'w') as f:
        json.dump(data, f)


def get_ig_media_info(api, media_id):

    data = api.get_media_info(
        media_id = media_id,
        return_json = True
    )

    with open("data/instagram/ig_media_info.json", 'w') as f:
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

        with open("data/instagram/ig_photo.json", 'w') as f:
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

        with open("data/instagram/ig_publish_photo.json", 'w') as f:
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

        with open("data/instagram/ig_enabling_comments.json", 'w') as f:
            json.dump(data, f)