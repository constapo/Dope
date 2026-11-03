---
name: deepagents-web-research
description: Searches multiple web sources, synthesizes findings, and produces cited research reports using delegated subagents. Use when the user asks to research a topic online, search the web, look something up, find current information, compare options, or produce a research report.
license: MIT
---

# Web Research Skill

Adapted for Claude Code from langchain-ai/deepagents (MIT, see LICENSE).

For a quick fact, skip this process and answer with one or two WebSearch calls. Use it for questions that need several sources, comparisons, or a written report.

## Research Process

### Step 1: Create and Save a Research Plan

Before delegating, you MUST:

1. **Create a research folder** in the scratchpad directory if the session has one, otherwise in the working directory: `research_[topic_name]/`. Use the scratchpad unless the user wants the report kept in the project.
2. **Analyze the research question**: break it into distinct, non-overlapping subtopics.
3. **Write the plan** with the Write tool to `research_[topic_name]/research_plan.md`:
   - The main research question
   - 2-5 specific subtopics to investigate
   - Expected information from each subtopic
   - How results will be synthesized

**Planning guidelines:**
- **Simple fact-finding**: 1-2 subtopics
- **Comparative analysis**: 1 subtopic per compared item (max 3)
- **Complex investigations**: 3-5 subtopics

### Step 2: Delegate to Research Subagents

For each subtopic, use the Agent tool (`general-purpose` subagent) with:
- A clear, specific research question (no acronyms)
- The absolute path of the findings file it must write: `research_[topic_name]/findings_[subtopic].md`
- A budget of 3-5 web searches

Launch up to 3 subagents at once by putting the Agent calls in a single message, and set `run_in_background: false` so you wait for the findings.

**Subagent prompt template:**
```
Research [SPECIFIC TOPIC]. Use WebSearch to gather information and WebFetch to read the most useful pages.
When done, use the Write tool to save your findings to [ABSOLUTE PATH]/findings_[subtopic].md.
Include key facts, relevant quotes, and source URLs. Use 3-5 web searches maximum.
Reply with one line confirming the file was written.
```

### Step 3: Synthesize Findings

After all subagents finish:

1. **Read the findings files**: Glob `research_[topic_name]/findings_*.md`, then Read each one.
2. **Synthesize** a response that:
   - Directly answers the original question
   - Integrates insights from all subtopics
   - Cites specific sources with URLs (from the findings files)
   - Names any gaps, conflicts between sources, or limitations
3. **Write a final report** (if requested) to `research_[topic_name]/research_report.md`, and give the user its full absolute path.

To check a detail yourself, use WebFetch on the URL; Read is for local files only.

## Best Practices

- **Plan before delegating**: always write research_plan.md first
- **Clear subtopics**: give each subagent a distinct, non-overlapping scope
- **File-based communication**: subagents save findings to files instead of returning long text, which keeps your context small
- **Systematic synthesis**: read every findings file before answering
- **Stop appropriately**: 3-5 searches per subtopic is usually enough
