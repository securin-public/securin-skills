# Securin Platform Skills Plugin

Vulnerability management is not just a scanning problem. It's a prioritization problem: which of your millions of findings actually matter, which threats target your specific environment, what's worth remediating this sprint, and how do you explain the risk to leadership. The Securin Platform Skills Plugin packages Securin expertise and MCP-backed execution together so your AI agent can do real security work instead of giving generic vulnerability advice.

**[Install now](#install)** — Claude Code, Copilot, Cursor, Gemini CLI, Codex CLI, Windsurf, and any MCP-compatible host.

## One install, two layers of capability

### Securin skills: the brain

This plugin ships **8 curated Securin skills** that teach an agent how modern vulnerability management gets done. They provide workflows, decision trees, and guardrails for scenarios such as:

- **Investigate and enrich** with `securin-cve-enrichment` (Securin Core intelligence) and `securin-zero-day-exposure-analysis`
- **Triage your environment** with `securin-exposure-triage`, `securin-asset-triage`, and `securin-product-triage`
- **Correlate threats to your environment** with `securin-threat-correlation`
- **Find remediation guidance** with `securin-remediation-guidance`
- **Discover & do more with platform tools** with `securin-tool-search`

### Securin Platform MCP: the hands

The plugin wires in the **Securin Platform MCP Server**, which gives your agent **300+ structured tools across the Securin API surface**. That's the execution layer for searching assets, filtering exposures, aggregating by severity or workspace, querying threat intelligence, building deep links, and driving real vulnerability-management workflows.

## Why this plugin is different

This is not a prompt pack. It is a packaged Securin capability layer:

- **Skills** teach the agent when to use which Securin workflow and what to avoid.
- **MCP tools** let the agent act on live Securin Platform data.
- **Brand + visual communication** is enforced by default — outputs ship as Securin-branded reports, charts, and infographics.
- **Multi-host support** — the MCP server works with every MCP-compatible host, and the skills follow the open [Agent Skills](https://agentskills.io/home) standard supported by Claude Code, Codex CLI, GitHub Copilot, Gemini CLI, Cursor, Windsurf, and others.

## What you get

| Component | What it adds | Examples |
| --- | --- | --- |
| **Securin skills** | Securin expertise, workflows, and guardrails | CVE enrichment, exposure triage, threat correlation, zero-day analysis, remediation guidance |
| **Securin Platform MCP** | Live Securin Platform tooling | Search assets/exposures/components, aggregate and group-by, field discovery, deep-link creation, account access checks |
| **Brand & visual output** | Securin-branded reports and charts by default | Purple monotone palette, Lato typography, gradient charts, one-page CVE briefings, severity-distribution bar charts |

## Skills reference

The 8 skills in this plugin, when each one activates, and what it produces.

| Skill | When to use it | What you get |
| --- | --- | --- |
| **`securin-cve-enrichment`** | *"Enrich CVE-XXXX"* · *"Tell me about this CVE"* · *"What's the CISA KEV status?"* · *"Is this exploited in the wild?"* | A global intelligence briefing on the CVE — CVSS, EPSS, Securin Risk Index, KEV flag, exploitation history, threat-actor attribution, contributing factors, and a Securin-branded one-pager. No environment data. |
| **`securin-zero-day-exposure-analysis`** | *"Am I exposed to any zero-days?"* · *"Am I affected by [named zero-day like Regresshell, Citrix Bleed]?"* · *"Zero-day risk report for my account."* | Zero-day exposures in your environment (`vulnerabilities.tags = 'Zero Day'`), correlated CVEs, affected-asset pivot, KEV overlap, severity distribution chart, and remediation pointers. |
| **`securin-threat-correlation`** | *"Am I affected by CVE-X?"* · *"Does LockBit target my environment?"* · *"Are we vulnerable to [ransomware / threat actor]?"* · *"What threats target the CVEs in my environment?"* | A threat-to-environment correlation report — matched CVEs, affected assets with criticality and reachability, severity breakdown, and a clear *affected / not affected* verdict with deep links. |
| **`securin-asset-triage`** | *"Find assets where…"* · *"Break down assets by criticality / workspace / cloud provider"* · *"Which assets are exposed-to-internet?"* · *"Asset distribution by business unit."* | A filtered or aggregated view of your asset inventory with auto-detected composite-vs-source data model, a monotone bar chart, and per-bucket deep links. |
| **`securin-exposure-triage`** | *"Show open critical exposures"* · *"Exposures breaching SLA"* · *"Break down exposures by severity / workspace / status"* · *"Exposure volume over time."* | A ranked exposure list or aggregated view using the canonical `exposures.scores.score` sort, with severity-distribution chart, SLA column, and deep links back into the platform. |
| **`securin-product-triage`** | *"Which components run `log4j < 2.17`?"* · *"List products by vendor"* · *"Software inventory matching…"* · *"Is PAN-OS X in the catalog?"* | Product-catalog or component-inventory results (picks the right tool — `getProducts` vs `searchComponentData`), grouped by vendor/version with a Securin-branded chart. |
| **`securin-remediation-guidance`** | *"How do I fix exposure `exp-abc123`?"* · *"Patch guidance for CVE-XXX"* · *"Workaround for this vuln"* · *"Generate a ticket body for this exposure."* | An actionable fix plan that reads scanner-native remediation fields first (Qualys / Tenable / WIZ / Rapid7 / CrowdStrike / Snyk) via `getConfiguredIntegrations`, then offers optional vendor-advisory web search and a draft ticket body. |
| **`securin-tool-search`** | *"Is there a Securin tool for managing tags?"* · *"What MCP tools can I use for user management?"* · Any ask that doesn't fit the other 7 skills. | A BM25-ranked list of the top MCP tools matching your query (via `search_tools`), with one-line descriptions and a proposal for the next call. Fallback discovery for the long tail. |

All skills enforce four cross-cutting invariants: account-id preflight, deep links back into the platform, scope discipline (hand off to a sibling skill when the ask fits), and Securin-branded visual output.

## Install

### Prerequisites

- A Securin Platform account you can sign in to at <https://auth.securin.io>
- **Node.js 18+** on your PATH (used by `npx` for hosts that need the `mcp-remote` bridge)

No API token or bearer secret is required — authentication happens through the Securin identity provider automatically. A browser window opens on first use; future sessions reuse the stored credential.

### What you're installing

| Component | Delivery | Supported hosts |
| --- | --- | --- |
| **Securin MCP tools** (300+ API tools) | MCP server at `https://mcp.securin.io/mcp` | Every MCP-compatible host |
| **Securin skills** (8 workflows) | Standard `SKILL.md` files in `skills/` | Claude Code, Cowork, Codex CLI, GitHub Copilot, Gemini CLI, Cursor, Windsurf, and any host supporting the [Agent Skills](https://agentskills.io/home) standard |

---

### Claude Code / Claude Cowork

The plugin marketplace installs both the MCP server and all 8 skills automatically:

```bash
# Add the marketplace (first time only)
/plugin marketplace add securin-public/securin-skills

# Install the plugin
/plugin install securin-platform@securin-skills

# Update later
/plugin marketplace update securin-skills
```

The MCP configuration ships inside the plugin — no env vars, no token paste.

**Team distribution** — pre-configure the plugin for everyone by adding to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "securin-skills": {
      "source": {
        "source": "github",
        "repo": "securin-public/securin-skills"
      }
    }
  },
  "enabledPlugins": {
    "securin-platform@securin-skills": true
  }
}
```

---

### VS Code (GitHub Copilot)

**MCP tools** — add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "securin": {
      "type": "http",
      "url": "https://mcp.securin.io/mcp"
    }
  }
}
```

**Skills** — clone this repo and add the path to your VS Code settings (`settings.json`):

```json
{
  "chat.agentSkillsLocations": [
    { "path": "/path/to/securin-skills/skills" }
  ]
}
```

Or copy the skill subdirectories into your project's `.agents/skills/` for automatic discovery.

---

### Cursor

**MCP tools** — add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "securin": {
      "url": "https://mcp.securin.io/mcp"
    }
  }
}
```

**Skills** — clone this repo and copy the skill subdirectories from `skills/` into your project's `.agents/skills/` directory for automatic discovery.

---

### Windsurf

**MCP tools** — add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "securin": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.securin.io/mcp"]
    }
  }
}
```

**Skills** — clone this repo and copy the skill subdirectories from `skills/` into your project's `.agents/skills/` directory.

---

### Gemini CLI

**MCP tools** — add to `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "securin": {
      "url": "https://mcp.securin.io/mcp"
    }
  }
}
```

**Skills** — clone this repo and copy the skill subdirectories from `skills/` into `.gemini/skills/` or your project's `.agents/skills/` directory.

---

### OpenAI Codex CLI

**MCP tools** — add to `~/.codex/config.toml`:

```toml
[mcp_servers.securin]
url = "https://mcp.securin.io/mcp"
```

**Skills** — clone this repo and copy the skill subdirectories from `skills/` into your project's `.agents/skills/` directory.

---

### Claude Desktop (MCP tools only)

Claude Desktop does not load agent skills — only the MCP server connects.

| OS | Config file |
|---|---|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

```json
{
  "mcpServers": {
    "securin": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.securin.io/mcp"
      ]
    }
  }
}
```

Save and **fully quit and relaunch** Claude Desktop (a tray restart isn't enough).

---

### Any other MCP-compatible host

The Securin MCP endpoint (`https://mcp.securin.io/mcp`) uses Streamable HTTP transport. Hosts that support HTTP-based MCP can connect directly via the URL. Hosts that only support stdio transport can use the `npx mcp-remote` bridge:

```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote", "https://mcp.securin.io/mcp"]
}
```

For skills, clone this repo and point the host's skill loader at the `skills/` directory — each subdirectory contains a standard `SKILL.md` file with YAML frontmatter (`name`, `description`) and markdown instructions, following the [Agent Skills](https://openai.com/index/agentic-ai-foundation/) open standard.

## Verify the installation

After install, try three quick checks.

### 1. Verify the skills layer

Ask:

> What can you do with Securin?

You should get a response referencing specific Securin workflows (CVE enrichment, exposure triage, threat correlation, etc.) — not a generic "I can search your data" answer. This works on any host that loaded the skills.

### 2. Verify the Securin MCP

Ask:

> List my Securin accounts.

The first time, your browser opens to `auth.securin.io` to sign in. After that, you should see a real tool-backed response (calling `getUserProfile`) with the accounts your Securin identity has access to.

### 3. Verify a branded workflow

Ask:

> Enrich CVE-2024-3400.

You should get a full one-page CVE briefing — CVSS, EPSS, Securin Risk Index, CISA KEV, contributing factors, threat actors — in the Securin brand palette.

## Authentication

The Securin MCP Server uses the Securin identity provider (`auth.securin.io`) end-to-end. There are no bearer tokens to generate, paste, or rotate. The MCP client opens a browser on first use; the resulting credential is cached by `mcp-remote` under your user directory and reused silently.

### What the MCP can see

The Securin account(s) and workspaces visible to your signed-in identity determine what the agent can access. If you sign in as a user with *Viewer* role on three accounts, the agent can query all three. The first time you run an account-scoped query, the plugin asks you to pick.

### Switching identities

Clear the cached `mcp-remote` credential to force a re-login:

```bash
# macOS / Linux
rm -rf ~/.mcp-auth

# Windows (PowerShell)
Remove-Item -Recurse -Force $HOME\.mcp-auth
```

Then restart your host and run a Securin query — the browser will prompt again.

## Prompts to try

Once installed, try prompts like these:

- `Enrich CVE-2024-3400.`
- `Show me my open critical exposures breaching SLA.`
- `Am I exposed to any zero-days?`
- `Am I affected by LockBit?`
- `Break down assets by criticality and workspace.`
- `What threat actors target the CVEs in my environment?`
- `How do I fix exposure <exposure-id>?`
- `Generate a ticket body for the top five critical exposures.`
- `Is there a Securin tool for managing tags?`

## Branding

Outputs are Securin-branded by default — purple monotone palette, light theme, Lato typography, Securin wordmark. You can override per-conversation:

```
> Switch to a dark theme.
> Use our brand colors instead — primary #005B99, accent #FF6B00.
> Drop the logo and use minimal styling.
```

Drop your approved Securin logo files into `skills/_shared/securin_logos/` (filenames `Securin_logo_purple.svg/.png`, `Securin_logo_white.svg/.png`) and every branded output will pick them up automatically. To change the default permanently, edit `skills/_shared/brand.md`.

## Repository layout

If you are exploring or customizing the plugin source, the key pieces are:

- `.claude-plugin/marketplace.json` — marketplace catalog (enables `/plugin marketplace add`)
- `.claude-plugin/plugin.json` — plugin manifest
- `.mcp.json` — Securin Platform MCP server configuration (runs `mcp-remote` against `https://mcp.securin.io/mcp`)
- `skills/` — the 8 Securin skill definitions
- `skills/_shared/` — shared invariants (account preflight, deep links, FQL grammar, sorting rules, brand guidelines)
- `skills/_shared/securin_logos/` — Securin wordmark assets for branded outputs
- `README.md` — this document
- `SECURITY.md` — vulnerability-disclosure policy
- `LICENSE` — usage terms

## Troubleshooting

### The agent is not using Securin skills

- **Claude Code / Cowork:** Make sure the plugin installed successfully (`/plugin` lists `securin-platform`).
- **Other hosts:** Verify the skills were copied into the correct directory (`.agents/skills/`, `.gemini/skills/`, etc.) and each subdirectory contains a `SKILL.md` file.
- Reload or restart your host so it re-indexes skills and MCP configuration.

### MCP tools are not showing up

- Verify Node.js 18+ is installed and `npx` works: `node --version` and `npx --version`.
- **Claude Code / Cowork:** Run `/mcp` and confirm `securin` is listed.
- **Claude Desktop:** Fully quit and relaunch — a tray restart isn't enough.
- **Other hosts:** Check the host's MCP server logs for connection errors. Verify the config file path and JSON/TOML format for your specific host.
- On macOS, if the host can't find `npx`, launch it from a terminal so it inherits your shell PATH.

### The sign-in browser window never opens

- `mcp-remote` needs to be able to spawn a browser. If you're on a headless system or the browser launcher is blocked, check the `mcp-remote` logs in your host's MCP output for a manual sign-in URL you can open by hand.
- Corporate SSO / proxy can break the OAuth redirect. Ask your IT team to allow the callback URL that `mcp-remote` prints in the console.

### "I have access to multiple accounts — which should I use?"

Expected behavior on first query. Pick one, or say *"use account 123"* at the start of the conversation to skip the prompt. The plugin remembers the choice for the rest of the conversation.

### I need to sign in as a different user

Clear the cached credential:

```bash
rm -rf ~/.mcp-auth        # macOS / Linux
Remove-Item -Recurse -Force $HOME\.mcp-auth    # Windows PowerShell
```

Restart your host and trigger any Securin query; the browser will open again.

### Empty results on asset queries

Your account may use the composite-data model. The plugin auto-detects this; if results still look wrong, tell it *"use the composite asset model"* explicitly.

### No chart appears in the response

Your host may not support file artifacts. The plugin falls back to an ASCII bar chart plus the underlying data table.

## Learn more

- [Securin Platform documentation](https://docs.securin.io)
- [Securin Platform MCP Server](https://github.com/securin-inc/securin-mcp)
- [Model Context Protocol specification](https://modelcontextprotocol.io)
- [Agent Skills open standard](https://openai.com/index/agentic-ai-foundation/) (Agentic AI Foundation / Linux Foundation)

## Feedback & support

- **Report issues:** https://github.com/securin-public/securin-skills/issues
- **Product support:** support@securin.io
- **Security disclosures:** see [SECURITY.md](SECURITY.md)

## Contribution

Contributions are welcome. File issues or pull requests against [securin-public/securin-skills](https://github.com/securin-public/securin-skills). For the upstream MCP server source, see [securin-inc/securin-mcp](https://github.com/securin-inc/securin-mcp).

---

Copyright © Securin, Inc. Licensed under the terms in [LICENSE](LICENSE).
