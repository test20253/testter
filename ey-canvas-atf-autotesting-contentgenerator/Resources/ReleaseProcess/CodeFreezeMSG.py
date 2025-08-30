import subprocess
import re
import argparse
import json

def run_command(command):
    """Executes a terminal command and returns the output, handling errors."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {' '.join(command)}\n{e}")
        return None

def parse_arguments() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="GitHub Issue and PR Automation")
    parser.add_argument("--repo", type=str, default="", help="GitHub repository (e.g., ey-org/ey-canvas-atf-autotesting-oversight)")
    return parser.parse_args()

def get_open_prs(repo):
    """Retrieves the list of open PRs in JSON format."""
    result = run_command(["gh", "pr", "list", "--repo", repo, "--state", "open", "--json", "number"])
    return json.loads(result) if result else []

def add_comment_to_pr(repo, pr_number, message):
    """Adds a review comment to a PR."""
    command = ["gh", "pr", "review", str(pr_number), "--comment", "-b", message, "--repo", repo]
    if run_command(command) is not None:
        print(f"Comment added to PR #{pr_number}")
    else:
        print(f"Failed to add comment to PR #{pr_number}")

def main():
    args = parse_arguments()
    repo = args.repo
    message = """# CODE FREEZE !
    We are currently in a **CODE FREEZE** due to the release stabilization process.
    Merging is allowed once the new release is published.
    """

    open_prs = get_open_prs(repo)
    if open_prs:
        for pr in open_prs:
            add_comment_to_pr(repo, pr["number"], message)
        print("All comments added successfully.")
    else:
        print("No open PRs found.")

if __name__ == "__main__":
    main()
