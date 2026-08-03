#!/usr/bin/env python3
"""Validate the llmwiki-bridge plugin repository without external packages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "llmwiki-bridge"
SKILLS = PLUGIN / "skills"


REQUIRED_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "SECURITY.md",
    "PRIVACY.md",
    "TERMS.md",
    "CHANGELOG.md",
    "AGENTS.md",
    ".claude-plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
    "plugins/llmwiki-bridge/.claude-plugin/plugin.json",
    "plugins/llmwiki-bridge/.codex-plugin/plugin.json",
    "plugins/llmwiki-bridge/skills/setup/SKILL.md",
    "plugins/llmwiki-bridge/skills/setup/agents/openai.yaml",
    "plugins/llmwiki-bridge/skills/status/SKILL.md",
    "plugins/llmwiki-bridge/skills/status/agents/openai.yaml",
    "plugins/llmwiki-bridge/skills/doctor/SKILL.md",
    "plugins/llmwiki-bridge/skills/doctor/agents/openai.yaml",
    "scripts/build_codex_submission.py",
    "specs/plugin-onboarding/spec.md",
    "specs/plugin-onboarding/plan.md",
    "specs/plugin-onboarding/tasks.md",
    "specs/plugin-onboarding/tests.md",
    "docs/decisions/0001-skills-first-host-plugin-boundary.md",
    "docs/submission/openai-listing.md",
    "docs/submission/claude-listing.md",
    "docs/validation/0.1.0-cross-platform.md",
]


TEXT_SUFFIXES = {".md", ".json", ".yml", ".yaml", ".py", ".txt"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(relative: str) -> object:
    path = ROOT / relative
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{relative} is not valid JSON: {exc}")


def assert_required_files() -> None:
    missing = [name for name in REQUIRED_FILES if not (ROOT / name).is_file()]
    if missing:
        fail("missing required files: " + ", ".join(missing))


def assert_claude_marketplace() -> None:
    data = load_json(".claude-plugin/marketplace.json")
    if not isinstance(data, dict):
        fail("Claude marketplace must be an object")
    if data.get("name") != "knowledge-bridge-labs":
        fail("Claude marketplace name must be knowledge-bridge-labs")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("Claude marketplace must contain exactly one plugin")
    entry = plugins[0]
    if entry.get("name") != "llmwiki-bridge":
        fail("Claude marketplace plugin name must be llmwiki-bridge")
    if entry.get("source") != "./plugins/llmwiki-bridge":
        fail("Claude marketplace source must be ./plugins/llmwiki-bridge")
    if "description" in data or "description" in entry:
        fail("Claude marketplace must omit optional description fields for 2.1.117 compatibility")


def assert_codex_marketplace() -> None:
    data = load_json(".agents/plugins/marketplace.json")
    if not isinstance(data, dict):
        fail("Codex marketplace must be an object")
    if data.get("name") != "knowledge-bridge-labs":
        fail("Codex marketplace name must be knowledge-bridge-labs")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("Codex marketplace must contain exactly one plugin")
    entry = plugins[0]
    if entry.get("name") != "llmwiki-bridge":
        fail("Codex marketplace plugin name must be llmwiki-bridge")
    source = entry.get("source")
    if source != {"source": "local", "path": "./plugins/llmwiki-bridge"}:
        fail("Codex marketplace source must be local ./plugins/llmwiki-bridge")
    policy = entry.get("policy")
    if policy != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
        fail("Codex marketplace policy must include AVAILABLE and ON_INSTALL")
    if entry.get("category") != "Productivity":
        fail("Codex marketplace category must be Productivity")


def assert_plugin_manifests() -> None:
    claude = load_json("plugins/llmwiki-bridge/.claude-plugin/plugin.json")
    codex = load_json("plugins/llmwiki-bridge/.codex-plugin/plugin.json")
    for label, data in [("Claude", claude), ("Codex", codex)]:
        if not isinstance(data, dict):
            fail(f"{label} plugin manifest must be an object")
        if data.get("name") != "llmwiki-bridge":
            fail(f"{label} plugin name must be llmwiki-bridge")
        if data.get("skills") != "./skills/":
            fail(f"{label} plugin skills path must be ./skills/")
        description = data.get("description", "")
        if "llmwiki-serve" not in description:
            fail(f"{label} description must name llmwiki-serve")
        if "lb" in data.get("name", ""):
            fail(f"{label} plugin name must not use lb")
    interface = codex.get("interface")
    if not isinstance(interface, dict):
        fail("Codex manifest must include interface metadata")
    if interface.get("displayName") != "LLMWiki Bridge":
        fail("Codex displayName must be LLMWiki Bridge")
    if interface.get("privacyPolicyURL") != "https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/PRIVACY.md":
        fail("Codex privacyPolicyURL must point to public PRIVACY.md")
    if interface.get("termsOfServiceURL") != "https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/TERMS.md":
        fail("Codex termsOfServiceURL must point to public TERMS.md")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        fail("Codex defaultPrompt must be a list of one to three prompts")
    for skill_name in ["llmwiki-bridge:setup", "llmwiki-bridge:status", "llmwiki-bridge:doctor"]:
        if not any(isinstance(prompt, str) and skill_name in prompt for prompt in prompts):
            fail(f"Codex defaultPrompt must include {skill_name}")
    if "version" in claude:
        fail("Claude manifest must omit fixed version for git-SHA marketplace updates")
    if "displayName" in claude:
        fail("Claude manifest must omit displayName for 2.1.117 compatibility")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        fail(f"{path.relative_to(ROOT)} must start with YAML frontmatter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError:
        fail(f"{path.relative_to(ROOT)} frontmatter is not closed")
    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            fail(f"{path.relative_to(ROOT)} frontmatter line lacks ':'")
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields


def assert_skills() -> None:
    expected = ["doctor", "setup", "status"]
    actual = sorted(path.name for path in SKILLS.iterdir() if path.is_dir())
    if actual != expected:
        fail(f"skill directories must be exactly {expected}; got {actual}")
    for name in expected:
        path = SKILLS / name / "SKILL.md"
        fields = parse_frontmatter(path)
        if not fields.get("description"):
            fail(f"{path.relative_to(ROOT)} must include description frontmatter")
        text = path.read_text(encoding="utf-8").lower()
        normalized_text = re.sub(r"\s+", " ", text)
        required_terms = [
            "explicit approval",
            "install",
            "process",
            "configuration",
            "home",
            "modify",
            "upload",
            "llmwiki-serve ls --json",
            "llmwiki-agent-bridge",
            "/mcp/stream",
        ]
        if name == "setup":
            required_terms.append("setup")
            required_terms.extend(["query text", "https", "0.0.0.0"])
        if name == "doctor":
            required_terms.extend(["query text", "https", "0.0.0.0"])
        for term in required_terms:
            if term not in text:
                fail(f"{path.relative_to(ROOT)} must mention {term!r}")
        if name == "setup":
            setup_terms = [
                "wiki -> llmwiki-serve -> claude code/codex",
                "agent bridge is never part of the default single-source topology",
                "do not insert `llmwiki-agent-bridge`",
                "explicitly asks for multiple sources",
                "one aggregate endpoint",
                "runtime-backed answer synthesis",
                "do not automatically widen discovery",
                "parent, siblings, workspace root, home directory",
                "mounted drives",
                "cloud-sync folders",
                "recent-project lists",
                "broad sensitive-content inspection",
                "stay inside the source boundary the user approved",
            ]
            for term in setup_terms:
                if term not in normalized_text:
                    fail(f"{path.relative_to(ROOT)} must include setup regression guard {term!r}")
        if name == "doctor":
            doctor_terms = [
                "is not approval to probe",
                "dns lookup",
                "tcp connection attempts",
                "http or https requests",
                "user's ip address",
                "yes/no approval question",
                "wait for the next user response",
                "resolve-dnsname",
                "test-netconnection",
                "invoke-webrequest",
                "fetch",
                "do not run",
            ]
            for term in doctor_terms:
                if term not in normalized_text:
                    fail(f"{path.relative_to(ROOT)} must include doctor regression guard {term!r}")
        if name == "status":
            status_terms = [
                "exactly once",
                "20-30 second timeout",
                "recommended timeout: 25 seconds",
                "if the bounded `llmwiki-serve ls --json` call times out",
                "do not retry",
                "do not run `npx`",
                "do not run fixed-port scans",
                "at most once",
                "separately approved that exact command",
                "healthy sources only",
                "usable direct mcp",
                "diagnostic base url",
                "do not append `/mcp/stream` to stale",
                "unhealthy",
                "ambiguous",
                "wildcard-host",
            ]
            for term in status_terms:
                if term not in normalized_text:
                    fail(f"{path.relative_to(ROOT)} must include status regression guard {term!r}")


def assert_skill_openai_metadata() -> None:
    expected = {
        "setup": {
            "display_name": "LLMWiki Bridge Setup",
            "short_description": "Connect a wiki source safely",
            "default_prompt": "Use $setup ",
        },
        "status": {
            "display_name": "LLMWiki Bridge Status",
            "short_description": "Inspect running source status",
            "default_prompt": "Use $status ",
        },
        "doctor": {
            "display_name": "LLMWiki Bridge Doctor",
            "short_description": "Diagnose LLMWiki readiness",
            "default_prompt": "Use $doctor ",
        },
    }
    for name, fields in expected.items():
        path = SKILLS / name / "agents" / "openai.yaml"
        text = path.read_text(encoding="utf-8")
        if not text.startswith("interface:\n"):
            fail(f"{path.relative_to(ROOT)} must start with interface metadata")
        for key, value in fields.items():
            if f'{key}: "{value}' not in text:
                fail(f"{path.relative_to(ROOT)} must include {key} matching {value!r}")


def assert_no_forbidden_components() -> None:
    forbidden_names = {"lb", "lb.cmd", "lb.ps1", "lb.sh", "hooks.json", ".mcp.json", ".app.json"}
    found = []
    for path in PLUGIN.rglob("*"):
        if path.name in forbidden_names:
            found.append(str(path.relative_to(ROOT)))
    if found:
        fail("forbidden plugin component(s): " + ", ".join(found))


def assert_submission_docs() -> None:
    openai = (ROOT / "docs" / "submission" / "openai-listing.md").read_text(encoding="utf-8").lower()
    openai_normalized = re.sub(r"\s+", " ", openai)
    openai_terms = [
        "listing copy",
        "starter prompts",
        "positive test cases",
        "negative test cases",
        "expected behavior",
        "privacy and approval boundaries",
        "healthy sources only",
        "does not append `/mcp/stream`",
    ]
    for term in openai_terms:
        if term not in openai_normalized:
            fail(f"docs/submission/openai-listing.md must include {term!r}")

    claude = (ROOT / "docs" / "submission" / "claude-listing.md").read_text(encoding="utf-8").lower()
    claude_normalized = re.sub(r"\s+", " ", claude)
    claude_terms = [
        "name: llmwiki bridge",
        "use cases",
        "security notes",
        "repository: https://github.com/knowledge-bridge-labs/llmwiki-plugins",
        "documentation: https://knowledge-bridge-labs.github.io/llmwiki-docs/",
        "privacy policy: https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/privacy.md",
        "terms: https://github.com/knowledge-bridge-labs/llmwiki-plugins/blob/main/terms.md",
        "pre-submit checklist",
        "not a submitted form",
    ]
    for term in claude_terms:
        if term not in claude_normalized:
            fail(f"docs/submission/claude-listing.md must include {term!r}")

    validation = (ROOT / "docs" / "validation" / "0.1.0-cross-platform.md").read_text(encoding="utf-8").lower()
    validation_normalized = re.sub(r"\s+", " ", validation)
    validation_terms = [
        "windows x64",
        "dgx ubuntu arm64",
        "first-commit findings",
        "post-fix pass",
        "redacted",
        "bridge-start status",
        "bridge-start doctor",
    ]
    for term in validation_terms:
        if term not in validation_normalized:
            fail(f"docs/validation/0.1.0-cross-platform.md must include {term!r}")


def assert_codex_submission_builder() -> None:
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "dist/" not in gitignore.splitlines():
        fail(".gitignore must ignore dist/")

    script = (ROOT / "scripts" / "build_codex_submission.py").read_text(encoding="utf-8")
    builder_terms = [
        ".codex-plugin",
        "plugin.json",
        "skills/",
        "ZipInfo",
        "compresslevel=9",
        "codex-skills.zip",
        ".claude-plugin",
        ".mcp.json",
        ".app.json",
        "README.md",
    ]
    for term in builder_terms:
        if term not in script:
            fail(f"scripts/build_codex_submission.py must include {term!r}")

    workflow = (ROOT / ".github" / "workflows" / "release-host-gates.yml").read_text(encoding="utf-8")
    workflow_terms = [
        "python scripts/build_codex_submission.py",
        "actions/upload-artifact@v4",
        "dist/llmwiki-bridge-*-codex-skills.zip",
    ]
    for term in workflow_terms:
        if term not in workflow:
            fail(f".github/workflows/release-host-gates.yml must include {term!r}")
    forbidden_release_uploads = ["gh release upload", "softprops/action-gh-release", "actions/upload-release-asset"]
    for term in forbidden_release_uploads:
        if term in workflow:
            fail("release host workflow must not upload ZIPs to tag releases")


def assert_no_sensitive_literals() -> None:
    windows_user = re.compile(r"\b[A-Za-z]:\\(?:Users|Documents and Settings)\\[^\\\s]+")
    posix_user = re.compile("/" + "home" + r"/[^/\s]+|/" + "Users" + r"/[^/\s]+")
    secret_patterns = [
        re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
        re.compile(r"ghp_[A-Za-z0-9_]{16,}"),
        re.compile(r"npm_[A-Za-z0-9_]{16,}"),
        re.compile(r"AKIA[0-9A-Z]{16}"),
    ]
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        if path.is_dir() or ".git" in path.parts:
            continue
        if path.suffix not in TEXT_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if windows_user.search(text) or posix_user.search(text):
            offenders.append(str(path.relative_to(ROOT)))
            continue
        if any(pattern.search(text) for pattern in secret_patterns):
            offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        fail("potential sensitive literal(s): " + ", ".join(sorted(set(offenders))))


def main() -> None:
    assert_required_files()
    assert_claude_marketplace()
    assert_codex_marketplace()
    assert_plugin_manifests()
    assert_skills()
    assert_skill_openai_metadata()
    assert_no_forbidden_components()
    assert_submission_docs()
    assert_codex_submission_builder()
    assert_no_sensitive_literals()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
