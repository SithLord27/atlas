import sys
from rich.console import Console

console = Console()

def help_menu():
    console.print("""
[bold cyan]ATLAS – Personal Study Brain[/bold cyan]

Commands:

  python atlas.py index
  python atlas.py search "query"
  python atlas.py organize
""")

def main():
    if len(sys.argv) < 2:
        help_menu()
        return

    cmd = sys.argv[1]

    if cmd == "index":
        from core import indexer
        indexer.main()        # your existing entry point

    elif cmd == "search":
        from core import search as s
        query = " ".join(sys.argv[2:])
        s.main_cli(query)     # we’ll add this tiny wrapper

    elif cmd == "organize":
        from automation import organizer
        organizer.run()

    else:
        help_menu()


if __name__ == "__main__":
    main()
