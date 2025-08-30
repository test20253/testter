import time
import os
import xml.etree.ElementTree as ET
import json
import pathlib
from shutil import copyfile
import tempfile
from robot.utils.asserts import fail
import threading

from Tests.custom_methods.SystemActionExecutor import SystemActionExecutor


class CommonMethods:
    _file_lock = threading.Lock()

    @staticmethod
    def update_engagement_information_in_config(engagement_type, engagement_property, value_to_update):
        config_file = CommonMethods.read_json_file("Tests/filesForTests/temp_engagements.json")
        config_file[engagement_type.strip()][engagement_property] = str(value_to_update)
        CommonMethods.write_json_file("Tests/filesForTests/temp_engagements.json", config_file)

    @staticmethod
    def get_engagements_information():
        config_file = CommonMethods.read_json_file("Tests/filesForTests/temp_engagements.json")
        return config_file

    @staticmethod
    def get_engagement_information_from_config(engagement_type, engagement_property):
        config_file = CommonMethods.read_json_file("Tests/filesForTests/temp_engagements.json")
        return config_file[engagement_type][engagement_property]

    @staticmethod
    def set_engagement_information_in_config(engagement_type, engagement_property, value_to_set):
        CommonMethods.update_engagement_information_in_config(engagement_type.strip(), engagement_property,
                                                              value_to_set)

    @staticmethod
    def get_test_status(test_name):
        tests_config_file = CommonMethods.read_json_file("Tests/filesForTests/temp_test_information.json")
        test_config = tests_config_file[test_name]
        return test_config["status"]

    @staticmethod
    def set_test_status(test_name, status):
        global_execution_type = CommonMethods.get_value_in_temp_variable("global_execution_type")
        if (global_execution_type == "testsuite"):
            tests_config_file = CommonMethods.read_json_file("Tests/filesForTests/temp_test_information.json")
            tests_config_file[test_name]["status"] = status
            CommonMethods.write_json_file("Tests/filesForTests/temp_test_information.json", tests_config_file)

    @staticmethod
    def fail_test_case_if_dependency_not_met(test_name):
        global_execution_type = CommonMethods.get_value_in_temp_variable("global_execution_type")
        if (global_execution_type == "testsuite"):
            dependencies_met = CommonMethods.are_test_dependencies_met(test_name)
            if dependencies_met == False:
                CommonMethods.throw_exception(f"Dependencies not met for the test case {test_name}")

    @staticmethod
    def are_test_dependencies_met(test_name):
        tests_config_file = CommonMethods.read_json_file("Tests/filesForTests/temp_test_information.json")
        test_config = tests_config_file[test_name]
        required_flag = True
        optional_flag = True
        for required_test_case_id in test_config["requiredForExecution"]:
            if CommonMethods.get_test_status_by_id(tests_config_file, required_test_case_id) == "RUNNING":
                required_flag = False
                break
        for optional_test_cases_id in test_config["optionals"]:
            combination_met = False
            for optional_test_case_id in optional_test_cases_id:
                teststatusbyid = CommonMethods.get_test_status_by_id(tests_config_file, optional_test_case_id)
                if (teststatusbyid == "PASSED" or teststatusbyid == "NOT RUNNED"):
                    combination_met = True
            if combination_met == False:
                optional_flag = False
        if (required_flag == False) or (optional_flag == False):
            return False
        return True

    @staticmethod
    def get_test_status_by_id(tests_config_file, test_id):
        for key, value in tests_config_file.items():
            if value["id"] == test_id:
                return value["status"]
        raise Exception(f"Test with Id {test_id} was not found in the test_information file")

    @staticmethod
    def throw_exception(message):
        raise Exception(message)

    @staticmethod
    def get_app_env_variable(environment):
        path_to_app_vars = os.path.join(os.getcwd(), "Tests", "resources", "env", "env.xml")
        with open(path_to_app_vars) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        parameters_for_environment = {}
        correct_environment = False
        for line in content:
            if correct_environment == True:
                if f'</parameters>' in line:
                    break
                if 'type="app"' in line:
                    var_name = line.split(' name="')[1].split('" type=')[0]
                    var_value = line.split(' value="')[1].split('"/>')[0]
                    parameters_for_environment[var_name] = var_value
            if correct_environment == False:
                if f'<env envname="{environment}">' in line:
                    correct_environment = True
        return parameters_for_environment

    @staticmethod
    def value_plus_another_value(value1, value2):
        result = int(value1) + int(value2)
        return result

    @staticmethod
    def get_data_sheet_full_set(data_sheet_name, ID):
        tree = ET.parse(os.path.join(os.getcwd(), "Tests", "resources", "dataset", f"{data_sheet_name}.xml"))
        root = tree.getroot()
        result = {}
        for row in root.findall("row"):
            if (row.find("ID").text == ID):
                data_params = row.findall(".//")
                for data in data_params:
                    result[data.tag] = data.text
        return result

    @staticmethod
    def get_parameters_of_url(url):
        parameters = url.split("?", 1)[1]
        return f"?{parameters}"

    @staticmethod
    def get_base_url(url):
        base_url = "http://" + url.split("/")[2] + "/"
        return base_url

    @staticmethod
    def get_number_of_keys(dict_data_sheet):
        return len(dict_data_sheet)

    @staticmethod
    def get_number_of_non_empty_keys(dict_data_sheet):
        amount_of_keys = 0
        for key in dict_data_sheet:
            if None != dict_data_sheet[key] and dict_data_sheet[key] != "":
                amount_of_keys += 1
            else:
                return amount_of_keys
        return amount_of_keys

    @staticmethod
    def replace_string_character_with_another(string_to_modify, char_to_remove, char_to_add):
        new_string = string_to_modify.replace(char_to_remove, char_to_add)
        return new_string

    @staticmethod
    def get_full_path_of_project_file(relative_path):
        splitted_path = relative_path.split("/")
        path = os.getcwd()
        for part_of_relative_path in splitted_path:
            path = os.path.join(path, part_of_relative_path)
        return path

    @staticmethod
    def get_variable_value(variable_name):
        path_to_app_vars = os.path.join(os.getcwd(), "Tests", "resources", "variable", "var.xml")
        with open(path_to_app_vars) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
        for line in content:
            if f'name="{variable_name}"' in line:
                variable_value = line.split(f'value="')[1].split(f'" desc=')[0]
                return variable_value
        raise Exception(f"There was not a variable named {variable_name} in the variables file")

    @staticmethod
    def create_empty_json_file(path):
        try:
            CommonMethods.read_json_file(path)
        except Exception:
            CommonMethods.write_json_file(path, dict())

    @staticmethod
    def set_value_in_temp_variable(variable_name, value):
        CommonMethods.create_empty_json_file("Tests/filesForTests/temp.json")
        temp_file = CommonMethods.read_json_file("Tests/filesForTests/temp.json")
        temp_file[variable_name] = value
        CommonMethods.write_json_file("Tests/filesForTests/temp.json", temp_file)
        return value

    @staticmethod
    def create_temp_config_file(initial_path, final_path):
        copyfile(initial_path, final_path)

    @staticmethod
    def get_value_in_temp_variable(variable_name):
        temp_file = CommonMethods.read_json_file("Tests/filesForTests/temp.json")
        return temp_file[variable_name]

    @staticmethod
    def return_as_local_variable(variable_value):
        return variable_value

    @staticmethod
    def read_json_file(file_path):
        with open(file_path) as json_file:
            data = json.load(json_file)
            return data

    @staticmethod
    def write_json_file(file_path, dict_to_write):
        with open(file_path, 'w') as fp:
            json.dump(dict_to_write, fp)

    @staticmethod
    def check_for_downloaded_file(path, part_of_file_name):
        file_list = os.listdir(path)
        for file_name in file_list:
            if part_of_file_name in file_name:
                return True
        return False

    @staticmethod
    def generate_list(string_with_list_values):
        list_to_return = string_with_list_values.split("|")
        return list_to_return

    @staticmethod
    def wait_page_to_load(driver):
        page_state = ''
        while page_state != 'complete':
            time.sleep(1)
            page_state = driver.execute_script('return document.readyState;')

    @staticmethod
    def get_download_path():
        location = (pathlib.Path.home() / "Downloads")
        return location

    @staticmethod
    def value_minus_another_value(value1, value2):
        """
        This function return substracton of the two inputs
        value1: first input
        value2: second input
        """
        result = int(value1) - int(value2)
        return result

    @staticmethod
    def create_temp_suite_config_file(filename):
        """
        This Method create a temporal Json based in the file 'engagements.json'
        filename (str): Name of the temporal File that will be Created
        """

        try:
            original_file_path = "Tests\\filesForTests\\Config\\engagements.json"
            temp_file_path = tempfile.gettempdir() + '\\'
            temp_file = temp_file_path + filename + ".json"
            if os.path.exists(temp_file):
                print(f'[INFO] the file {filename}.json already existed')
            else:
                copyfile(original_file_path, temp_file)
                CommonMethods._fill_json_config_file(filename)
        except:
            fail(f"The File {filename} doesn't be created, check the original file: {original_file_path} ")

    @staticmethod
    def set_engagement_information_in_suite_config(filename, engagement_type, engagement_property, value_to_set):
        """
        This method update the engagement information in a json file
        filename (str): name of the Json file, for parallel execution use {SUITE_NAME}
        engagement_type (str): Engagement Type that will be set
        engagement_property (str): engagement property that will be updated
        value_to_set (str): New value to be set in engagement_property
        """
        try:
            with CommonMethods._file_lock:
                temp_file_path = tempfile.gettempdir() + '\\'
                config_file = CommonMethods.read_json_file(temp_file_path + filename + ".json")
                config_file[engagement_type.strip()][engagement_property] = str(value_to_set)
                CommonMethods.write_json_file(temp_file_path + filename + ".json", config_file)
        except Exception as e:
            fail(
                f"The File {filename} couldn't be updated. Check File: {temp_file_path + filename}.json Error: {str(e)}")

    @staticmethod
    def get_engagement_information_from_suite_config(filename, engagement_type, engagement_property):
        """
        This method get the engagement information in a json file
         filename (str): name of the Json file, for parallel execution use {SUITE_NAME}
        engagement_type (str): Engagement Type that will be seted
        engagement_property (str): engagement property that will be uptated
        value_to_set (str): New value to be seted in engagement_property

        """
        try:
            temp_file_path = tempfile.gettempdir() + '\\' + filename + ".json"
            config_file = CommonMethods.read_json_file(temp_file_path)
            return config_file[engagement_type][engagement_property]
        except:
            fail(f"The File {filename} dosen't exist, check the  path of: {temp_file_path}, or check the DataSheet ")

    @staticmethod
    def _delete_temp_files(prefix):
        """
        This method remove all the files that have the "prefix" into the TEMP folder
        prefix(str): Prefix of the files that you need to be removed
        """
        files = os.listdir(tempfile.gettempdir())

        for file in files:
            if file.startswith(prefix):
                try:
                    os.remove(tempfile.gettempdir() + "\\" + file)
                    print(f"[INFO] {file}  Removed")
                except:
                    print(f"[INFO] {file} Doesn't be removed")

    @staticmethod
    def _initialization_of_temp_engagement_information_json_file(temp_file_name, global_Id, local_Id):
        CommonMethods.create_temp_suite_config_file(temp_file_name)
        CommonMethods.set_engagement_information_in_suite_config(temp_file_name, "Content", "global_Id", global_Id)
        CommonMethods.set_engagement_information_in_suite_config(temp_file_name, "Content", "local_Id", local_Id)

    @staticmethod
    def get_automation_user_info_from_credential_manager(credential_user_name: str = 'CanvasAutomationUser1') -> dict:
        """
        This method returns the email for the AutomationUsers for executions
        automation_user (str): name of the credential of the users: CanvasAutomationUser1
                                                                    CanvasAutomationUser2
                                                                    CanvasAutomationUser3
        """
        if credential_user_name is None or not credential_user_name:
            credential_user_name = 'CanvasAutomationUser1'
        try:
            with CommonMethods._file_lock:
                return SystemActionExecutor()._get_credentials_password(credential_user_name)

        except:
            raise ValueError(f"Error retrieving credentials for: '{credential_user_name}'")

    @staticmethod
    def _fill_json_config_file(temp_file_name):
        """
        This method completes the information in the Json config file using the Variables section
            args:
                temp_file_name: Name of the Json file to be created the suggested value for Scriptles is ${SUITE_NAME}.
        """
        global_Id = CommonMethods.get_variable_value("global_Id")
        local_Id = CommonMethods.get_variable_value("local_Id")

        if global_Id != '' and global_Id != None:
            CommonMethods.set_engagement_information_in_suite_config(temp_file_name, "Content", "global_Id", global_Id)
        if local_Id != '' and local_Id != None:
            CommonMethods.set_engagement_information_in_suite_config(temp_file_name, "Content", "local_Id", local_Id)

    @staticmethod
    def copy_rename_and_save_file_to_temp(original_file_path: str, custom_filename: str,
                                          final_file_path='C:\\FilesForTest\\temp'):
        """
         Args:
            original_file_path (str): The path to the original file that you want to copy.
            custom_filename (str): The new custom name for the copied file.
            final_file_path (str, optional): The directory path where the copied file should be saved.

        Returns:
            str: The path of the newly copied and renamed file.
        """
        with CommonMethods._file_lock:
            try:
                temp_file = final_file_path + '\\' + custom_filename
                if os.path.exists(temp_file):
                    print(f'[INFO] the file {custom_filename} already existed')
                else:
                    copyfile(original_file_path, temp_file)
                return temp_file

            except:
                fail(f"The File {custom_filename} doesn't be created, check the original file: {original_file_path} ")

    @staticmethod
    def _delete_directory_files(directory_path='C:\\FilesForTest\\temp'):
        """
        This method deletes all the files in a specific directory.
        Args:
            directory_path (str): The path to the directory from which files will be removed.

        """
        files = os.listdir(directory_path)

        for file in files:
            try:
                os.remove(directory_path + '\\' + file)
                print(f"[INFO] {file}  Removed")
            except:
                print(f"[INFO] {file} Doesn't be removed")

    @staticmethod
    def validate_if_channel_language_file_already_exists(label: str, response: dict):

        """
        This function checks whether in dict(temp json)-> channel language dict exists or not.
        if not exists temp json will be created .if exists checkup will be carried out whether
        json holds the channel and language data

        :param label     :  label value can be channel,language or serviceline string value
                            (in order to differentiate whether it is channel or language)
        :param response  :  json response which contains channel language and it's id
        :return          :  no returntype
        """

        if os.path.exists("Tests/filesForTests/Config/channel_language_list.json"):
            label_info = CommonMethods.read_json_file("Tests/filesForTests/Config/channel_language_list.json")

            if label_info[label] == {}:
                CommonMethods.create_channel_language_dictionary(label=label, response=response, label_info=label_info)
        else:
            label_info = {"channel": {}, "language": {}, "service_line": {}, "service_org": {}, "module": {}, "user": {}}
            CommonMethods.create_empty_json_file("Tests/filesForTests/Config/channel_language_list.json")
            CommonMethods.create_channel_language_dictionary(label=label, response=response, label_info=label_info)

    @staticmethod
    def create_channel_language_dictionary(label: str, response: dict, label_info: dict):

        """
        This functions stores the value in temp json for channel and language and serviceline
        from the response

        :param label        : label refers to channel,language or serviceline string value
                            (in order to differentiate whether it is channel or language)
        :param response     : json response which contains entire channel language and it's id
        :param label_info   : response which holds the channel and language data
        :return:            : no returntype
        """

        var = {}
        if label == "language":
            for index in response[0]:
                try:
                    var[index["languageId"]] = index["languageName"]
                except KeyError:
                    var[index["id"]] = index["name"]
        elif label == "user":
            var = {response['users'][0]['emailAddress']:response['users'][0]['id']}
        else:
            for index in response[0]:
                var[index["id"]] = index["name"]

        label_info[label] = var
        CommonMethods.write_json_file("Tests/filesForTests/Config/channel_language_list.json", label_info)

    @staticmethod
    def get_channel_language_name(channel: str, language: str, service_line: str = '') -> str:

        """
        This function gets the channel language serviceline name from the id
        which is stored in temp json

        :param channel  : channel id
        :param language : language id
        :return         : string which has channel language and service line names
        """

        label_info = CommonMethods.read_json_file("Tests/filesForTests/Config/channel_language_list.json")
        channel_name = label_info["channel"].get(channel)
        language_name = label_info["language"].get(language)
        service_line_name = label_info["service_line"].get(service_line)
        response = f"[Channel: {channel_name}][Language: {language_name}][Service line: {service_line_name}]"
        return response

    @staticmethod
    def get_labels_from_config(label: str, label_name: str):
        if os.path.exists("Tests/filesForTests/Config/channel_language_list.json"):
            config_file = CommonMethods.read_json_file("Tests/filesForTests/Config/channel_language_list.json")
            content = config_file[label]

            if label=="user" and content!={}:
                return content[label_name]

            if content == {}:
                return None

            key = [id for id, value in content.items() if value == label_name]
            label_id = key[0]
            return label_id

        else:
            return None