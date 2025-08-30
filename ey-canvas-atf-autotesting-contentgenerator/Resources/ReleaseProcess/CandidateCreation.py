import subprocess
import re
import argparse

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing: {' '.join(command)}\n{e}")
        return None

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Release Process Automation")
    parser.add_argument("--release_version", type=str, default="v9.2.2",  help="Release version (v2.0, v3.0.1, etc.)")
    parser.add_argument("--repo", type=str, default= "", help="GitHub repository (e.g., ey-org/ey-canvas-atf-autotesting-oversight)")

    return parser.parse_args()

def main():
    args = parse_arguments()
    release_version = args.release_version
    repo = args.repo

    tasks = [
        f"release/CG_candidate_{release_version}",
        f"release/RC_candidate_{release_version}"
    ]

    # Create the main issue and get its number
    main_issue_output = run_command(["gh", "issue", "create", "--repo", repo, "--title", f"Release {release_version} ",
                                     "--body", f"This is the main issue for release {release_version}.", "--label", "release"])

    # Validate that the main issue was created successfully
    main_issue_match = re.search(r".*/(\d+)$", main_issue_output)
    if main_issue_match:
        main_issue_number = main_issue_match.group(1)
        print(f"Main issue created: #{main_issue_number}")
    else:
        print("Error creating the main issue.")
        exit(1)

    # Try to create the branch for the main issue
    branch_name = f"release/candidate_{release_version}"
    branch_output = run_command(["gh", "issue", "develop", main_issue_number, "--repo", repo, "--base", "Develop", "--name", branch_name])
    if branch_output:
        print(f"Branch created: {branch_name} based on Develop")
    else:
        print(f"Could not create branch for: {branch_name}, but the process will continue.")

    # Create sub-issues and branches
    sub_issues = []
    for task in tasks:
        sub_issue_output = run_command(["gh", "issue", "create", "--repo", repo, "--title", task,
                                        "--body", f"Sub-issue for task: {task}", "--label", "release"])

        sub_issue_match = re.search(r".*/(\d+)$", sub_issue_output)
        if sub_issue_match:
            sub_issue_number = sub_issue_match.group(1)
            sub_issues.append(f"- [ ] #{sub_issue_number} {task}")
            print(f"Sub-issue created: #{sub_issue_number} -> {task}")

            # Try to create the branch for the sub-issue
            branch_output = run_command(["gh", "issue", "develop", sub_issue_number, "--repo", repo, "--base", "Develop", "--name", task])
            if branch_output:
                print(f"Branch created: {task} based on Develop")
            else:
                print(f"Could not create branch for: {task}, but the process will continue.")
        else:
            print(f"Error creating sub-issue for: {task}")

    # Update the main issue with the list of sub-issues
    if sub_issues:
        issue_body = "### Tasks\n" + "\n".join(sub_issues)
        update_output = run_command(["gh", "issue", "edit", main_issue_number, "--repo", repo, "--body", issue_body])
        if update_output:
            print("Main issue updated with sub-issues.")
    else:
        print("No sub-issues were created.")

if __name__ == "__main__":
    main()
