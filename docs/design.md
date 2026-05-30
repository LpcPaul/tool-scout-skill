# Design Notes

Tool Scout is intentionally small enough to ship as an Agent Skill.

## Product Boundary

It solves:

- "Find existing software tools that can solve this job."
- "Do not force the user to know whether the answer is a Skill, MCP, Agent, repo, package, plugin, or SaaS."
- "Avoid default search misses caused by weak query wording."

It does not solve:

- authenticated product testing
- package installation
- runtime security scanning
- benchmark execution
- full SaaS procurement

## Architecture

```text
user need
  -> query planning
  -> parallel searchers
  -> normalized candidates
  -> dedupe
  -> V0/V1 gates
  -> explainable ranking
  -> report
```

## Why Skill First

A Skill is the right first delivery format because the core value is a repeatable search workflow, not a standalone UI. The workflow can be used by the AI whenever it detects a tool-selection problem.

If the Skill proves useful on repeated failure cases, it can later become:

- a CLI package
- a hosted search service
- a GitHub app
- a browser extension
- a shared MCP server

