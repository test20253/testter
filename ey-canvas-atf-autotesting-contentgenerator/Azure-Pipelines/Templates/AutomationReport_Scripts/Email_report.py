import datetime
import os
import argparse
import re

import requests
import matplotlib.pyplot as plt
import base64
from dateutil import parser
from requests.auth import HTTPBasicAuth


# Function to calculate execution time
def get_execution_time(start_time):
    current_time = datetime.datetime.utcnow()
    converted_current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    convert_start_time = parser.isoparse(start_time)
    convert_finish_time = parser.isoparse(converted_current_time)
    diff = convert_finish_time - convert_start_time
    total_seconds = diff.total_seconds()
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    print("execution time")
    print(f"{int(hours)}: {int(minutes)}: {seconds:.2f}")
    return f"{int(hours)}: {int(minutes)}: {seconds:.2f}"


# Function to get release version
def get_release_version(branch_name):
    release_version = branch_name.replace('refs/heads/', '')
    release_version = release_version.replace('/', ' ')
    print("release time")
    print(release_version)
    return release_version

# Function to get recipients based on the email_recipients argument
def get_recipients(email_recipients):

    email_pattern = r'\b[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}\b'

    emails = re.findall(email_pattern, email_recipients)
    print("emails")
    print(emails)
    email_list = [{"email": email} for email in emails]

    return email_list

# Function to get test runs from the API
def get_test_runs(url, auth):
    response = requests.get(url=url, auth=auth)
    print("testrun")
    print(auth)
    print(response)
    return response.json()['value']


# Function to get time response from the API
def get_time_response(url_for_time, auth):
    print("time response")
    time = requests.get(url=url_for_time, auth=auth, verify=False)
    print(time)
    return time


# Function to generate pie chart
def generate_pie_chart(passed_tests, failed_tests, skipped_tests):
    fig, ax = plt.subplots()
    colors = ['#068E06', '#F60C0C', '#FFFF00']  # Light Green, Red, Yellow
    labels = []
    values = []

    if passed_tests > 0:
        labels.append('Passed')
        values.append(passed_tests)
    else:
        labels.append('Passed')
        values.append(0)

    if failed_tests > 0:
        labels.append('Failed')
        values.append(failed_tests)
    else:
        labels.append('Failed')
        values.append(0)

    if skipped_tests > 0:
        labels.append('Skipped')
        values.append(skipped_tests)
    else:
        labels.append('Skipped')
        values.append(0)

    ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, wedgeprops={'edgecolor': 'white'})
    ax.set_title('Test Results')
    plt.tight_layout()  # Adjusts the spacing between subplots to prevent label overlap
    plt.savefig('chart.png')


# Function to attach image to email
def attach_image_to_email():
    with open("chart.png", "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode('utf-8')

    return {
        "content": encoded_string,
        "type": "image/png",
        "filename": "chart.png",
        "disposition": "inline",
        "content_id": "Chart"
    }


def main():
    # Argument parser
    parser1 = argparse.ArgumentParser(description='Send Email')
    parser1.add_argument("--pat_token", default="", type=str, help="devops token to access pipeline")
    parser1.add_argument("--sendgrid_token", default="", type=str, help="Sendgrid token to send email")
    parser1.add_argument("--environment", default="UAT3", type=str, help="environment")
    parser1.add_argument("--buildid", default="", type=str, help="buildid")
    parser1.add_argument("--email_recipients", default="", type=str, help="buildid")
    parser1.add_argument("--emailSubject", default="", type=str, help="email Subject")
    args = parser1.parse_args()
    user = os.getenv('devops_user')
    auth = HTTPBasicAuth(user, args.pat_token)

    # URLs for API calls
    url = f"https://dev.azure.com/EYCTCanvas/FAST.ATF/_apis/test/runs?includeRunDetails=true&api-version=6.0&buildUri=vstfs:///Build/Build/{args.buildid}"
    url_for_time = f"https://dev.azure.com/EYCTCanvas/FAST.ATF/_apis/build/builds/{args.buildid}"

    # Get start time and calculate execution time
    time_response = get_time_response(url_for_time, auth)
    print(user)
    print(time_response)
    startTime = time_response.json()['startTime']
    executionTime = get_execution_time(startTime)

    # Get the branch name
    branch_name = time_response.json()['sourceBranch']
    release_version = get_release_version(branch_name)

    # Get test runs
    list_of_testruns = get_test_runs(url, auth)
    print(list_of_testruns)
    list_suite = []
    total_tests = 0
    passed_tests = 0
    skipped_tests = 0

    # Loop through test runs and calculate totals
    for get in list_of_testruns:
        total_tests += get['totalTests']
        passed_tests += get['passedTests']
        skipped_tests += get['notApplicableTests']
        list_suite.append({
            'serial': list_of_testruns.index(get) + 1,
            'suitename': get['pipelineReference']['phaseReference']['phaseName'],
            'passedtests': get['passedTests'],
            'failedtests': get['totalTests'] - get['passedTests'] - get['notApplicableTests'],
            'skippedtests': get['notApplicableTests'],
            'totaltests': get['totalTests'],
            'percentage': round((get['passedTests'] / get['totalTests']) * 100, 2),
            'runlink': get['webAccessUrl']
        })
        print(list_suite)

    # Generate pie chart
    generate_pie_chart(passed_tests, total_tests - passed_tests - skipped_tests, skipped_tests)

    # Get recipients
    recipients = get_recipients(args.email_recipients)
    print(recipients)
    print("suites added")
    print(list_suite)
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%m-%d-%Y")

    pass_percentage = round((passed_tests / total_tests) * 100, 2)
    # Sendgrid API call
    sendgrid_url = "https://api.sendgrid.com/v3/mail/send"
    headers = {'Authorization': 'Bearer ' + args.sendgrid_token, "content-type": "application/json"}
    body = {
        "from": {"email": "test.autom.canvas.tt1@ey.com"},
        "personalizations": [{
            "to": recipients,
            "dynamic_template_data": {
                "environment": args.environment,
                "header": f"{args.emailSubject} Automation Report | {args.environment} | {formatted_date} | {release_version}",
                "subject": f"{args.emailSubject} Automation Report | {args.environment} | {formatted_date} | {release_version} | {pass_percentage}% pass",
                "totaltests": total_tests,
                "passedtests": passed_tests,
                "failedtests": total_tests - passed_tests - skipped_tests,
                "skippedtests": skipped_tests,
                "Percentage": round((passed_tests / total_tests) * 100, 2),
                "executionTime": executionTime,
                "totalSuites": len(list_suite),
                "buildid": args.buildid,
                "emailSubject": args.emailSubject,
                "artifacts": f"https://dev.azure.com/EYCTCanvas/FAST.ATF/_build/results?buildId={args.buildid}&view=artifacts&pathAsName=false&type=publishedArtifacts",
                "suites": list_suite
            }
        }],
        "attachments": [attach_image_to_email()],
        "template_id": "d-52ff9590ea354236927aa109e7df961c"
    }
    sendgrid_response = requests.post(url=sendgrid_url, headers=headers, json=body, verify=False)
    print(body)
    print(sendgrid_response)

if __name__ == "__main__":
    main()
