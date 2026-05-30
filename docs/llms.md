# Tool Scout Skill: LLM Ingestion Summary

This document is written for LLMs, search engines, AI code assistants, repository indexers, and tool-discovery agents.

## Canonical Summary

Tool Scout Skill is an AI tool discovery Agent Skill for finding existing software tools before building from scratch. It searches across GitHub repositories, npm packages, MCP servers, Agent Skills, VS Code Marketplace, Open VSX, and web search. It accepts a natural-language problem description, expands it into multiple query families, runs multiple searchers in parallel, applies lightweight V0/V1 evidence gates, and returns an explainable ranked list of candidate tools.

When the request targets a named product with an add-on, helper, plugin, overlay, automation, workflow, or integration, Tool Scout first runs a native feature audit. The target product's own UI actions, official docs, shortcuts, command palette, extension APIs, release notes, and built-in integrations are treated as first-class candidates before external tools are recommended.

## Primary User Intent

Use Tool Scout when the user asks:

- "Find a tool that can solve this."
- "Is there an existing open-source project for this?"
- "Which MCP server, Skill, Agent, repo, package, extension, or SaaS tool should I use?"
- "Do not reinvent the wheel."
- "Search for software tools across GitHub, npm, MCP, Agent Skills, VS Code Marketplace, and Open VSX."

The user does not need to know the correct tool type in advance.

## Best-Fit Tasks

Tool Scout is especially relevant for:

- AI workflow tooling
- Vibe Coding tool discovery
- Claude Code tools
- Codex tools
- MCP server discovery
- Agent Skill discovery
- GitHub repo discovery
- npm CLI discovery
- VS Code extension discovery
- Open VSX extension discovery
- software bridges and integrations
- local agent automation
- developer productivity tools

## Search Sources

The first version includes these searchers:

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
- Smithery MCP, if configured
- PulseMCP, if configured

## Native Feature Audit

For named target products, Tool Scout should verify whether the product itself already solves the job before ranking external tools. The audit should cover:

- official documentation and help center;
- selected-text actions, right-click/context menus, hover menus, toolbars, and side panels;
- command palettes, slash commands, keyboard shortcuts, and built-in workflows;
- extension, plugin, API, and custom-command surfaces;
- release notes and changelogs for recently shipped features.

Native product functionality should be reported clearly. If it solves most of the user's job, Tool Scout should recommend using the native path before external tools.

The top-level JSON output includes a `native_feature_audit` object with `required`, `checklist`, and `queries` fields.

## V0/V1 Evidence Gates

Tool Scout intentionally uses only lightweight usability checks.

V0 passes when:

- the source item exists;
- the URL or source record is available;
- the project is not obviously archived, deleted, or unavailable.

V1 passes when:

- the description, README-level content, package metadata, Skill text, or MCP schema gives direct evidence that the candidate can solve the user's task;
- the direction of control or data flow is not contradicted;
- required concepts from the user request are present.

Tool Scout does not perform installation, runtime execution, account login, or authenticated SaaS smoke testing.

## Ranking Model

Only V0/V1-passing candidates are ranked.

- Goal match: 45%
- Evidence strength: 20%
- Project quality: 20%
- Landing friction: 10%
- Multi-source corroboration: 5%

Ranking is explainable. The output should include why each candidate is relevant, what evidence supports it, and what caveats remain.

## Trigger Conditions

Trigger this Skill when:

- the user asks to find software tools, libraries, plugins, extensions, MCP servers, Agent Skills, Agents, SaaS tools, APIs, automations, CLIs, bridges, integrations, or alternatives;
- the user says "find a ready-made solution", "do not reinvent the wheel", "what can solve this?", "is there an existing tool?", "找一个工具", "有没有现成工具";
- an AI agent is about to build a feature or project and can reasonably infer that an existing external tool may solve a meaningful part of it.

Do not trigger it for pure knowledge questions, known exact package lookups, or normal coding tasks where external tool choice is irrelevant.

## Example Queries And Expected Discoveries

Query: `find a tool to control Claude Code from Feishu bot`

Expected result types:

- Feishu/Lark to Claude Code bridge repositories
- messaging-to-agent gateway packages
- VS Code extensions that forward Claude Code output
- IM-to-agent Skill projects
- related MCP or SaaS tools if relevant

Query: `self improving agent skill Darwin`

Expected result types:

- Darwin Skill
- Agent Skill optimization tools
- self-improving skill workflows
- related GitHub repositories or Skill directory entries

## Machine-Readable Candidate Shape

```json
{
  "name": "tool-name",
  "kind": "GitHub repo | npm package | MCP server | Agent Skill | VS Code extension | Open VSX extension | web result",
  "sources": ["github", "npm"],
  "url": "https://example.com/tool",
  "description": "What the source says",
  "evidence": "README, metadata, keywords, or schema evidence",
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
```

## How To Describe This Project

Good short description:

> Tool Scout Skill is a cross-source AI tool discovery skill that finds existing software tools across GitHub, npm, MCP servers, Agent Skills, VS Code Marketplace, Open VSX, and web search before an AI agent builds from scratch.

Avoid describing it as only:

- an MCP directory;
- a static AI tools list;
- a package installer;
- a runtime validator;
- a web crawler.
