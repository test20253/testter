import argparse
import os
import sys

from scriptless.Core.framework.init_runner import Init_Runner

parser = argparse.ArgumentParser(description='CT ADO Scriptless Test Execution',
                                 formatter_class=argparse.RawTextHelpFormatter)


# Arguments - Scriptless parameters

parser.add_argument("--mode", default="testcase", type=str, help="Execution Mode (testcase/testsuite)")
parser.add_argument("--file", default="", help="Name of Test suite/Test case file")
parser.add_argument("--name", default="", help="Name of Test suite/test case")
parser.add_argument("--environment", default="UAT3", type=str,
                    help="Environment where automation script need to execute (QA/DEV/PROD)")
parser.add_argument("--tags", default="", type=str,
                    help="Test tags for execution (Smoke/Regression/Sanity)")
parser.add_argument("--browser", default="chromium-edge-incognito", type=str,
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
parser.add_argument("--debug", default=False, type=str,
                    help="execute tests in debug mode")

# Arguments - Scriptless configuration

parser.add_argument("--local", default=True, type=str, help="Local/Pipeline execution")
parser.add_argument("--git_pull", default=False, type=str, help="Pull changes from Repo (True/False)")
parser.add_argument("--update_files", default=False, type=str, help="update files from official Scriptless repository")
parser.add_argument("--email", default="", help="User email address")
parser.add_argument("--pat_token", default="", help="PAT Token")

# Arguments - Azure DevOps Test Execution

parser.add_argument("--organization", default="EYCTCanvas", help="ADO Organisation")
parser.add_argument("--project", default="FAST.ATF", help="ADO Project name")
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

# Arguments - Email and Teams notifications

parser.add_argument("--share_test_result_config", default="MailSubject= EY CANVAS Notification Weekly Execution Status | MailTitle= Automation Report | DisableNotification=False", type=str,
                    help="set MailSubject, mail title, and 'disable mail' configurations separated by | , "
                         "ex: 'MailSubject=custom mail subject | MailTitle=custom title | DisableNotification=False or True")
parser.add_argument("--share_test_result_mail", default="", type=str,
                    help="give email ids to share test result.separate them by |, allows ey.com for mail")
parser.add_argument("--share_test_result_teams_channel", default="", type=str,
                    help="add 'Incoming webhook' app to team channel and give its url to get test result in Teams channel")

# Arguments - Automatic Object Locator
parser.add_argument("--object_locator", default=False, type=bool, help="Automatic Object Locator V1.1.0")

# Argument - Meta data regeneration
parser.add_argument("--refresh_metadata", default=False, type=bool, help="Refresh meta data")

init_run = Init_Runner()
try:
    cur_dir = str(os.path.dirname(os.path.abspath(__file__)))
    status = init_run.start_scriptless(parser, cur_dir)
except (Exception,) as e:
    status = 1
    init_run.get_error_details()
sys.exit(init_run.get_error_details()) if status > 0 else sys.exit(0)
