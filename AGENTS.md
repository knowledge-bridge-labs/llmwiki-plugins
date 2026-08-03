# Agent Instructions

This repository distributes Claude Code and Codex plugin metadata for
`llmwiki-bridge`.

## Scope

- Edit only this repository when working on plugin packaging.
- Runtime behavior remains in `llmwiki-serve`, `llmwiki-bridge-start`,
  `llmwiki-agent-bridge`, and `llmwiki-chat`.
- Do not add package installers, executable aliases, background processes, MCP
  servers, or model runtime code to this repository unless a new spec and ADR
  explicitly change that boundary.

## Required Context Before Changes

Read these files before non-trivial edits:

- `README.md`
- `SECURITY.md`
- `specs/plugin-onboarding/spec.md`
- `specs/plugin-onboarding/plan.md`
- `docs/decisions/0001-skills-first-host-plugin-boundary.md`
- relevant plugin manifests and skill files

For changes that touch existing LLMWiki command contracts, inspect the released
package documentation or sibling checkouts first. Do not invent commands or
options.

## Validation

Run:

```bash
py -3 scripts/validate_repo.py
py -3 scripts/run_optional_validators.py
```

If `claude` is installed, run:

```bash
claude plugin validate ./plugins/llmwiki-bridge
```

If the Codex plugin-creator validator exists, run it against
`./plugins/llmwiki-bridge`.

## Data Safety

Never commit:

- credentials, bearer tokens, API keys, or cookies
- private endpoint URLs
- local absolute paths
- raw screenshots or logs with local paths
- wiki source content copied from a private vault
