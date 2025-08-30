from datetime import datetime, timedelta
from scriptless.Core.library.common.CustomBase import CustomBase
from Tests.Utils.tokens.TokenNames import TokenNames
from Tests.Utils.tokens.TokenAPI import TokenAPI
from Tests.custom_methods.CommonMethods import CommonMethods
from Tests.custom_methods.MSALTokenMethods import MSALTokenMethods
from Tests.Utils.logging.LoggerFactory import Logger
logger = Logger(__name__).get_logger()

class TokenMethodsV2(CustomBase):

    def get_token(self, token_name: TokenNames,
                  user_name_token='CanvasAutomationUser1'):
        """

        Args:
            token_name: One of the values of the enum Tests/Utils/tokens/TokenNames.py
            engagement_data: dictionary with the following keys of the given engagement:

                                "incountry_app_uri"
                                "incountry_app_audience"
                                "hercules_app_audience"
                                "hercules_app_uri"

                             Not mandatory for tokens that are having static tenant url, E.g: UNIVERSAL
                             Note:A method called get_engagement_full_data in Tests/Utils/EngagementData.py exist and will return the needed data in the format this method is expecting

            user_name_token: user_name in the forma of the .env file E.g: CanvasAutomationUser1

        Returns:
            Bearer token
        """

        token_api = TokenAPI()

        urls_for_msal = self.get_url_for_msal_request_for_a_token_name(token_name=token_name)

        body = {
            "user": user_name_token,
            "token_name": str(token_name),
            "location_url": urls_for_msal["location_url"]
            }
        logger.info("urls")
        logger.info(urls_for_msal)

        token_info = token_api.get_token(body)

        if token_info is None:
            logger.info(f"Token not found, trying to get a new one... using this information: {body}")
            token_info=self.create_token(token_name=token_name,user_name_token=user_name_token)
        else:
            logger.info(f"Token found, checking if expired")
            token_info = self.refresh_token_if_expired(token_info=token_info)

        return token_info["token"]



    def create_token(self, token_name: TokenNames,
                  user_name_token='CanvasAutomationUser1'):
        """
        Create the token doing the API call to MSAL and save the token in pysondb
        Args:
            token_name: One of the values of the enum TokenNames
            engagement_data: dict with the following keys: location_url and resource name
            user_name_token: username in the .env E.g CanvasAutomationUser1

        Returns:
            Used body for creating the token with the following structure
            body = {
                "user": user_name_token,
                "token_name": str(token_name),
                "location_url": urls_for_msal["location_url"],
                "resource_name":urls_for_msal["resource_name"],
                "token":token
            }
        """
        token_api = TokenAPI()
        urls_for_msal = self.get_url_for_msal_request_for_a_token_name(token_name=token_name)
        token = MSALTokenMethods().get_token(resource_name=urls_for_msal["resource_name"],token_name=token_name,user_name_token=user_name_token)
        body = {
            "user": user_name_token,
            "token_name": str(token_name),
            "location_url": urls_for_msal["location_url"],
            "resource_name":urls_for_msal["resource_name"],
            "token":token
        }
        token_api.post_token(body)
        return body

    def refresh_token_if_expired(self, token_info):
        """
        check token_expiration_time in pyson and if it is greater than the actual time, will generate a new one and update the token in pyson
        Args:
            token_info: dictionary with the following keys:
                        user
                        token_name
                        location_url
                        resource_name
                        token

        Returns:
            None
        """
        token_api = TokenAPI()
        token_expiration_time = datetime.strptime(token_info["expiration_time"], "%m/%d/%Y, %H:%M:%S")
        now = datetime.now()

        if now > token_expiration_time:
            logger.info(f"Token expired, getting a new one from MSAL")
            token = MSALTokenMethods().get_token(token_info["resource_name"], token_info["user"])
            body = {
                "user": token_info["user"],
                "token_name": token_info["token_name"],
                "location_url": token_info["location_url"],
                "token": token,
                "creation_time": now.strftime("%m/%d/%Y, %H:%M:%S"),
                "expiration_time": (now + timedelta(minutes=40)).strftime("%m/%d/%Y, %H:%M:%S")
            }
            token_api.put_token(body)
            token_info =body
        else:
            logger.info(f"Token is not expired")
        return token_info



    def get_url_for_msal_request_for_a_token_name(self, token_name: TokenNames):
        """

        Args:
            token_name: One of the values of the enum Tests/Utils/tokens/TokenNames.py
            engagement_data: dictionary with the following keys of the given engagement:

                                "incountry_app_uri"
                                "incountry_app_audience"
                                "hercules_app_audience"
                                "hercules_app_uri"

                             Not mandatory for tokens that are having static tenant url, E.g: UNIVERSAL
                             Note:A method called get_engagement_full_data in Tests/Utils/EngagementData.py exist and will return the needed data in the format this method is expecting
        Returns:
            dictionary with the needed urls for get the MSAL token E.g
            {
                "location_url": "https://eycanvascoreapi-euw-uat3.eyua.net",
                "resource_name": "https://eygs.onmicrosoft.com/canvas-uat3-nor",
            }
        """
        logger.info("getting tenant urls for get msal token")
        env_variables = CommonMethods().get_app_env_variable(self.get_current_environment())
        try:
            if token_name == TokenNames.TOKEN_NAME_UNIVERSAL:
                location_url = env_variables["universalAPIEndpoint"]
                resource_name = env_variables["cgTenent"]


        except KeyError as e:
            logger.error(msg=f"error trying to get URLs for MSAL, from scriptless env vars: {str(e)}")
            raise e
        except Exception as e:
            logger.error(msg=f"error trying to get URLs for MSAL, please check you are sending proper engagement_data as per of the method TokenMethodsV2.get_url_for_msal_request_for_a_token_name method documentation: {str(e)}")
            raise e

        urls_for_msal={"location_url": location_url, "resource_name": resource_name}
        logger.debug(f"urls for tenant url to get msal token {urls_for_msal}")
        return urls_for_msal
