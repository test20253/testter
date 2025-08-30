import xml.etree.ElementTree as ET
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

console = Console()

def get_non_empty_xml_variables(xml_path, include_variable_names):
    """
    Get the names of XML variables that are non-empty and included in the specified list.

    Args:
        xml_path (str): Path to the XML file.
        include_variable_names (list): List of variable names to include in the check.

    Returns:
        list: A list of variable names that have non-empty values and vtypes.
    """
    if not isinstance(include_variable_names, list):
        raise ValueError("[bold red]❌ ERROR:[/bold red] include_variable_names must be a list.")

    include_set = set(include_variable_names)

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        console.print(f"[bold red]❌ ERROR:[/bold red] Failed to parse XML file: {xml_path}\n{e}")
        return []
    except FileNotFoundError:
        console.print(f"[bold red]❌ ERROR:[/bold red] File not found: {xml_path}")
        return []

    non_empty_variables = [
        variable.get('name')
        for variable in root.findall('variable')
        if (variable.get('value') or variable.get('vtype')) and variable.get('name') in include_set
    ]

    if non_empty_variables:
        table = Table(title="🚨 Non-Empty Variables Found", header_style="bold blue")
        table.add_column("Variable Name", style="yellow", overflow="fold")

        for name in non_empty_variables:
            table.add_row(name)

        console.print(table)
        console.print(Panel(f"[bold red]⚠️ Warning:[/bold red] {len(non_empty_variables)} non-empty variables found in var.xml.",
                            title="Summary", style="bold yellow"))

    else:
        console.print("[green]✅ No non-empty variables found.[/green]")

    return non_empty_variables


def main():
    xml_file_path = 'Tests/resources/variable/var.xml'
    include_variable_names = [
        'engagementid_primary', 
        'engagementid_component',
        'engagementid_archive',
        'engagementid_secondary'
    ]

    non_empty_variables = get_non_empty_xml_variables(xml_file_path, include_variable_names)
    assert len(non_empty_variables) == 0, "[bold red]❌ ERROR:[/bold red] Expected no non-empty variables."

if __name__ == "__main__":
    main()
