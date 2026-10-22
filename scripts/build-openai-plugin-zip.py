#!/usr/bin/env python3
"""Build the OpenAI plugin zip. The zip root is the Agent Plugin package."""

from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ZIP_NAME = "securin-platform-openai-0.1.0.zip"

INCLUDE_DIRS = ("skills", "assets")
INCLUDE_FILES = ("LICENSE", "README.md")
SKIP_DIR_NAMES = {".git", "node_modules", "__pycache__", "dist"}


def iter_files(path: Path):
    for child in sorted(path.rglob("*")):
        if not child.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in child.relative_to(path).parts):
            continue
        yield child


def build(destination: Path | None = None) -> Path:
    destination = destination or (DIST / ZIP_NAME)
    destination.parent.mkdir(parents=True, exist_ok=True)
    codex_mcp = {
        "mcpServers": {
            "securin": {
                "url": "https://mcp.securin.io/mcp"
            }
        }
    }
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.write(ROOT / "packaging" / "openai" / "plugin.json", "plugin.json")
        archive.write(ROOT / "packaging" / "openai" / "mcp.json", "mcp.json")
        archive.writestr(
            ".mcp.json",
            json.dumps(codex_mcp, indent=2) + "\n",
        )
        archive.write(
            ROOT / "packaging" / "openai" / ".codex-plugin" / "plugin.json",
            ".codex-plugin/plugin.json",
        )
        for name in INCLUDE_FILES:
            archive.write(ROOT / name, name)
        for directory in INCLUDE_DIRS:
            base = ROOT / directory
            for file_path in iter_files(base):
                archive.write(file_path, file_path.relative_to(ROOT).as_posix())
    verify(destination)
    return destination


def verify(destination: Path) -> None:
    with zipfile.ZipFile(destination) as archive:
        names = set(archive.namelist())
        required = {
            "plugin.json",
            "mcp.json",
            ".mcp.json",
            ".codex-plugin/plugin.json",
            "LICENSE",
            "README.md",
            "assets/logo.svg",
            "assets/logo.png",
            "skills/securin-cve-enrichment/SKILL.md",
        }
        missing = sorted(required - names)
        if missing:
            raise SystemExit(f"OpenAI zip missing {missing}")
        banned = [
            name
            for name in names
            if name.endswith(".mcpb")
            or name.startswith("mcpb/")
            or "node_modules/" in name
            or name.endswith(".env")
            or name.endswith(".pem")
        ]
        if banned:
            raise SystemExit(f"OpenAI zip contains banned paths: {banned[:10]}")
        plugin = json.loads(archive.read("plugin.json"))
        mcp = json.loads(archive.read("mcp.json"))
        if plugin.get("name") != "securin-platform" or plugin.get("version") != "0.1.0":
            raise SystemExit("OpenAI zip plugin identity drifted")
        url = mcp.get("mcpServers", {}).get("securin", {}).get("url")
        if url != "https://mcp.securin.io/mcp":
            raise SystemExit("OpenAI zip MCP URL drifted")
        blob = archive.read("mcp.json") + archive.read("plugin.json")
        if b"clientSecret" in blob or b"http://" in blob:
            raise SystemExit("OpenAI zip contains a secret field or a non HTTPS URL")
    print(f"wrote {destination} ({destination.stat().st_size} bytes)")


def main() -> int:
    build()
    return 0


if __name__ == "__main__":
    sys.exit(main())
