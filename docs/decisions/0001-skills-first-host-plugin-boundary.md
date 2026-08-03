# 0001 Skills-First Host Plugin Boundary

## Status

Accepted

## Context

Knowledge Bridge Labs already publishes separate packages for the runtime
stack:

- `llmwiki-serve` serves a single existing knowledge source as read-only cited
  context.
- `llmwiki-bridge-start` guides first-run source discovery, source startup,
  optional Agent Bridge registration, and smoke checks.
- `llmwiki-agent-bridge` provides optional multi-source and runtime-backed
  synthesis.
- `llmwiki-chat` provides an optional browser workbench.

Claude Code and Codex users need plugin-driven onboarding, but a plugin that
ships its own executable, daemon, MCP server, or runtime wrapper would blur the
existing package boundaries and create additional security review surface.

## Decision

The public plugin ID is `llmwiki-bridge` and the display name is
`LLMWiki Bridge`.

The MVP plugin is skills-first:

- It ships exactly three shared skills: `setup`, `status`, and `doctor`.
- It ships Claude Code and Codex manifests for the same plugin folder.
- It does not ship an `lb` alias, executable, MCP server, hook, monitor,
  background process, wiki compiler, crawler, or model runtime.
- It reuses `llmwiki-bridge-start` as the onboarding core.
- It keeps `llmwiki-serve` direct source setup as the default for one source.
- It suggests `llmwiki-agent-bridge` only for multi-source or runtime-backed
  synthesis.

Every skill must keep explicit approval gates before package installation,
process start, or configuration writes.

## Consequences

- The plugin can be reviewed as host instructions and metadata rather than a
  new runtime component.
- Runtime fixes remain in the existing runtime repositories.
- Users get namespaced host commands such as `/llmwiki-bridge:setup`, not a new
  global `lb` command.
- The plugin remains robust when host MCP registration commands differ because
  it can return verified endpoint URLs instead of inventing host-specific
  commands.

## Follow-Ups

- Push the marketplace repository to GitHub.
- Run Claude Code and Codex local marketplace install smokes.
- Submit the Claude community marketplace form after public repository
  validation passes.
- Decide later whether additional skills such as `connect-remote` or
  `add-source` are needed; each new skill requires a spec update.

## Links

- Spec: `specs/plugin-onboarding/spec.md`
- Tests: `specs/plugin-onboarding/tests.md`
- Claude Code plugin docs: `https://code.claude.com/docs/en/plugins`
- Claude Code marketplace docs: `https://code.claude.com/docs/en/plugin-marketplaces`

