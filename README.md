<p align="center">
  <img src="skills/_shared/securin_logos/Securin_logo_purple.png" alt="Securin" height="48">
</p>

<h3 align="center">Securin Platform — Skills & MCP Server</h3>

<p align="center">
  8 agent skills + 40+ MCP tools that give your AI agent access to the Securin Platform.<br>
  Works with Claude Code, VS Code, Cursor, Windsurf, Gemini CLI, Codex CLI, and any MCP-compatible host.
</p>

<p align="center">
  <a href="https://insiders.vscode.dev/redirect/mcp/install?name=securin&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fmcp.securin.io%2Fmcp%22%7D"><img src="https://img.shields.io/badge/VS_Code-Install_MCP_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white" alt="Install in VS Code"></a>
  <a href="https://insiders.vscode.dev/redirect/mcp/install?name=securin&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fmcp.securin.io%2Fmcp%22%7D&quality=insiders"><img src="https://img.shields.io/badge/VS_Code_Insiders-Install_MCP_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white" alt="Install in VS Code Insiders"></a>
  <a href="cursor://anysphere.cursor-deeplink/mcp/install?name=securin&config=eyJ1cmwiOiJodHRwczovL21jcC5zZWN1cmluLmlvL21jcCJ9"><img src="https://img.shields.io/badge/Cursor-Install_MCP_Server-000000?style=flat-square&logo=cursor&logoColor=white" alt="Install in Cursor"></a>
</p>

---

## MCP Server

The Securin Platform MCP Server gives your AI agent 40+ tools across the Securin API surface — search assets, filter exposures, aggregate by severity, query threat intelligence, build deep links, and more. The server uses Streamable HTTP transport at `https://mcp.securin.io/mcp`.

All API tools are prefixed with `Securin__` (e.g. `Securin__searchVulnerabilityData`, `Securin__aggregateCompositeAssetData`, `Securin__aggregateWeaknessData`). Two meta-tools are unprefixed:

- `ping` — health check
- `search_tools` — natural-language search over all available tools

**Finding the right tool** — with 40+ tools, use `search_tools` instead of scanning the full list:

```
search_tools(query="jira integrations", top_k=5)
```

Tips: use specific nouns (`connector credentials` > `get credentials`), describe what you want to do (`import scan results from Jira` > `import`), or call a tool directly if you already know its name.

## Skills

8 workflows that teach your agent how to do vulnerability management with Securin. Skills follow the open [Agent Skills](https://agentskills.io/home) standard.

| Skill | What it does |
| --- | --- |
| `securin-cve-enrichment` | Global CVE intelligence briefing — CVSS, EPSS, Securin Risk Index, CISA KEV, exploitation history, threat-actor attribution. No environment data. |
| `securin-zero-day-exposure-analysis` | Zero-day exposures in your environment, correlated CVEs, affected assets, severity distribution, remediation pointers. |
| `securin-threat-correlation` | Answers "am I affected by X?" — maps a CVE, threat actor, or ransomware group to your actual environment and gives a clear verdict. |
| `securin-asset-triage` | Ad-hoc asset search, filter, and aggregation. Break down by criticality, workspace, cloud provider, etc. |
| `securin-exposure-triage` | Ranked exposure lists or aggregated views — open criticals, SLA breaches, severity distribution, volume over time. |
| `securin-product-triage` | Product catalog and component inventory search. Find specific versions, group by vendor, check what's deployed. |
| `securin-remediation-guidance` | Actionable fix plans — reads scanner-native remediation fields, offers vendor advisory lookup, drafts ticket bodies. |
| `securin-tool-search` | Fallback discovery for the long tail. BM25 search over all MCP tools when the other 7 skills don't fit. |

## Endpoints & Authentication

The MCP server exposes two endpoints. Both serve the same tools — pick based on how you're connecting:

| Endpoint | URL | Auth | When to use |
|---|---|---|---|
| `/mcp` | `https://mcp.securin.io/mcp` | OAuth (SSO login) | **Interactive use.** You're a human using Claude Code, VS Code, Cursor, Claude Desktop, etc. A browser opens for SSO login — no tokens to manage. |
| `/api/mcp` | `https://mcp.securin.io/api/mcp` | Bearer token | **Programmatic use.** CI/CD pipelines, scripts, custom agents, server-to-server — anywhere a browser can't open. |

Most users should use `/mcp`. Use `/api/mcp` only when you need headless, token-based access.

### OAuth (interactive — `/mcp`)

No tokens to generate or rotate. Your MCP client opens a browser to `auth.securin.io` on first use. Log in with your existing Securin credentials (same as the web app), and the token is returned to the client automatically. Token refresh is handled automatically — you don't need to re-login unless your session has been idle for an extended period.

The credential is cached under `~/.mcp-auth` and reused silently on subsequent sessions.

### Bearer token (programmatic — `/api/mcp`)

For headless environments, obtain a bearer token and pass it in the `Authorization` header:

1. Generate a `client_id` and `client_secret` via **App Access** in the Securin Platform
2. Exchange them for an access token:

```bash
curl -X POST https://platformapi.securin.io/account-service/api/v1/oauth2/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=<your-client-id>&client_secret=<your-client-secret>"
```

Response:

```json
{
  "access_token": "eyJhbG...",
  "token_type": "Bearer",
  "expires_in": 300,
  "refresh_token": "eyJhbG...",
  "refresh_expires_in": 1800
}
```

3. Pass the `access_token` in the `Authorization` header when connecting to `/api/mcp`:

```
Authorization: Bearer <access_token>
```

The token expires after the `expires_in` period — use the `refresh_token` to obtain a new one, or call the token endpoint again.

If the token is missing or invalid, you receive a `401 Unauthorized`.

See the [full API reference](https://docs.securin.io/panther-services/apidef/apis/public/login/login/login) for details.

### What the MCP can see

Your Securin identity determines what the agent can access — same accounts and workspaces you'd see in the platform UI. Access control is enforced by the Securin Platform API based on your account's roles and permissions.

### Data safety

The MCP server is a transparent proxy. It does not store, cache, or log your credentials or API responses. Your token is forwarded to the Securin Platform API and discarded after the request.

### Switching identities

Clear the cached credential and restart your host:

```bash
# macOS / Linux
rm -rf ~/.mcp-auth

# Windows (PowerShell)
Remove-Item -Recurse -Force $HOME\.mcp-auth
```

In Claude Code, you can also run `/mcp`, select the `securin` server, and choose **Clear credentials**.

## Install

### Prerequisites

- A Securin Platform account ([platform.securin.io](https://platform.securin.io))
- **Node.js 18+** on your PATH (needed by Claude Code, Claude Desktop, Windsurf, and other stdio-only hosts that use the `mcp-remote` bridge)

---

### Claude Code / Claude Cowork

The plugin marketplace installs both the MCP server and all 8 skills:

```bash
# Add the marketplace (first time only)
/plugin marketplace add securin-public/securin-skills

# Install the plugin
/plugin install securin-platform@securin-skills

# Update later
/plugin marketplace update securin-skills
```

**Team distribution** — pre-configure for everyone via your project's `.claude/settings.json`:

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
      "args": ["-y", "mcp-remote", "https://mcp.securin.io/mcp"]
    }
  }
}
```

Save, then **fully quit and relaunch** Claude Desktop (a tray restart isn't enough).

---

### VS Code, Cursor, Windsurf, Gemini CLI, Codex CLI, and others

See **[docs/host-setup.md](docs/host-setup.md)** for per-host setup instructions, including one-click install badges for VS Code and Cursor.

---

### Using `/api/mcp` (bearer token)

For CI/CD pipelines, custom agents, or any headless environment where a browser can't open, use the `/api/mcp` endpoint with a bearer token. The configs are the same as above — swap the URL to `https://mcp.securin.io/api/mcp` and add an `Authorization` header.

See [Bearer token](#bearer-token-programmatic--apimcp) above for how to obtain a token.

**Claude Code** — add via CLI:

```bash
claude mcp add securin \
  --transport http \
  --url https://mcp.securin.io/api/mcp \
  --header "Authorization: Bearer <your-access-token>"
```

**Claude Desktop** — add to your config file:

```json
{
  "mcpServers": {
    "securin": {
      "command": "npx",
      "args": [
        "-y", "mcp-remote",
        "https://mcp.securin.io/api/mcp",
        "--header", "Authorization:${AUTH_TOKEN}"
      ],
      "env": {
        "AUTH_TOKEN": "Bearer <your-access-token>"
      }
    }
  }
}
```

**VS Code / Cursor / other HTTP-native hosts** — same pattern, add a `headers` field:

```json
{
  "servers": {
    "securin": {
      "type": "http",
      "url": "https://mcp.securin.io/api/mcp",
      "headers": {
        "Authorization": "Bearer <your-access-token>"
      }
    }
  }
}
```

## Verify the installation

After install, try three checks:

**1. Skills loaded?** — Ask: *"What can you do with Securin?"* You should get a response referencing specific workflows (CVE enrichment, exposure triage, etc.), not a generic answer.

**2. MCP connected?** — Ask: *"List my Securin accounts."* The first time, a browser opens to `auth.securin.io` for sign-in. After that, you'll see a real response with your accounts.

**3. End-to-end?** — Ask: *"Enrich CVE-2024-3400."* You should get a full CVE briefing with CVSS, EPSS, risk index, KEV status, and threat actor attribution.

## Prompts to try

```
Enrich CVE-2024-3400.
Show me my open critical exposures breaching SLA.
Am I exposed to any zero-days?
Am I affected by LockBit?
Break down assets by criticality and workspace.
What threat actors target the CVEs in my environment?
How do I fix exposure <exposure-id>?
```

## Troubleshooting

### Skills not loading

- **Claude Code:** check the plugin installed — `/plugin` should list `securin-platform`.
- **Other hosts:** verify skill folders were copied to the right directory (`.agents/skills/`, `.gemini/skills/`, etc.) and each has a `SKILL.md` file.
- Restart your host so it re-indexes.

### MCP tools not showing up

- Verify Node.js 18+: `node --version` and `npx --version`.
- **Claude Code:** run `/mcp` and confirm `securin` is listed.
- **Claude Desktop:** fully quit and relaunch — tray restart isn't enough.
- On macOS, launch the host from a terminal so it inherits your shell PATH.

### Browser sign-in never opens

- `mcp-remote` needs to spawn a browser. On headless systems, check `mcp-remote` logs for a manual sign-in URL.
- Corporate SSO / proxy can break the OAuth redirect — ask IT to allow the callback URL printed in the console.

### "Which account should I use?"

Expected on first query if you have multiple Securin accounts. Pick one, or say *"use account 123"* to skip the prompt. The choice persists for the conversation.

### "Authentication successful, but server reconnection failed"

Clear your MCP auth tokens and reconnect. In Claude Code, run `/mcp`, select the `securin` server, and choose **Clear credentials**, then re-authenticate. For other hosts, delete `~/.mcp-auth` and restart.

### Empty results on asset queries

Your account may use the composite data model. The plugin auto-detects this; if results look wrong, tell the agent *"use the composite asset model"* explicitly.

## Learn more

- [Securin Platform docs](https://docs.securin.io)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Agent Skills standard](https://agentskills.io/home)

## Contributing

Contributions welcome — file issues or pull requests against [securin-public/securin-skills](https://github.com/securin-public/securin-skills).

## Support

- **Issues:** [securin-public/securin-skills/issues](https://github.com/securin-public/securin-skills/issues)
- **Product support:** support@securin.io
- **Security disclosures:** see [SECURITY.md](SECURITY.md)

---

Copyright &copy; Securin, Inc. Licensed under the terms in [LICENSE](LICENSE).
