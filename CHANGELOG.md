# Changelog

## Unreleased

No unreleased changes yet.

## 0.1.0 - 2026-08-04

- Released the initial public GitHub marketplace version of the skills-first
  `llmwiki-bridge` plugin for Claude Code and Codex.
- Added shared `setup`, `status`, and `doctor` skills.
- Added Claude Code and Codex marketplace metadata.
- Added plugin onboarding spec, ADR, validation script, and CI.
- Fixed forward-test regressions in setup, doctor, and status skill guidance:
  single-source setup now hard-pins the direct `llmwiki-serve` topology, remote
  doctor checks require a separate yes/no probe approval, and status discovery
  is a one-shot bounded command.
- Removed Claude Code optional manifest fields that older Claude Code 2.1.117
  rejects during validation.
- Added Privacy and Terms documents and pointed Codex listing metadata at those
  public GitHub paths.
- Clarified direct MCP endpoint derivation from `llmwiki-serve ls --json` base
  URLs and strengthened remote endpoint disclosure.
- Added a tag/manual release host gate for current Claude Code and Codex CLI
  validation.
- Added generated `agents/openai.yaml` metadata for the `setup`, `status`, and
  `doctor` skills.
- Added `skill-creator` quick validation to optional local validator gates.
- Hardened status guidance and validation so stale, unhealthy, ambiguous, and
  wildcard-host sources cannot be presented with usable `/mcp/stream` URLs.
- Added public OpenAI/Codex and Claude submission drafts plus a redacted
  cross-platform validation record.
- Added a deterministic skills-only Codex submission ZIP builder and release
  host CI artifact upload.
- Verified public GitHub marketplace install on Windows x64 and DGX Ubuntu
  ARM64 for both Claude Code and Codex.
- Built the release Codex skills-only ZIP:
  `dist/llmwiki-bridge-0.1.0-codex-skills.zip`.
- ZIP SHA256:
  `622DB83E37F57DB3C16569BA45254B1011822B30ED23B750CD72FE644C2CD7F7`.
- Claude community marketplace form and OpenAI directory portal submission are
  intentionally manual/pending and were not submitted for this release record.
