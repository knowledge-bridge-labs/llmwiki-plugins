---
name: status
description: Show read-only LLMWiki Bridge status for local llmwiki-serve sources and optional bridge-start handoff state. Use when the user asks what is running, whether sources are healthy, which MCP URLs exist, or whether bridge-start or Agent Bridge state is present without cleanup or restart.
---

# LLMWiki Bridge Status

This skill is read-only.

## Do

- Run `llmwiki-serve ls --json` when `llmwiki-serve` is available.
- Use the result to distinguish healthy, stale, registered, and orphan local
  source servers.
- Report direct source MCP Streamable HTTP endpoints by taking each
  `llmwiki-serve ls --json` `url` value, removing any trailing slash, and
  appending `/mcp/stream`.
- Do not reconstruct endpoint URLs from separate host and port fields.
- Do not pass wildcard bind hosts such as `0.0.0.0`, `::`, or `[::]` to a
  client. If a reported URL uses a wildcard host, report that the user must
  confirm a reachable host before configuration.
- Ask before running any `npx llmwiki-bridge-start@latest ...` command if that
  command may download the package.
- If approved and useful, run:

```bash
npx llmwiki-bridge-start@latest status --json
```

## Do Not

- Do not restart existing `llmwiki-serve` servers.
- Do not kill duplicate or stale processes unless the user explicitly asks for
  cleanup.
- Do not install packages from status. If a missing dependency must be
  installed, switch to setup and ask for explicit approval first.
- Do not run fixed-port scans or heuristic loopback scans.
- Do not use `llmwiki-serve ls --probe-port` unless the user gives a specific
  port to diagnose.
- Do not run home-wide discovery from status; route the user to setup and ask
  for explicit approval before any home scan.
- Do not write Claude Code, Codex, MCP, bridge, or project configuration.
- Do not modify, normalize, compile, or upload wiki files while checking
  status.
- Do not print private local roots in shared reports; redact them when writing
  docs, issues, or public output.

## Suggested Output

Summarize:

- source count
- healthy source URLs
- stale or duplicate notes
- direct MCP Streamable HTTP URLs
- any wildcard bind addresses that need a user-confirmed client host
- whether `llmwiki-agent-bridge` appears reachable, if `bridge-start status`
  was approved
- next setup command only when the user asks to connect or repair a source
