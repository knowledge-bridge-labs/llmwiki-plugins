# Changelog

## Unreleased

- Removed Claude Code optional manifest fields that older Claude Code 2.1.117
  rejects during validation.
- Added Privacy and Terms documents and pointed Codex listing metadata at those
  public GitHub paths.
- Clarified direct MCP endpoint derivation from `llmwiki-serve ls --json` base
  URLs and strengthened remote endpoint disclosure.
- Added a tag/manual release host gate for current Claude Code and Codex CLI
  validation.

## 0.1.0 - 2026-08-03

- Added initial skills-first `llmwiki-bridge` plugin for Claude Code and Codex.
- Added shared `setup`, `status`, and `doctor` skills.
- Added Claude Code and Codex marketplace metadata.
- Added plugin onboarding spec, ADR, validation script, and CI.
