# Canvas Automation: *ey-canvas-atf-autotesting-core*

## Description
Canvas Automation is a project that provides automated tests for the Canvas web application. It utilizes the Scriptless framework, based on Robot Framework keywords, to interact with Selenium and perform end-to-end (E2E) testing on critical Canvas functionalities.

## Key Features
The Canvas Automation project includes test suites that cover the following functionalities:

### Canvas main Application
- Engagement creation
- Profile completion
- Task creation
- Engagement sharing functionalities
- Archive processes
- Restore processes
- Roll Forward processes

### Economics Application
- Create Project
- Check Canvas Data in Dashboards
- Cosmos DB validations
- Check Financial data
- Check Canvas Data in Dashboards


# Getting Started

## Requirements
1. [git latest version.](https://git-scm.com/downloads)
2. Pycharm or [vscode](https://code.visualstudio.com/download) (**VSCODE recommended**)
4. [python version 3.11.7](https://www.python.org/ftp/python/3.11.7/).
5. [Java Version 11](https://corretto.aws/downloads/latest/amazon-corretto-11-x64-windows-jdk.msi)

## Fresh install:
1. Clone the repo `git clone https://github.com/ey-org/ey-canvas-atf-autotesting-contentgenerator.git`
2. Navigate to your repo `cd ey-canvas-atf-autotesting-contentgenerator`
3. Create a virtual environment in the repository folder: `python -m venv venv`
4. In your code editor, select the Python interpreter from the virtual environment created in the previous step.
5. Activate the venv
   - windows : `.\venv\Scripts\Activate`
   - Linux / macOS: `source venv/bin/activate`
6. Generate a [PAT Token in Azure](https://docs.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=preview-page)
7. Run the following command (replace <PAT-TOKEN> with the generated PAT TOKEN from the previous step):
  - Option1 Generic installation: `pip install CTE-ADO-Script-less==3.7.0 --index-url https://build:<PAT-TOKEN>@eysbp.pkgs.visualstudio.com/_packaging/ADO-Scriptless/pypi/simple`
  - Option2 Using PS1 Script: `.\Resources\scriptlesVersionVerification.ps1 -pat_token '<PAT-TOKEN>' -requiredVersion '3.7.0'`
> [!NOTE]
> Replace 3.7.0 with the version configured for your project, you can ask about this to [@ey-canvas-titans-core](https://github.com/orgs/ey-org/teams/ey-canvas-titans-core)
8. Download the edge driver for your microsoft edge
9. Go to "C:/" and create a folder called "SeleniumWebDrivers"
10. Inside "SeleniumWebDrivers", create another folder called "EdgeDriver"
11. Add the download executable from the edge driver in this location
12. Complete the installation running `pip install -r requirements.txt`
13. Add valid credentials for the executor users as a dictionary. **Please use the [Keyvault script](https://dev.azure.com/EYCTCanvas/FAST.ATF/_wiki/wikis/FAST.ATF.wiki/3056/Secrets-Management)**
    ```Python
    CanvasAutomationUser1={'userName': 'email_value','password': 'password_value','credentialUserName': 'CanvasAutomationUser1'}
    CanvasAutomationUser2={'userName': 'email_value','password': 'password_value','credentialUserName': 'CanvasAutomationUser2'}
    CanvasAutomationUser3={'userName': 'email_value','password': 'password_value','credentialUserName': 'CanvasAutomationUser3'}
    ```

14. Add the folder "C:\FilesForTest\temp" and create the file "TestFile.txt" with some text
 

# Continuous Integration

## Pull Request Verification
The repository includes automated quality checks that run on every pull request:

### Static Analysis Reports
- **Automated reporting**: Static analysis results are automatically posted as comments on pull requests
- **Report location**: Look for the "🔍 Static Analysis Report" comment on your PR
- **Report format**: Reports are collapsible and contain detailed findings from multiple analyzers
- **Status integration**: PRs will show a failed status if critical issues are found

The static analysis framework checks for:
- Duplicate content in XML files
- Skipped test elements
- Test reference integrity
- Variable definitions
- Engagement ID spelling consistency
- Gitignore validation

# Contribute
- [Contributing Guidelines](./CONTRIBUTING.md)
- [Conventional Commits](https://dev.azure.com/EYCTCanvas/FAST.ATF/_wiki/wikis/FAST.ATF.wiki/1818/Conventional-Commits)
- [Branch Strategy and git Flow](https://dev.azure.com/EYCTCanvas/FAST.ATF/_wiki/wikis/FAST.ATF.wiki/1948/Git-Flow-Branching-Strategy)

