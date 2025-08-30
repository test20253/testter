import datetime
import os
import argparse
import re
from TeamsNotification import TeamsNotification
from typing import Any, Dict, List

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Release Process Automation')
    parser.add_argument("--webhook_release_channel", default="", type=str, help="webhookUrl")
    parser.add_argument("--webhook_general_channel", default="", type=str, help="webhookUrl")
    parser.add_argument("--release_version", default="v00.00.00", type=str, help="release_version")
    parser.add_argument("--branch_creation_date", default="2025-03-11", type=str, help="branch_creation_date")
    parser.add_argument("--release_date", default="2025-03-17", type=str, help="release_date")
    return parser.parse_args()

def send_pre_release_notification(webhookUrl: str, release_version: str, branch_creation_date,release_date) -> None:
    TeamsNotification().send_pre_release_msg(webhookUrl, release_version, branch_creation_date, release_date)

def send_code_freeze_notification(webhookUrl: str, release_version: str) -> None:
    TeamsNotification().send_code_freeze_msg(webhookUrl,release_version )

def main():
    args = parse_arguments()
    send_pre_release_notification(args.webhook_release_channel, args.release_version, args.branch_creation_date, args.release_date)
    send_code_freeze_notification(args.webhook_general_channel, args.release_version)

if __name__ == "__main__":
    main()
