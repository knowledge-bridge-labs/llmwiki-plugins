# Plugin Onboarding Tests

## Static Acceptance

- `py -3 scripts/validate_repo.py` passes.
- Required repository files are present.
- Root Claude marketplace JSON parses and points to `./plugins/llmwiki-bridge`.
- Root Codex marketplace JSON parses and points to `./plugins/llmwiki-bridge`.
- Claude plugin manifest parses and uses `name: llmwiki-bridge`.
- Codex plugin manifest parses and uses `name: llmwiki-bridge`.
- Exactly three skill directories exist: `setup`, `status`, and `doctor`.
- No file creates an `lb` alias or executable.
- Skill text includes approval gates for install, process start, and config
  writes.
- Skill text requires bounded discovery and no home-wide scan without approval.
- Skill text forbids wiki modification and upload.
- No committed file contains private local path patterns or obvious secret
  placeholders.

## Host Validator Acceptance

Run locally when the host CLIs are installed:

```bash
claude plugin validate ./plugins/llmwiki-bridge
```

```bash
py -3 "$HOME/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py" ./plugins/llmwiki-bridge
```

The repository also provides:

```bash
py -3 scripts/run_optional_validators.py
```

This optional runner skips missing host tools and reports which validators were
actually executed.

## Manual Smoke Acceptance

Claude Code local marketplace smoke:

```text
/plugin marketplace add ./llmwiki-plugins
/plugin install llmwiki-bridge@knowledge-bridge-labs
/reload-plugins
/llmwiki-bridge:setup
```

Codex local marketplace smoke:

```bash
codex plugin marketplace add ./llmwiki-plugins
codex plugin add llmwiki-bridge@knowledge-bridge-labs
```

After installing in Codex, start a new thread before testing skill invocation.

## Runtime Behavior Acceptance

The skills should lead the agent to:

- run `llmwiki-serve ls --json` before starting new source servers
- reuse existing healthy source servers
- ask before `uv tool install llmwiki-serve`
- ask before `npx llmwiki-bridge-start@latest ...` when it may download the
  npm package
- ask before `llmwiki-serve serve ...`
- ask before writing any MCP or bridge configuration
- prefer direct `http://127.0.0.1:<port>/mcp/stream` URLs for one source
- suggest Agent Bridge only for multi-source or runtime-backed synthesis
