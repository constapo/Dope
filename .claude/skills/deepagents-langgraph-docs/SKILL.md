---
name: deepagents-langgraph-docs
description: Fetches and references LangGraph Python documentation to build stateful agents, create multi-agent workflows, and implement human-in-the-loop patterns. Use when the user asks about LangGraph, graph agents, state machines, agent orchestration, LangGraph API, or needs LangGraph implementation guidance.
license: MIT
---

# langgraph-docs

Adapted for Claude Code from langchain-ai/deepagents (MIT, see LICENSE).

## Workflow

### 1. Fetch the Documentation Index

Use WebFetch to read https://docs.langchain.com/llms.txt. It lists every documentation page with a short description.

### 2. Select Relevant Documentation

Pick the 2-4 most relevant URLs from the index. Prioritize:
- **Implementation questions**: specific how-to guides
- **Conceptual questions**: core concept pages
- **End-to-end examples**: tutorials
- **API details**: reference docs

### 3. Fetch and Apply

Use WebFetch on the selected URLs (fetch them in parallel), then complete the user's request from the documentation content. Prefer the docs over memory: LangGraph's API changes often.

If WebFetch fails or returns empty content, retry once, then try WebSearch for the topic. If both fail, tell the user and suggest checking https://docs.langchain.com/oss/python/langgraph/overview directly.
