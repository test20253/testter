from Tests.custom_methods.CommonMethods import CommonMethods as CM
from dotenv import load_dotenv

from Tests.custom_methods.SystemActionExecutor import SystemActionExecutor


class MSALTokenEnvironmentProperties:
    properties = {

        "client_id": "d2094542-d036-499d-aa67-0b8e92f4ca39",
        "redirect_uri": "https://eygs.onmicrosoft.com/canvas-automationsuite",
        "ad_instance": "https://login.microsoftonline.com/",
        "url": "https://eygs.onmicrosoft.com/",
        "tenant": "eygs.onmicrosoft.com",
        "username": "",
        "password": "",
    }

    def set_properties(user_name_token: str = 'CanvasAutomationUser1'):
        user_info = SystemActionExecutor()._get_credentials_password(user_name_token)
        MSALTokenEnvironmentProperties.properties['username'] = user_info['userName']
        MSALTokenEnvironmentProperties.properties['password'] = user_info['password']

    def get_all_properties():
        all_properties = MSALTokenEnvironmentProperties.properties
        return all_properties

    def get_properties(environment):
        all_properties = MSALTokenEnvironmentProperties.get_all_properties()
        environment_properties = all_properties[environment]
        return environment_properties

    def get_scopes(environment, token_name):
        properties = MSALTokenEnvironmentProperties.get_properties(environment)
        scopes = properties[token_name] + "/.default"
        scoes_list = scopes.split()
        return scoes_list

    def get_authority():
        all_properties = MSALTokenEnvironmentProperties.properties
        authority = all_properties["ad_instance"] + all_properties["tenant"]
        return authority

    def get_universal_token_scopes_list():
        environment = CM.get_value_in_temp_variable("Environment")
        environment_in_lower_case = environment.lower()
        all_properties = MSALTokenEnvironmentProperties.get_all_properties()
        resource_name = all_properties["url"] + "canvas-" + environment_in_lower_case
        scope = resource_name + "/.default"
        scopes_list = scope.split()
        return scopes_list

    def get_scopes_list(resource_name, user_name_token: str = 'CanvasAutomationUser1'):
        MSALTokenEnvironmentProperties.set_properties(user_name_token)
        scope = resource_name + "/.default"
        scopes_list = scope.split()
        return scopes_list
