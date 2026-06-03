import sys
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

class DeepSearchEngine:
    def __init__(self, max_results=20):
        self.max_results = max_results
        self.ddgs = DDGS()

    def search(self, query):
        console.print(f"[bold blue]Searching for:[/bold blue] {query}...")
        results = []
        try:
            search_results = self.ddgs.text(query, max_results=self.max_results)
            for res in search_results:
                results.append({
                    'title': res['title'],
                    'url': res['href'],
                    'snippet': res['body']
                })
        except Exception as e:
            console.print(f"[bold red]Search Error:[/bold red] {e}")
        return results

    def extract_content(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text[:2000] + "..." if len(text) > 2000 else text
        except Exception as e:
            return f"Error extracting {url}: {e}"

    def run(self, query):
        results = self.search(query)
        if not results:
            console.print("[yellow]No results found.[/yellow]")
            return

        for i, res in enumerate(results, 1):
            console.print(Panel(
                f"[bold cyan]{res['title']}[/bold cyan]\n[link={res['url']}][blue]{res['url']}[/blue][/link]\n\n{res['snippet']}",
                title=f"Result {i}",
                expand=False
            ))
            
            # Extract content for MORE results automatically (top 3)
            if i <= 3:
                console.print(f"\n[bold green]Deep Extracting from Result {i}...[/bold green]")
                content = self.extract_content(res['url'])
                console.print(Panel(content, title=f"Extracted Content {i} (Preview)", border_style="green"))
                console.print("-" * 50)

if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Python programming best practices"
    engine = DeepSearchEngine()
    engine.run(query)
