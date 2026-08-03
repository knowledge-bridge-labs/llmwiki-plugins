# Plugin Onboarding Spec

## Problem

Claude Code and Codex users need a low-friction way to connect existing
LLMWiki, Markdown, or Obsidian-style knowledge to their coding-agent sessions
without learning the full LLMWiki stack on the first run.

The plugin must make the safe direct `llmwiki-serve` path obvious and avoid
confusing the plugin with `llmwiki-agent-bridge`, which is an optional runtime
and multi-source escalation layer.

## Goals

- Publish one public plugin ID: `llmwiki-bridge`.
- Use display name `LLMWiki Bridge`.
- Support both Claude Code and Codex from one repository.
- Ship only shared skills for MVP: `setup`, `status`, and `doctor`.
- Reuse `llmwiki-bridge-start` as the onboarding core.
- Prefer direct `llmwiki-serve` connection for a single source.
- Suggest `llmwiki-agent-bridge` only for multi-source or runtime-backed
  synthesis.
- Require explicit user approval before package install, process start, or
  configuration writes.
- Preserve read-only wiki defaults and local-first network posture.
- Keep Claude Code metadata compatible with older Claude Code validators while
  preserving richer Codex listing metadata.

## Non-Goals

- No `lb` executable, alias, or bare command namespace.
- No MCP server, hook, monitor, daemon, language server, or app component in
  the MVP.
- No wiki compilation, ingestion, crawling, authoring, synchronization, or
  upload.
- No model runtime management.
- No claim that `llmwiki-agent-bridge` is required for single-source use.
- No committed private endpoints, local paths, tokens, logs, or wiki content.

## Requirements

1. Repository root must contain Claude Code marketplace metadata at
   `.claude-plugin/marketplace.json`.
2. Repository root must contain Codex marketplace metadata at
   `.agents/plugins/marketplace.json`.
3. `plugins/llmwiki-bridge` must contain both `.claude-plugin/plugin.json` and
   `.codex-plugin/plugin.json`.
4. `plugins/llmwiki-bridge/skills` must contain exactly `setup`, `status`, and
   `doctor`.
5. Setup must start with a concise identity and safety explanation.
6. Setup/status/doctor must not instruct agents to restart existing
   `llmwiki-serve` servers automatically.
7. Setup/status/doctor must not instruct agents to scan home directories unless
   the user explicitly approves after a privacy notice.
8. Setup/status/doctor must not instruct agents to modify or upload wiki files.
9. Status and doctor must use `llmwiki-serve ls --json` for local discovery,
   not guessed fixed ports.
10. Any use of `llmwiki-bridge-start` must reference real commands observed in
    its released CLI help.
11. Public listing copy and repository docs must clearly distinguish the plugin
    from Agent Bridge runtime synthesis, even when a host manifest omits
    optional description fields for compatibility.
12. Direct MCP Streamable HTTP endpoints must be derived from each
    `llmwiki-serve ls --json` base `url` by appending `/mcp/stream`; skills must
    not reconstruct client URLs from separate host and port fields.
13. Wildcard bind hosts such as `0.0.0.0`, `::`, and `[::]` must not be passed
    to clients. The user must confirm a reachable client host first.
14. Remote or non-loopback endpoints require disclosure that probes and later
    search or query text are sent to the remote operator. HTTPS is recommended
    by default; plain HTTP requires explicit approval on a private or trusted
    network.
15. The Codex manifest must point to public GitHub Privacy and Terms documents.
16. Release host gates must run current Claude Code root/plugin validation and
    a current Codex isolated marketplace add/install/list smoke before public
    registration.

## Compatibility

- Claude Code skills are invoked through namespaced commands such as
  `/llmwiki-bridge:setup`.
- Codex loads the same skill folders through `.codex-plugin/plugin.json`.
- Codex keeps `interface.displayName: LLMWiki Bridge`; Claude Code's plugin
  manifest omits optional display and fixed version fields for older validator
  compatibility and git-SHA marketplace updates.
- The plugin is skills-first and should remain usable even when host-specific
  MCP configuration commands differ or change.
- When host MCP configuration syntax is unclear, the skills return verified
  endpoint URLs instead of inventing commands.

## Safety Review

The MVP has no executable plugin code. Its risk is instruction quality: an
agent following the skill might install packages, start servers, probe networks,
or write config too eagerly. The spec therefore treats approval gates as a
hard requirement and validates that the published skill text includes them.
