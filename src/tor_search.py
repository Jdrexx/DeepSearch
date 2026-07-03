import sys
from urllib.parse import unquote
import requests
from bs4 import BeautifulSoup
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

class TorSearchEngine:
    def __init__(self, tor_proxy="socks5h://127.0.0.1:9050"):
        self.proxies = {
            'http': tor_proxy,
            'https': tor_proxy
        }
        self.session = requests.Session()
        self.session.proxies.update(self.proxies)

    def check_tor_connection(self):
        try:
            # Check if we're actually on Tor
            response = self.session.get("https://check.torproject.org/", timeout=15)
            if "Congratulations. This browser is configured to use Tor." in response.text:
                return True
            return False
        except Exception as e:
            console.print(f"[bold red]Connection Error:[/bold red] Could not connect to Tor. Is Tor running on port 9050?\n{e}")
            return False

    def search_onion_ahmia(self, query):
        """Searches Ahmia.fi, which indexes .onion sites."""
        console.print(f"[bold blue]Searching .onion sites for:[/bold blue] {query}...")
        results = []
        try:
            response = self.session.get("https://ahmia.fi/search/", params={"q": query}, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ahmia uses a list with class 'result' for search hits
            for res in soup.find_all('li', class_='result'):
                link_tag = res.find('a')
                title = link_tag.get_text() if link_tag else "No Title"
                url_path = link_tag['href'] if link_tag else "#"
                
                # Cleanup snippet
                snippet_tag = res.find('p')
                snippet = snippet_tag.get_text() if snippet_tag else "No description available."
                
                # Ahmia redirects: /search/redirect?search_result=...&redirect_url=http://onionlink.onion
                if "redirect_url=" in url_path:
                    url_path = unquote(url_path.split("redirect_url=")[1])
                
                results.append({
                    'title': title.strip(),
                    'url': url_path.strip(),
                    'snippet': snippet.strip()
                })
        except Exception as e:
            console.print(f"[bold red]Search Error:[/bold red] {e}")
        return results

    def extract_onion_content(self, url):
        try:
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.decompose()
            text = '\n'.join([p.get_text().strip() for p in soup.find_all(['p', 'h1', 'h2', 'h3']) if p.get_text().strip()])
            return text[:1500] + "..." if len(text) > 1500 else text
        except Exception as e:
            return f"Failed to reach target .onion site: {e}"

    def run_cli(self):
        console.print(Panel(
            "[bold magenta]TOR Deep Search (.onion)[/bold magenta]\n[dim]Routing all traffic through SOCKS5 proxy (127.0.0.1:9050)[/dim]",
            border_style="magenta"
        ))
        
        if not self.check_tor_connection():
            console.print("[red]ERROR: Tor is NOT active or port 9050 is blocked.[/red]")
            console.print("[yellow]Please open the Tor Browser or start the Tor service first.[/yellow]")
            return

        console.print("[green]✔ TOR Connection Verified.[/green]\n")
        last_query = None

        while True:
            user_input = Prompt.ask("[bold yellow]Onion Search Query (or 'r' to refresh, 'exit' to quit)[/bold yellow]")
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
                last_query = user_input
            
            results = self.search_onion_ahmia(search_query)
            if not results:
                console.print("[yellow]No .onion matches found.[/yellow]")
            else:
                for i, res in enumerate(results[:10], 1):
                    console.print(Panel(
                        f"[bold cyan]{res['title']}[/bold cyan]\n[link={res['url']}][blue]{res['url']}[/blue][/link]\n\n{res['snippet']}",
                        title=f"Onion Result {i}",
                        expand=False
                    ))
                    
                    # Optional deep extract for the very first result
                    if i == 1:
                        console.print(f"[dim italic]Deep Extracting first onion site...[/dim italic]")
                        content = self.extract_onion_content(res['url'])
                        console.print(Panel(content, title="Onion Site Content", border_style="green"))
            
            console.print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    engine = TorSearchEngine()
    engine.run_cli()
