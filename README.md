# Tool Scout Skill

Tool Scout is a lightweight Agent Skill for finding existing software tools before building from scratch.

It is designed for cases where the user or the AI knows the job to be done, but does not know whether the best answer is a GitHub project, npm package, MCP server, Agent Skill, VS Code extension, Open VSX extension, SaaS tool, or another software artifact.

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

## Current Version

This is a first working version. It is intentionally not a heavy validator:

- It does not install packages.
- It does not run MCP servers.
- It does not authenticate with external SaaS tools.
- It does not perform real account or API smoke tests.

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

## Ranking Summary

Only candidates passing V0/V1 are ranked.

- Goal match: 45%
- Evidence strength: 20%
- Project quality: 20%
- Landing friction: 10%
- Multi-source corroboration: 5%

The ranking is deliberately explainable rather than opaque.

## Development

Run tests:

```bash
python3 -m unittest discover -s tests
```
