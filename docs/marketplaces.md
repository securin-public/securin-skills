# Marketplace formats

Plugin name `securin-platform`. Package version `0.1.0`. Homepage `https://securin.io`. Support `support@securin.io`. Logo files in `assets/` are copies of the existing Securin icon in `skills/_shared/securin_logos/`. The license field in every manifest is `LicenseRef-Securin-Proprietary`, which points at the root `LICENSE`. Legal has not signed off on that identifier. See [submission.md](submission.md).

The remote server for every listing is `https://mcp.securin.io/mcp`. Auth is per user OAuth. Details and redirect URIs are in [oauth-redirects.md](oauth-redirects.md). Tool boundaries are in [tool-scope.md](tool-scope.md).

## Cursor Marketplace

Format: Cursor plugin.

| File | Role |
| --- | --- |
| `.cursor-plugin/plugin.json` | Manifest. `mcpServers` is pinned to `./mcp.json` so a host that also sees `.mcp.json` still starts the same HTTPS server. |
| `mcp.json` | Remote server, `type` `http`, no headers and no token. |
| `skills/*/SKILL.md` | Six skills. `skills/_shared` has no `SKILL.md`, so it is not a skill. |
| `assets/logo.svg` | Logo path in the manifest. |

Submit the public GitHub repository at https://cursor.com/marketplace/publish. There is one plugin at the repository root, so this repo does not add `.cursor-plugin/marketplace.json`. That file is for a repository that holds several plugins in subfolders.

Cursor also loads an Agent Plugin when `plugin.json` sits at the repository root. This repo keeps the OpenAI Agent Plugin manifest under `packaging/openai/` and puts it at the root of the upload zip only. A second root `plugin.json` in git could be installed beside the Cursor manifest.

## Grok Bot and Grok

Grok Bot lists plugins with the Cursor plugin format. The same `.cursor-plugin/plugin.json`, `mcp.json`, skills, and logo are the Grok Bot package. There is no separate Grok Bot manifest.

The Grok Bot submission form is https://x.ai/bot/marketplace/submit-a-plugin. The form can target Grok Bot, Cursor, and Grok. On 2026-10-18 the form marked Grok as coming soon. Confirm the label on the day you submit.

xAI Grok on the web also has a connector callback, `https://grok.com/connectors-oauth-exchange-code/`. That is an allowlist item, not a second package. See [oauth-redirects.md](oauth-redirects.md).

### Grok Build catalog

Grok Build installs from the catalog in `xai-org/plugin-marketplace`. A third party entry points at this repository with a pinned commit. The Grok reader looks for `.grok-plugin/plugin.json` first, then `.cursor-plugin/plugin.json`. This repo includes `.grok-plugin/plugin.json` so the catalog resolves version `0.1.0`, the six skills, and `./mcp.json`.

The catalog pull request cannot be opened with a correct commit SHA until this package is on the default branch. The JSON to paste is in [submission.md](submission.md).

## OpenAI

Checked against OpenAI plugin docs on 2026-10-22.

ChatGPT apps and Codex plugins now share one plugin directory. A plugin may include skills, an MCP server, or both. An Apps SDK user interface is optional. This package does not add a custom UI, an `.app.json` file, or lifecycle hooks. Hooks and app references are not accepted in a public zip today.

The upload is a zip with `plugin.json` at the zip root, not a pull request. Build it with `python3 scripts/build-openai-plugin-zip.py`. Sources:

| File in git | File in the zip |
| --- | --- |
| `packaging/openai/plugin.json` | `plugin.json` (Agent Plugins schema plus `extensions.com.openai`) |
| `packaging/openai/mcp.json` | `mcp.json` (`type` `streamable-http`, OAuth dynamic registration, no client secret) |
| generated from `mcp.json` at the repo root | `.mcp.json` (URL only, for the Codex compatibility path) |
| `packaging/openai/.codex-plugin/plugin.json` | `.codex-plugin/plugin.json` |

Current OpenAI docs say `extensions.com.openai` replaces `.codex-plugin/plugin.json` when both exist. The overlay is still in the zip so an older Codex build that reads only the overlay gets the same name, version, skills path, and OAuth server. The two files carry the same listing text.

The published Agent Plugins MCP schema does not allow an `extensions` object on a server. OpenAI docs require `extensions["com.openai"].auth` in `mcp.json`. Validation checks the portable fields against the published schema after removing `extensions`, then checks the auth object separately. The auth object sets `client.mode` to `dcr` and does not contain `clientId` or `clientSecret`.

Domain verification, a reviewer account, a video, and country availability are portal steps. They are not files in this repo.

Codex CLI can also connect without the zip by using the HTTPS URL in [host-setup.md](host-setup.md).

## Anthropic

Two listings exist, and they are different artifacts.

### Claude Code plugin and directory

| File | Role |
| --- | --- |
| `.claude-plugin/plugin.json` | Plugin manifest, including directory fields `icon`, `supportUrl`, and `privacyPolicyUrl` |
| `.claude-plugin/marketplace.json` | Marketplace id `securin-skills`. Install id remains `securin-platform@securin-skills`. |
| `.mcp.json` | Same HTTPS server as `mcp.json`, `type` `http` |

`.mcp.json` no longer runs `npx`. The Anthropic directory blocks an unpinned `npx` launcher, and a pinned launcher is still held for a reviewer. Native HTTPS avoids that download. Claude Desktop users who need a stdio process keep using `securin-platform.mcpb`.

Directory submission is a portal flow at https://claude.ai/directory/manage for a plugin bundle and, separately, an MCP connector. `claude plugin validate` is the local syntax check. It was not available in the environment that prepared this change. JSON Schema checks cover the published Schema Store documents saved under `packaging/schemas/`.

### Claude Desktop MCPB

`mcpb/manifest.json` and `securin-platform.mcpb` are the Desktop bundle. The manifest version is `1.2.3`. The marketplace plugin version stays `0.1.0`. The bundle was already shipping at `1.2.2` with `license` set to `MIT`, which does not match the root `LICENSE`. `1.2.3` changes that field to `LicenseRef-Securin-Proprietary` and refreshes the description. It does not reset the bundle to `0.1.0`, because a lower version would look like an older Desktop release.

The bundle runs vendored `mcp-remote` `0.1.38` from inside the archive. It does not curl a script and it does not download an unpinned package at install time.
