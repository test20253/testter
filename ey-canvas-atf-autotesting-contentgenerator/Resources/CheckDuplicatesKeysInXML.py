import argparse
import os
import xml.etree.ElementTree as ET
import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

try:
    from CustomExceptions.InvalidKeyException import InvalidKeyException
except ModuleNotFoundError:
    import pathlib
    import sys
    sys.path.append(str(pathlib.Path(__file__).parent.parent))
    from CustomExceptions.InvalidKeyException import InvalidKeyException


def print_exception_list(exceptions, message, level="ERROR"):
    """Prints exceptions using `rich` and raises an error if level is 'ERROR'."""
    if exceptions:
        panel_title = "[bold red]❌ ERRORS[/]" if level == "ERROR" else "[bold yellow]⚠️ WARNINGS[/]"
        panel_message = "\n".join(exceptions)
        console.print(Panel(panel_message, title=panel_title, border_style="red" if level == "ERROR" else "yellow"))
        
        if level == "ERROR":
            raise Exception(message)


def get_duplicate_key_values_in_list(list_dict, file_name, unique_keys):
    """Finds duplicate key values in a list of dictionaries."""
    df = pd.DataFrame(list_dict)

    try:
        repeated_rows_len = len(df[unique_keys]) - len(df[unique_keys].drop_duplicates())
    except Exception as e:
        raise InvalidKeyException(
            f"🔴 The file '{file_name}' does not contain one or more of the keys {unique_keys}. Details: {str(e)}"
        )

    repeated_rows_df = df.groupby(unique_keys, as_index=False).size()
    repeated_rows_df = repeated_rows_df[repeated_rows_df["size"] > 1].rename(columns={"size": "Occurrences"}).dropna()

    return {
        "repeated_rows_len": repeated_rows_len,
        "repeated_rows_dataframe": repeated_rows_df.astype({"Occurrences": "int32"})
    }


def verify_no_duplicate_key_in_xml_files(directory, unique_keys, files_to_check=[]):
    """Verifies that no duplicate keys exist in XML files within a directory."""
    errors = []
    warnings = []

    if not os.path.exists(directory):
        console.print(Panel(f"[bold red]❌ ERROR:[/] The directory '{directory}' does not exist.", border_style="red"))
        return

    for filename in os.listdir(directory):
        if filename.endswith(".xml") and (filename in files_to_check or not files_to_check):
            file_path = os.path.join(directory, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                try:
                    root = ET.parse(file).getroot()
                    list_dict = [dict((attr.tag, attr.text) for attr in el) for el in root]
                except ET.ParseError:
                    warnings.append(f"⚠️ Skipping file '{filename}' due to XML parsing errors.")
                    continue

                try:
                    duplicates_dict = get_duplicate_key_values_in_list(list_dict, filename, unique_keys)

                    if duplicates_dict["repeated_rows_len"] > 0:
                        table = Table(title=f"🚨 Duplicates Found in {filename}", header_style="bold blue")
                        for key in unique_keys:
                            table.add_column(key, style="cyan", overflow="fold")
                        table.add_column("Occurrences", style="yellow")

                        for _, row in duplicates_dict["repeated_rows_dataframe"].iterrows():
                            table.add_row(*[str(row[key]) for key in unique_keys], str(row["Occurrences"]))

                        console.print(Panel(table, title=f"[bold red]❌ Duplicates in {filename}[/]", border_style="red"))
                        errors.append(f"🔴 {duplicates_dict['repeated_rows_len']} duplicate entries found in {filename}.")

                except InvalidKeyException as e:
                    warnings.append(str(e))

    print_exception_list(
        exceptions=warnings,
        message=f"⚠️ Some files in '{directory}' could not be reviewed. Check the logs for details.",
        level="WARNING"
    )

    print_exception_list(
        exceptions=errors,
        message=f"❌ Duplicate {unique_keys} found in some files in '{directory}'. Check the logs for details."
    )

    if not errors:
        console.print(Panel("[bold green]✅ No duplicate keys found in the XML files![/]", border_style="green"))


def list_of_strings(arg):
    """Converts a comma-separated string to a list of strings."""
    try:
        return [] if arg == "[]" else arg.replace("<SPACE>", " ").split(",")
    except:
        return []


def main():
    parser = argparse.ArgumentParser(description="🔍 Process XML files to find duplicate key names.")
    parser.add_argument("unique_keys", type=list_of_strings, help="Keys to check for duplicates (e.g., ['ID'])")
    parser.add_argument("directory", type=str, help="Directory containing XML files to analyze")
    parser.add_argument("files_to_check", default=[], type=list_of_strings,
                        help="List of specific XML files to check (e.g., ['test.xml']). Leave empty to check all.")

    args = parser.parse_args()

    verify_no_duplicate_key_in_xml_files(
        directory=args.directory,
        unique_keys=args.unique_keys,
        files_to_check=args.files_to_check
    )


if __name__ == "__main__":
    main()
