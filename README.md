# LLMWiki Bridge Plugins

[![CI](https://github.com/knowledge-bridge-labs/llmwiki-plugins/actions/workflows/ci.yml/badge.svg)](https://github.com/knowledge-bridge-labs/llmwiki-plugins/actions/workflows/ci.yml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](./LICENSE)

`llmwiki-bridge` is a skills-first plugin for Claude Code and Codex. It helps
coding agents connect to existing LLMWiki, Markdown, or Obsidian-style
knowledge through the published LLMWiki tools without becoming another runtime
service.

Version 0.1.1 is a Codex/OpenAI submission-readiness patch for manifest
metadata, listing fixtures, and validation records only, with runtime behavior unchanged
from 0.1.0.

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

When a healthy running source is discovered, use the base `url` from
`llmwiki-serve ls --json`, remove any trailing slash, and append `/mcp/stream`
for the usable direct MCP Streamable HTTP endpoint. Do not rebuild the URL from
separate host and port fields. Stale, unhealthy, orphaned, duplicate, timed-out,
or ambiguous sources may be shown with their diagnostic base URL only; do not
append `/mcp/stream` or present them as usable MCP endpoints. If a source reports
a wildcard bind host such as `0.0.0.0`, `::`, or `[::]`, confirm a reachable
client host with the user before constructing an MCP URL or writing any client
configuration.

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

SQLite GraphStore is configured on the `llmwiki-serve` process, not in this
plugin. In `llmwiki-serve` 0.2.10 and newer, the base serve package includes
the built-in SQLite GraphStore, it remains off by default, and no `[sqlite]`,
`[graph]`, bridge, or chat extra is required.

Do not run commands that install packages, start processes, or write client
configuration until the user has explicitly approved that step.

## Claude Code Marketplace

This repository is a Claude Code marketplace because it contains
`.claude-plugin/marketplace.json` at the repository root.

Run slash commands inside an active Claude Code session. For local testing from
this repository:

```text
/plugin marketplace add .
/plugin install llmwiki-bridge@knowledge-bridge-labs
/reload-plugins
/llmwiki-bridge:setup
```

For public GitHub distribution from inside an active Claude Code session:

```text
/plugin marketplace add knowledge-bridge-labs/llmwiki-plugins
/plugin install llmwiki-bridge@knowledge-bridge-labs
/reload-plugins
/llmwiki-bridge:setup
```

Use `/reload-plugins` only to activate the plugin in an already-running Claude
Code session. If you install from the shell before starting Claude Code, start a
new Claude Code session instead; no reload is needed.
In the slash flow, `/plugin install ...` opens plugin details where you confirm
the installation scope: user, project, or local.

Shell alternative for user-scope installation:

```bash
claude plugin marketplace add knowledge-bridge-labs/llmwiki-plugins --scope user
claude plugin install llmwiki-bridge@knowledge-bridge-labs --scope user
```

To update from inside an active Claude Code session:

```text
/plugin marketplace update knowledge-bridge-labs
/plugin update llmwiki-bridge@knowledge-bridge-labs
/reload-plugins
```

Shell update alternative:

```bash
claude plugin marketplace update knowledge-bridge-labs
claude plugin update llmwiki-bridge@knowledge-bridge-labs --scope user
```

Start a new Claude Code session after shell updates, or run `/reload-plugins`
in an already-running session. Claude Code plugin skills are namespaced by
plugin ID. Do not document or create a bare `/setup` or `/lb` command for this
plugin.

Reference: Claude Code plugin discovery, marketplace, and command details are
documented in the [plugin discovery guide](https://code.claude.com/docs/en/discover-plugins),
[marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces), and
[plugins reference](https://code.claude.com/docs/en/plugins-reference).

## Codex Marketplace

This repository is also a Codex plugin marketplace because it contains
`.agents/plugins/marketplace.json` at the repository root. The Codex marketplace
entry points at the same plugin folder as Claude Code.

The CLI must expose `codex plugin`; this exact flow has been verified with Codex
CLI 0.146.0.

Local test:

```bash
codex plugin marketplace add .
codex plugin add llmwiki-bridge@knowledge-bridge-labs
```

Public GitHub distribution:

```bash
codex plugin marketplace add knowledge-bridge-labs/llmwiki-plugins --ref main
codex plugin add llmwiki-bridge@knowledge-bridge-labs
```

After installation, start a new Codex thread so newly installed skills are
loaded in context.

Codex updates are a marketplace refresh only:

```bash
codex plugin marketplace upgrade knowledge-bridge-labs
```

Then start a new Codex CLI session or chat so the refreshed snapshot is loaded.

After registering the marketplace, the interactive plugin browser is also
available:

```text
codex
/plugins
```

Reference: OpenAI documents Codex marketplace installation in the
[plugin packaging guide](https://developers.openai.com/plugins/build/plugins#add-a-marketplace-from-the-cli),
[Codex plugin marketplace command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli#codex-plugin-marketplace),
[Codex plugin command reference](https://learn.chatgpt.com/docs/developer-commands?surface=cli#codex-plugin),
and [Codex plugin directory guide](https://learn.chatgpt.com/docs/plugins#plugin-directory-in-codex-cli).

Codex can use the plugin through normal natural language:

```text
Set up LLMWiki Bridge for this repo.
Check my LLMWiki source status.
Run an LLMWiki Bridge doctor check.
```

For explicit skill invocation, name the installed plugin skill:

```text
Use the llmwiki-bridge:setup skill to connect ./wiki.
Use the llmwiki-bridge:status skill and do not start any processes.
Use the llmwiki-bridge:doctor skill for a read-only readiness check.
```

## Safety Defaults

- No wiki files are modified, compiled, normalized, or uploaded.
- No home-wide discovery is run unless the user explicitly approves it.
- Existing `llmwiki-serve` servers are discovered with `llmwiki-serve ls --json`;
  they are not restarted automatically.
- Direct local serving binds to `127.0.0.1` by default.
- Non-loopback or remote URLs require explicit user approval before probing or
  configuration.
- Remote probes and later search or query text are sent to the remote operator.
  Use HTTPS by default. Use plain HTTP only on a private or otherwise trusted
  network after explicit approval.
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
| `plugins/llmwiki-bridge/skills/*/agents/openai.yaml` | Codex skill-list metadata generated with the official skill-creator helper. |
| `scripts/build_codex_submission.py` | Deterministic skills-only Codex submission ZIP builder. |
| `docs/submission/` | Public OpenAI/Codex and Claude marketplace listing drafts. |
| `docs/validation/` | Redacted cross-platform validation records. |
| `PRIVACY.md` | Privacy policy URL used by Codex listing metadata. |
| `TERMS.md` | Terms of service URL used by Codex listing metadata. |
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

The optional validator script also runs the official `skill-creator`
`quick_validate.py` gate for `setup`, `status`, and `doctor` when that system
skill is installed. It skips unavailable tools. It does not install Claude Code,
Codex, Node, Python packages, or any LLMWiki runtime.

Release host gates run separately on tags and manual dispatch. They install the
current Claude Code and Codex CLIs, require Claude root and plugin validation,
smoke-test Codex local marketplace add/install/list in an isolated `CODEX_HOME`,
build the public skills-only Codex submission ZIP, and upload that ZIP only as a
CI artifact.

Build the public skills-only Codex submission archive locally:

```bash
py -3 scripts/build_codex_submission.py
```

The ZIP is written under ignored `dist/` and contains only
`.codex-plugin/plugin.json` and `skills/**` from `plugins/llmwiki-bridge`.
