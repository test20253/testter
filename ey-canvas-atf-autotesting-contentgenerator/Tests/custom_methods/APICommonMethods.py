from Tests.Utils.decorators.HeadersDecorator import add_headers
from Tests.Utils.tokens.TokenNames import TokenNames
from Tests.custom_methods.BaseClass.BaseAPIClass import BaseAPIClass
from Tests.custom_methods.DateMethods import DateMethods
from Tests.custom_methods.TokenMethods import TokenMethods
from typing import Dict
from Tests.custom_methods.CommonMethods import CommonMethods as CM



class APICommonMethods(BaseAPIClass):

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_channel(self, headers={}, user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches the existing form data
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.SELECT_CHANNEL()
        url = base_uri + path_parameter
        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers)
        CM.validate_if_channel_language_file_already_exists(label="channel", response=response)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_channel_language(self, channel_id, headers={}, user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches the existing form data
        """

        if headers is None:
            headers = {}
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.SELECT_CHANNEL_LANGUAGE()
        url = base_uri + path_parameter
        params = {
            "Active": "true",
            "ChannelId": channel_id

        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers)
        CM.validate_if_channel_language_file_already_exists(label="language", response=response)
        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_service_line(self, headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches the existing form data
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.SELECT_SERVICE_LINE()
        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers)
        CM.validate_if_channel_language_file_already_exists(label="service_line", response=response)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def get_service_organisation(self, user_name_token: str = 'CanvasAutomationUser1', headers={}) -> Dict[str, any]:
        """
        This method fetches the existing form data
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_SERVICE_ORGANIZATION()
        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers)
        CM.validate_if_channel_language_file_already_exists(label="service_org", response=response)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def add_cg_user(self, first_name: str, last_name: str, user_name: str,
                    headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
                This method adds the user in cg application
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.SEARCH_CG_USER()
        url = base_uri + path_parameter
        body = {
            "multiple": "true",
            "newUsers": [
                {
                    "domainId": user_name,
                    "firstName": first_name,
                    "lastName": last_name,
                    "displayName": first_name + " " + last_name,
                    "emailAddress": user_name,
                    "contactPhone": ""
                }
            ]
        }

        response = self.make_api_request(method=self.METHOD_POST, url=url, headers=headers, json=body)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def revoke_cg_user_role(self, user_id: int = 199, headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
                        This method revokes the user roles
                """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.REVOKE_CG_USER_ROLE(user_id)
        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_DELETE, url=url, headers=headers)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def add_user_role_for_current_user(self, channel_id: int, organisation_id: int, role_id: int,
                                       module_id: int, service_line_id: int, language_id: int, user_id: int = 243,
                                    user_name_token: str = 'CanvasAutomationUser1',headers={}) -> Dict[str, any]:
        """
            This method adds corresponding role for the user
        """

        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.ADD_CG_USER()
        url = base_uri + path_parameter
        body = {
            "userId": user_id,
            "serviceModuleId": module_id,
            "serviceLineId": service_line_id,
            "serviceOrganizationId": organisation_id,
            "roleId": role_id,
            "channelId": channel_id,
            "languages": [language_id],
            "IncludeSubChannel": "false"
        }

        response = self.make_api_request(method=self.METHOD_POST, url=url, headers=headers, json=body)
        self.custom_base.log_message(response)
        self.custom_base.log_message(headers)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def revoke_cg_user_access(self, organisation_id: int, role_id: int, module_id: int, service_line_id: int,
                              user_id: int = 243, headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.REVOKE_CG_USER_ACCESS()
        url = base_uri + path_parameter
        body = {
            "ModuleId": module_id,
            "ServiceLineId": service_line_id,
            "OrganizationId": organisation_id,
            "RoleId": role_id,
            "UserId": user_id
        }

        response = self.make_api_request(method=self.METHOD_DELETE, url=url, headers=headers, params=body)
        self.console_response_log(response=response)
        return response


    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def get_user_id_for_logged_user(self, user_name: str, headers = {}, user_name_token: str = 'CanvasAutomationUser1',) -> Dict[str, any]:
        

        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.SEARCH_CG_USER()
        url = base_uri + path_parameter
        body = {
            "myInfo": "true",
            "skip": 0,
            "take": 100,
            "includeInactive": "false",
            "search": user_name,
            "searchType": 2
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=body)
        CM.validate_if_channel_language_file_already_exists(label="user", response=response)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def get_user_roles_for_user(self, user_id, headers={}, user_name_token='CanvasAutomationUser1') -> Dict[str, any]:
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_USER_ROLES_FOR_USER(user_id)
        url = base_uri + path_parameter
        body = {
            "skip": 0,
            "take": 100,
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=body)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_service_module(self, headers={},user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
                        This method revokes the user roles
                """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.SELECT_SERVICE_MODULE()
        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers)
        CM.validate_if_channel_language_file_already_exists(label="module", response=response)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_metadata_tag(self, headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches metadata tags for psp index
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_METADATA_TAG()
        url = base_uri + path_parameter
        params = {
            "Active": "true"
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_atlas_guidance_type(self, headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches types of atlas guidance
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_ATLAS_GUIDANCE_TYPE()
        url = base_uri + path_parameter
        params = {
            "Active": "true"
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_service_for_atlas_guidance_type(self, guidance_type_id: int,
                                               headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches services id for selected type of atlas guidance using guidance type id
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GUIDANCE_SERVICE()
        url = base_uri + path_parameter
        params = {
            "IsActive": "true",
            "guidanceTypeId": guidance_type_id
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def select_service_line_for_all_type(self, headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches the existing form data
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.SELECT_SERVICE_LINE_FOR_ALL()
        url = base_uri + path_parameter
        params = {
            "IsActiveOnly": "true"
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def get_service_organisation_for_type_all(self, servicemoduleId, user_name_token: str = 'CanvasAutomationUser1',headers={} ) -> Dict[str, any]:
        """
        This method fetches the existing form data
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_SERVICE_ORGANIZATION_FOR_ALL()
        url = base_uri + path_parameter
        params = {
            "ServiceModuleId": servicemoduleId,
            "IsActive":"true"
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def get_channels_languages_for_user(self, user_id: str, module_id: str, organisation_id: str, role_id: str, service_line_id: str,
                                     headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method gets channels and languages assigned for specific user
        Args:
                channel_id ,language_id                  : labels where risk factor data fetched
        Return
                Dict[str, any]: contains API Response
        """

        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_CHANNELS_LANGUAGES_FOR_USER(user_id)
        url = base_uri + path_parameter
        params = {
            "moduleId": module_id,
            "organizationId": organisation_id,
            "roleId": role_id,
            "serviceLineId": service_line_id
        }

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def get_atlas_guidance_profile_answers_inclusion_id(self, channel_id: str, guidance_id: str, data_entity_id: str,
                                                        data_entity_uid: str,
                                                    headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches inclusion id for selected channel language service line combination

            Args:
                    channel_id                            : ID of the channel label
                    data_entity_uid                       : Represents the body ID.
                    guidance_id,
                    data_entity_id                        : IDs required for creating the request body.

            Returns:
                    Dict[str, any]                        : Dictionary containing the API response
        """

        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION_ID(guidance_id=guidance_id,
                                                                                       data_entity_id=data_entity_id,
                                                                                       data_entity_uid=data_entity_uid)

        params = {"channelId": channel_id}

        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def get_atlas_guidance_profile_answers_exclusion_id(self, channel_id: str, guidance_id: str, data_entity_id: str,
                                                        data_entity_uid: str,
                                                  headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method fetches exclusion id for selected channel language service line combination

            Args:
                    channel_id                            : ID of the channel label
                    data_entity_uid                       : Represents the body ID.
                    guidance_id,
                    data_entity_id                        : IDs required for creating the request body.

            Returns:
                    Dict[str, any]                        : Dictionary containing the API response
        """

        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.GET_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION_ID(guidance_id=guidance_id,
                                                                                       data_entity_id=data_entity_id,
                                                                                       data_entity_uid=data_entity_uid)

        params = {"channelId": channel_id}

        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_GET, url=url, headers=headers, params=params)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def remove_localization_from_atlas_guidance_profile_inclusion(self, guidance_id, data_entity_uid,
                                                                  data_entity_id, inclusion_id,
                                                       headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method removes the localized atlas guidance profile inclusion answers

        Args:
                data_entity_uid                                : Represents the body ID.
                guidance_id,
                data_entity_id,
                inclusion_id                                   : IDs required for creating the request body.

        Returns:
              Dict[str, any]                                   : Dictionary containing the API response
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_INCLUSION(guidance_id=guidance_id,
                                                                                       data_entity_id=data_entity_id,
                                                                                       data_entity_uid=data_entity_uid,
                                                                                       inclusion_id=inclusion_id)
        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_DELETE, url=url, headers=headers)
        self.console_response_log(response=response)
        return response

    @add_headers(TokenNames.TOKEN_NAME_UNIVERSAL)
    def remove_localization_from_atlas_guidance_profile_exclusion(self, guidance_id, data_entity_uid,
                                                                  data_entity_id, exclusion_id,
                                                       headers={} ,user_name_token: str = 'CanvasAutomationUser1') -> Dict[str, any]:
        """
        This method removes the localized atlas guidance profile exclusion answers

        Args:
                data_entity_uid                                : Represents the body ID.
                guidance_id,
                data_entity_id,
                exclusion_id                                   : IDs required for creating the request body.

        Returns:
              Dict[str, any]                           : Dictionary containing the API response
        """
        
        base_uri = self.API_UNIVERSAL
        path_parameter = self.endpoints.REMOVE_ATLAS_GUIDANCE_PROFILE_ANSWER_EXCLUSION(guidance_id=guidance_id,
                                                                                       data_entity_id=data_entity_id,
                                                                                       data_entity_uid=data_entity_uid,
                                                                                       exclusion_id=exclusion_id)
        url = base_uri + path_parameter

        response = self.make_api_request(method=self.METHOD_DELETE, url=url, headers=headers)
        self.console_response_log(response=response)
        return response
