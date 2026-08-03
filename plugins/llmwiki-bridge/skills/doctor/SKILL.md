---
name: doctor
description: Run a read-only readiness check for LLMWiki Bridge prerequisites, local source discovery, and optional bridge reachability.
---

# LLMWiki Bridge Doctor

Use this skill when the user asks why LLMWiki Bridge setup is not working or
wants a readiness check before setup.

Doctor is read-only by default. Ask before installing packages, starting
processes, probing non-loopback URLs, or writing configuration.
Do not run home-wide discovery from doctor; route the user to setup and ask for
explicit approval before any home scan.
Do not modify, normalize, compile, or upload wiki files while running doctor.

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

For a remote or non-loopback URL, first explain that the check contacts that
network address and may expose the user's IP address to the remote operator.
Proceed only after explicit approval.

## Diagnosis Rules

- Missing `llmwiki-serve`: recommend `uv tool install llmwiki-serve`; do not
  run it without approval.
- No healthy local source: ask for a bounded source path, then use the setup
  skill flow.
- Existing healthy source: do not restart it; report its direct MCP Streamable
  HTTP URL.
- Multiple sources or answer synthesis needed: suggest `llmwiki-agent-bridge`
  as an optional escalation.
- Runtime failures belong to the runtime or Agent Bridge layer, not this
  plugin. Keep direct source setup available when source retrieval is healthy.

## Output

Report:

- pass/fail/unknown for each checked dependency
- healthy local sources discovered through `llmwiki-serve ls --json`
- whether bridge-start doctor was run or skipped
- the smallest next action that respects the user's approval boundary
