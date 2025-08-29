import argparse
import os
from Tests.Utils.EngagementCleanup import APIDeleteEngagementById
from Tests.custom_methods.CommonMethods import CommonMethods as CM
from Core.framework.init_runner import Init_Runner
from Core.framework.migration import migration

parser = argparse.ArgumentParser(description='CT QA Test Execution')
parser.add_argument("--environment", default="QA", type=str, help="Environment where automation script "
                                                                  "need to execute (QA/DEV/PROD)")
parser.add_argument("--mode", default="testcase", type=str, help="Execution Mode (TestCase/TestSuite)")
parser.add_argument("--tags", default="", type=str, help="Test tags for execution (Smoke/Regression/Sanity)")
parser.add_argument("--browser", default="chrome-incognito", type=str,
                    help="Browser to execute scripts (chrome/chrome-sso/chrome-incognito/headlesschrome/firefox"
                         "/firefox-private/chromium-edge/chromium-edge-incognito/chromium-edge-sso)")
parser.add_argument("--git_pull", default=False, type=bool, help="Pull changes from Repo (True/False)")
parser.add_argument("--local", default=False, type=bool, help="Local/Pipeline execution")
parser.add_argument("--env_vars", default="{}", type=str, help="OS environment parameters to be set before execution")
parser.add_argument("--file", default="", help="Name of Test suite/Test case file")
parser.add_argument("--name", default="", help="Name of Test suite/test case")
parser.add_argument("--dataindex", default="",
                    help="Data Index for TestCase execution, applicable only for test case mode")
parser.add_argument("--convert", default=False, help="Convert Scriptless scripts in to v2.0 compatible format")
parser.add_argument("--parallel", default="tests", help="suite/tests")
parser.add_argument("--thread_count", default="0", type=int, choices=range(0, 5), help="Number of tests to run parallel (0/1/2/3/4)")

args = parser.parse_args()

init_run = Init_Runner()
cur_dir = str(os.path.dirname(os.path.abspath(__file__)))
init_run.init_config(cur_dir)

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


#Generating temp config files from templates
CM.create_temp_config_file("Tests/filesForTests/Config/engagements.json", "Tests/filesForTests/temp_engagements.json")
CM.create_temp_config_file("Tests/filesForTests/Config/test_information.json", "Tests/filesForTests/temp_test_information.json")

#Setting up environment variables
CM.set_value_in_temp_variable("Environment", args.environment)

#Setting up environment variables in case of mocking
engagementid_primary = CM.get_variable_value("engagementid_primary")
engagementid_component = CM.get_variable_value("engagementid_component")
engagementid_archive = CM.get_variable_value("engagementid_archive")

CM.update_engagement_information_in_config("Primary", "engagementId", engagementid_primary)
CM.update_engagement_information_in_config("Component", "engagementId", engagementid_component)
CM.update_engagement_information_in_config("Archive", "engagementId", engagementid_archive)

engagements_information = CM.get_engagements_information()
if engagementid_archive != None or engagementid_archive != "":
    CM.set_value_in_temp_variable("UseExistingEngagementInCaseOfError", engagements_information)

#Retrieving type of execution
if (args.mode == "testcase" ):
    CM.set_value_in_temp_variable("global_execution_type", "testcase")
else:
    CM.set_value_in_temp_variable("global_execution_type", "testsuite")
    
if (args.mode == "testcase"  or args.mode =="testsuite"):
    temp_file_name = 'Scriptless Execution.' + args.name  
    CM._initialization_of_temp_engagement_information_json_file(temp_file_name,engagementid_primary,engagementid_component,engagementid_archive)
    CM._initialization_of_temp_engagement_information_json_file("Scriptless Execution.Custom suite",engagementid_primary,engagementid_component,engagementid_archive)

if args.convert:
    migration().main()
else:
    if args.git_pull:
        init_run.pull_repo()
    init_run.setup_env_var(args)
    if not init_run.check_os_env_vars():
        print("[WARNING] MISSING ENVIRONMENT VARIABLES!!! TEST EXECUTION MAY FAIL")
    init_run.custom_generator()

    init_run.execute_testcases(args)
    
    if app_variables["deleteEngagement"].lower() == 'true':
        APIDeleteEngagementById(environment=args.environment, prefix_file_name='Scriptless Execution.')
    CM._delete_temp_files('Scriptless Execution.')