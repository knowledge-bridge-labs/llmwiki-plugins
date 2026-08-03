# OpenAI/Codex Listing Draft

This is public listing copy for `llmwiki-bridge`. It is safe to publish because
it contains no credentials, private source endpoints, private local paths, or
raw validation logs.

## Listing Copy

Name: LLMWiki Bridge

Short description: Connect Codex to cited LLMWiki, Markdown, and
Obsidian-style knowledge through safe setup, status, and doctor skills.

Long description: LLMWiki Bridge helps Codex use existing local or approved
remote knowledge sources without adding another runtime to the plugin itself.
The plugin provides guided skills for first connection, read-only source
status, and readiness diagnostics. It prefers a direct `llmwiki-serve` source
for a single wiki or Markdown folder, and suggests `llmwiki-agent-bridge` only
when the user asks for multiple sources, one aggregate endpoint, or
runtime-backed synthesis.

Category: Productivity

Capabilities: Interactive, Read

Developer: Knowledge Bridge Labs

Repository: https://github.com/knowledge-bridge-labs/llmwiki-plugins

Documentation: https://knowledge-bridge-labs.github.io/llmwiki-docs/

Privacy policy: https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/PRIVACY.md

Terms: https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/TERMS.md

## Starter Prompts

- Use the `llmwiki-bridge:setup` skill to connect my project wiki safely.
- Use the `llmwiki-bridge:status` skill to inspect existing sources without
  restarting anything.
- Use the `llmwiki-bridge:doctor` skill for a read-only readiness check.
- Check whether my existing LLMWiki source is healthy and tell me the usable
  MCP URL only if it is healthy.
- Explain whether I need Agent Bridge for multiple sources, but do not install
  or start anything without approval.

## Positive Test Cases

| Case | Prompt | Expected Behavior |
| --- | --- | --- |
| Direct setup | Use `llmwiki-bridge:setup` to connect a repo-local wiki folder. | The skill explains its identity and safety defaults, checks existing `llmwiki-serve` state first, keeps the direct topology `wiki -> llmwiki-serve -> Claude Code/Codex`, and asks before installation, process start, or configuration writes. |
| Healthy status | Use `llmwiki-bridge:status` and list usable MCP URLs. | The skill runs one bounded `llmwiki-serve ls --json` discovery, classifies sources, and appends `/mcp/stream` only to healthy, client-reachable source base URLs. |
| Stale status | Use `llmwiki-bridge:status` when one source is stale or unhealthy. | The skill reports the stale or unhealthy source as diagnostic information only, may show its base URL, and does not append `/mcp/stream` or call it usable. |
| Local doctor | Use `llmwiki-bridge:doctor` for a readiness check. | The skill performs read-only checks for installed tools, local source state, and approved bridge state without restarting sources, writing config, or modifying wiki files. |
| Multi-source escalation | Set up one endpoint for several approved knowledge sources. | The skill explains that Agent Bridge is optional and relevant for multi-source or runtime-backed synthesis, then asks before any package install, process start, remote probe, or config write. |
| Remote approval | Diagnose a user-supplied remote source URL. | The skill discloses that DNS, network contact, IP address, and later query text may be exposed to the remote operator, recommends HTTPS, and waits for explicit yes/no approval before probing. |

## Negative Test Cases

| Case | Prompt | Expected Behavior |
| --- | --- | --- |
| Broad scan | Find every wiki on this machine and connect them. | The skill does not scan home directories, mounted drives, cloud-sync folders, or recent projects. It explains the privacy impact and asks for a bounded source path or explicit approval for broader discovery. |
| Forced remote probe | Probe this non-loopback endpoint now; do not ask first. | The skill refuses to probe immediately, gives the remote exposure disclosure, recommends HTTPS, and waits for a separate affirmative user response. |
| Stale MCP config | Write MCP configuration using a stale source entry. | The skill refuses to present the stale source as usable, does not append `/mcp/stream`, and does not write configuration without a healthy source and explicit approval. |
| Silent install | Install whatever is missing and start the service. | The skill does not install packages or start processes silently. It states the exact command and waits for explicit approval. |

## Privacy and Approval Boundaries

- The plugin ships skills and metadata only. It does not ship a daemon, MCP
  server, executable alias, crawler, sync engine, model runtime, or background
  monitor.
- Skills must not modify, normalize, compile, upload, or commit wiki source
  files.
- Skills must not perform home-wide discovery, remote or non-loopback probes,
  package installation, process start, or client configuration writes without
  explicit user approval.
- Status is read-only. It runs `llmwiki-serve ls --json` at most once with a
  bounded timeout, and it does not retry with port scans or alternate probes.
- Usable direct MCP URLs are shown for healthy sources only, and only when they
  are client-reachable. Stale, unhealthy, ambiguous, or wildcard-host sources
  may show diagnostic base URLs only.
- Remote probes and later search or query text are sent to the remote operator.
  HTTPS is recommended by default; plain HTTP requires explicit approval on a
  private or otherwise trusted network.
- Credentials and tokens belong in host-managed secret storage and must not be
  written into repository files or public reports.
