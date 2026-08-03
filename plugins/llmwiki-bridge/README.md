# LLMWiki Bridge Plugin

This folder is the installable `llmwiki-bridge` plugin shared by Claude Code
and Codex.

It contains only skills:

- `setup`
- `status`
- `doctor`

It intentionally does not contain an `lb` executable, MCP server, hook,
monitor, background process, or model runtime.

When a skill reports a direct MCP endpoint, it should use the base `url` from
`llmwiki-serve ls --json` and append `/mcp/stream`. It should not rebuild the
client URL from separate host and port fields. Wildcard bind hosts such as
`0.0.0.0`, `::`, or `[::]` need a user-confirmed reachable host before any
client configuration is written.
