import os
import tempfile
from Tests.custom_methods.APIMethods import APIMethods
from Tests.custom_methods.CommonMethods import CommonMethods
from Tests.custom_methods.TokenMethods import TokenMethods


class APIDeleteContentById:

    def __init__(self, environment, prefix_file_name):

        universal_token = TokenMethods.get_token("CanvasAutomationUser1")
        if universal_token:
            self.token = 'Bearer ' + universal_token
            self.env_variables = CommonMethods.get_app_env_variable(environment)
            files = os.listdir(tempfile.gettempdir())
            self.suite_names = [os.path.splitext(file)[0] for file in files if file.startswith(prefix_file_name)]
            self._delete_instruction()
            self._delete_psp_index()


        else:
            print(f'[WARN] The token is Not valid the instruction were not Deleted')

    def _delete_instruction(self):
        """
        Deletes all global and local instructions stored in the JSON configuration file.
        """

        for suite_name in self.suite_names:

            module_name = CommonMethods.get_engagement_information_from_suite_config(suite_name, 'Content', 'module')
            config_instruction_id = CommonMethods.get_engagement_information_from_suite_config(suite_name, 'Content',
                                                                                               'global_Id')
            auth = self.token
            env_variables = self.env_variables

            if config_instruction_id != '' and module_name == "Group Audit":
                print(f"[INFO] {suite_name}  File name for deletion")
                self.delete_and_approve_deleted_instruction(auth=auth, env_variables=env_variables,
                                                            config_instruction_id=config_instruction_id)

            config_instruction_id = CommonMethods.get_engagement_information_from_suite_config(suite_name, 'Content',
                                                                                               'local_Id')

            if config_instruction_id != '' and module_name == "Group Audit":
                self.delete_and_approve_deleted_instruction(auth=auth, env_variables=env_variables,
                                                            config_instruction_id=config_instruction_id)

    def delete_and_approve_deleted_instruction(self, env_variables, config_instruction_id, auth):

        get_instruction = self.get_entity_response(endpoint='/api/v1/GroupInstruction/',
                                                   config_id=config_instruction_id)
        if get_instruction is not None:

            channel_id = get_instruction['responseBody']['entityList'][0]['authoredChannelId']
            language_id = get_instruction['responseBody']['entityList'][0]['authoredLanguageId']
            service_line_id = get_instruction['responseBody']['entityList'][0]['serviceLineId']

            delete_response = APIMethods.api_request('DELETE', url=env_variables[
                                                                       'universalAPIEndpoint'] + '/api/v1/GroupInstruction/' + config_instruction_id,
                                                     params='', headers="", body='', cookies='', files='', auth=auth,
                                                     timeout='', allow_redirects='', proxies='', verify=False,
                                                     stream='',
                                                     cert='')

            approved_deleted_response = self.approve_deleted_entity(config_id=config_instruction_id,
                                                                    channel_id=channel_id,
                                                                    language_id=language_id,
                                                                    endpoint='/api/v1/groupinstruction/approve',
                                                                    service_line_id=service_line_id, data_entity_id=36)

            if approved_deleted_response['responseStatusCode'] == 201 and delete_response['responseStatusCode'] == 200:
                print(f'[INFO] -- The instruction with Id {config_instruction_id} was DELETED')
        else:
            print(f'[INFO] -- The instruction with Id {config_instruction_id} was DELETED during Execution')

    def get_entity_response(self, endpoint, config_id):

        url_endpoint = self.env_variables['universalAPIEndpoint'] + endpoint + config_id + '?channelId='

        channel = APIMethods.api_request(method='GET',
                                         url=self.env_variables['universalAPIEndpoint'] + '/api/v1/Channels',
                                         params='',
                                         headers="", body='', cookies='', files='', auth=self.token,
                                         timeout='',
                                         allow_redirects='', proxies='', verify=False, stream='',
                                         cert='')
        service_line = APIMethods.api_request(method='GET',
                                              url=self.env_variables['universalAPIEndpoint'] + '/api/v1/ServiceLine',
                                              params='',
                                              headers="", body='', cookies='', files='', auth=self.token,
                                              timeout='',
                                              allow_redirects='', proxies='', verify=False, stream='',
                                              cert='')

        for service_id in range(1, len(service_line['responseBody']) + 1):
            for channel_id in range(1, len(channel['responseBody']) + 1):

                get_entity = APIMethods.api_request('GET', url=url_endpoint + str(
                    channel_id) + "&languageId=1&serviceLineId=" + str(service_id),
                                                    params='',
                                                    headers="", body='', cookies='', files='', auth=self.token,
                                                    timeout='',
                                                    allow_redirects='', proxies='', verify=False, stream='',
                                                    cert='')
                try:
                    if get_entity['responseBody']['entityList'] != []:
                        return get_entity
                except:
                    break

    def approve_deleted_entity(self, config_id, channel_id, language_id, service_line_id, data_entity_id, endpoint):

        pending_approval = APIMethods.api_request('PUT', url=self.env_variables[
                                                                 'universalAPIEndpoint'] + '/api/v1/EntityStatus',
                                                  params='', headers="",
                                                  body={"selectedEntities": [config_id],
                                                        "channelId": channel_id,
                                                        "languageId": language_id,
                                                        "serviceLineId": service_line_id,
                                                        "entityStatusTypeId": "4",
                                                        "dataEntityId": data_entity_id},
                                                  cookies='', files='', auth=self.token,
                                                  timeout='', allow_redirects='', proxies='', verify=False,
                                                  stream='', cert='')

        approved_response = APIMethods.api_request('POST', url=self.env_variables['universalAPIEndpoint'] + endpoint,
                                                   params='', headers="",
                                                   body={"dataEntityUIDs": [config_id],
                                                         "channelId": channel_id,
                                                         "languageId": language_id,
                                                         "serviceLineId": service_line_id},
                                                   cookies='', files='', auth=self.token, timeout='',
                                                   allow_redirects='', proxies='',
                                                   verify=False, stream='', cert='')

        return approved_response

    def _delete_psp_index(self):

        for suite_name in self.suite_names:

            module_name = CommonMethods.get_engagement_information_from_suite_config(suite_name, 'Content', 'module')
            config_psp_index_id = CommonMethods.get_engagement_information_from_suite_config(suite_name, 'Content',
                                                                                             'global_Id')

            if config_psp_index_id != '' and module_name == "PSPIndexes":
                print(f"[INFO] {suite_name} File name for deletion")
                self.delete_and_approve_deleted_psp_index(auth=self.token, env_variables=self.env_variables,
                                                          config_psp_index_id=config_psp_index_id)

            config_psp_index_id = CommonMethods.get_engagement_information_from_suite_config(suite_name, 'Content',
                                                                                             'local_Id')

            if config_psp_index_id != '' and module_name == "PSPIndexes":
                self.delete_and_approve_deleted_psp_index(auth=self.token, env_variables=self.env_variables,
                                                          config_psp_index_id=config_psp_index_id)

    def delete_and_approve_deleted_psp_index(self, env_variables, config_psp_index_id, auth):

        get_psp_index = self.get_entity_response(endpoint='/api/v1/pspindex/', config_id=config_psp_index_id)

        if get_psp_index is not None:

            channel_id = get_psp_index['responseBody']['entityList'][0]['authoredChannelId']
            language_id = get_psp_index['responseBody']['entityList'][0]['authoredLanguageId']
            service_line_id = get_psp_index['responseBody']['entityList'][0]['serviceLineId']

            delete_url = env_variables[
                             'universalAPIEndpoint'] + '/api/v1/PSPIndex/' + config_psp_index_id + '?DeleteType=delete&channelId=' + str(
                channel_id) + "&languageId=1&serviceLineId=" + str(service_line_id)

            delete_response = APIMethods.api_request('DELETE', url=delete_url,
                                                     params='',
                                                     headers="", body='', cookies='', files='', auth=auth,
                                                     timeout='', allow_redirects='', proxies='', verify=False,
                                                     stream='',
                                                     cert='')

            approved_deleted_response = self.approve_deleted_entity(config_id=config_psp_index_id,
                                                                    channel_id=channel_id,
                                                                    language_id=language_id,
                                                                    endpoint='/api/v1/pSPIndex/approve',
                                                                    service_line_id=service_line_id, data_entity_id=33)

            if approved_deleted_response['responseStatusCode'] == 201 and delete_response['responseStatusCode'] == 200:
                print(f'[INFO] -- The psp index with Id {config_psp_index_id} was DELETED')

        else:
            print(f'[INFO] -- The psp index with Id {config_psp_index_id} was DELETED during Execution')
