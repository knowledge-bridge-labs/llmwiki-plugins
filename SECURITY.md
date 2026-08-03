# Security Policy

## Supported Versions

The plugin is in public preview. Security fixes are made on the default branch
and released through the marketplace repository.

## Reporting

Please report security issues privately through GitHub Security Advisories for
`knowledge-bridge-labs/llmwiki-plugins` when available, or contact the
maintainers through the project issue tracker without including secrets or
private data.

## Plugin Boundaries

`llmwiki-bridge` is a skills-first plugin. It does not ship a daemon, MCP
server, background monitor, executable alias, crawler, sync engine, model
runtime, or authentication gateway.

The skills must preserve these defaults:

- No wiki source file edits.
- No wiki upload.
- No home-wide scan without explicit approval.
- No non-loopback network probing without explicit approval.
- No package installation without explicit approval.
- No process start without explicit approval.
- No client configuration write without explicit approval.
- No committed bearer tokens, API keys, private endpoints, or raw logs.

When connecting a remote `llmwiki-serve` or `llmwiki-agent-bridge` endpoint,
explain that probes and later search or query text are sent to the remote
operator. Use HTTPS by default. Use plain HTTP only on a private or otherwise
trusted network after explicit approval, and use host-managed secret storage
when credentials are needed. Do not write tokens into repository files.
