# Plugin Onboarding Plan

## Implementation

1. Initialize a new marketplace repository.
2. Scaffold the Codex plugin with the official `plugin-creator` helper.
3. Add Claude Code marketplace and plugin manifests following the official
   `.claude-plugin` structure.
4. Replace scaffold placeholder metadata with public `llmwiki-bridge` metadata.
5. Write shared skill instructions for `setup`, `status`, and `doctor`.
6. Add repository docs, security policy, changelog, license, and contributing
   guide.
7. Add a validation script that checks JSON, skill frontmatter, required files,
   approval-language requirements, and data-safety patterns.
8. Add CI that runs the repository validation script on Windows and Ubuntu.
9. Run optional official host validators where available locally.
10. Add a tag/manual release host gate that installs current Claude Code and
    Codex CLIs, validates Claude root/plugin manifests, and smoke-tests Codex
    marketplace add/install/list in an isolated home.
11. Generate `agents/openai.yaml` for each skill with the official
    `skill-creator` helper and gate them through quick validation.
12. Commit the MVP on `feat/initial-plugin`.

## Affected Files

- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `plugins/llmwiki-bridge/.claude-plugin/plugin.json`
- `plugins/llmwiki-bridge/.codex-plugin/plugin.json`
- `plugins/llmwiki-bridge/skills/*/SKILL.md`
- `plugins/llmwiki-bridge/skills/*/agents/openai.yaml`
- `scripts/validate_repo.py`
- `scripts/run_optional_validators.py`
- `.github/workflows/ci.yml`
- `.github/workflows/release-host-gates.yml`
- repository governance docs
- this spec and ADR

## Rollout

1. Use local marketplace installation for Claude Code and Codex.
2. Push the repository to GitHub.
3. Share marketplace install commands from the README.
4. Submit the Claude community marketplace form after the GitHub repository is
   public and `claude plugin validate` passes.
5. Keep plugin changes on a release branch until the first public marketplace
   smoke is complete.

## Risks

- Host validators may not be installed on every development machine.
- Claude Code and Codex marketplace schemas are similar but not identical, and
  validator flags can differ across installed host CLI versions.
- Skills can become stale if `llmwiki-bridge-start` or `llmwiki-serve` command
  contracts change.
- Users may expect Agent Bridge to be mandatory unless the plugin wording keeps
  direct source setup first.

## Mitigations

- Keep host manifests minimal and schema-specific.
- Keep Claude Code optional fields out of the Claude manifest until older
  validators accept them consistently.
- Run the Codex helper validator and Claude Code validator when available.
- Validate skill text against required approval and safety phrases.
- Do not document host MCP configuration commands unless the host CLI has been
  inspected in the current environment.
