# Tool Scout Skill

> AI tool discovery Agent Skill for finding existing software tools across GitHub, npm, MCP servers, Agent Skills, VS Code extensions, Open VSX, and web search before building from scratch.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](pyproject.toml)

Tool Scout is a lightweight **tool discovery skill** for Codex, Claude Code, and other AI coding agents. It helps users and agents answer one practical question:

> "Is there already a software tool, MCP server, Agent Skill, GitHub repo, npm package, VS Code extension, or SaaS product that can solve this problem?"

It is designed for cases where the user or the AI knows the job to be done, but does not know whether the best answer is a GitHub project, npm package, MCP server, Agent Skill, VS Code extension, Open VSX extension, SaaS tool, or another software artifact.

## Common Search Queries This Project Should Match

Tool Scout is relevant for searches like:

- AI tool discovery skill
- find existing software tools before building
- search GitHub npm MCP Agent Skills at once
- MCP server discovery and ranking
- Agent Skill search
- Claude Code tool discovery
- Codex tool discovery
- Vibe Coding tool finder
- software tool scout agent
- find tools by describing a problem
- open source tool discovery for AI agents
- cross-source developer tool search

## What It Does

- Expands a vague tool need into multiple search query families.
- Runs multiple searchers in parallel.
- Searches across GitHub, npm, MCP directories, Agent Skill directories, VS Code Marketplace, Open VSX, and web search.
- Normalizes candidates into one schema.
- Applies only V0/V1 usability gates:
  - V0: source exists and is not obviously dead.
  - V1: metadata or README-level evidence indicates the tool can solve the requested task.
- Ranks surviving candidates by relevance, evidence strength, project quality, adoption, and landing friction.
- Explains why each result is ranked where it is.

## Why It Exists

Normal search often misses useful tools because the user's wording and the builder's wording do not match. A user may ask for a "Skill", but the best answer may be an MCP server, GitHub repository, npm CLI, VS Code extension, or paid SaaS tool.

Tool Scout treats tool discovery as a multi-source retrieval problem:

```text
problem description
  -> query families
  -> parallel searchers
  -> normalized candidates
  -> V0/V1 evidence gates
  -> explainable ranking
```

This is especially useful for AI workflow tooling, Vibe Coding, local agent automation, Claude Code tools, Codex tools, MCP servers, Agent Skills, bridges, integrations, and developer productivity tools.

## Example Use Cases

```bash
python3 .claude/skills/tool-scout/scripts/tool_scout.py "find a tool to control Claude Code from Feishu bot"
```

This query should find candidates such as Feishu/Lark to Claude Code bridges, messaging-to-agent gateways, VS Code extensions, npm packages, and related GitHub projects.

```bash
python3 .claude/skills/tool-scout/scripts/tool_scout.py "self improving agent skill Darwin"
```

This query should find self-improving Agent Skill projects such as Darwin Skill and related skill optimization tools.

## Current Version

This is a first working version. It is intentionally not a heavy validator:

- It does not install packages.
- It does not run MCP servers.
- It does not authenticate with external SaaS tools.
- It does not perform real account or API smoke tests.

## How It Differs From Directories

Tool Scout is not another static AI tools directory. It is a search workflow and Agent Skill that:

- searches multiple tool ecosystems at once;
- accepts a task description instead of requiring the user to know the tool type;
- classifies tool shape after retrieval;
- filters results using V0/V1 evidence gates;
- explains why one candidate ranks above another.

It can complement MCP directories, Agent Skill marketplaces, GitHub search, npm search, VS Code Marketplace, Open VSX, and general web search.

## Skill Entry

The Skill lives at:

```text
.claude/skills/tool-scout/SKILL.md
```

Run the scout directly:

```bash
python3 .claude/skills/tool-scout/scripts/tool_scout.py "find a tool to control Claude Code from Feishu bot"
```

Useful options:

```bash
python3 .claude/skills/tool-scout/scripts/tool_scout.py "self improving agent skill" --limit 12 --json
python3 .claude/skills/tool-scout/scripts/tool_scout.py "Feishu Claude Code bridge" --sources github,npm,vscode,openvsx,mcp,glama,agentskill,web
```

## Environment Variables

The script works without credentials, but optional keys improve coverage and rate limits:

- `GITHUB_TOKEN`: higher GitHub API rate limits.
- If `GITHUB_TOKEN` is not set and GitHub CLI is authenticated, the script will try `gh auth token`.
- `SMITHERY_API_KEY`: Smithery MCP registry search.
- `PULSEMCP_API_KEY`: PulseMCP registry search.
- `BRAVE_API_KEY`: Brave Web Search.

## Included Searchers

First version:

- GitHub repository search
- npm registry search
- Official MCP Registry
- Glama MCP directory
- OpenAgentSkill API
- agentskill.sh API
- VS Code Marketplace
- Open VSX Registry
- Brave Search, if configured
- Jina search endpoint, best effort fallback

Optional searchers:

- Smithery MCP, if `SMITHERY_API_KEY` is configured
- PulseMCP, if `PULSEMCP_API_KEY` is configured

## Ranking Summary

Only candidates passing V0/V1 are ranked.

- Goal match: 45%
- Evidence strength: 20%
- Project quality: 20%
- Landing friction: 10%
- Multi-source corroboration: 5%

The ranking is deliberately explainable rather than opaque.

## Output Schema

The JSON output is designed to be readable by other AI agents:

```json
{
  "need": "Feishu bot controls Claude Code",
  "queries": ["Feishu bot controls Claude Code", "Feishu Claude Code bridge"],
  "sources": ["github", "npm", "mcp", "agentskill"],
  "candidates": [
    {
      "name": "example/tool",
      "kind": "GitHub repo",
      "sources": ["github", "npm"],
      "url": "https://github.com/example/tool",
      "v0": true,
      "v1": true,
      "score": 0.91,
      "scores": {
        "goal_match": 1.0,
        "evidence_strength": 0.85,
        "project_quality": 0.72,
        "landing_friction": 0.8,
        "multi_source": 0.33
      },
      "reasons": ["directly matches the hard terms and direction"]
    }
  ]
}
```

## For LLMs And Search Indexers

The machine-readable summary is available in [`llms.txt`](llms.txt). A longer LLM ingestion note is available in [`docs/llms.md`](docs/llms.md). SEO and GEO notes are in [`docs/seo-geo.md`](docs/seo-geo.md).

## Development

Run tests:

```bash
python3 -m unittest discover -s tests
```
