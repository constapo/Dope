---
name: deepagents-arxiv-search
description: Searches arXiv for preprints and academic papers, retrieves abstracts, and filters by topic. Use when the user asks to find research papers, search arXiv, look up preprints, find academic articles in physics, math, CS, biology, statistics, or related fields.
license: MIT
---

# arXiv Search Skill

Adapted for Claude Code from langchain-ai/deepagents (MIT, see LICENSE).

## Usage

Run the bundled script with Bash. It needs only Python 3 (no packages). Use this skill's base directory, shown when the skill loads:

```bash
python3 <skill-base-dir>/arxiv_search.py "your search query" [--max-papers N] [--sort relevance|date|updated]
```

- `query` (required): plain words search everywhere; arXiv field syntax also works, e.g. `ti:transformer AND cat:cs.CL`, `au:hinton`
- `--max-papers` (optional): maximum results (default 10)
- `--sort` (optional): `relevance` (default), `date` (newest submitted), or `updated`

### Example

```bash
python3 .claude/skills/deepagents-arxiv-search/arxiv_search.py "deep learning drug discovery" --max-papers 5
```

Prints title, authors, publication date, abstract URL, PDF link and abstract for each paper.

## Tips

- For "latest" or "recent" papers, use `--sort date`.
- To read a paper in full, open its PDF or abstract URL with WebFetch.
- Cite papers with their arXiv URL in the answer.
