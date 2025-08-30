import os
import shutil
import tempfile

from Tests.Utils.ContentCleanup import APIDeleteContentById
from Tests.Utils.logging.LoggerFactory import Logger

from Tests.custom_methods.CommonMethods import CommonMethods as CM
from scriptless.internal.runner import Runner


class UserListener:
    """
    A custom listener class that extends the CustomBase class.
    This listener can perform various actions before and after the test run.

    Methods:
        before_run():
            Called before the test run starts (Only Python code should be executed here, scriptless keywords will not be accessible).

        after_run():
            Called after the test run ends (Only Python code should be executed here, scriptless keywords will not be accessible).

    """

    ROBOT_LISTENER_API_VERSION = 2
    _TEMP_FILE_NAME = "Tests/filesForTests/temp.json"

    @staticmethod
    def before_run():
        """
        Called before the test run starts. Only Python code should be executed here;
        scriptless keywords will not be accessible.
        """
        args = Runner().argument_parser("run")
        args.mode = args.mode.lower()

        UserListener._remove_temp_files()
        UserListener._create_temp_files()

        # Setting up environment variables
        CM.set_value_in_temp_variable("Environment", args.environment)
        global_Id = CM.get_variable_value("global_Id")
        local_Id = CM.get_variable_value("local_Id")
        CM.update_engagement_information_in_config("Content", "global_Id", global_Id)
        CM.update_engagement_information_in_config("Content", "local_Id", local_Id)

        # Set global execution type
        CM.set_value_in_temp_variable("global_execution_type", args.mode)

        # create temp file for engagement information
        UserListener._initialize_temp_engagement_file(args)

    @staticmethod
    def after_run():
        """
        Called after the test run ends (Only Python code should be executed here, scriptless keywords will not be accessible).
        """
        args = Runner().argument_parser("run")
        UserListener()._move_log_file_to_the_report_folder()
        app_variables = CM.get_app_env_variable(args.environment)
        if app_variables["deleteEntity"].lower() == 'true':
            APIDeleteContentById(environment=args.environment, prefix_file_name='Scriptless Execution.')
        CM._delete_directory_files()
        file = tempfile.gettempdir() + '\\' + UserListener._generate_temp_file_name(args) + '.json'
        try:
            os.remove(file)
            print(f"File {file} removed successfully.")
        except FileNotFoundError:
            print(f"File {file} not found, skipping.")
        except Exception as e:
            print(f"Error occurred while removing {file}: {e}")


    def start_suite(self, name, attrs):
        """
        Called when suite starts.
        """
        pass

    def end_suite(self, name, attrs):
        pass

    def start_test(self, name, attrs):
        """
        Called when test starts.
        """
        print(f"Test {name} started.")

    def end_test(self, name, attrs):
        pass

    @staticmethod
    def _remove_temp_files():
        files_to_remove = [
            "Tests/filesForTests/temp.json",
            "Tests/filesForTests/temp_engagements.json",
            "Tests/filesForTests/temp_test_information.json",
            "Tests/filesForTests/temp_api/token_handler.json",
            "Tests/resources/local_db/Token.json"
        ]
        for file in files_to_remove:
            try:
                os.remove(file)
                print(f"File {file} removed successfully.")
            except FileNotFoundError:
                print(f"File {file} not found, skipping.")
            except Exception as e:
                print(f"Error occurred while removing {file}: {e}")

    @staticmethod
    def _create_temp_files():
        CM.create_temp_config_file("Tests/filesForTests/Config/engagements.json",
                                   "Tests/filesForTests/temp_engagements.json")
        CM.create_temp_config_file("Tests/filesForTests/Config/test_information.json",
                                   "Tests/filesForTests/temp_test_information.json")



    @staticmethod
    def _initialize_temp_engagement_file(args):
       temp_file_name = UserListener._generate_temp_file_name(args)
       global_Id = CM.get_variable_value("global_Id")
       local_Id = CM.get_variable_value("local_Id")

       CM.update_engagement_information_in_config("Content", "global_Id", global_Id)
       CM.update_engagement_information_in_config("Content", "local_Id", local_Id)

       if (args.mode == "testcase"):
           CM._initialization_of_temp_engagement_information_json_file(temp_file_name, global_Id, local_Id)

    @staticmethod
    def _generate_temp_file_name(args) -> str:
        return f'Scriptless Execution.{args.file.replace(".xml", "_")}{args.name}'
    
    @staticmethod
    def _move_log_file_to_the_report_folder():
        logger = Logger(__name__)
        today_execution_report = logger.get_today_execution_report_folder()
        execution_report_last_folder = logger.get_last_folder_alphabetically(today_execution_report)
        log_file_name = logger.log_file_name
        try:
            shutil.move(f"{today_execution_report}/{log_file_name}",
                        f"{today_execution_report}/{execution_report_last_folder}/{log_file_name}")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except PermissionError as e:
            logger.error(f"Permission error: {e}")
        except shutil.Error as e:
            logger.error(f"Shutil error: {e}")
