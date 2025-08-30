import json
import threading
from Tests.Utils.TokensUsers import TokensUsers
from Tests.custom_methods.APIMethods import APIMethods
from Tests.custom_methods.CommonMethods import CommonMethods as CM
from datetime import datetime, timedelta
import os
from selenium.webdriver import Chrome, ChromeOptions
from Tests.custom_methods.SeleniumMethods import SeleniumMethods as SM
from Tests.custom_methods.LogInMethods import LogInMethods as LM
from selenium.webdriver.common.keys import Keys
from time import sleep
from scriptless.Core.framework.data_handler import Data_handler
import re
import threading

class TokenMethods:

    TOKEN_NAME_UNIVERSAL = "CGTOKEN"


    _TOKEN_LOCK = threading.Lock()
    
    @staticmethod
    def get_token_from_Browser(driver,token_name, user_name_token ='CanvasAutomationUser1'):
        sleep(10)
        token_value = TokenMethods._get_correct_token_from_local_storage(driver, token_name)
        country_code = ''
        TokenMethods._update_token_on_file(token_name,token_value,country_code)
        TokensUsers.set_token(user_name_token,token_name,token_value)
        return token_value

    @staticmethod
    def update_token(user_name_token, token_name, token_value):
        TokensUsers.set_token(user_name_token, token_name, token_value)
    
    def _update_token_on_file(token_name,token_value,user_name_token):
        
        with TokenMethods._TOKEN_LOCK:
            now = datetime.now()
            

            if TokenMethods._validate_if_token_file_already_exists() == False:
                TokenMethods._create_token_file()
            now_string = now.strftime("%Y%m%d%H%M%S%f")
            tokens_information = CM.read_json_file("Tests/filesForTests/temp_api/token_handler.json")
            tokens_information[user_name_token] = {
                    "duration": 3500,
                    "creation_time": now_string,
                    "value": token_value,
            }
            #if engagement_name != "" and engagement_name != None:
            #    tokens_information[token_name]["country_code"] = country_code
            #    tokens_information[token_name]["engagements"].append(engagement_name)
            file_name = f"token_handler.json"
            CM.write_json_file(f"Tests/filesForTests/temp_api/{file_name}", tokens_information)

    @staticmethod
    def _validate_if_token_file_already_exists():
        if os.path.exists("Tests/filesForTests/temp_api/token_handler.json"):
            return True
        return False
    
    @staticmethod
    def _create_token_file():
        empty_token_file = {}
        TokenMethods._create_dir_if_token_dir_already_exists()
        CM.write_json_file("Tests/filesForTests/temp_api/token_handler.json", empty_token_file)

    @staticmethod
    def _create_dir_if_token_dir_already_exists():
        newpath = 'Tests/filesForTests/temp_api' 
        if not os.path.exists(newpath):
            os.makedirs(newpath)

    @staticmethod
    def _validate_if_valid_token_already_exists(token_name, engagement_name):
        token_information = CM.read_json_file("Tests/filesForTests/temp_api/token_handler.json")
        if engagement_name == "" or engagement_name == None:
            if token_name in token_information:
                return True
        else:
            for token, token_value in token_information.items():
                if token_name in token:
                    if engagement_name in token_value["engagements"]:
                        return True
        return False
    
    @staticmethod
    def _get_token_information(token_name):
        token_information = CM.read_json_file("Tests/filesForTests/temp_api/token_handler.json")

        if token_name in token_information:
            return token_information[token_name]

    @staticmethod
    def _check_if_token_is_expired(token_name):
        token_information = TokenMethods._get_token_information(token_name)
        now = datetime.now()
        created_date_token = datetime.strptime(token_information["creation_time"], "%Y%m%d%H%M%S%f")
        expiration_date_token = created_date_token + timedelta(seconds=(int(token_information["duration"]) - 600))
        if now > expiration_date_token:
            return True
        return False
    
    @staticmethod
    def _generate_token_and_add_token_info_to_file(token_name, engagement_name):
        driver = TokenMethods._start_web_driver_sso_and_go_to_the_correct_page(token_name, engagement_name)
        if (engagement_name != "" and engagement_name != None):
            engagement_country_code = TokenMethods._get_country_code_of_engagement(driver, engagement_name)
            token_name = token_name.split("-")[0] + "-" + engagement_country_code
            if TokenMethods._validate_if_valid_token_already_exists(token_name, "") == True:
                if TokenMethods._check_if_token_is_expired(token_name, engagement_name) == False:
                    tokens_information = CM.read_json_file("Tests/filesForTests/temp_api/token_handler.json")
                    tokens_information[token_name]["engagements"].append(engagement_name)
                    file_name = f"token_handler.json"
                    CM.write_json_file(f"Tests/filesForTests/temp_api/{file_name}", tokens_information)
                    return None
        country_code = TokenMethods._get_country_code_from_token_name(token_name)
        TokenMethods._go_to_correct_url_for_token_generation(driver, token_name)
        duration = 3500
        token_value = TokenMethods._get_correct_token_from_local_storage(driver, token_name)
        driver.quit()
        now = datetime.now()
        now_string = now.strftime("%Y%m%d%H%M%S%f")
        tokens_information = CM.read_json_file("Tests/filesForTests/temp_api/token_handler.json")
        tokens_information[token_name] = {
                "duration": duration,
                "creation_time": now_string,
                "value": token_value,
                "country_code": country_code,
                "engagements": []
            }
        if engagement_name != "" and engagement_name != None:
            tokens_information[token_name]["country_code"] = country_code
            tokens_information[token_name]["engagements"].append(engagement_name)
        file_name = f"token_handler.json"
        CM.write_json_file(f"Tests/filesForTests/temp_api/{file_name}", tokens_information)

    @staticmethod
    def _get_country_code_from_token_name(token_name):
        token_name_splitted = token_name.split("-")
        if len(token_name_splitted) == 1:
            return ""
        else:
            return token_name_splitted[1]

    @staticmethod
    def _run_query_and_add_token_info_to_file(local_storage_key_query, token_name, duration):
        local_storage_key_query = local_storage_key_query.replace("default:", "")
        if "UNIVERSAL" == token_name:
            driver = TokenMethods._start_web_driver_sso_and_go_to_the_correct_page(token_name)
            token_value, expire_date = TokenMethods._generate_universal_token(driver, local_storage_key_query)
        if "HERCULES-" in token_name:
            driver = TokenMethods._start_web_driver_sso_and_go_to_the_correct_page(token_name)
            token_value, expire_date = TokenMethods._generate_universal_token(driver, local_storage_key_query)
        now = datetime.now()
        now_string = now.strftime("%Y%m%d%H%M%S%f")
        tokens_information = CM.read_json_file("Tests/filesForTests/temp_api/token_handler.json")
        tokens_information[token_name] = {
                "duration": duration,
                "creation_time": now_string,
                "value": token_value
            }
        file_name = f"token_handler.json"
        CM.write_json_file(f"Tests/filesForTests/temp_api/{file_name}", tokens_information)

    @staticmethod
    def _get_country_code_of_engagement(driver, engagement_name):
        SM.wait_for_element_visibility_by_xpath(driver, "//section[contains(text(),'Dummy Client for Canvas Testing')]")
        search_box = SM.wait_for_element_to_be_clickeable_by_xpath(driver, "//input[@type='search']")
        SM.input_text_on_webelement(search_box, f"{engagement_name}")
        SM.input_text_on_webelement(search_box, Keys.ENTER)
        SM.wait_for_a_certain_amount_of_elements(driver, f"//div[text()='{engagement_name}']", 1, 60)
        SM.wait_for_element_visibility_by_xpath(driver, "//section[contains(text(),'Dummy Client for Canvas Testing')]")
        try:
            SM.wait_for_configurable_element_visibility_by_xpath(driver, "//div[@class='motif-timeline']", 15)
        except Exception:
            pass
        engagement_box = SM.get_webelement_by_xpath(driver, "//li[1]//section[contains(@class,'engagementname')]//a")
        #engagement_box = SM.get_webelement_by_xpath(driver, "//li[1]//section[contains(text(),'Dummy Client for Canvas Testing')]")
        hercules_url = SM.get_attribute_of_webelement(engagement_box, "href")
        if hercules_url == None:
            incountryuri = TokenMethods.get_incountryuri_from_get_home_json(driver,"UNIVERSAL",engagement_name)
            hercules_url = incountryuri
        country_code = hercules_url.split("eycanvascore-")[1].split("-")[0]
        return country_code

    @staticmethod
    def _go_to_correct_url_for_token_generation(driver, token_name):
        if "HERCULES-" in token_name:
            hercules_url = TokenMethods.get_token_url(token_name)
            driver.get(hercules_url)
            SM.wait_for_element_visibility_by_xpath(driver, '//span[@class="error-message"]')
            sleep(5)
            

    @staticmethod
    def _generate_local_storage_key_query(key_without_permissions, userPermissions, token_name):
        if "HERCULES-" in token_name:
            environment = CM.get_value_in_temp_variable("Environment")
            env_variables = CM.get_app_env_variable(environment)
            hercules_env = token_name.split("HERCULES-")[1]
            userPermissions = env_variables[f"userPermissions-{hercules_env}"]
        key_without_permissions = key_without_permissions.replace("default:", "")
        local_storage_key = f"return window.localStorage.getItem('{key_without_permissions}-{userPermissions}')"
        return local_storage_key

    @staticmethod
    def _generate_universal_token(driver, local_storage_key_query):
        storage_response = driver.execute_script(local_storage_key_query)
        storage_response_dict = json.loads(storage_response)
        token = storage_response_dict["secret"]
        expireDate = storage_response_dict["expiresOn"]
        return token, expireDate

    @staticmethod
    def _get_key_of_token(driver, iteration):
        try:
            key_name = driver.execute_script(f'return window.localStorage.key({iteration})')
        except Exception as e:
            raise Exception(f"Failed to get key name of token at index {iteration}: {str(e)}")
        return key_name

    def _get_universal_key(driver, portalNameUri, key_name):
        print(f'Start _get_universal_key()')
        storage_response = driver.execute_script(f"return window.localStorage.getItem('{key_name}')")
        environment = CM.get_value_in_temp_variable("Environment")
        portalNameUri = portalNameUri.replace("(environment)", environment.lower())
        print(f'key_name: {key_name}')
#       if f"/{portalNameUri}/.default" in key_name:
        try:
            storage_response_dict = json.loads(storage_response)
        except Exception:
            storage_response_dict = dict()
        if "secret" in storage_response_dict:
            if "expiresOn" in storage_response_dict:
                if "target" in storage_response_dict:
                    if "profile openid email" not in storage_response_dict["target"]:
                        print(f'secret: {storage_response_dict["secret"]}')
                        return storage_response_dict["secret"]

    @staticmethod
    def _get_correct_token_from_local_storage(driver, token_name):
        key_position = 0
        token = None
        key_name = TokenMethods._get_key_of_token(driver, key_position)

        print(f'key_position: {key_position}')
        print(f'key_name: {key_name}')

        while key_name is not None and token is None:

            if "UNIVERSAL" == token_name:
                token = TokenMethods._get_universal_key(driver, "canvas-(environment)", key_name)

            key_name = TokenMethods._get_key_of_token(driver, key_position)
            key_position += 1

        if token is None:
            raise Exception(f"There was no token found for {token_name}")
        return token
    
    @staticmethod
    def _start_web_driver_sso_and_go_to_the_correct_page(token_name, engagement_name):
        timeout = Data_handler().get_env_var_value("veryLongTimeOut")
        options = ChromeOptions()
        options.use_chromium = True
        options.add_argument("--incognito")
        driver = Chrome(executable_path="C:/SeleniumWebDrivers/ChromeDriver/chromedriver.exe", options=options)
        environment = CM.get_value_in_temp_variable("Environment")
        env_variables = CM.get_app_env_variable(environment)
        driver.get(env_variables["CanvasURL"])        
        webelement = SM.wait_for_element_to_be_clickeable_by_xpath(driver, '//input[@type="email"]', timeout )
        SM.input_text_on_webelement(webelement, env_variables["executingUser"])
        SM.wait_for_element_visibility_by_xpath(driver, '//input[@type="submit"]')
        webelement = SM.wait_for_element_to_be_clickeable_by_xpath(driver, '//input[@type="submit"]', timeout)
        SM.click_webelement(webelement)
        SM.wait_for_element_visibility_by_xpath(driver, '//div[@id="loginHeader"]')
        LM.authenticate_incognito_user(driver, env_variables["executingUser"], "R-cln0M-Y2")
        SM.wait_for_element_visibility_by_xpath(driver, "//input[@type='search']")
        return driver
        
    @staticmethod
    def get_endpoint_url(token_name, engagement_name):
        environment = CM.get_value_in_temp_variable("Environment")
        env_variables = CM.get_app_env_variable(environment)
        if "HERCULES-" in token_name:
            hercules_api_url = env_variables["herculesAPIEndpoint"]
            token_splitted = token_name.split("HERCULES-")
            if token_splitted[1] == "":
                country_code = TokenMethods._get_token_information(token_name, engagement_name)["country_code"]
            else:
                country_code = token_splitted[1]
            hercules_api_url = hercules_api_url.replace('{{instance}}', country_code)
            return hercules_api_url
        if "UNIVERSAL" == token_name:
            return env_variables["universalAPIEndpoint"]
        if "UNIVERSAL2-" in token_name:
            hercules_api_url = env_variables["universal2APIEndpoint"]
            token_splitted = token_name.split("UNIVERSAL2-")
            if token_splitted[1] == "":
                country_code = TokenMethods._get_token_information(token_name, engagement_name)["country_code"]
            else:
                country_code = token_splitted[1]
            endpoint_country_code = APIMethods.get_endpoint_country_code(country_code, environment)
            hercules_api_url = hercules_api_url.replace('{{instance}}', endpoint_country_code)
            return hercules_api_url
        raise Exception(f"Not a valid token_name {token_name}")

    @staticmethod
    def get_token_url(token_name):
        environment = CM.get_value_in_temp_variable("Environment")
        env_variables = CM.get_app_env_variable(environment)
        if "HERCULES-" in token_name:
            hercules_url = env_variables["HerculesURL"]
            country_id = token_name.split("HERCULES-")[1]
            hercules_url = hercules_url.replace('{{instance}}', country_id)
            return hercules_url
        if "UNIVERSAL" == token_name:
            return env_variables["CanvasURL"]
        if "UNIVERSAL2-" in token_name:
            #universal2_url = env_variables["universal2APIEndpoint"]
            #country_id = token_name.split("UNIVERSAL2-")[1]
            #universal2_url = universal2_url.replace('{{instance}}', country_id)
            #return universal2_url
            return env_variables["CanvasURL"]
        raise Exception(f"Not a valid token_name {token_name}")

    @staticmethod
    def _get_correct_token_from_local_storage_for_universal(driver, token_name):
        key_position = 0
        token = None
        key_name = TokenMethods._get_key_of_token(driver, key_position)
        while key_name != None and token == None:
            key_position += 1
            if key_name != None:
                if "UNIVERSAL" == token_name:
                    token = TokenMethods._get_universal_key(driver, key_name)
            key_name = TokenMethods._get_key_of_token(driver, key_position)
        if token == None:
            raise Exception(f"There was no token found for {token_name}")
        return token   

    @staticmethod
    def get_incountryuri_from_get_home_json(driver, token_name, engagement_name):
        token=TokenMethods._get_correct_token_from_local_storage_for_universal(driver, token_name)
        response = APIMethods.api_request_get_home_json(token,engagement_name)
        incountryuri = response["responseBody"]["collections"]["clients"][0]["collections"]["workspaces"][0]["collections"]["engagements"][0]["data"]["incountryuri"]
        return incountryuri

    @staticmethod
    def get_token(token_name):
        with TokenMethods._TOKEN_LOCK:
            try:
                tokens_information = CM.read_json_file("Tests/filesForTests/temp_api/token_handler.json")
                if TokenMethods._check_if_token_has_expired(tokens_information[token_name]):
                    return tokens_information[token_name]['value']
                return None
            except:
                print(f'There was no token with the name {token_name}')
            
    @staticmethod
    def _check_if_token_has_expired(token_information):
        now = datetime.now()
        created_date_token = datetime.strptime(token_information["creation_time"], "%Y%m%d%H%M%S%f")
        expiration_date_token = created_date_token + timedelta(seconds=(int(token_information["duration"]) + 600))
        if now < expiration_date_token:
            return True
        print(f'[WARN] The token was expided at {expiration_date_token}')
        return False 
