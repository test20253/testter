import datetime
import requests
import matplotlib.pyplot as plt
import base64
from dateutil import parser
from typing import List, Dict, Any
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class _HttpClient:
    @staticmethod
    def get(url: str, auth: Any) -> requests.Response:
        try:
            response = requests.get(url=url, auth=auth, verify=False)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None

class _DataProcessor:
    @staticmethod
    def calculate_execution_time(start_time) -> str:
        current_time = datetime.datetime.utcnow()
        converted_current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        convert_start_time = parser.isoparse(start_time)
        convert_finish_time = parser.isoparse(converted_current_time)
        diff = convert_finish_time - convert_start_time
        total_seconds = diff.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{int(hours)}: {int(minutes)}: {seconds:.2f}"


    @staticmethod
    def format_release_version(branch_name: str) -> str:
        release_version = branch_name.replace('refs/heads/', '')
        release_version = release_version.replace('/', ' ')
        return release_version

    @staticmethod
    def format_recipients(email_recipients: str, requested_by: str) -> List[Dict[str, str]]:
        email_recipients = email_recipients.lower().split(',')
        email_recipients = [email.strip() for email in email_recipients]
        requested_by = requested_by.strip().lower()

        if requested_by.endswith("@ey.com") and requested_by not in email_recipients:
            email_recipients.append(requested_by)

        return [{"email": email} for email in email_recipients]

    @staticmethod
    def calculate_pass_percentage(passed_tests: int, total_tests: int) -> float:
        return round((passed_tests / total_tests) * 100, 2)

    @staticmethod
    def calculate_failed_tests(total_tests: int, passed_tests: int, skipped_tests: int) -> int:
        return total_tests - passed_tests - skipped_tests

class _ChartGenerator:
    @staticmethod
    def generate_pie_chart(passed_tests: int, failed_tests: int, skipped_tests: int, filename: str = 'chart.png') -> None:
        fig, ax = plt.subplots()
        labels = []
        values = []
        colors = []

        if passed_tests > 0:
            labels.append('Passed')
            values.append(passed_tests)
            colors.append('#068E06')  # Light Green

        if failed_tests > 0:
            labels.append('Failed')
            values.append(failed_tests)
            colors.append('#F60C0C')  # Red

        if skipped_tests > 0:
            labels.append('Skipped')
            values.append(skipped_tests)
            colors.append('#FF6600')  # Yellow

        ax.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, wedgeprops={'edgecolor': 'white'})
        ax.set_title('Test Results')
        plt.tight_layout()  # Adjusts the spacing between subplots to prevent label overlap
        plt.savefig(filename)

    @staticmethod
    def attach_image_to_email(filename: str = 'chart.png') -> Dict[str, str]:
        try:
            with open(filename, "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            return {
                "content": encoded_string,
                "type": "image/png",
                "filename": filename,
                "disposition": "inline",
                "content_id": "Chart"
            }
        except FileNotFoundError as e:
            print(f"Failed to attach image: {e}")
            return {}

class PipelineDataExtractor:
    BUILD_URL_TEMPLATE = "https://dev.azure.com/EYCTCanvas/FAST.ATF/_apis/build/builds/{build_id}"
    TEST_RUNS_URL_TEMPLATE = "https://dev.azure.com/EYCTCanvas/FAST.ATF/_apis/test/runs?includeRunDetails=true&api-version=6.0&buildUri=vstfs:///Build/Build/{build_id}"

    def __init__(self, build_id: str, auth: Any):
        self.build_id = build_id
        self.auth = auth
        self.pipeline_data = self._get_pipeline_data()
        self.test_totals = self._get_test_totals()

    def _get_pipeline_data(self) -> Dict[str, Any]:
        url_for_time = self.BUILD_URL_TEMPLATE.format(build_id=self.build_id)
        time_response = _HttpClient.get(url_for_time, self.auth)
        if time_response is None:
            raise Exception("Failed to get time response")
        return time_response.json()

    def get_execution_time(self) -> str:
        start_time = self.pipeline_data['startTime']
        return _DataProcessor.calculate_execution_time(start_time)

    def get_release_version(self) -> str:
        branch_name = self.pipeline_data['sourceBranch']
        return _DataProcessor.format_release_version(branch_name)

    def _get_test_totals(self) -> Dict[str, int]:
        url = self.TEST_RUNS_URL_TEMPLATE.format(build_id=self.build_id)
        list_of_testruns = _HttpClient.get(url, self.auth).json().get('value', [])
        total_tests = 0
        passed_tests = 0
        skipped_tests = 0
        list_suite = []

        for get in list_of_testruns:
            total_tests += get['totalTests']
            passed_tests += get['passedTests']
            skipped_tests += get['notApplicableTests']
            list_suite.append({
                'serial': list_of_testruns.index(get) + 1,
                'suitename': get['name'],
                'passedtests': get['passedTests'],
                'failedtests': get['totalTests'] - get['passedTests'] - get['notApplicableTests'],
                'skippedtests': get['notApplicableTests'],
                'totaltests': get['totalTests'],
                'percentage': round((get['passedTests'] / get['totalTests']) * 100, 2),
                'runlink': get['webAccessUrl']
            })

        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'skipped_tests': skipped_tests,
            'list_suite': list_suite
        }

    def get_test_totals(self) -> Dict[str, int]:
        return self.test_totals

    def get_recipients(self, email_recipients: str) -> List[Dict[str, str]]:
        requested_by = self.pipeline_data['requestedBy']['uniqueName']
        return _DataProcessor.format_recipients(email_recipients, requested_by)

    def get_formatted_date(self) -> str:
        current_date = datetime.datetime.now()
        return current_date.strftime("%m-%d-%Y")

    def get_failed_tests(self) -> int:
        return _DataProcessor.calculate_failed_tests(self.test_totals['total_tests'], self.test_totals['passed_tests'], self.test_totals['skipped_tests'])

    def get_pass_percentage(self) -> float:
        return _DataProcessor.calculate_pass_percentage(self.test_totals['passed_tests'], self.test_totals['total_tests'])

    def generate_pie_chart(self, filename: str = 'chart.png') -> None:
        _ChartGenerator.generate_pie_chart(self.test_totals['passed_tests'], self.get_failed_tests(), self.test_totals['skipped_tests'], filename)