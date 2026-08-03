# Claude Marketplace Submission Draft

This draft is for preparing a Claude marketplace submission. It is not a
submitted form, attestation, or approval record.

## Submission Metadata

Name: LLMWiki Bridge

Plugin ID: `llmwiki-bridge`

Short description: Connect Claude Code to cited LLMWiki, Markdown, and
Obsidian-style knowledge through safe setup, status, and doctor skills.

Long description: LLMWiki Bridge provides Claude Code skills for connecting to
existing knowledge through `llmwiki-serve`. It starts with the direct
single-source topology and keeps `llmwiki-agent-bridge` as an optional
escalation path for multiple sources, one aggregate endpoint, or runtime-backed
synthesis. The plugin is skills-first and does not include a daemon, MCP server,
hook, executable alias, crawler, or model runtime.

Category: Productivity

License: Apache-2.0

Repository: https://github.com/knowledge-bridge-labs/llmwiki-plugins

Documentation: https://knowledge-bridge-labs.github.io/llmwiki-docs/

Privacy policy: https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/PRIVACY.md

Terms: https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/TERMS.md

## Use Cases

- Guide a first safe connection from Claude Code to an existing LLMWiki,
  Markdown, or Obsidian-style source.
- Inspect existing `llmwiki-serve` sources without restarting or cleaning them
  up.
- Run read-only readiness checks for installed tools, local sources, and
  explicitly approved bridge-start state.
- Produce healthy-source-only direct MCP Streamable HTTP URLs for host
  configuration.
- Explain when Agent Bridge is useful for multiple sources or runtime-backed
  synthesis, without making it the default for one source.

## Security Notes

- The plugin contains only shared skills and host metadata.
- It does not ship executables, an MCP server, background processes, hooks,
  crawlers, sync jobs, or model runtime code.
- Skills require explicit approval before package installation, process start,
  remote or non-loopback probing, or client configuration writes.
- Skills must not modify, normalize, compile, upload, or commit wiki source
  files.
- Status must not append `/mcp/stream` for stale, unhealthy, ambiguous, or
  wildcard-host source entries.
- Remote probes and later query text can be visible to the remote operator.
  HTTPS is recommended by default, and plain HTTP requires explicit approval on
  a private or otherwise trusted network.
- Credentials and tokens must stay out of repository files and public reports.

## Pre-Submit Checklist

- [ ] Repository is public and points to the intended release commit.
- [ ] `py -3 scripts/validate_repo.py` passes.
- [ ] `py -3 scripts/run_optional_validators.py` passes or documents skipped
      unavailable host validators.
- [ ] `claude plugin validate .` passes with the target Claude Code CLI.
- [ ] `claude plugin validate ./plugins/llmwiki-bridge` passes with the target
      Claude Code CLI.
- [ ] Claude local marketplace add/install/list smoke has passed in an
      isolated test home.
- [ ] Codex local marketplace add/install/list smoke has passed in an isolated
      test home.
- [ ] `py -3 scripts/build_codex_submission.py` builds and prints the expected
      skills-only ZIP contents.
- [ ] Public listing copy contains no credentials, private endpoints, private
      local paths, or raw logs.
- [ ] Privacy and Terms URLs resolve to public repository documents.
- [ ] No real marketplace form or security attestation has been submitted from
      this draft.
