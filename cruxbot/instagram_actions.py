from facebook import GraphAPI
from pyfacebook import IgProApi


def get_ig_user_info(api,  # type: IgProApi
                     username  # type: str
                     ):

    data = api.discovery_user(
        username=username,
        return_json=True
    )

    return data


def get_ig_user_medias(api,  # type: IgProApi
                       username  # type: str
                       ):

    data = api.discovery_user_medias(
        username=username,
        return_json=True
    )

    return data


def get_ig_media_info(api,  # type: IgProApi
                      media_id  # type: str
                      ):

    data = api.get_media_info(
        media_id=media_id,
        return_json=True
    )

    return data


def post_ig_photo(api,  # type: GraphAPI
                  instagram_business_id,  # type: str
                  image_url  # type: str
                  ):

    response = api.request(
        path="{0}/{1}/{2}".format("v9.0", instagram_business_id, "media"),
        args={
            "image_url": image_url
        },
        post_args={
            "access_token": api.access_token
        },
        method="POST"
    )

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

    return data
