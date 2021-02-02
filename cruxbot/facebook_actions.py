import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

from typing import Dict, List, Optional, Union, Tuple, Set

from attr import attrs, attrib
from pyfacebook import Api, BaseModel
from pyfacebook.error import PyFacebookException
from pyfacebook.utils.param_validation import enf_comma_separated

from cruxbot.utils.extend_base import ExtBaseApi

import json


@attrs
class People(BaseModel):

    id = attrib(default = None, type = Optional[str])
    name = attrib(default = None, type = Optional[str])
    email = attrib(default = None, type = Optional[str], repr = False)


@attrs
class PageConversation(BaseModel):

    id = attrib(default = None, type = Optional[str])
    link = attrib(default = None, type = Optional[str], repr = False)
    snippet = attrib(default = None, type = Optional[str], repr = False)
    updated_time = attrib(default = None, type = Optional[str])
    message_count = attrib(default = None, type = Optional[int])
    unread_count = attrib(default = None, type = Optional[int])
    participants = attrib(default = None, type = Optional[Dict])
    senders = attrib(default = None, type = Optional[Dict])
    can_reply = attrib(default = None, type = Optional[bool], repr = False)
    is_subscribed = attrib(default = None, type = Optional[bool], repr = False)

    def __attrs_post_init__(self):
        if self.participants is not None and isinstance(self.participants, dict):
            participants = self.participants.get("data", [])
            self.participants = [People.new_from_json_dict(par) for par in participants]
        if self.senders is not None and isinstance(self.senders, dict):
            senders = self.senders.get("data", [])
            self.senders = [People.new_from_json_dict(sender) for sender in senders]


@attrs
class Comment(BaseModel):

    id = attrib(default = None, type = Optional[str])

    def __init__(self, id):
        self.id = id


class ExtApi(ExtBaseApi):
    DEFAULT_CONVERSATION_FIELDS = [
        "id", "link", "snippet", "updated_time", "message_count",
        "unread_count", "participants", "senders", "can_reply",
        "is_subscribed",
    ]

    DEFAULT_COMMENT_FIELDS = [
        "attachment_id", "attachment_share_url", "attachment_url",
        "source", "message",
    ]


    def page_by_next(self,
                     target,  # type: str
                     resource,  # type: str
                     args,  # type: Dict
                     next_page,  # type: str
                     ):

        if next_page is not None:
            resp = self._request(
                path = next_page
            )
        else:
            resp = self._request(
                path = "{version}/{target}/{resource}".format(
                    version = self.version,
                    target = target,
                    resource = resource
                ),
                args = args
            )

        next_page = None
        data = self._parse_response(resp)

        if "paging" in data:
            next_page = data["paging"].get("next")

        return next_page, data


    def get_posts():
        # Se crea un objeto Api para la conexión, a partir del contructor, al cual se le
        # pasa por parámetros, las constantes anteriormente definidas.
        api = Api(
            app_id="APP_ID",
            app_secret="APP_SECRET",
            long_term_token="ACCESS_TOKEN",
        )

        # Se llama a un método del objeto Api, el cual nos devuelve los posteos hechos por
        # el usuario, en su muro.
        # Hay algunos filtros que se pueden pasar por parámetro, para manipular que
        # información se desea obtener.
        data = api.get_page_posts(
            page_id="user_id",
            since_time="2020-05-01",
            count=None,
            limit=100,
            return_json=True,
        )

        with open("data\\facebook\\fb_posts.json", 'w') as f:
            json.dump(data, f)


    def get_comments():
        # Se crea un objeto Api para la conexión, a partir del contructor, al cual se le
        # pasa por parámetros, las constantes anteriormente definidas.
        api = Api(
            app_id="APP_ID",
            app_secret="APP_SECRET",
            long_term_token="ACCESS_TOKEN",
        )

        # Se llama a un método del objeto Api, el cual nos devuelve los posteos hechos por
        # el usuario, en su muro.
        # Hay algunos filtros que se pueden pasar por parámetro, para manipular que
        # información se desea obtener.
        data = api.get_comments_by_object(
            object_id="102579945106245_116261920404714",
            count=None,
            limit=100,
            return_json=True,
        )

        with open("data\\facebook\\fb_get_comments.json", 'w') as f:
            json.dump(data, f)


    def get_page_conversations(self,
                               page_id,  # type: str
                               access_token,  # type: str
                               fields = None,  # type: Optional[Union[str, List, Tuple, Set]]
                               folder = "inbox",  # type: str
                               count = 10,  # type: Optional[int]
                               limit = 200,  # type: int,
                               return_json = False  # type: bool
                               ):

        if fields is None:
            fields = self.DEFAULT_CONVERSATION_FIELDS

        args = {
            "access_token": access_token,
            "fields": enf_comma_separated("fields", fields),
            "folder": folder,
            "limit": limit,
        }

        conversations = []
        next_page = None

        while True:
            next_page, data = self.page_by_next(
                target = page_id,
                resource="conversations",
                args = args,
                next_page = next_page
            )
            data = data.get("data", [])

            if return_json:
                conversations.extend(data)
            else:
                conversations.extend([PageConversation.new_from_json_dict(item) for item in data])

            if count is not None:
                conversations = conversations[:count]
                break
            if next_page is None:
                break
        return conversations


    def get_conversation_messages(self,
                                    conversation_id,  # type: str
                                    access_token,  # type: str
                                    fields,  # fields=None,  # type: Optional[Union[str, List, Tuple, Set]]
                                    count,  # count=10,  # type: Optional[int]
                                    limit,  # limit=200,  # type: int,
                                    return_json  # return_json=False  # type: bool
                                ):

        # PRE: Revieces parameters who allows us to customize our request.

        # POST: Calls functions and manages its responses,
        # in order to return the messages amount we established.

        args = {
            "access_token": access_token,
            "fields": enf_comma_separated("fields", fields),  # enf_comma_separated basically filters
            "limit": limit                                    # the fields we passed by parameter.
        }

        messages = []
        next_page = None

        finish_loop = False
        while not finish_loop:
            next_page, data = self.page_by_next(
                target=conversation_id, resource="messages",  # messages is an important resource.
                args=args, next_page=next_page
            )
            data = data.get("data", [])

            messages.extend(data)

            messages = messages[:count]  # It just leaves the messages amount we want.

            if next_page is None:
                finish_loop = True

        if return_json:
            with open("data\\facebook\\fb_get_conversation_messages.json", 'w') as f:
                json.dump(messages, f)


    def path_builder(self,
                     target,  # type: str
                     resource,  # type: str
                     post_args,  # type: Dict
                     ):

        resp = self._request(
            path = "{version}/{target}/{resource}".format(
                version = self.version,
                target = target,
                resource = resource
            ),
            post_args = post_args
        )

        data = self._parse_response(resp)

        return data


    def post_comment(self,
                     post_id,  # type: str
                     access_token,  # type: str
                     message,
                     return_json = False  # type: bool
                     ):

        post_args = {
            "access_token": access_token,
            "message": message
        }

        comment = []

        data = self.path_builder(
            target = post_id,
            resource = "comments",
            post_args = post_args,
        )

        if return_json:
            comment.extend(data)

        with open("data\\facebook\\fb_post_comment.json", 'w') as file:
            json.dump(data, file)


    def post_publication(self,
                     page_id,  # type: str
                     access_token,  # type: str
                     message,
                     return_json = False  # type: bool
                     ):

        post_args = {
            "access_token" : access_token,
            "message" : message
        }

        comment = []

        data = self.path_builder(
            target = page_id,
            resource = "feed",
            post_args = post_args,
        )

        if return_json:
            comment.extend(data)

        with open("data\\facebook\\fb_post_publication.json", 'w') as file:
            json.dump(data, file)


    def edit_posts(self,
                     post_id,  # type: str
                     access_token,  # type: str
                     message,
                     return_json = False  # type: bool
                     ):

        post_args = {
            "access_token" : access_token,
            "message" : message
        }

        comment = []

        data = self.path_builder(
            target = post_id,
            resource = "",  # It has to be empty.
            post_args = post_args,
        )

        if return_json:
            comment.extend(data)
        
        with open("data\\facebook\\fb_edit_posts.json", 'w') as file:
            json.dump(data, file)


    def put_like(self,
                object_id,  # type: str
                access_token,  # type: str
                return_json = False  # type: bool
            ):

        post_args = {
            "access_token" : access_token
        }

        comment = []

        data = self.path_builder(
            target = object_id,
            resource = "likes",
            post_args = post_args
        )

        if return_json:
            comment.extend(data)

        with open("data\\facebook\\fb_put_like.json", 'w') as file:
            json.dump(data, file)

  
    def build_path_of_photo(self,
                    target,  # type: str
                    resource,  # type: str
                    post_args,  # type: Dict
                    files,
                    ):    

        resp = self._request(
            path = "{version}/{target}/{resource}".format(
                version = self.version, 
                target = target, 
                resource = resource
            ),
            post_args = post_args,
            files = {"source": files}
        )

        data = self._parse_response(resp)

        return data


    def post_photo(self,
                    page_id,  # type: str
                    access_token,  # type: str
                    files,
                    return_json = False  # type: bool
                    ):

        post_args = {
            "access_token" : access_token
        }

        response = []

        data = self.build_path_of_photo(
            target = page_id, 
            resource = "photos/picture",
            post_args = post_args,
            files = files 
        )

        if return_json:
            response.extend(data)
        
        with open("data\\facebook\\fb_post_photo.json", 'w') as file:
            json.dump(data, file)


    def post_profile_photo(self,
                    page_id,  # type: str
                    access_token,  # type: str
                    files,
                    return_json = False
                    ):

        post_args = {
            "access_token" : access_token
        }

        response = []

        try:
            data = self.build_path_of_photo(
                target = page_id, 
                resource = "picture",
                post_args = post_args,
                files = files 
            )

        except PyFacebookException as error:
            return error