---
name: setup
description: Set up a safe first connection from Claude Code or Codex to existing LLMWiki, Markdown, or Obsidian knowledge through llmwiki-serve.
---

# LLMWiki Bridge Setup

Use this skill when the user wants to connect Claude Code or Codex to an
existing LLMWiki, Markdown, or Obsidian-style knowledge source.

Start every setup by giving this short explanation in your own words:

- LLMWiki Bridge connects the current coding agent to existing knowledge through
  `llmwiki-serve`.
- Use it when the user wants cited project, note, ADR, runbook, or wiki context
  available across coding-agent sessions.
- Do not use it as a wiki authoring tool, crawler, sync engine, hosted RAG
  service, auth gateway, model runtime, or replacement for `llmwiki-agent-bridge`.
- It will not modify, normalize, compile, or upload wiki files.
- It will not scan the user's home directory, install packages, start
  processes, probe non-loopback URLs, or write client configuration without
  explicit approval.
- Local source servers bind to `127.0.0.1` by default. `llmwiki-serve` may write
  local I/O debug logs unless the user chooses `--io-log off`.
- Remote or non-loopback endpoints should use HTTPS by default. Plain HTTP is
  appropriate only on a private or otherwise trusted network after explicit
  approval.

## Required Flow

1. Read-only preflight first.
2. Ask for explicit approval before installing or downloading packages.
3. Ask for explicit approval before starting or restarting any process.
4. Ask for explicit approval before writing Claude Code, Codex, MCP, bridge, or
   project configuration.
5. Prefer direct `llmwiki-serve` source connections for one source.
6. Suggest `llmwiki-agent-bridge` only when the user wants multiple sources or
   runtime-backed answer synthesis.

## Read-Only Preflight

Run only commands that do not install packages, start processes, or write
configuration. Good preflight commands include:

```bash
llmwiki-serve --help
llmwiki-serve ls --json
node --version
npm --version
```

If `llmwiki-serve` is missing, recommend this install command and ask before
running it:

```bash
uv tool install llmwiki-serve
```

If the setup needs `llmwiki-bridge-start` and it is not already available
locally, tell the user that `npx llmwiki-bridge-start@latest` may download and
cache the npm package, then ask before running it.

Do not run the bare `npx llmwiki-bridge-start@latest` command as a preflight:
the default guided flow can propose a broader scan and can start processes
after user selections.

## Choose The Source Path

Ask the user to choose one of these bounded setup paths:

- Known local wiki folder: `npx llmwiki-bridge-start@latest --path ./wiki`
- Current repository only: `npx llmwiki-bridge-start@latest --cwd`
- Workspace-level discovery: `npx llmwiki-bridge-start@latest --workspace`
- Existing running source: inspect `llmwiki-serve ls --json` and use the
  reported URL without restarting it.
- Remote source: require an explicit URL from the user and explicit approval
  before probing or saving it. Explain that probes and later search text or
  query text are sent to that remote operator.

Do not run home-wide discovery unless the user explicitly asks for it after the
privacy notice.

## Direct Source Setup

For one local source, prefer direct `llmwiki-serve` registration. If the source
is already running, use the URL reported by:

```bash
llmwiki-serve ls --json
```

Build the direct MCP Streamable HTTP endpoint from the `url` field reported by
`llmwiki-serve ls --json`:

- Parse the reported base URL instead of reconstructing host and port from
  separate fields.
- Remove any trailing slash from the base URL and append `/mcp/stream`.
- Do not pass wildcard bind hosts such as `0.0.0.0`, `::`, or `[::]` to a
  client. If a reported URL uses a wildcard host, ask the user to confirm the
  reachable host: usually `127.0.0.1` or `localhost` for same-machine use, or
  an approved LAN hostname, LAN IP, or HTTPS URL for remote use.

Before writing host configuration, inspect the host's current documented MCP
configuration command or UI. Do not invent a Claude Code or Codex MCP command.
If the host command is unclear, return the endpoint URL and the health-check
result to the user instead of writing configuration.

If starting a source is needed, ask before running:

```bash
npx llmwiki-bridge-start@latest --path ./wiki
```

or, when the user wants direct manual control:

```bash
llmwiki-serve serve ./wiki --host 127.0.0.1 --port 8765
```

Use `--io-log off` only when the user asks to disable local debug logging or the
workspace policy requires it.

## Optional Agent Bridge Escalation

Suggest Agent Bridge only when at least one of these is true:

- The user wants one endpoint across multiple `llmwiki-serve` sources.
- The user wants runtime-backed answer synthesis from source evidence.
- The target coding agent cannot manage multiple source endpoints directly.

After approval, use the existing onboarding harness rather than hand-building
bridge state:

```bash
npx llmwiki-bridge-start@latest --path ./wiki --setup-bridge
npx llmwiki-bridge-start@latest register --bridge http://127.0.0.1:8788 --config .llmwiki-bridge-start/sources.json
npx llmwiki-bridge-start@latest smoke --bridge http://127.0.0.1:8788 --mode evidence-only
```

Use `--replace` only if the user explicitly asks to replace the bridge
registry.

## Completion Criteria

The setup is complete when you can report:

- the selected source folder or approved remote URL
- whether an existing source was reused or a new source was started
- the source health result
- the direct MCP Streamable HTTP URL, or the approved bridge URL when bridge
  escalation was selected
- for remote or non-loopback URLs, whether HTTPS is used or plain HTTP was
  explicitly approved for a trusted network
- a first cited context result, smoke result, or the specific blocking check
