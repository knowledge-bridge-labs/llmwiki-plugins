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
    "plugins/llmwiki-bridge/skills/status/SKILL.md",
    "plugins/llmwiki-bridge/skills/doctor/SKILL.md",
    "specs/plugin-onboarding/spec.md",
    "specs/plugin-onboarding/plan.md",
    "specs/plugin-onboarding/tasks.md",
    "specs/plugin-onboarding/tests.md",
    "docs/decisions/0001-skills-first-host-plugin-boundary.md",
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


def assert_no_forbidden_components() -> None:
    forbidden_names = {"lb", "lb.cmd", "lb.ps1", "lb.sh", "hooks.json", ".mcp.json", ".app.json"}
    found = []
    for path in PLUGIN.rglob("*"):
        if path.name in forbidden_names:
            found.append(str(path.relative_to(ROOT)))
    if found:
        fail("forbidden plugin component(s): " + ", ".join(found))


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
    assert_no_forbidden_components()
    assert_no_sensitive_literals()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
