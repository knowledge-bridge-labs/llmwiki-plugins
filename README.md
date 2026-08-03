# LLMWiki Bridge Plugins

[![CI](https://github.com/knowledge-bridge-labs/llmwiki-plugins/actions/workflows/ci.yml/badge.svg)](https://github.com/knowledge-bridge-labs/llmwiki-plugins/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)

`llmwiki-bridge` is a skills-first plugin for Claude Code and Codex. It helps
coding agents connect to existing LLMWiki, Markdown, or Obsidian-style
knowledge through the published LLMWiki tools without becoming another runtime
service.

The plugin does not ship an `lb` alias, executable, MCP server, background
process, wiki compiler, crawler, or model runtime. It packages three
namespaced skills:

| Skill | Claude Code invocation | Purpose |
| --- | --- | --- |
| setup | `/llmwiki-bridge:setup` | Guided first connection to one local or remote knowledge source, with optional escalation to Agent Bridge only when needed. |
| status | `/llmwiki-bridge:status` | Read-only inventory of local `llmwiki-serve` sources and bridge-start handoff state. |
| doctor | `/llmwiki-bridge:doctor` | Read-only readiness checks for installed tools, running source servers, and optional bridge reachability. |

## What This Plugin Connects

Start with a direct `llmwiki-serve` source when you have one wiki, Markdown
folder, or Obsidian-style vault and your coding agent can use that source
itself. The source server exposes cited context, search, read, graph, and MCP
Streamable HTTP endpoints.

Add `llmwiki-agent-bridge` only when you want one endpoint across multiple
sources or model-backed answer synthesis. The marketplace wording and skills
avoid treating Agent Bridge as the default runtime.

The plugin reuses the existing onboarding package:

```bash
npx llmwiki-bridge-start@latest --path ./wiki
npx llmwiki-bridge-start@latest status --json
npx llmwiki-bridge-start@latest doctor
```

It also relies on the published source CLI:

```bash
uv tool install llmwiki-serve
llmwiki-serve serve ./wiki --host 127.0.0.1 --port 8765
llmwiki-serve ls --json
```

Do not run commands that install packages, start processes, or write client
configuration until the user has explicitly approved that step.

## Claude Code Marketplace

This repository is a Claude Code marketplace because it contains
`.claude-plugin/marketplace.json` at the repository root.

Local test:

```text
/plugin marketplace add ./llmwiki-plugins
/plugin install llmwiki-bridge@knowledge-bridge-labs
/reload-plugins
/llmwiki-bridge:setup
```

GitHub distribution after the repository is pushed:

```text
/plugin marketplace add knowledge-bridge-labs/llmwiki-plugins
/plugin install llmwiki-bridge@knowledge-bridge-labs
/reload-plugins
```

Claude Code plugin skills are namespaced by plugin ID. Do not document or
create a bare `/setup` or `/lb` command for this plugin.

## Codex Marketplace

This repository is also a Codex plugin marketplace because it contains
`.agents/plugins/marketplace.json` at the repository root. The Codex marketplace
entry points at the same plugin folder as Claude Code.

Local test:

```bash
codex plugin marketplace add ./llmwiki-plugins
codex plugin add llmwiki-bridge@knowledge-bridge-labs
```

GitHub distribution after the repository is pushed:

```bash
codex plugin marketplace add knowledge-bridge-labs/llmwiki-plugins --ref main
codex plugin add llmwiki-bridge@knowledge-bridge-labs
```

After installation, start a new Codex thread so newly installed skills are
loaded in context.

## Safety Defaults

- No wiki files are modified, compiled, normalized, or uploaded.
- No home-wide discovery is run unless the user explicitly approves it.
- Existing `llmwiki-serve` servers are discovered with `llmwiki-serve ls --json`;
  they are not restarted automatically.
- Direct local serving binds to `127.0.0.1` by default.
- Non-loopback or remote URLs require explicit user approval before probing or
  configuration.
- Tokens, private endpoints, local paths, logs, and credentials must not be
  committed to this repository.
- The plugin asks before package installation, process start, and client
  configuration writes.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `.claude-plugin/marketplace.json` | Claude Code marketplace catalog. |
| `.agents/plugins/marketplace.json` | Codex marketplace catalog. |
| `plugins/llmwiki-bridge/.claude-plugin/plugin.json` | Claude Code plugin manifest. |
| `plugins/llmwiki-bridge/.codex-plugin/plugin.json` | Codex plugin manifest. |
| `plugins/llmwiki-bridge/skills/` | Shared skills loaded by both hosts. |
| `scripts/validate_repo.py` | JSON, frontmatter, structure, and safety validation. |
| `scripts/run_optional_validators.py` | Local optional official validator runner. |
| `specs/plugin-onboarding/` | MVP requirements, plan, tasks, and test contract. |
| `docs/decisions/` | Architecture decision records. |

## Validation

Run the repository validator:

```bash
py -3 scripts/validate_repo.py
```

Run optional host validators when the corresponding CLIs are available:

```bash
py -3 scripts/run_optional_validators.py
```

The optional validator script skips unavailable tools. It does not install
Claude Code, Codex, Node, Python packages, or any LLMWiki runtime.
