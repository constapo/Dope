#!/usr/bin/env python3
"""arXiv Search.

Searches the arXiv preprint repository through its public Atom API.
Standard library only: no packages to install.

Adapted for Claude Code from langchain-ai/deepagents (MIT); the original
needed the `arxiv` package and never printed its results.
"""

import argparse
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API_URL = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
SORTS = {"relevance": "relevance", "date": "submittedDate", "updated": "lastUpdatedDate"}


def _build_query(query: str) -> str:
    """Turn plain words into an AND search; pass arXiv field syntax through."""
    if ":" in query:
        return query
    return " AND ".join(f"all:{word}" for word in query.split())


def query_arxiv(query: str, max_papers: int = 10, sort: str = "relevance") -> str:
    """Return formatted results for an arXiv search, or an error message."""
    params = urllib.parse.urlencode(
        {
            "search_query": _build_query(query),
            "start": 0,
            "max_results": max_papers,
            "sortBy": SORTS[sort],
            "sortOrder": "descending",
        }
    )
    request = urllib.request.Request(
        f"{API_URL}?{params}", headers={"User-Agent": "claude-code-arxiv-skill"}
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            feed = ET.fromstring(response.read())
    except Exception as e:  # network or XML errors
        return f"Error querying arXiv: {e}"

    papers = []
    for entry in feed.findall(f"{ATOM}entry"):

        def text(tag: str) -> str:
            node = entry.find(f"{ATOM}{tag}")
            return " ".join(node.text.split()) if node is not None and node.text else ""

        authors = [
            " ".join(a.findtext(f"{ATOM}name", "").split())
            for a in entry.findall(f"{ATOM}author")
        ]
        if len(authors) > 5:
            authors = authors[:5] + ["et al."]
        pdf = next(
            (l.get("href") for l in entry.findall(f"{ATOM}link") if l.get("title") == "pdf"),
            "",
        )
        papers.append(
            f"Title: {text('title')}\n"
            f"Authors: {', '.join(authors)}\n"
            f"Published: {text('published')[:10]}\n"
            f"URL: {text('id')}\n"
            + (f"PDF: {pdf}\n" if pdf else "")
            + f"Summary: {text('summary')}"
        )
    return "\n\n".join(papers) or "No papers found on arXiv."


def main() -> None:
    """Command-line entry point."""
    parser = argparse.ArgumentParser(description="Search arXiv for research papers")
    parser.add_argument("query", help="Search query, e.g. 'diffusion models' or 'ti:transformer AND cat:cs.CL'")
    parser.add_argument("--max-papers", type=int, default=10, help="Maximum results (default: 10)")
    parser.add_argument("--sort", choices=sorted(SORTS), default="relevance", help="Sort order (default: relevance)")
    args = parser.parse_args()

    result = query_arxiv(args.query, max_papers=args.max_papers, sort=args.sort)
    print(result)
    if result.startswith("Error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
