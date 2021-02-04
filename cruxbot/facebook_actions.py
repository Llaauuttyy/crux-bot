from typing import Dict, List, Optional, Union, Tuple, Set

from pyfacebook.utils.param_validation import enf_comma_separated

from facebook import GraphAPI, GraphAPIError
from pyfacebook import Api


DEFAULT_CONVERSATION_FIELDS = [
    "id", "link", "snippet", "updated_time", "message_count",
    "unread_count", "participants", "senders", "can_reply",
    "is_subscribed"
]

DEFAULT_MESSAGE_FIELDS = [
    "created_time", "from", "id", "message", "tags", "to"
]

def path_builder(api,  # type: Api
                 target,  # type: str
                 resource,  # type: str
                 method = "GET",  # type: str
                 args = None,  # type: Dict 
                 post_args = None,  # type: Dict
                 enforce_auth = True  # type: bool
                 ):

    response = api._request(
        path = "{version}/{target}/{resource}".format(
            version = api.version,
            target = target,
            resource = resource
        ),
        method = method,
        args = args,
        post_args = post_args,
        enforce_auth = enforce_auth
    )

    data = api._parse_response(response)

    return data


def page_by_next(api,  # type: Api
                 target,  # type: str
                 resource,  # type: str
                 args,  # type: Dict
                 next_page,  # type: str
                 ):

    if next_page is not None:
        response = api._request(
            path = next_page
        )

    else:
        response = api._request(
            path = "{version}/{target}/{resource}".format(
                version = api.version,
                target = target,
                resource = resource
            ),
            args = args
        )

    next_page = None
    data = api._parse_response(response)

    if "paging" in data:
        next_page = data["paging"].get("next")

    return next_page, data


def get_posts(api,  # type: Api
              user_id  # type: str
              ):
    # Se llama a un método del objeto Api, el cual nos devuelve los posteos hechos por
    # el usuario, en su muro.
    # Hay algunos filtros que se pueden pasar por parámetro, para manipular que
    # información se desea obtener.
    data = api.get_page_posts(
        page_id = user_id,
        since_time = "2020-05-01",
        limit = 100,
        return_json = True,
    )

    return data


def get_comments(api,  # type: Api
                 object_id  # type: str
                 ):

    data = api.get_comments_by_object(
        object_id = object_id,
        count = None,
        limit = 100,
        return_json = True,
    )

    return data


def get_page_conversations(api,  # type: Api
                           page_id,  # type: str
                           fields = None,  # type: Optional[Union[str, List, Tuple, Set]]
                           folder = "inbox",  # type: str
                           count = 10,  # type: Optional[int]
                           limit = 200  # type: int,
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
        fields = DEFAULT_CONVERSATION_FIELDS

    args = {
        "access_token": api._access_token,
        "fields": enf_comma_separated("fields", fields),
        "folder": folder,
        "limit": limit
    }

    conversations = []
    next_page = None

    while True:
        next_page, data = page_by_next(
            api = api,
            target = page_id, 
            resource = "conversations",
            args = args, 
            next_page = next_page
        )

        data = data.get("data", [])

        conversations.extend(data)

        if count is not None:
            conversations = conversations[:count]
            break
        if next_page is None:
            break

    return conversations


def get_conversation_messages(api,  # type: Api
                              conversation_id,  # type: str
                              fields = None,  # type: Optional[Union[str, List, Tuple, Set]]
                              count = 10,  # type: Optional[int]
                              limit = 200,  # type: int
                              ):

    # PRE: Receives parameters who allows us to customize our request.
    # POST: Calls functions and manages its responses,
    #       in order to return the messages amount we established.

    if fields is None:
        fields = DEFAULT_MESSAGE_FIELDS

    args = {
        "access_token": api._access_token,
        "fields": enf_comma_separated("fields", fields),  # enf_comma_separated basically filters
        "limit": limit                                    # the fields we passed by parameter.
    }

    messages = []
    next_page = None

    while True:
        next_page, data = page_by_next(
            api = api,
            target = conversation_id, 
            resource = "messages",  # messages is an important resource.
            args = args, 
            next_page = next_page
        )
        data = data.get("data", [])

        messages.extend(data)

        messages = messages[:count]  # It just leaves the messages amount we want.

        if count is not None:
            messages = messages[:count]
            break
        if next_page is None:
            break

    return messages


def post_comment(api,  # type: Api
                 post_id,  # type: str
                 message  # type: str
                 ):

    post_args = {
        "access_token": api._access_token,
        "message": message
    }

    data = path_builder(
        api = api,
        target = post_id,
        resource = "comments",
        post_args = post_args
    )

    return data
    
 
def post_publication(api,  # type: Api
                     page_id,  # type: str
                     message  # type: str  
                     ):

    post_args = {
        "access_token": api._access_token,
        "message": message
    }

    data = path_builder(
        api = api,
        target = page_id,
        resource = "feed",
        post_args = post_args
    )

    return data


def post_like(api,  # type: Api
              object_id  # type: str
              ):

    post_args = {
        "access_token": api._access_token
    }

    data = path_builder(
        api = api,
        target = object_id,
        resource = "likes",
        post_args = post_args
    )

    return data


def post_photo(api,  # type: GraphAPI
               page_id,  # type: str
               image
               ):

    data = api.put_photo(
        image = image,
        album_path = "{0}/photos/picture".format(page_id)
    )

    return data


def post_profile_photo(api,  # type: GraphAPI
                       page_id,  # type: str
                       image
                       ):

    try:
        data = api.put_photo(
            image = image,
            album_path = "{0}/picture".format(page_id)
        )
    except GraphAPIError as error:
        data = error

    return data


def delete_publication(api,  # type: Api
                       post_id  # type: str
                       ):

    args = {
        "access_token": api._access_token,
    }

    data = path_builder(
        api = api,
        target = post_id,
        resource = "",  # It has to be empty.
        method = "DELETE",
        args = args,
        enforce_auth = False
    )

    return data