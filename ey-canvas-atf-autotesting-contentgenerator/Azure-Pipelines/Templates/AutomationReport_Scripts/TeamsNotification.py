import os
import requests
import json

import urllib3
from string import Template
from NotificationHandler import PostNotification

class TeamsNotification(PostNotification):

    GOOD_COLOR = "Good"  # Green
    WARNING_COLOR = "Warning"  # Yellow
    ATTENTION_COLOR = "Attention"  # Red
    CONTENT_TYPE = "application/json"

    def get_color_for_percentage(self, pass_percentage):
        if pass_percentage >= 75:
            return self.GOOD_COLOR  # Green for Good
        elif 50 <= pass_percentage < 75:
            return self.WARNING_COLOR  # Yellow for Warning
        else:
            return self.ATTENTION_COLOR  # Red for Attention

    def load_template(self, template_path) :
        try:
            base_dir = os.path.dirname(__file__)
            file_path = os.path.join(base_dir, template_path)

            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

        except FileNotFoundError:
            raise FileNotFoundError(f"The template file was not found at the path: {template_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Error parsing the JSON file: {template_path}")
        except Exception as e:
            raise Exception(f"An error occurred while loading the template file: {e}")

    def apply_template_parameters(self, json_string: str, parameters: dict) -> str:
        """Replace the placeholders into a JSON string with the parameters values."""
        for key, value in parameters.items():
            placeholder = f"{{{{{key}}}}}"  # format {{key}}
            json_string = json_string.replace(placeholder, str(value))

        return Template(json_string).safe_substitute(parameters)        

    def send_request(self, webhook_url, body):
        """Sends an HTTP POST request with the specified body."""
        headers = {"Content-Type": self.CONTENT_TYPE}
        try:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            response = requests.post(url=webhook_url, headers=headers, json=body, verify=False)
            response.raise_for_status()
            print("Request was successful!", response.json())
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        
    def send_code_freeze_msg(self, webhook_url, release_version):
        base_dir = os.path.dirname(__file__)
        relative_path = "resources\\CodeFreezeNotificationTemplate.json"
        file_path = os.path.join(base_dir, relative_path)
        template_data = self.load_template(file_path)
        json_string = json.dumps(template_data)
        parameters ={'release_version': f'{release_version}'}
        replaced_string = self.apply_template_parameters(json_string, parameters)
        body = json.loads(replaced_string)
        self.send_request(webhook_url, body)
        

    def send_pre_release_msg(self,webhook_url, release_version, branch_creation_date, release_date):
        base_dir = os.path.dirname(__file__)

        relative_path = "resources\\PreReleaseNotificationTemplate.json"
        file_path = os.path.join(base_dir, relative_path)
        print(file_path)
        template_data = self.load_template(file_path)
        json_string = json.dumps(template_data)
        parameters ={'release_version': f'{release_version}', 
                'release_date': f'{release_date}', 
                'branch_creation_date': f'{branch_creation_date}'
                }
        replaced_string = self.apply_template_parameters(json_string, parameters)
        body = json.loads(replaced_string)
        self.send_request(webhook_url, body)

    def send_post_request(self, webhookUrl, build_id, environment, notification_title, passed_tests, failed_tests, skipped_tests, pass_percentage, formatted_date, release_version):
        base_dir = os.path.dirname(__file__)
        relative_path = "resources\\TeamsNotificationTemplate.json"
        file_path = os.path.join(base_dir, relative_path)
        template_data = self.load_template(file_path)
        json_string = json.dumps(template_data)
        parameters ={'build_id': f'{build_id}', 
                'environment': f'{environment}', 
                'passed_tests': passed_tests, 
                'failed_tests': failed_tests, 
                'skipped_tests': skipped_tests, 
                'pass_percentage': pass_percentage, 
                'formatted_date': f'{formatted_date}', 
                'release_version': f'{release_version}',
                'notification_title':f'{notification_title}',
                'color':f'{self.get_color_for_percentage(pass_percentage)}',
                'GOOD_COLOR' :self.GOOD_COLOR,
                'WARNING_COLOR':self.WARNING_COLOR,
                'ATTENTION_COLOR':self.ATTENTION_COLOR,
                'CONTENT_TYPE':self.CONTENT_TYPE
                }
        
        json_string = json.dumps(template_data)
        replaced_string = self.apply_template_parameters(json_string, parameters)
        body = json.loads(replaced_string)
        self.send_request(webhookUrl, body)
