---
name: deepagents-remember
description: "Review the current conversation and capture valuable knowledge — best practices, coding conventions, architecture decisions, workflows, and user feedback — into persistent memory (CLAUDE.md) or reusable skills. Use when the user says: (1) remember this, (2) save what we learned, (3) update memory, (4) capture learnings."
license: MIT
---

Adapted for Claude Code from langchain-ai/deepagents (MIT, see LICENSE).

Review our conversation and capture valuable knowledge. Focus especially on **best practices** we discussed or discovered: these are the most important things to preserve.

## Step 1: Identify Best Practices and Key Learnings

Scan the conversation for:

### Best Practices (highest priority)
- **Patterns that worked well**: approaches, techniques, or solutions we found effective
- **Anti-patterns to avoid**: mistakes, gotchas, or approaches that caused problems
- **Quality standards**: criteria we established for good code, documentation, or processes
- **Decision rationale**: why we chose one approach over another

### Other Valuable Knowledge
- Coding conventions and style preferences
- Project architecture decisions
- Workflows and processes we developed
- Tools, libraries, or techniques worth remembering
- Feedback the user gave about your behavior or outputs

Skip anything the code or git history already shows, and anything only relevant to this one task.

## Step 2: Decide Where to Store Each Learning

### -> Memory (CLAUDE.md) for preferences and guidelines
Use memory when the knowledge is a preference, a guideline, or a simple rule to always keep in mind.

- **Project** (`./CLAUDE.md` at the repo root): project-specific conventions and decisions. Shared with everyone through git.
- **Personal, this project** (`./CLAUDE.local.md`): private notes for this project; keep it out of git.
- **Global** (`~/.claude/CLAUDE.md`): universal preferences across all projects. In a cloud session this file does not survive the session, so prefer the project file there.

If the project already keeps notes elsewhere (for example a `memory/` folder or `notes/` that CLAUDE.md points to), follow that convention instead of starting a new place.

Keep each CLAUDE.md under about 200 lines: every line is loaded into every session. Merge or replace outdated entries instead of appending duplicates.

### -> Skill for reusable workflows and methodologies
Create a skill when we developed a multi-step process worth reusing, a methodology for a type of task, or a procedure that should be followed consistently. Skills encode **how** to do something well, not just **what** to remember, and load only when needed.

## Step 3: Create Skills for Significant Best Practices

### Skill Location
- Project: `.claude/skills/<skill-name>/SKILL.md` (shared through git)
- Personal: `~/.claude/skills/<skill-name>/SKILL.md`

For anything beyond a simple skill, use the `deepagents-skill-creator` skill.

### Skill Structure
```
skill-name/
├── SKILL.md          (required - main instructions with best practices)
├── scripts/          (optional - executable code)
├── references/       (optional - detailed documentation)
└── assets/           (optional - templates, examples)
```

### SKILL.md Format
```markdown
---
name: skill-name
description: "What this skill does AND when to use it. Include triggers like 'when the user asks to X' or 'when working with Y'. This description determines when the skill activates."
---

# Skill Name

## Overview
Brief explanation of what this skill accomplishes.

## Best Practices
- Best practice 1: explanation
- Best practice 2: explanation

## Process
1. First, do X
2. Then, do Y
3. Finally, do Z

## Common Pitfalls
- Pitfall to avoid and why
```

### Key Principles
1. **Encode best practices prominently**: put them near the top so they guide the whole workflow
2. **Concise is key**: only include non-obvious knowledge
3. **Clear triggers**: the description decides when the skill activates; be specific
4. **Imperative form**: "Create a file", not "You should create a file"
5. **Include anti-patterns**: what NOT to do is often as valuable as what to do

## Step 4: Update Memory for Simpler Learnings

Read the target file first, then use Edit to update it (or Write to create it):

```markdown
## Best Practices
- When doing X, always Y because Z
- Avoid A because it leads to B
```

## Step 5: Summarize Changes

Tell the user what you captured and where:
- Skills created (with the key best practices encoded)
- Memory entries added or changed (with file path)

If the files are in the repo, ask before committing them unless the user already asked you to commit.
