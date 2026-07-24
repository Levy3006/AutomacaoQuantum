import pyfiglet
from rich.console import Console
from rich.text import Text
from datetime import datetime

console = Console()

def print_banner(texto):
    art = pyfiglet.figlet_format(texto, font="big")
    
    
    console.print(f"\n[bold cyan]{art}[/bold cyan]", end="")
    
    console.print(
        "[bold white]  Extraction Automation[/bold white]  "
        "[dim]│  CAPEF · GERIM  │  "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M')}[/dim]"
    )
    console.print("[cyan]" + "─" *100 + "[/cyan]")
    console.print("[cyan]" + "─" *100 + "[/cyan]\n")
