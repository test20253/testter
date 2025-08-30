import json
import subprocess
import sys
from typing import Dict
from robot.utils.asserts import assert_equal
from scriptless.Core.library.common.CustomBase import CustomBase
import urllib3
from scriptless.Core.framework.data_handler import Data_handler
from Tests.Utils.TokensUsers import TokensUsers
from Tests.Utils.tokens.TokenNames import TokenNames
from Tests.Utils.decorators.RetryDecorators import retry, silent_retry_with_default
from Tests.custom_methods.TokenMethods import TokenMethods
from urllib.parse import urlencode
from Tests.resources.constants.Endpoints import Endpoints
from Tests.resources.constants.api.artemis.ArtemisEndpoints import ArtemisEndpoints


class BaseAPIClass:
    API_UNIVERSAL = Data_handler().get_env_var_value("universalAPIEndpoint")
    API_ARTEMIS = Data_handler().get_env_var_value("artemisAPIEndpoint")

    HEADERS = {
        "Authorization": "your_token",
        "User-Agent": "Canvas Automation"
    }

    METHOD_GET = "GET"
    METHOD_POST = "POST"
    METHOD_PUT = "PUT"
    METHOD_PATCH = "PATCH"
    METHOD_DELETE = "DELETE"

    STATUS_CODE_200 = 200
    STATUS_CODE_204 = 204
    STATUS_CODE_201 = 201

    def __init__(self):
        self.custom_base = CustomBase()
        self.endpoints = Endpoints()
        self.artemis_endpoints = ArtemisEndpoints()

    def get_headers(self, token_name, user_name='CanvasAutomationUser1'):
        headers = self.HEADERS.copy()
        headers["Authorization"] = "Bearer " + TokensUsers.get_token(user_name, token_name)
        return headers

    def get_headers_v2(self, token_name: TokenNames, user_name_token='CanvasAutomationUser1'):
        from Tests.custom_methods.TokenMethodsV2 import TokenMethodsV2
        headers = self.HEADERS.copy()
        headers["Authorization"] = "Bearer " + TokenMethodsV2().get_token(user_name_token=user_name_token,
                                                                          token_name=token_name)

        return headers

    def add_params_to_url(self, url, params):
        if params:
            query_string = urlencode(params)
            url = f"{url}?{query_string}"
        return url

    @silent_retry_with_default(default_return_value=None, retries=3, retry_delay=2, exceptions=(Exception,), error_message="Max retries exceeded")
    def make_api_request(self, method, url, params=None, json=None, verify=False, headers=None):
        response = None
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = self.custom_base.get_restapi_instance().apirequest(
                method=method,
                url=url,
                json=json,
                verify=verify,
                headers=headers,
                params=params
            )
        except:
            response = self.custom_base.get_restapi_instance().apirequest(
                method=method,
                url=url,
                json=json,
                verify=verify,
                headers=headers,
                params=params
            )
        finally:
            pass

        return response

    def validate_response_status_code(self, response, expected_status_code):
        self.custom_base.log_message(
            f'{sys._getframe(1).f_code.co_name}() method status code: {response["status_code"]}')
        assert_equal(response["status_code"], expected_status_code, f"Status code should be {expected_status_code}")

    def make_api_request_power_shell(self, url: str, method: str, headers: Dict[str, str],
                                     params: Dict[str, str] = None, body: Dict[str, str] = None) -> Dict[str, str]:
        """
        Perform an API request using PowerShell.

        Args:
            url (str): The URL of the API to which the request will be made.
            method (str): The HTTP method to be used for the request (e.g., 'GET', 'POST', 'PUT', 'DELETE', etc.).
            headers (Dict[str, str]): A dictionary containing the HTTP headers in key-value format.
            params (Dict[str, str], optional): A dictionary containing request parameters in key-value format. Default is None.
            body (Dict[str, str], optional): A dictionary containing the request body in key-value format. Default is None.

        Returns:
            Dict[str, str]: A dictionary containing the API response in JSON format.

        """
        headers = json.dumps(headers)
        url = self.add_params_to_url(url, params).replace('&', '"&"') if params is not None else url
        body = json.dumps(body) if body is not None else ""

        powershell_comand = f"./Resources/ApiRequestScript.ps1 -url {url} -method {method} -headers '{headers}'"

        if body:
            powershell_comand = f"./Resources/ApiRequestScript.ps1 -url {url} -method {method} -headers '{headers}' -body '{body}'"

        result = subprocess.run(['powershell.exe', '-Command', powershell_comand], stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        powershell_response = json.loads(result.stdout)
        return powershell_response

    def console_response_log(self, response):
        self.custom_base.log_message(
            f'{sys._getframe(1).f_code.co_name}() method actual status code: {response["status_code"]}')
        if response.get('errors') is not None:
            self.custom_base.log_message(
                f'{sys._getframe(1).f_code.co_name}() error message is: {response["errors"]}')