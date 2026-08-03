# Terms Of Service

LLMWiki Bridge is provided as open-source software under the Apache License
2.0. See [LICENSE](./LICENSE).

The plugin provides setup, status, and doctor skills that help a coding agent
connect to user-selected LLMWiki, Markdown, or Obsidian-style knowledge sources
through the published LLMWiki tools. It does not provide a hosted service,
authentication gateway, model runtime, crawler, sync engine, or production
authorization layer.

Users are responsible for choosing which local paths and remote endpoints to
connect, for obtaining permission to access those sources, and for protecting
any private data they expose to a local or remote runtime.

Remote and non-loopback endpoints should use HTTPS by default. Plain HTTP
should be limited to private or otherwise trusted networks and used only after
explicit approval.
