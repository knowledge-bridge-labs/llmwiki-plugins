# Contributing

Thanks for improving the LLMWiki Bridge plugin.

This repository packages host plugins only. Runtime behavior belongs in the
published LLMWiki packages:

- `llmwiki-serve`: read-only source server.
- `llmwiki-bridge-start`: onboarding harness.
- `llmwiki-agent-bridge`: optional multi-source or runtime-backed bridge.
- `llmwiki-chat`: optional browser workbench.

## Development Rules

- Keep the public plugin ID `llmwiki-bridge` stable.
- Do not add a bare `lb` alias, executable, shell script, or command.
- Keep the MVP skills to `setup`, `status`, and `doctor` unless a spec and ADR
  explicitly expand the surface.
- Do not document commands that are not present in the released packages.
- Do not add credentials, private URLs, local absolute paths, raw logs, or
  wiki content to examples, tests, or docs.
- Ask for explicit approval before any skill instructs an agent to install
  packages, start processes, or write client configuration.

## Checks

Run:

```bash
py -3 scripts/validate_repo.py
py -3 scripts/run_optional_validators.py
```

When changing host-specific metadata, test with the relevant host CLI:

```text
claude plugin validate ./plugins/llmwiki-bridge
```

```bash
py -3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" ./plugins/llmwiki-bridge
```
