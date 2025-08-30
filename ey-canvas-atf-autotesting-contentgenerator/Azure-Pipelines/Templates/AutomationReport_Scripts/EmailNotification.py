import requests
import json
import base64
from typing import List, Dict, Any
import json


class _HttpClient:
    @staticmethod
    def post(url: str, headers: Dict[str, str], data: Any) -> requests.Response:
        try:
            response = requests.post(url=url, headers=headers, json=data, verify=False)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"HTTP request failed: {e}")
            return None


class EmailNotification:
    @staticmethod
    def get_chart_attachment() -> str:
        try:
            with open("chart.png", "rb") as img_file:
                encoded_string = base64.b64encode(img_file.read()).decode('utf-8')
            return {
                "content": encoded_string,
                "type": "image/png",
                "filename": "chart.png",
                "disposition": "inline",
                "content_id": "Chart"
            }
        except FileNotFoundError as e:
            print(f"Failed to attach image: {e}")
            return ""

    def send_post_request(
            self, sendgrid_url: str, recipients: List[Dict[str, str]], environment: str, email_subject: str,
            formatted_date: str, release_version: str, pass_percentage: float, total_tests: int,
            passed_tests: int, skipped_tests: int, execution_time: str, list_suite: List[Dict[str, Any]],
            build_id: str, sendgrid_token: str
    ) -> None:
        headers = {
            'Authorization': f'Bearer {sendgrid_token}',
            'Content-Type': 'application/json'
        }
        email_content = {
            "from": {"email": "test.autom.canvas.tt1@ey.com"},
            "personalizations": [{
                "to": recipients,
                "dynamic_template_data": {
                    "environment": environment,
                    "header": f"{email_subject} Automation Report | {environment} | {formatted_date} | {release_version}",
                    "subject": f"{email_subject} Automation Report | {environment} | {formatted_date} | {release_version} | {pass_percentage}% pass",
                    "totaltests": total_tests,
                    "passedtests": passed_tests,
                    "failedtests": total_tests - passed_tests - skipped_tests,
                    "skippedtests": skipped_tests,
                    "Percentage": round((passed_tests / total_tests) * 100, 2),
                    "executionTime": execution_time,
                    "totalSuites": len(list_suite),
                    "buildid": build_id,
                    "emailSubject": email_subject,
                    "artifacts": f"https://dev.azure.com/EYCTCanvas/FAST.ATF/_build/results?buildId={build_id}&view=artifacts&pathAsName=false&type=publishedArtifacts",
                    "suites": list_suite
                }
            }],
            "attachments": [self.get_chart_attachment()],
            "template_id": "d-52ff9590ea354236927aa109e7df961c"
        }
        response = _HttpClient.post(sendgrid_url, headers, email_content)
        if response:
            print("Email sent successfully!")
        else:
            print("Failed to send email.")