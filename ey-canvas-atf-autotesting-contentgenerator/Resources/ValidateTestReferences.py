import os
import xml.etree.ElementTree as ET
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

# Base paths
BASE_PATH_SUITE = "Tests/test_suites"
BASE_PATH_TEST = "Tests/test_cases"
MAX_ERRORS_ALLOWED = 0
MAX_NOT_FOUND_ALLOWED = 0

# Status constants
STATUS_FOUND = "Found"
STATUS_NOT_FOUND = "Test Not Found"
STATUS_FILE_NOT_FOUND = "Test File Not Found"
STATUS_XML_PARSE_ERROR = "XML Parse Error"

# Rich color constants
COLOR_ERROR = "red"
COLOR_SUCCESS = "green"
COLOR_WARNING = "yellow"
COLOR_INFO = "cyan"
COLOR_HIGHLIGHT = "magenta"

console = Console()

# Cache to avoid reading the same test file several times
test_file_cache = {}


# Cache to avoid reading the same test file several times
test_file_cache = {}

def parse_test_suite(xml_file):
    """Extract test cases and their reference files from a test suite XML file."""
    if not os.path.exists(xml_file):
        console.print(f"[{COLOR_ERROR}]❌ The file {xml_file} does not exist.[/{COLOR_ERROR}]")
        return []

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except ET.ParseError:
        console.print(f"[{COLOR_ERROR}]❌ Failed to parse the XML file {xml_file}.[/{COLOR_ERROR}]")
        return []
    test_cases = []
    for test_case in root.findall(".//test-case"):
        file_name = test_case.get("test-case-file")
        case_name = test_case.get("test-case-name")
        if file_name and case_name:
            test_cases.append((file_name, case_name))

    return test_cases

def load_test_cases_from_file(test_file):
    """Load test cases from an XML file and cache them."""
    full_path = os.path.join(BASE_PATH_TEST, test_file)
    
    if full_path in test_file_cache:
        return test_file_cache[full_path]
    
    if not os.path.exists(full_path):
        return STATUS_FILE_NOT_FOUND

    try:
        test_cases = set()
        for event, elem in ET.iterparse(full_path, events=("start",)):
            if elem.tag == "test-case":
                name = elem.get("name")
                if name:
                    test_cases.add(name)
        test_file_cache[full_path] = test_cases
        return test_cases
    except ET.ParseError:
        return STATUS_XML_PARSE_ERROR

def check_test_case_exists(test_cases, test_case_name):
    """Check if a specific test case exists within the loaded test cases."""
    if isinstance(test_cases, str):  # Handles error statuses
        return test_cases
    return STATUS_FOUND if test_case_name in test_cases else STATUS_NOT_FOUND

def test_case_exists_in_file(test_file, test_case_name):
    """Check if a specific test case exists in the referenced XML file."""
    test_cases = load_test_cases_from_file(test_file)
    return check_test_case_exists(test_cases, test_case_name)

def analyze_suite(xml_file, verbose):
    """Analyze a single test suite."""
    test_cases = parse_test_suite(xml_file)
    suite_results = []

    if verbose:
        console.print(f"\n🔍 [bold cyan]Checking test cases in suite:[/bold cyan] {xml_file}\n")

    for file_name, case_name in test_cases:
        result = test_case_exists_in_file(file_name, case_name)
        suite_results.append((xml_file, file_name, case_name, result))

        if verbose:
            status_msg = {
                STATUS_FOUND: f"✅ {case_name} found in {file_name}",
                STATUS_NOT_FOUND: f"❌ {case_name} NOT found in {file_name}",
            }.get(result, f"⚠️ {case_name}: {result} ({file_name})")
            console.print(status_msg)

    return suite_results

def display_summary(all_results):
    """Display summary table of results."""
    summary_table = Table(title="Summary of Test Case Validation", show_lines=True)
    summary_table.add_column("Status", justify="center")
    summary_table.add_column("Count", justify="center")

    total_cases = len(all_results)
    found_cases = sum(1 for _, _, _, status in all_results if status == STATUS_FOUND)
    not_found_cases = sum(1 for _, _, _, status in all_results if status == STATUS_NOT_FOUND)
    error_cases = sum(1 for _, _, _, status in all_results if status not in [STATUS_FOUND, STATUS_NOT_FOUND])

    summary_table.add_row("✅ Found", str(found_cases))
    summary_table.add_row("❌ Not Found", str(not_found_cases))
    summary_table.add_row("⚠️ Errors", str(error_cases))
    summary_table.add_row("📊 Total Cases", str(total_cases))

    console.print("\n📌 [bold cyan]Validation Summary:[/bold cyan]")
    console.print(summary_table)

def display_errors(all_results):
    """Display details of missing or error test cases."""
    error_cases = [result for result in all_results if result[3] != "Found"]
    if error_cases:
        error_table = Table(title="Details of Missing or Error Test Cases", show_lines=True)
        error_table.add_column("Suite File", justify="left", style="cyan")
        error_table.add_column("Test File", justify="left", style="magenta")
        error_table.add_column("Test Case", justify="left", style="yellow")
        error_table.add_column("Status", justify="center", style="red")

        for suite_file, test_file, test_case, status in error_cases:
            error_table.add_row(suite_file, test_file, test_case, status)
            console.print(f'Suite File: {suite_file}')
            console.print(f'Test File:  {test_file}')
            console.print(f'Missing Test Case:  {test_case}')
            console.print("\n")

        console.print("\n🚨 [bold red]Errors and Missing Test Cases Summary:[/bold red]")
        console.print(error_table)

def check_assertions(not_found_cases, error_cases):
    """Check and print assertion failures."""
    failed_assertions = []
    if error_cases > MAX_ERRORS_ALLOWED:
        failed_assertions.append(f"🚨 Assertion Failed: Too many errors ({error_cases} > {MAX_ERRORS_ALLOWED})")
    if not_found_cases > MAX_NOT_FOUND_ALLOWED:
        failed_assertions.append(f"🚨 Assertion Failed: Too many missing test cases ({not_found_cases} > {MAX_NOT_FOUND_ALLOWED})")
    
    if failed_assertions:
        console.print("\n❌ [bold red]Assertions Failed:[/bold red]")
        for failure in failed_assertions:
            console.print(f"   {failure}")
    assert not failed_assertions, "One or more assertions failed."

def main():
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description="Validate test cases in XML test suites.")
    parser.add_argument("--verbose", action="store_true", help="Show detailed logs.")
    parser.add_argument("--suite-file", type=str, help="Analyze only a specific test suite XML file.")
    args = parser.parse_args()
    
    all_results = []
    if args.suite_file:
        suite_path = os.path.join(BASE_PATH_SUITE, args.suite_file)
        if os.path.exists(suite_path):
            all_results.extend(analyze_suite(suite_path, args.verbose))
        else:
            console.print(f"[red]❌ Error: The specified suite file '{args.suite_file}' does not exist.[/red]")
            return
    else:
        suite_files = [os.path.join(BASE_PATH_SUITE, f) for f in os.listdir(BASE_PATH_SUITE) if f.endswith(".xml")]
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(analyze_suite, suite, args.verbose): suite for suite in suite_files}
            for future in as_completed(futures):
                all_results.extend(future.result())
    
    display_summary(all_results)
    display_errors(all_results)
    check_assertions(sum(1 for _, _, _, status in all_results if status == STATUS_NOT_FOUND),
                     sum(1 for _, _, _, status in all_results if status not in [STATUS_FOUND, STATUS_NOT_FOUND]))
    console.print(f"\n⏳ Execution Time: {time.time() - start_time:.2f} seconds\n")

if __name__ == "__main__":
    main()
