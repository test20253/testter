import argparse
import os
import sys

from Core.framework.init_runner import Init_Runner

from Tests.Utils.ContentCleanup import APIDeleteContentById
from Tests.custom_methods.CommonMethods import CommonMethods as CM
 
parser = argparse.ArgumentParser(description='CT ADO Scriptless Test Execution',
                                 formatter_class=argparse.RawTextHelpFormatter)

# Arguments - Scriptless parameters

parser.add_argument("--mode", default="", type=str, help="Execution Mode (TestCase/TestSuite)")
parser.add_argument("--file", default="", help="Name of Test suite/Test case file")
parser.add_argument("--name", default="", help="Name of Test suite/test case")
parser.add_argument("--environment", default="QA", type=str,
                    help="Environment where automation script need to execute (QA/DEV/PROD)")
parser.add_argument("--tags", default="", type=str,
                    help="Test tags for execution (Smoke/Regression/Sanity)")
parser.add_argument("--browser", default ="chromium-edge-incognito", type=str,
                    help="Browser to execute scripts (chrome/chrome-sso/chrome-incognito/headlesschrome/firefox"
                         "/chromium-edge/chromium-edge-incognito/chromium-edge-sso)")
parser.add_argument("--env_vars", default="{}", type=str,
                    help="OS environment parameters to be set before pipeline execution")
parser.add_argument("--dataindex", default="",
                    help="Data Index for TestCase execution, applicable only for test case mode ")
parser.add_argument("--retry", default="0", help="Number of retries on test case failure")
parser.add_argument("--parallel", default="tests", help="suite/tests")
parser.add_argument("--thread_count", default="0", help="Number of tests to run parallel")
parser.add_argument("--execute_failed_test", default="False", type=str,
                    help="False: dynamic test suite configuration not used\n"
                         "create_xml: creates dynamic xml file in Tests/test_suites folder\n"
                         "create_and_execute: creates and execute dynamic xml file in Tests/test_suites folder")

# Arguments - Debugging

parser.add_argument("--screen_capture_all_steps", default=False, type=str,
                    help="Capture screenshot for steps (True / False)")
parser.add_argument("--loglevel", default="INFO", type=str,
                    help="TRACE, DEBUG, INFO (default), WARN, ERROR and NONE (no logging)")

# Arguments - Scriptless configuration

parser.add_argument("--local", default=True, type=str, help="Local/Pipeline execution")
parser.add_argument("--git_pull", default=False, type=str, help="Pull changes from Repo (True/False)")
parser.add_argument("--update_files", default=False, type=str, help="update files from official Scriptless repository")
parser.add_argument("--email", default="", help="User email address")
parser.add_argument("--pat_token", default="", help="PAT Token")

# Arguments - Azure DevOps Test Execution

parser.add_argument("--organization", default="", help="ADO Organisation")
parser.add_argument("--project", default="", help="ADO Project name")
parser.add_argument("--build_id", default="", type=str, help="Pipeline build Id")

parser.add_argument("--update_ado", default="False", type=str,
                    help="ADO Test Case Execution Status update required or not\n"
                    "False: ADO Test Case Result Status is not updated\n"
                    "real_time_status: status is updated after every test case finishes\n"
                    "update_status: status is updated without attachment files at the end of execution\n"
                    "full_update: status is updated and execution report files are attached at the end of execution\n"
                    "real_time_full_update: status is updated after every test case finishes and upload execution"
                         "report file at end of test execution")
parser.add_argument("--ado_plan_id", default="", type=str,
                    help="ADO TestPlan ID, applicable only for test case mode")
parser.add_argument("--ado_suite_id", default="", type=str,
                    help="ADO TestSuite ID, applicable only for test case mode")
init_run = Init_Runner()

try:
    args = init_run.custom_arg_parser(parser)
    cur_dir = str(os.path.dirname(os.path.abspath(__file__)))
    init_run.init_config(cur_dir, args)
    #init_run.check_latest_version(args)

    if args.update_files:
        init_run.update_files()
        exit()
    if args.git_pull:
        init_run.pull_repo()
    init_run.setup_env_var(args)

    app_variables = CM.get_app_env_variable(args.environment)


    #Removing temp files
    try:
        os.remove("Tests/filesForTests/temp.json")
    except Exception:
        pass
    try:
        os.remove("Tests/filesForTests/temp_engagements.json")
    except Exception:
        pass
    try:
        os.remove("Tests/filesForTests/temp_test_information.json")
    except Exception:
        pass
    try:
        os.remove("Tests/filesForTests/temp_api/token_handler.json")
    except Exception:
        pass
 


    #Generating temp config files from templates
    CM.create_temp_config_file("Tests/filesForTests/Config/engagements.json", "Tests/filesForTests/temp_engagements.json")
    CM.create_temp_config_file("Tests/filesForTests/Config/test_information.json", "Tests/filesForTests/temp_test_information.json")
   
    #Setting up environment variables
    CM.set_value_in_temp_variable("Environment", args.environment)

    #Setting up environment variables in case of mocking
    global_Id = CM.get_variable_value("global_Id")
    local_Id = CM.get_variable_value("local_Id")
    
    CM.update_engagement_information_in_config("Content", "global_Id", global_Id)
    CM.update_engagement_information_in_config("Content", "local_Id", local_Id)
    
    engagements_information = CM.get_engagements_information()
    if global_Id != None or global_Id != "":
        CM.set_value_in_temp_variable("UseExistingEngagementInCaseOfError", engagements_information)
    

    #Retrieving type of execution
    if (args.mode == "testcase" ):
        CM.set_value_in_temp_variable("global_execution_type", "testcase")
    else:
        CM.set_value_in_temp_variable("global_execution_type", "testsuite")
    
    if (args.mode == "testcase"  or args.mode =="testsuite"):
        temp_file_name = 'Scriptless Execution.' + args.name  
        CM._initialization_of_temp_engagement_information_json_file(temp_file_name,global_Id,local_Id)
        CM._initialization_of_temp_engagement_information_json_file("Scriptless Execution.Custom suite",global_Id,local_Id)
        #Retrieving type of execution
        if (args.mode == "testcase" ):
            CM.set_value_in_temp_variable("global_execution_type", "testcase")
        else:
            CM.set_value_in_temp_variable("global_execution_type", "testsuite")

    if (args.mode == "testcase"  or args.mode =="testsuite"):
        temp_file_name = 'Scriptless Execution.' + args.name  
        CM._initialization_of_temp_engagement_information_json_file(temp_file_name,global_Id,local_Id)
        CM._initialization_of_temp_engagement_information_json_file("Scriptless Execution.Custom suite",global_Id,local_Id)

    if not init_run.check_os_env_vars():
        print("\033[93m" + "[WARNING] MISSING ENVIRONMENT VARIABLES!!! TEST EXECUTION MAY FAIL" + "\033[0m")
    init_run.custom_generator()
    status = init_run.execute_testcases(args)
except Exception as e:
    status = 1
    init_run.get_error_details()

if app_variables["deleteEntity"].lower() == 'true':
    APIDeleteContentById(environment=args.environment, prefix_file_name='Scriptless Execution.')


CM._delete_temp_files('Scriptless Execution.')
CM._delete_directory_files()
sys.exit(init_run.get_error_details()) if status > 0 else sys.exit(0)