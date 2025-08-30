import os
import xml.etree.ElementTree as ET
import argparse
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text

console = Console()

def get_module_names_from_xml_file(file_path, tag):
    """
    Extract module names from an XML file based on a given tag.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        return [module.get('name') for module in root.findall(tag) if module.get('name')]
    except ET.ParseError:
        console.print(f"[bold red]❌ ERROR:[/bold red] Failed to parse XML file: {file_path}")
        return []

def find_unique_and_duplicate_names(module_names_list):
    """
    Identify unique and duplicate module names.
    """
    unique_module_names = set()
    duplicates = set()

    for name in module_names_list:
        if name in unique_module_names:
            duplicates.add(name)
        else:
            unique_module_names.add(name)

    return list(unique_module_names), list(duplicates)

def check_for_duplicates_in_directory(directory, tag):
    """
    Check all XML files in the directory for duplicate module names.
    """
    all_files_duplicates = {}  
    files_processed = 0  
    xml_files = [f for f in os.listdir(directory) if f.endswith('.xml')]

    with Progress() as progress:
        task = progress.add_task("[cyan]Scanning XML files...", total=len(xml_files))

        for filename in xml_files:
            files_processed += 1
            file_path = os.path.join(directory, filename)

            module_names_list = get_module_names_from_xml_file(file_path, tag)
            _, duplicates = find_unique_and_duplicate_names(module_names_list)

            if duplicates:
                all_files_duplicates[filename] = duplicates
            
            progress.update(task, advance=1)

    return all_files_duplicates, files_processed 

def main():
    parser = argparse.ArgumentParser(description='Process XML files to find duplicate module names.')
    parser.add_argument('tag', type=str, help='The XML tag to search for (e.g., "test-suite", "test-case", "app-module").')
    parser.add_argument('directory', type=str, help='The directory containing XML files to process.')

    args = parser.parse_args()

    console.print(Panel(Text("🔍 XML Duplicate Name Checker", justify="center", style="bold cyan")))

    duplicates_in_files, total_files_processed = check_for_duplicates_in_directory(args.directory, args.tag)

    if duplicates_in_files:
        table = Table(title="🚨 Files with Duplicate Module Names", header_style="bold red")
        table.add_column("File", style="bold yellow")
        table.add_column("Duplicate Names", style="bold white")

        for filename, duplicates in duplicates_in_files.items():
            table.add_row(filename, ", ".join(duplicates))

        console.print(table)
    else:
        console.print("[green]✅ No duplicate module names found in any XML files.[/green]")

    summary = Panel(f"📄 Total XML files analyzed: {total_files_processed}\n"
                    f"📂 Number of files with duplicates: {len(duplicates_in_files)}",
                    title="📊 Summary", style="bold blue")

    console.print(summary)

    assert len(duplicates_in_files) <= 3, "[bold red]❌ ERROR: The maximum duplicity value has been exceeded.[/bold red]"

if __name__ == "__main__":
    main()
