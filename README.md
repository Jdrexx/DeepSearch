# Deep Search Toolkit

A specialized Python toolkit for high-depth information retrieval and deep-web exploration. This project provides two primary interfaces for gathering information from the surface web and the dark web (.onion sites).

## 🚀 Features

- **Deep Extraction**: Goes beyond snippets by fetching and cleaning full-text content from top results.
- **Surface Web Search**: Fetches up to 20 high-relevance results using DuckDuckGo.
- **Dark Web Search**: Fully routed through the Tor network to find and extract data from `.onion` sites.
- **Interactive CLI**: Rich terminal interface with clickable links, status panels, and a search refresh feature.
- **Privacy First**: Local execution with proxy support for sensitive research.

---

## 🛠️ Components

### 1. Surface Deep Search (`src/main.py`)
Used for standard web research where you need broad results and instant content previews.
- **Engine**: DuckDuckGo.
- **Capacity**: 20 results per query.
- **Auto-Extract**: Deep-cleans the top 3 results for immediate reading in the terminal.

### 2. TOR Deep Search (`src/tor_search.py`)
Used for researching hidden services and `.onion` domains safely.
- **Engine**: Ahmia (Onion Index).
- **Network**: All traffic is proxied through SOCKS5 (127.0.0.1:9050).
- **Safety**: Includes a built-in Tor connection validator.

---

## 📋 Prerequisites

1. **Python 3.11+**
2. **Tor Browser** (Required only for the TOR Search feature. It must be open and connected to act as the network gateway.)

---

## 🏃 Launching the Programs

For convenience, use the provided Windows batch files:

### For Surface Web Search:
- Double-click **`launch.bat`**

### For Dark Web Search:
1. Open the **Tor Browser**.
2. Double-click **`launch_tor.bat`**

---

## ⌨️ Command Shortcuts

Inside the interactive prompt:
- `r`: **Refresh** the last search query to check for updated results.
- `exit` or `quit`: Safely close the program.
- **Ctrl + Click**: Open any blue URL directly in your default web browser.

---

## 📁 Project Structure

```text
deep_search/
├── launch.bat          # Surface search launcher
├── launch_tor.bat      # Tor search launcher
├── src/
│   ├── main.py         # Standard search CLI
│   ├── search.py       # Core surface search logic
│   └── tor_search.py   # Core onion search logic
└── venv/               # Isolated dependencies
```
