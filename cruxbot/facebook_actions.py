from typing import Dict, List, Optional, Union, Tuple, Set

from attr import attrs, attrib
from pyfacebook import Api, BaseModel
from pyfacebook.error import PyFacebookException
from pyfacebook.utils.param_validation import enf_comma_separated

import json
import requests


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


class ExtApi(Api):
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


    def _requestFile(self, path, method="GET", args=None, post_args=None, files=None, enforce_auth=True):

        if args is None:
            args = dict()
        if post_args is not None:
            method = "POST"
        if enforce_auth:
            if method == "POST" and "access_token" not in post_args:
                post_args["access_token"] = self._access_token
            elif method == "GET" and "access_token" not in args:
                args["access_token"] = self._access_token

            # add appsecret_proof parameter
            # Refer: https://developers.facebook.com/docs/graph-api/securing-requests/
            if method == "POST" and "appsecret_proof" not in post_args:
                secret_proof = self._generate_secret_proof(self.app_secret, post_args["access_token"])
                if secret_proof is not None:
                    post_args["appsecret_proof"] = secret_proof
            elif method == "GET" and "appsecret_proof" not in args:
                secret_proof = self._generate_secret_proof(self.app_secret, args["access_token"])
                if secret_proof is not None:
                    args["appsecret_proof"] = secret_proof

        # check path
        if not path.startswith("https"):
            path = self.base_url + path
        try:
            response = self.session.request(
                method,
                path,
                timeout=None,
                params=args,
                data=post_args,
                proxies=self.proxies,
                files=files,
            )
        except requests.HTTPError as e:
            raise PyFacebookException(ErrorMessage(code=ErrorCode.HTTP_ERROR, message=e.args[0]))
        headers = response.headers
        self.rate_limit.set_limit(headers)
        if self.sleep_on_rate_limit:
            sleep_seconds = self.rate_limit.get_sleep_seconds(sleep_data=self.sleep_seconds_mapping)
            time.sleep(sleep_seconds)
        return response

  
    def build_path_of_photo(self,
                    target,  # type: str
                    resource,  # type: str
                    post_args,  # type: Dict
                    files,
                    ):    

        resp = self._requestFile(
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