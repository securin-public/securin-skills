#!/usr/bin/env python3
"""Validate marketplace manifests and packaging docs.

Schema snapshots under packaging/schemas/ were retrieved on 2026-10-22:

- https://agent-plugins.org/schemas/1.0.0/plugin.schema.json
- https://agent-plugins.org/schemas/1.0.0/mcp.schema.json
- https://json.schemastore.org/claude-code-plugin-manifest.json
- https://json.schemastore.org/claude-code-marketplace.json
- https://raw.githubusercontent.com/modelcontextprotocol/mcpb/main/schemas/mcpb-manifest-v0.3.schema.json

The OpenAI auth object is not part of the Agent Plugins MCP schema. This
script checks that object against the fields OpenAI documents for dynamic
client registration, and checks the rest of mcp.json against the published
schema.
"""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

from jsonschema import FormatChecker
from jsonschema.validators import validator_for

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "packaging" / "schemas"
META_PATH = ROOT / "packaging" / "metadata.json"

STYLE_FILES = [
    ROOT / "docs" / "oauth-redirects.md",
    ROOT / "docs" / "submission.md",
    ROOT / "docs" / "marketplaces.md",
    ROOT / "docs" / "tool-scope.md",
    ROOT / "skills" / "_shared" / "tool-safety.md",
]

BANNED_CHARS = {
    "\u2014": "em dash",
    "\u2013": "en dash",
    "'": "apostrophe",
    "\u2019": "right single quote",
    "\u2018": "left single quote",
}

PLUGIN_KEYS = [
    ROOT / ".cursor-plugin" / "plugin.json",
    ROOT / ".grok-plugin" / "plugin.json",
    ROOT / ".claude-plugin" / "plugin.json",
    ROOT / "packaging" / "openai" / "plugin.json",
    ROOT / "packaging" / "openai" / ".codex-plugin" / "plugin.json",
]


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def ok(self) -> bool:
        return not self.errors


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def schema_validate(report: Report, instance: object, schema_name: str, label: str) -> None:
    schema = load_json(SCHEMA_DIR / schema_name)
    validator_cls = validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(instance), key=lambda err: list(err.path))
    for err in errors:
        where = "/".join(str(part) for part in err.path) or "<root>"
        report.fail(f"{label} failed {schema_name} at {where}: {err.message}")


def style_text(report: Report, label: str, text: str) -> None:
    for line_no, line in enumerate(text.splitlines(), 1):
        for char, name in BANNED_CHARS.items():
            if char in line:
                report.fail(f"{label}:{line_no} contains {name}")
                break
        if " VRI" in line or "VI " in f" {line} " or " APT" in line:
            report.fail(f"{label}:{line_no} uses a retired product name")


def strip_extensions(node: object) -> object:
    if isinstance(node, dict):
        return {
            key: strip_extensions(value)
            for key, value in node.items()
            if key != "extensions"
        }
    if isinstance(node, list):
        return [strip_extensions(value) for value in node]
    return node


def assert_https_mcp(report: Report, label: str, document: dict) -> None:
    servers = document.get("mcpServers")
    if not isinstance(servers, dict) or "securin" not in servers:
        report.fail(f"{label} must define mcpServers.securin")
        return
    server = servers["securin"]
    url = server.get("url") if isinstance(server, dict) else None
    if url != "https://mcp.securin.io/mcp":
        report.fail(f"{label} MCP URL is {url!r}")
    blob = json.dumps(document)
    if "http://" in blob or "clientSecret" in blob or "client_secret" in blob:
        report.fail(f"{label} contains a non HTTPS URL or a client secret field")
    if "npx" in blob or "mcp-remote" in blob:
        report.fail(f"{label} must not launch npx or mcp-remote")


def check_plugin_identity(report: Report, path: Path, meta: dict) -> None:
    document = load_json(path)
    if not isinstance(document, dict):
        report.fail(f"{path} is not an object")
        return
    for key in ("name", "version", "description", "homepage", "license"):
        if document.get(key) != meta[key]:
            report.fail(f"{path} {key} does not match packaging/metadata.json")
    author = document.get("author") or {}
    if author.get("name") != meta["authorName"] or author.get("email") != meta["supportEmail"]:
        report.fail(f"{path} author does not match packaging/metadata.json")
    style_text(report, str(path.relative_to(ROOT)), json.dumps(document))


def check_openai_auth(report: Report, document: dict) -> None:
    try:
        auth = document["mcpServers"]["securin"]["extensions"]["com.openai"]["auth"]
    except (KeyError, TypeError):
        report.fail("OpenAI mcp.json is missing extensions.com.openai.auth")
        return
    if auth.get("type") != "oauth":
        report.fail("OpenAI auth type must be oauth")
    client = auth.get("client") or {}
    if client.get("mode") != "dcr":
        report.fail("OpenAI auth must use dynamic client registration")
    if "clientId" in client or "clientSecret" in auth or "clientSecret" in client:
        report.fail("OpenAI auth must not carry a client id or secret")
    for key in ("authorizationUrl", "tokenUrl", "registrationUrl", "resource"):
        value = auth.get(key, "")
        if not isinstance(value, str) or not value.startswith("https://"):
            report.fail(f"OpenAI auth {key} must be an https URL")
    if auth.get("baseScopes") != ["openid"]:
        report.fail("OpenAI auth baseScopes must be openid only")


def check_skills(report: Report) -> None:
    skills = ROOT / "skills"
    if (skills / "_shared" / "SKILL.md").exists():
        report.fail("skills/_shared must not contain SKILL.md")
    found = 0
    for skill_dir in sorted(skills.glob("securin-*")):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.is_file():
            report.fail(f"{skill_dir.name} is missing SKILL.md")
            continue
        found += 1
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            report.fail(f"{skill_md} is missing frontmatter")
            continue
        front = text.split("---", 2)[1]
        if "\nname:" not in f"\n{front}" or "\ndescription:" not in f"\n{front}":
            report.fail(f"{skill_md} frontmatter needs name and description")
    if found != 6:
        report.fail(f"expected 6 skills, found {found}")


def check_logos(report: Report) -> None:
    pairs = [
        (ROOT / "assets" / "logo.svg", ROOT / "skills" / "_shared" / "securin_logos" / "securin-icon-on-light.svg"),
        (ROOT / "assets" / "logo.png", ROOT / "skills" / "_shared" / "securin_logos" / "securin-icon-on-light.png"),
        (ROOT / "assets" / "logo-dark.svg", ROOT / "skills" / "_shared" / "securin_logos" / "securin-icon-on-dark.svg"),
        (ROOT / "assets" / "logo-dark.png", ROOT / "skills" / "_shared" / "securin_logos" / "securin-icon-on-dark.png"),
    ]
    for copy, source in pairs:
        if not copy.is_file() or not source.is_file():
            report.fail(f"missing logo {copy}")
            continue
        if hashlib.sha256(copy.read_bytes()).digest() != hashlib.sha256(source.read_bytes()).digest():
            report.fail(f"{copy.name} does not match {source}")


def check_mcpb_archive(report: Report, manifest: dict) -> None:
    archive = ROOT / "securin-platform.mcpb"
    if not archive.is_file():
        report.fail("securin-platform.mcpb is missing")
        return
    with zipfile.ZipFile(archive) as bundle:
        names = set(bundle.namelist())
        if "manifest.json" not in names or "server/package.json" not in names:
            report.fail("MCPB archive is missing manifest.json or server/package.json")
            return
        packed = json.loads(bundle.read("manifest.json"))
        packed_package = json.loads(bundle.read("server/package.json"))
    if packed != manifest:
        report.fail("securin-platform.mcpb manifest.json does not match mcpb/manifest.json")
    disk_package = load_json(ROOT / "mcpb" / "server" / "package.json")
    if packed_package != disk_package:
        report.fail("MCPB archive server/package.json does not match mcpb/server/package.json")
    if packed.get("license") == "MIT" or packed.get("version") != "1.2.3":
        report.fail("MCPB archive license or version was not updated")


def validate(report: Report | None = None) -> Report:
    report = report or Report()
    meta = load_json(META_PATH)
    if not isinstance(meta, dict):
        report.fail("packaging/metadata.json must be an object")
        return report

    for path in PLUGIN_KEYS:
        check_plugin_identity(report, path, meta)

    claude_plugin = load_json(ROOT / ".claude-plugin" / "plugin.json")
    schema_validate(report, claude_plugin, "claude-code-plugin-manifest.schema.json", "Claude plugin")
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    schema_validate(report, marketplace, "claude-code-marketplace.schema.json", "Claude marketplace")
    plugins = marketplace.get("plugins") if isinstance(marketplace, dict) else None
    if not isinstance(plugins, list) or len(plugins) != 1:
        report.fail("Claude marketplace must list one plugin")
    elif plugins[0].get("description") != meta["description"] or plugins[0].get("version") != meta["version"]:
        report.fail("Claude marketplace plugin entry drifted from metadata")
    if isinstance(marketplace, dict) and marketplace.get("name") != "securin-skills":
        report.fail("Claude marketplace id must stay securin-skills")

    cursor = load_json(ROOT / ".cursor-plugin" / "plugin.json")
    grok = load_json(ROOT / ".grok-plugin" / "plugin.json")
    if isinstance(cursor, dict) and cursor.get("mcpServers") != "./mcp.json":
        report.fail("Cursor manifest must pin mcpServers to ./mcp.json")
    if isinstance(grok, dict) and grok.get("mcpServers") != "./mcp.json":
        report.fail("Grok manifest must pin mcpServers to ./mcp.json")
    if isinstance(cursor, dict) and cursor.get("logo") != "assets/logo.svg":
        report.fail("Cursor logo path must be assets/logo.svg")

    root_mcp = load_json(ROOT / "mcp.json")
    dot_mcp = load_json(ROOT / ".mcp.json")
    if root_mcp != dot_mcp:
        report.fail("mcp.json and .mcp.json must stay identical")
    assert_https_mcp(report, "mcp.json", root_mcp if isinstance(root_mcp, dict) else {})
    if isinstance(root_mcp, dict):
        server = root_mcp.get("mcpServers", {}).get("securin", {})
        if server.get("type") != "http":
            report.fail("root mcp.json type must be http for Cursor and Claude")

    openai_plugin = load_json(ROOT / "packaging" / "openai" / "plugin.json")
    schema_validate(report, openai_plugin, "agent-plugin.schema.json", "OpenAI plugin")
    openai_mcp = load_json(ROOT / "packaging" / "openai" / "mcp.json")
    if isinstance(openai_mcp, dict):
        schema_validate(
            report,
            strip_extensions(openai_mcp),
            "agent-mcp.schema.json",
            "OpenAI mcp.json portable fields",
        )
        check_openai_auth(report, openai_mcp)
        assert_https_mcp(report, "OpenAI mcp.json", strip_extensions(openai_mcp))

    mcpb = load_json(ROOT / "mcpb" / "manifest.json")
    schema_validate(report, mcpb, "mcpb-manifest-v0.3.schema.json", "MCPB manifest")
    if isinstance(mcpb, dict):
        if mcpb.get("name") != meta["name"] or mcpb.get("homepage") != meta["homepage"]:
            report.fail("MCPB name or homepage drifted")
        if mcpb.get("license") != meta["license"] or mcpb.get("version") != meta["mcpbVersion"]:
            report.fail("MCPB license or version drifted")
        style_text(report, "mcpb/manifest.json", json.dumps(mcpb))
        check_mcpb_archive(report, mcpb)

    package_json = load_json(ROOT / "mcpb" / "server" / "package.json")
    if isinstance(package_json, dict):
        if package_json.get("dependencies", {}).get("mcp-remote") != "0.1.38":
            report.fail("mcp-remote must be pinned to 0.1.38")
        if package_json.get("license") != meta["license"]:
            report.fail("mcpb server package license drifted")

    check_logos(report)
    check_skills(report)
    for path in STYLE_FILES:
        style_text(report, str(path.relative_to(ROOT)), path.read_text(encoding="utf-8"))
    style_text(report, "metadata description", meta["description"])
    return report


def main() -> int:
    report = validate()
    if report.errors:
        print(f"manifest validation failed ({len(report.errors)})")
        for message in report.errors:
            print(f"- {message}")
        return 1
    print("manifest validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
