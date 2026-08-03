# Privacy Policy

LLMWiki Bridge is a skills-only plugin for Claude Code and Codex. The plugin
repository does not run a hosted service, collect telemetry, store user data,
or upload wiki content.

The skills may guide a coding agent to run local commands such as
`llmwiki-serve ls --json`, `llmwiki-bridge-start status`, or
`llmwiki-bridge-start doctor` after the user approves the relevant step. Those
commands run on the user's machine or on infrastructure the user chooses.

When a user connects to a remote or non-loopback `llmwiki-serve` or
`llmwiki-agent-bridge` endpoint, probes and later search or query text are sent
to that remote operator. Use HTTPS by default. Plain HTTP should be used only on
a private or otherwise trusted network after explicit user approval.

Do not commit private endpoints, local paths, logs, secrets, wiki content, or
credentials to this repository.
