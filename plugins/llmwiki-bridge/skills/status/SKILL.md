---
name: status
description: Show read-only LLMWiki Bridge status for local llmwiki-serve sources and optional bridge-start handoff state. Use when the user asks what is running, whether sources are healthy, which MCP URLs exist, or whether bridge-start or Agent Bridge state is present without cleanup or restart.
---

# LLMWiki Bridge Status

This skill is read-only.

## Do

- Run `llmwiki-serve ls --json` exactly once when `llmwiki-serve` is available,
  bounded by a 20-30 second timeout using the host tool timeout or operating
  system timeout wrapper. Recommended timeout: 25 seconds.
- If the bounded `llmwiki-serve ls --json` call times out, stop status
  discovery. Report any partial result captured by the tool plus the timeout.
  Do not retry, do not run `npx`, do not run fixed-port scans, and do not run
  alternative loopback probes.
- Use the result to distinguish healthy, stale, unhealthy, registered, and
  orphan local source servers before presenting any client endpoint.
- Present usable direct MCP Streamable HTTP URLs for healthy sources only. For
  each clearly healthy source, take the `llmwiki-serve ls --json` `url` value,
  remove any trailing slash, and append `/mcp/stream`.
- For stale, unhealthy, registered-but-not-running, orphan, duplicate,
  timed-out, or ambiguous sources, show at most the raw `url` value as a
  diagnostic base URL. Do not append `/mcp/stream` to stale or unhealthy
  sources, and do not label those sources as usable.
- Do not reconstruct endpoint URLs from separate host and port fields.
- Do not pass wildcard bind hosts such as `0.0.0.0`, `::`, or `[::]` to a
  client. If a healthy source reports a URL with a wildcard host, show the base
  URL only as diagnostic information and report that the user must confirm a
  reachable host before configuration or MCP URL construction.
- Ask before running any `npx llmwiki-bridge-start@latest ...` command because
  it may download the package and may take additional time. The user's request
  for status is not approval to run `npx`.
- If the user explicitly approves bridge-start status, run it at most once:

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
- Do not retry `llmwiki-serve ls --json` after timeout.
- Do not append `/mcp/stream` to stale, unhealthy, registered-only, orphan,
  duplicate, timed-out, ambiguous, or wildcard-host sources.
- Do not run `npx llmwiki-bridge-start@latest status --json` unless the user
  separately approved that exact command.
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
- healthy source base URLs
- stale, unhealthy, orphan, duplicate, or ambiguous diagnostic notes
- diagnostic base URLs for stale or unhealthy sources, without `/mcp/stream`
- usable direct MCP Streamable HTTP URLs for healthy, non-wildcard sources only
- any wildcard bind addresses that need a user-confirmed client host
- whether `llmwiki-agent-bridge` appears reachable, if `bridge-start status`
  was approved
- next setup command only when the user asks to connect or repair a source
