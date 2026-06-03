import sys
import os
from search import DeepSearchEngine
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def main():
    console.print("[bold magenta]Welcome to Deep Search Engine[/bold magenta]")
    console.print("Type 'exit' or 'quit' to stop.\n")
    
    engine = DeepSearchEngine(max_results=20)
    last_query = None
    
    while True:
        user_input = Prompt.ask("[bold yellow]Search Query (or 'r' to refresh last, 'exit' to quit)[/bold yellow]")
            
        if user_input.lower() in ['exit', 'quit']:
            break
            
        # Handle refresh logic
        if user_input.lower() == 'r':
            if not last_query:
                console.print("[yellow]No previous search to refresh.[/yellow]")
                continue
            console.print(f"[dim]Refreshing: {last_query}[/dim]")
            search_query = last_query
        elif not user_input.strip():
            continue
        else:
            search_query = user_input
            last_query = user_input # Store for refresh
            
        try:
            engine.run(search_query)
        except KeyboardInterrupt:
            console.print("\n[yellow]Search interrupted.[/yellow]")
        except Exception as e:
            console.print(f"[bold red]Unexpected Error:[/bold red] {e}")
        
        console.print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
