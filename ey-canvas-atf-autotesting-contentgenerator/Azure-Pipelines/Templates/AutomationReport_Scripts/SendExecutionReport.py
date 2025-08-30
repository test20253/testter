import datetime
import os
import argparse
import re
from requests.auth import HTTPBasicAuth
from EmailNotification import EmailNotification
from TeamsNotification import TeamsNotification
from GetPipelineData import PipelineDataExtractor
from typing import Any, Dict, List


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Send Email')
    parser.add_argument("--pat_token", default="", type=str, help="devops token to access pipeline")
    parser.add_argument("--sendgrid_token", default="", type=str, help="Sendgrid token to send email")
    parser.add_argument("--environment", default="", type=str, help="environment")
    parser.add_argument("--buildid", default="", type=str, help="buildid")
    parser.add_argument("--email_recipients", default="", type=str, help="buildid")
    parser.add_argument("--emailSubject", default="", type=str, help="email Subject")
    parser.add_argument("--sendgrid_url", default="", type=str, help="sendgrid_url")
    parser.add_argument("--webhookUrl", default="", type=str, help="webhookUrl")
    return parser.parse_args()


def get_authentication(pat_token: str) -> HTTPBasicAuth:
    user = os.getenv('devops_user')
    return HTTPBasicAuth(user, pat_token)


def send_teams_notification(webhookUrl: str, build_id: str, environment: str, emailSubject: str, passed_tests: int,
                            failed_tests: int, skipped_tests: int, pass_percentage: float, formatted_date: str,
                            release_version: str, branch_name: str) -> None:
    pattern = r'^refs/heads/Release_\d+\.\d+\.\d+$'
    if re.match(pattern, branch_name):
        print(f"Current branch is a release branch: {branch_name}")
        TeamsNotification().send_post_request(
            webhookUrl, build_id, environment, emailSubject, passed_tests, failed_tests,
            skipped_tests, pass_percentage, formatted_date, release_version)
    else:
        print(f"Current branch is not a release branch: {branch_name}")


def main():
    args = parse_arguments()
    auth = get_authentication(args.pat_token)
    # Extract pipeline data
    extractor = PipelineDataExtractor(args.buildid, auth)
    executionTime = extractor.get_execution_time()
    release_version = extractor.get_release_version()
    test_totals = extractor.get_test_totals()
    recipients = extractor.get_recipients(args.email_recipients)
    formatted_date = extractor.get_formatted_date()
    failed_tests = extractor.get_failed_tests()
    pass_percentage = extractor.get_pass_percentage()

    # Generate pie chart
    extractor.generate_pie_chart()


    # Send Teams notification
    send_teams_notification(
        args.webhookUrl, args.buildid, args.environment, args.emailSubject, test_totals['passed_tests'],
        failed_tests, test_totals['skipped_tests'], pass_percentage, formatted_date, release_version,
        extractor.pipeline_data['sourceBranch']
    )


if __name__ == "__main__":
    main()