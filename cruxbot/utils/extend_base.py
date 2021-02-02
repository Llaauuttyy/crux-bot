import time
import requests

from pyfacebook.error import PyFacebookException, ErrorMessage, ErrorCode
from pyfacebook import BaseApi

class ExtBaseApi(BaseApi):

    def _request(self, 
                 path, 
                 method = "GET", 
                 args = None, 
                 post_args = None, 
                 files = None, 
                 enforce_auth = True
                 ):
        # type: (str, str, Optional[dict], Optional[dict], bool) -> Response
        """
        Build the request and send request to Facebook.
        :param path: The path for resource on facebook.
        :param method: Http methods.
        :param args: GET parameters.
        :param post_args: POST parameters.
        :param enforce_auth: Set to True mean this request need access token.
        :return: The Response instance.
        """

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
                timeout = None,
                params = args,
                data = post_args,
                proxies = self.proxies,
                files = files,
            )
        except requests.HTTPError as e:
            raise PyFacebookException(ErrorMessage(code = ErrorCode.HTTP_ERROR, message = e.args[0]))

        headers = response.headers
        self.rate_limit.set_limit(headers)

        if self.sleep_on_rate_limit:
            sleep_seconds = self.rate_limit.get_sleep_seconds(sleep_data = self.sleep_seconds_mapping)
            time.sleep(sleep_seconds)

        return response      