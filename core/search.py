from core.ranker import score_page
import json
import sys
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()

BASE_DIR = Path(__file__).parent.parent
INDEX_FILE = BASE_DIR / "index" / "atlas_index.json"


def load_index():
    if not INDEX_FILE.exists():
        console.print("[red]Index not found! Run indexer first.[/red]")
        sys.exit(1)

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def highlight(text, query):
    t = Text(text)
    t.highlight_words([query], style="bold yellow")
    return t


def search(query):
    index = load_index()

    words = query.lower().split()

    results = []

    for file, pages in index.items():
        for p in pages:

            text = p["text"]

            score = score_page(text, words)

            if score > 0:

                pos = text.lower().find(words[0])
                start = max(0, pos - 70)
                end = min(len(text), pos + 70)

                snippet = text[start:end].replace("\n", " ")

                results.append({
                    "file": file,
                    "page": p["page"],
                    "score": score,
                    "snippet": snippet
                })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

    results.sort(key=lambda x: x["score"], reverse=True)
    return results


def show_results(results, query):
    table = Table(title=f"Results for: '{query}'")

    table.add_column("Book", style="cyan")
    table.add_column("Page", style="magenta")
    table.add_column("Matches", style="yellow")
    table.add_column("Preview", style="green")

    for r in results[:15]:
        table.add_row(
            Path(r["file"]).name,
            str(r["page"]),
            str(r["score"]),
            highlight(r["snippet"], query)
        )

    console.print(table)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: python search.py \"query\"[/yellow]")
        sys.exit(0)

    query = " ".join(sys.argv[1:])
    results = search(query)

    if not results:
        console.print("[red]No matches found[/red]")
    else:
        show_results(results, query)

def main_cli(query):
    results = search(query)

    if not results:
        console.print("[red]No matches found[/red]")
    else:
        show_results(results, query)


