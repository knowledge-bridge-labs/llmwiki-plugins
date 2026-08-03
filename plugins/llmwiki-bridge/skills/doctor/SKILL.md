---
name: doctor
description: Run a read-only LLMWiki Bridge readiness and troubleshooting check for prerequisites, local source discovery, and optional bridge reachability. Use when setup fails, sources are not found, MCP connection is unclear, or the user asks to diagnose LLMWiki Bridge before making changes.
---

# LLMWiki Bridge Doctor

Doctor is read-only by default. Ask before installing packages, starting
processes, probing non-loopback URLs, or writing configuration.
Do not run home-wide discovery from doctor; route the user to setup and ask for
explicit approval before any home scan.
Do not modify, normalize, compile, or upload wiki files while running doctor.
Remote or non-loopback endpoints should use HTTPS by default. Plain HTTP should
be limited to private or otherwise trusted networks after explicit approval.

A user's request such as "diagnose http://example.invalid:8765" is not approval to probe a remote or non-loopback network endpoint. Before any network
contact to a URL or redacted host, first tell the user all of this:

- the exact URL or redacted host that would be contacted
- that DNS lookup, TCP connection attempts, and HTTP or HTTPS requests may be
  sent to that host or its DNS providers
- that the user's IP address and later search text or query text may be visible
  to the remote operator if they continue using the endpoint
- that HTTPS is recommended, and plain HTTP should be used only on a private or
  otherwise trusted network

Then ask a yes/no approval question and wait for the next user response. Until
that next response explicitly approves the remote probe, do not run
`Resolve-DnsName`, `nslookup`, `dig`, `Test-NetConnection`, `nc`, `telnet`,
`curl`, `Invoke-WebRequest`, `wget`, `fetch`, `npx llmwiki-bridge-start doctor
--bridge ...`, or any other command/API that can perform DNS, TCP, HTTP, or
HTTPS network contact.

## Checks

Run available local checks:

```bash
llmwiki-serve --help
llmwiki-serve ls --json
node --version
npm --version
```

If the user approves a possible `npx` package download, run:

```bash
npx llmwiki-bridge-start@latest doctor
```

If the user gives an explicit bridge URL, check bridge readiness through the
published onboarding harness after approval:

```bash
npx llmwiki-bridge-start@latest doctor --bridge http://127.0.0.1:8788
```

For a remote or non-loopback URL, follow the remote probe approval gate above
even when the user included the URL in the diagnostic request. Proceed only
after the next user response gives explicit approval.

## Diagnosis Rules

- Missing `llmwiki-serve`: recommend `uv tool install llmwiki-serve`; do not
  run it without approval.
- No healthy local source: ask for a bounded source path, then use the setup
  skill flow.
- Existing healthy source: do not restart it; report its direct MCP Streamable
  HTTP URL by taking the `llmwiki-serve ls --json` `url` value, removing any
  trailing slash, and appending `/mcp/stream`. Do not reconstruct it from
  separate host and port fields.
- Wildcard bind host in a reported URL: do not pass `0.0.0.0`, `::`, or `[::]`
  to a client; ask the user to confirm the reachable client host.
- Multiple sources or answer synthesis needed: suggest `llmwiki-agent-bridge`
  as an optional escalation.
- Runtime failures belong to the runtime or Agent Bridge layer, not this
  plugin. Keep direct source setup available when source retrieval is healthy.
- Remote probe not yet approved: stop before network contact, report the
  disclosure, and ask the yes/no approval question.

## Output

Report:

- pass/fail/unknown for each checked dependency
- healthy local sources discovered through `llmwiki-serve ls --json`
- whether bridge-start doctor was run or skipped
- the smallest next action that respects the user's approval boundary
