from Tests.custom_methods.CommonMethods import CommonMethods as CM
from Tests.custom_methods.TokenMethods import TokenMethods as TM
from Tests.filesForTests.Config.MSALTokenEnvironmentProperties import MSALTokenEnvironmentProperties as EnvironmentProperties

from msal import PublicClientApplication
from Tests.Utils.logging.LoggerFactory import Logger
logger = Logger(__name__).get_logger()

class MSALTokenMethods:
    
    @staticmethod
    def _get_public_client_app(clientID, authority):
        publicClientApp = PublicClientApplication(clientID, authority= authority,verify = False)
        return publicClientApp

    @staticmethod
    def _get_token(scopes_list):
        environment = CM.get_value_in_temp_variable("Environment")
        all_properties = EnvironmentProperties.get_all_properties()
        client_id = all_properties["client_id"]
        username = all_properties["username"]
        password = all_properties["password"]
        authority = EnvironmentProperties.get_authority()
        result = ''
        publicClientApp = MSALTokenMethods._get_public_client_app(client_id, authority= authority)
        accounts = publicClientApp.get_accounts(username=username)
        if accounts:
            print("Account(s) exists in cache, probably with token too. Let's try.")
            result = publicClientApp.acquire_token_silent(scopes_list, account=accounts[0])
        elif not result:
            print("No suitable token exists in cache. Let's get a new one from AAD.")
            result = publicClientApp.acquire_token_by_username_password(
                username=username, password=password, scopes=scopes_list)
            token = result["access_token"]
        return token
    
    @staticmethod
    def get_universal_token():
        scopes_list = EnvironmentProperties.get_universal_token_scopes_list()
        token = MSALTokenMethods._get_token(scopes_list)
        return token
    
    @staticmethod
    def get_token(resource_name, token_name, user_name_token: str='CanvasAutomationUser1'):
        scopes_list = EnvironmentProperties.get_scopes_list(resource_name, user_name_token)
        logger.debug(f"trying to get the token from MSAL with the following scopes: {scopes_list}")
        token = TM.get_token(user_name_token)

        if token == None:
            token = MSALTokenMethods._get_token(scopes_list)
            TM._update_token_on_file(token_name=TM.TOKEN_NAME_UNIVERSAL, token_value=token, user_name_token=user_name_token)
            return token
        else:
            return token


