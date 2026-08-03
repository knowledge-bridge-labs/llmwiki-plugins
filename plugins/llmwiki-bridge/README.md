# LLMWiki Bridge Plugin

This folder is the installable `llmwiki-bridge` plugin shared by Claude Code
and Codex.

It contains only skills:

- `setup`
- `status`
- `doctor`

It intentionally does not contain an `lb` executable, MCP server, hook,
monitor, background process, or model runtime.

When a skill reports a usable direct MCP endpoint, it should do so for healthy
sources only. It should use the base `url` from `llmwiki-serve ls --json` and
append `/mcp/stream`, without rebuilding the client URL from separate host and
port fields. Stale, unhealthy, orphaned, duplicate, timed-out, ambiguous, or
wildcard-host sources may show a diagnostic base URL only and must not receive
`/mcp/stream` until they are healthy and client-reachable.
