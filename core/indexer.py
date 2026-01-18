import os
import json
from pathlib import Path
from PyPDF2 import PdfReader
from rich.console import Console

console = Console()

ALLOWED_EXTENSIONS = (".pdf", ".txt")
IGNORED_FOLDERS = ["venv"]

INDEX_DIR = Path("index")
INDEX_FILE = INDEX_DIR / "atlas_index.json"


def index_files(path):
    indexed = {}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in IGNORED_FOLDERS]

        console.print(f"\n[cyan]Scanning:[/cyan] {root}")

        for name in files:
            full_path = os.path.join(root, name)

            if not name.lower().endswith(ALLOWED_EXTENSIONS):
                console.print(f"[yellow]Ignore[/yellow] {name}")
                continue

            # ---------- PDF HANDLING ----------
            if name.lower().endswith(".pdf"):
                pages = []
                try:
                    pdf = PdfReader(full_path)

                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text() or ""
                        pages.append({
                            "page": i + 1,
                            "text": text
                        })

                except Exception as e:
                    console.print(f"[red]PDF error[/red] {name}: {e}")
                    continue

                indexed[full_path] = pages

            # ---------- TXT HANDLING ----------
            elif name.lower().endswith(".txt"):
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        text = f.read()

                    indexed[full_path] = [{
                        "page": 1,
                        "text": text
                    }]

                except Exception as e:
                    console.print(f"[red]TXT error[/red] {name}: {e}")

    return indexed


def save_index(data):
    INDEX_DIR.mkdir(exist_ok=True)

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

    console.print(f"\n[green]Index saved →[/green] [cyan]{INDEX_FILE}[/cyan]")


if __name__ == "__main__":
    data = index_files(".")

    console.print(f"\n[bold cyan]Indexed {len(data)} files[/bold cyan]\n")

    for f, pages in data.items():
        color = "blue" if f.lower().endswith(".pdf") else "green"

        console.print(
            f"[green]FILE[/green] → "
            f"[{color}]{f}[/{color}] "
            f"([cyan]{len(pages)} pages[/cyan])"
        )

    save_index(data)

def main():
    data = index_files(".")
    
    console.print(f"\n[bold cyan]Indexed {len(data)} files[/bold cyan]\n")

    for f, content in data.items():
        color = "blue" if f.lower().endswith(".pdf") else "green"

        console.print(
            f"[green]FILE[/green] → "
            f"[{color}]{f}[/{color}] "
            f"([cyan]{len(content)} pages[/cyan])"
        )


if __name__ == "__main__":
    main()

