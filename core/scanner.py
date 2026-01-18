import os
from rich.console import Console

console = Console()

def scan_folder(path):
    console.print(f"[cyan]Scanning folder:[/cyan] {path}\n")

    for root, dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)

            console.print(
                f"[green]FILE[/green] → {full_path}"
            )


if __name__ == "__main__":
    scan_folder(".")
