"""Unit tests for the Deep Search Toolkit engines (network mocked).

Covers:
- Surface search result mapping (DDGS output shape -> panel dicts)
- Content extraction truncation + error tolerance
- Tor engine proxy wiring (socks5h through 127.0.0.1:9050)
- Ahmia .onion result parsing incl. the redirect_url unquoting
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest

from search import DeepSearchEngine
from tor_search import TorSearchEngine


class FakeResponse:
    """Minimal requests.Response stand-in."""

    def __init__(self, text: str = "", ok: bool = True):
        self.text = text
        self._ok = ok

    def raise_for_status(self):
        if not self._ok:
            raise RuntimeError("HTTP 500")


class FakeDDGS:
    def __init__(self, results):
        self._results = results

    def text(self, query, max_results=20):
        return self._results


def test_surface_search_maps_results(monkeypatch):
    engine = DeepSearchEngine(max_results=5)
    monkeypatch.setattr(
        engine,
        "ddgs",
        FakeDDGS(
            [
                {"title": "T1", "href": "https://example.com/a", "body": "snip a"},
                {"title": "T2", "href": "https://example.com/b", "body": "snip b"},
            ]
        ),
    )
    results = engine.search("test query")
    assert len(results) == 2
    assert results[0] == {
        "title": "T1",
        "url": "https://example.com/a",
        "snippet": "snip a",
    }


def test_surface_search_empty_on_error(monkeypatch):
    engine = DeepSearchEngine(max_results=5)

    class Boom:
        def text(self, query, max_results=20):
            raise RuntimeError("ddgs down")

    monkeypatch.setattr(engine, "ddgs", Boom())
    assert engine.search("x") == []


def test_content_extraction_truncates(monkeypatch):
    engine = DeepSearchEngine()
    long_html = "<html><body><p>" + "word " * 5000 + "</p></body></html>"

    def fake_get(url, timeout):
        return FakeResponse(long_html)

    monkeypatch.setattr("search.requests.get", fake_get)
    content = engine.extract_content("https://example.com/")
    assert len(content) <= 2003  # 2000 chars + "..."
    assert content.endswith("...")


def test_content_extraction_error_tolerated(monkeypatch):
    engine = DeepSearchEngine()

    def fake_get(url, timeout):
        raise RuntimeError("connection refused")

    monkeypatch.setattr("search.requests.get", fake_get)
    assert "Error extracting" in engine.extract_content("https://example.com/")


def test_tor_engine_uses_socks5h_proxy():
    engine = TorSearchEngine()
    assert engine.proxies["http"] == "socks5h://127.0.0.1:9050"
    assert engine.proxies["https"] == "socks5h://127.0.0.1:9050"


def test_ahmia_parsing_unquotes_redirect_url(monkeypatch):
    engine = TorSearchEngine()
    html = """
    <ul>
      <li class="result">
        <a href="/search/redirect?search_result=x&amp;redirect_url=http%3A%2F%2Fabc123.onion%2Findex">Onion Site</a>
        <p>Some description</p>
      </li>
    </ul>
    """

    class FakeSession:
        proxies = {}

        def get(self, url, params=None, timeout=None):
            return FakeResponse(html)

    monkeypatch.setattr(engine, "session", FakeSession())
    results = engine.search_onion_ahmia("test")
    assert len(results) == 1
    assert results[0]["url"] == "http://abc123.onion/index"
    assert results[0]["title"] == "Onion Site"