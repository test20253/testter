import re
import os
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def extract_endpoints(file_path):
    """Extracts endpoints from the given file and returns them as a dictionary."""
    endpoints = defaultdict(list)
    pattern = r"(self\._\w+|\w+)\s*=\s*['\"](.*?)['\"]"

    if not os.path.exists(file_path):
        console.print(f"[bold red]❌ ERROR:[/] The file at path '{file_path}' does not exist.", style="bold red")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
    except Exception as e:
        console.print(f"[bold red]❌ ERROR:[/] Could not read file '{file_path}'.\n{e}", style="bold red")
        return {}

    matches = re.findall(pattern, content, re.MULTILINE)
    matches = [(key, value.lower()) for key, value in matches]

    for endpoint_name, endpoint_value in matches:
        endpoints[endpoint_value].append(endpoint_name)

    return endpoints

def get_duplicate_endpoints(endpoints):
    """Prints duplicate endpoints in a styled table and returns the count of duplicates."""
    duplicate_count = 0
    table = Table(title="🚨 Duplicate Endpoints Found", header_style="bold blue")
    table.add_column("Endpoint Value", style="cyan", overflow="fold")
    table.add_column("Duplicate Names", style="yellow", overflow="fold")

    for endpoint_value, endpoint_names in endpoints.items():
        if len(endpoint_names) > 1:
            table.add_row(endpoint_value, ", ".join(endpoint_names))
            duplicate_count += 1

    if duplicate_count > 0:
        console.print(table)
    else:
        console.print("[green]✅ No duplicate endpoints found.[/]")

    return duplicate_count

def main():
    dir_path = 'Tests/resources/constants/api'
    
    if not os.path.exists(dir_path):
        console.print(f"[bold red]❌ ERROR:[/] The directory '{dir_path}' does not exist.", style="bold red")
        return
    
    endpoints_file_paths = [
        os.path.join(root, file) 
        for root, _, files in os.walk(dir_path) 
        for file in files if file.endswith('.py')
    ]

    total_duplicate_count = 0
    console.print("\n[bold cyan]---- Duplicate Endpoint Report ----[/]\n")

    for file_path in endpoints_file_paths:
        console.print(f"[bold blue]📄 File:[/] {os.path.splitext(os.path.basename(file_path))[0]}")
        endpoints = extract_endpoints(file_path)
        duplicate_count = get_duplicate_endpoints(endpoints)
        total_duplicate_count += duplicate_count

        if duplicate_count == 0:
            console.print("\t[green]✅ No duplicates found.[/]\n")
        else:
            console.print(f"\t[red]⚠️ Number of duplicates in this file:[/] {duplicate_count}\n")

    console.print(Panel(f"[bold magenta]📊 Total duplicate endpoints across all files: {total_duplicate_count}[/]", style="bold yellow"))

    assert total_duplicate_count == 0, "[bold red]❌ ERROR:[/] The maximum duplicity value has been exceeded!"

if __name__ == "__main__":
    main()
