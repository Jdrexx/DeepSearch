# Deep Search Toolkit

A Python toolkit for information retrieval from the surface web and Tor hidden services (.onion sites). Provides two interfaces — one for standard web search via DuckDuckGo, one for dark web search routed through the Tor network.

## Features

- Surface web search: up to 20 results per query via DuckDuckGo, with auto-extraction of full-text content from top results
- Dark web search: queries routed through Tor SOCKS5 proxy to the Ahmia onion index
- Interactive CLI with clickable links, status panels, and search refresh
- Privacy-first: all execution is local with optional proxy support
- Cross-platform (removed Windows-only batch dependency — runs on Linux, macOS, and Windows)

## Components

### Surface Search (src/main.py)

Standard web research. Fetches 20 results per query, deep-extracts the top 3 for terminal reading.

### Tor Search (src/tor_search.py)

Hidden service research. All traffic through SOCKS5 (127.0.0.1:9050) with built-in Tor connection validation.

## Prerequisites

- Python 3.11+
- Tor Browser (required for Tor Search — must be connected before searching .onion sites)

## Quick Start

```bash
# Surface search
python src/main.py

# Tor search (Tor Browser must be running)
python src/tor_search.py
```

Windows users can double-click `launch.bat` (surface search) or `launch_tor.bat` (Tor search — Tor Browser must be open first).

## Interactive Commands

| Key             | Action                                  |
| --------------- | --------------------------------------- |
| `r`             | Refresh last search for updated results |
| `exit` / `quit` | Close the program                       |
| Ctrl+Click      | Open a URL in your browser              |

## Project Structure

```
deep_search/
├── src/
│   ├── main.py        # Standard search CLI
│   ├── search.py      # Core surface search logic
│   └── tor_search.py  # Core onion search logic
└── venv/              # Isolated dependencies
```