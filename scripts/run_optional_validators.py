#!/usr/bin/env python3
"""Run host-specific plugin validators when they are installed locally."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "llmwiki-bridge"
SKILLS = PLUGIN / "skills"
SKILL_NAMES = ["setup", "status", "doctor"]


def run(command: list[str]) -> int:
    print("+ " + " ".join(command))
    completed = subprocess.run(command, cwd=ROOT, check=False)
    return completed.returncode


def main() -> int:
    failures = 0
    ran = 0

    claude = shutil.which("claude")
    if claude:
        ran += 2
        failures += 1 if run([claude, "plugin", "validate", str(ROOT)]) else 0
        failures += 1 if run([claude, "plugin", "validate", str(PLUGIN)]) else 0
    else:
        print("SKIP: claude CLI not found; skipped Claude Code validator.")

    helper = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "plugin-creator"
        / "scripts"
        / "validate_plugin.py"
    )
    if helper.is_file():
        ran += 1
        failures += 1 if run([sys.executable, str(helper), str(PLUGIN)]) else 0
    else:
        print("SKIP: Codex plugin-creator validator not found.")

    quick_validate = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "skill-creator"
        / "scripts"
        / "quick_validate.py"
    )
    if quick_validate.is_file():
        for skill_name in SKILL_NAMES:
            ran += 1
            failures += 1 if run([sys.executable, str(quick_validate), str(SKILLS / skill_name)]) else 0
    else:
        print("SKIP: skill-creator quick_validate.py not found.")

    if not ran:
        print("No optional host validators were available.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
