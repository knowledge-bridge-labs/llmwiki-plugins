#!/usr/bin/env python3
"""Build a deterministic public Codex skills-only submission ZIP."""

from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLUGIN = ROOT / "plugins" / "llmwiki-bridge"
DEFAULT_DIST = ROOT / "dist"
ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
EXCLUDED_PARTS = {
    ".claude-plugin",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".git",
}
EXCLUDED_NAMES = {
    ".DS_Store",
    "Thumbs.db",
    ".mcp.json",
    ".app.json",
    "README",
    "README.md",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_manifest(plugin_dir: Path) -> dict[str, object]:
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing Codex manifest: {manifest_path}")
    except json.JSONDecodeError as exc:
        fail(f"invalid Codex manifest JSON: {exc}")
    if not isinstance(data, dict):
        fail("Codex manifest must be a JSON object")
    return data


def archive_name(manifest: dict[str, object]) -> str:
    name = manifest.get("name")
    version = manifest.get("version")
    if not isinstance(name, str) or not name:
        fail("Codex manifest must include a non-empty string name")
    if not isinstance(version, str) or not version:
        fail("Codex manifest must include a non-empty string version")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", version):
        fail(f"unsupported version for filename: {version!r}")
    return f"{name}-{version}-codex-skills.zip"


def should_exclude(relative: Path) -> bool:
    parts = set(relative.parts)
    if parts & EXCLUDED_PARTS:
        return True
    return relative.name in EXCLUDED_NAMES


def included_files(plugin_dir: Path) -> list[Path]:
    manifest_path = plugin_dir / ".codex-plugin" / "plugin.json"
    skills_dir = plugin_dir / "skills"
    if not manifest_path.is_file():
        fail("archive requires .codex-plugin/plugin.json")
    if not skills_dir.is_dir():
        fail("archive requires skills/")

    files = [manifest_path]
    for path in sorted(skills_dir.rglob("*"), key=lambda item: item.relative_to(plugin_dir).as_posix()):
        if not path.is_file():
            continue
        relative = path.relative_to(plugin_dir)
        if should_exclude(relative):
            continue
        files.append(path)
    return files


def validate_archive_paths(names: list[str]) -> None:
    if ".codex-plugin/plugin.json" not in names:
        fail("ZIP is missing .codex-plugin/plugin.json")
    if not any(name.startswith("skills/") for name in names):
        fail("ZIP is missing skills/**")
    for name in names:
        allowed = name == ".codex-plugin/plugin.json" or name.startswith("skills/")
        if not allowed:
            fail(f"ZIP contains non-public path: {name}")
        parts = set(Path(name).parts)
        if parts & EXCLUDED_PARTS:
            fail(f"ZIP contains excluded cache or host path: {name}")
        if Path(name).name in EXCLUDED_NAMES:
            fail(f"ZIP contains excluded file: {name}")


def write_zip(plugin_dir: Path, dist_dir: Path) -> Path:
    manifest = read_manifest(plugin_dir)
    output_path = dist_dir / archive_name(manifest)
    dist_dir.mkdir(parents=True, exist_ok=True)

    files = included_files(plugin_dir)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = path.relative_to(plugin_dir).as_posix()
            info = zipfile.ZipInfo(relative, ZIP_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    return output_path


def inspect_zip(path: Path) -> list[str]:
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
    if names != sorted(names):
        fail("ZIP contents are not sorted deterministically")
    validate_archive_paths(names)
    return names


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--plugin-dir",
        type=Path,
        default=DEFAULT_PLUGIN,
        help="Plugin directory to package, default: plugins/llmwiki-bridge",
    )
    parser.add_argument(
        "--dist-dir",
        type=Path,
        default=DEFAULT_DIST,
        help="Output directory, default: dist",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    plugin_dir = args.plugin_dir.resolve()
    dist_dir = args.dist_dir.resolve()
    if not plugin_dir.is_dir():
        fail(f"plugin directory does not exist: {plugin_dir}")

    output_path = write_zip(plugin_dir, dist_dir)
    names = inspect_zip(output_path)
    print(f"Built {output_path.relative_to(ROOT)}")
    print("Contents:")
    for name in names:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
