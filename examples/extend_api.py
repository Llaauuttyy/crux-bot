"""
    This show extend this api for support others methods.
"""
import sys
sys.path.append("C:/Users/Leonel/Documents/crux-bot")

from typing import Dict, List, Optional, Union, Tuple, Set

from attr import attrs, attrib
from pyfacebook import Api, BaseModel
from pyfacebook.utils.param_validation import enf_comma_separated

import cruxbot.utils.constant as constant


@attrs
class People(BaseModel):
    """
    Refer: https://developers.facebook.com/docs/graph-api/reference/v6.0/conversation
    """
    
    id = attrib(default = None, type = Optional[str])
    name = attrib(default = None, type = Optional[str])
    email = attrib(default = None, type = Optional[str], repr = False)


@attrs
class PageConversation(BaseModel):
    """
    Refer: https://developers.facebook.com/docs/graph-api/reference/v6.0/conversation
    """

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


class ExtApi(Api):

    DEFAULT_CONVERSATION_FIELDS = [
        "id", "link", "snippet", "updated_time", "message_count",
        "unread_count", "participants", "senders", "can_reply",
        "is_subscribed",
    ]


    def page_by_next(self,
                     target,  # type: str
                     resource,  # type: str
                     args,  # type: Dict
                     next_page,  # type: str
                     ):
        # type: (...) -> (str, Dict)
        """
        :param target: target id
        :param resource: target resource field
        :param args: fields for this resource
        :param next_page: next page url
        :return:
        """

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
        # type: (...) -> List[Union[Dict, PageConversation]]
        """
        Retrieve conversations for target page.
        Note:
            This is need page access token and with the scope `pages_messaging`.
        :param page_id: Target page id.
        :param access_token: Page access token
        :param fields: Fields for to get data. None will use default fields.
        :param folder: Folder for conversations. default is `inbox`.
        Accept value are:
            - inbox
            - other
            - page_done
            - pending
            - spam
        :param count: The count will retrieve for the conversation if it is possible. If set None will retrieve all.
        :param limit: Each request will retrieve count for conversation, should no more than 200.
        :param return_json: Set to false will return a list of PageConversation instances.
        Or return json data. Default is false.
        :return: Conversation data list.
        """

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
                resource = "conversations",
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


    def build_path_of_comment(self,
                              target,  # type: str
                              resource,  # type: str
                              post_args  # type: Dict
                              ):
        """
        :param target: target id
        :param resource: target resource field
        :param post_args: fields for this resource
        :return: JSON response
        """       

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
                     object_id,  # type: str
                     access_token,  # type: str
                     message
                     ):
        """
        Post a comment for target object.
        Note:
            This is need page access token and with the scope `pages_manage_engagement`.
        :param object_id: Target object id.
        :param access_token: Page access token.
        :param message: Message to be post as a comment
        :return: JSON response
        """

        post_args = {
            "access_token" : access_token,
            "message" : message
        }

        response = []

        data = self.build_path_of_comment(
            target = object_id, 
            resource = "comments",
            post_args = post_args, 
        )

        response.extend(data)

        return response


    def build_path_of_photo(self,
                            target,  # type: str
                            resource,  # type: str
                            post_args,  # type: Dict
                            files
                            ):
        """
        :param target: target id
        :param resource: target resource field
        :param post_args: fields for this resource
        :return: JSON response
        """       

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
                   files
                   ):
        """
        Post a photo for target page.
        Note:
            This is need page access token with the scope `pages_read_engagement` and `pages_manage_posts`.
        :param page_id: Target page id.
        :param access_token: Page access token.
        :param files: Files for post in page id.
        :return: JSON response.
        """

        post_args = {
            "access_token" : access_token
        }

        response = []

        data = self.build_path_of_photo(
            target = page_id, 
            resource = "photos",
            post_args = post_args,
            files = files 
        )

        response.extend(data)

        return response


if __name__ == '__main__':
    api = ExtApi(long_term_token = "long-term-token")

    con = api.post_photo(
        page_id = constant.PAGE_ID,
        access_token = constant.PAGE_ACCESS_TOKEN,
        files = open("perro-sorprendido.jpg", "rb")
    )

    print(con)