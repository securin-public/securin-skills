

### Securin Platform — Skills & MCP Server

Bring your Securin data into your AI tools. 8 ready-made workflows + 40+ tools  
for vulnerability triage, exposure analysis, threat correlation, and remediation.



Also works with Claude Code, Windsurf, Gemini CLI, Codex CLI, and any MCP-compatible host.

---

## What you get

**8 skills** — guided workflows your agent runs end-to-end. No prompt engineering required.


| Skill                                | What you can ask                                                                                                                |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| `securin-cve-enrichment`             | *"Enrich CVE-2024-3400."* — CVSS, EPSS, KEV, exploitation history, threat actors.                                               |
| `securin-zero-day-exposure-analysis` | *"Am I exposed to any zero-days?"* — Open zero-day exposures in your environment with affected assets and remediation pointers. |
| `securin-threat-correlation`         | *"Am I affected by LockBit?"* — Maps a CVE, threat actor, or ransomware group to your environment with a clear verdict.         |
| `securin-asset-triage`               | *"Break down assets by criticality and workspace."* — Search, filter, and aggregate your asset inventory.                       |
| `securin-exposure-triage`            | *"Show open criticals breaching SLA."* — Ranked exposure lists or aggregated views.                                             |
| `securin-product-triage`             | *"What versions of Apache do we have?"* — Product catalog and component inventory.                                              |
| `securin-remediation-guidance`       | *"How do I fix exposure 12345?"* — Actionable fix plans with vendor advisories and ticket bodies.                               |
| `securin-tool-search`                | Fallback when no other skill fits — searches all 40+ MCP tools.                                                                 |


**40+ MCP tools** — direct API access for everything else. All tools are prefixed with `Securin__` (e.g. `Securin__searchVulnerabilityData`). Two meta-tools are unprefixed: `ping` (health check) and `search_tools` (find a tool by description).

---

## Install

Pick your AI Assistant:

###  Claude Desktop

1. **[Download `securin-platform.mcpb](https://github.com/securin-public/securin-skills/raw/main/securin-platform.mcpb)`** (or click the button at the top).
2. Open the file. Claude Desktop installs it automatically.
3. Sign in to Securin when the browser opens. Done.

> Skills are not loaded by Claude Desktop. For full skills + MCP, use Claude Code.

Manual setup (config file)

Edit `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

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

Save, then **fully quit and relaunch** Claude Desktop. Requires Node.js 18+.



---

###  Claude Code

The plugin marketplace installs both the MCP server and all 8 skills:

```bash
/plugin marketplace add securin-public/securin-skills
/plugin install securin-platform@securin-skills
```

To update later: `/plugin marketplace update securin-skills`.

Pre-configure for your team

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "securin-skills": {
      "source": { "source": "github", "repo": "securin-public/securin-skills" }
    }
  },
  "enabledPlugins": {
    "securin-platform@securin-skills": true
  }
}
```



---

###  VS Code (GitHub Copilot)

Click the **[Install in VS Code](https://insiders.vscode.dev/redirect/mcp/install?name=securin&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fmcp.securin.io%2Fmcp%22%7D)** badge above, or run:

```bash
code --add-mcp '{"name":"securin","type":"http","url":"https://mcp.securin.io/mcp"}'
```

For skills: clone this repo and point VS Code at `skills/` — see [docs/host-setup.md](docs/host-setup.md#vs-code-github-copilot).

---

###  Cursor

Click the **[Install in Cursor](cursor://anysphere.cursor-deeplink/mcp/install?name=securin&config=eyJ1cmwiOiJodHRwczovL21jcC5zZWN1cmluLmlvL21jcCJ9)** badge above. Skills: clone this repo and copy `skills/` into your project's `.agents/skills/`.

---

### Other hosts

Windsurf, Gemini CLI, Codex CLI, and any MCP-compatible host: see **[docs/host-setup.md](docs/host-setup.md)** for per-host instructions.

---

## Try it

Once installed, ask:

```
Enrich CVE-2024-3400.
Show me my open critical exposures breaching SLA.
Am I exposed to any zero-days?
Am I affected by LockBit?
Break down assets by criticality and workspace.
What threat actors target the CVEs in my environment?
How do I fix exposure 12345?
```

The first time you ask anything that touches your data, a browser opens to `auth.securin.io` for sign-in. After that, your session is cached and reused silently.

---

## Authentication

Two endpoints, same tools — pick by how you connect:


| Endpoint   | URL                              | Auth                | Use when                                                             |
| ---------- | -------------------------------- | ------------------- | -------------------------------------------------------------------- |
| `/mcp`     | `https://mcp.securin.io/mcp`     | OAuth (browser SSO) | You're a person using an AI tool — **default for everything above**. |
| `/api/mcp` | `https://mcp.securin.io/api/mcp` | Bearer token        | Headless: CI/CD, scripts, server-to-server.                          |


### OAuth (default)

No tokens to manage. Sign in once via your browser; the session caches under `~/.mcp-auth` and refreshes automatically. To switch identities: `rm -rf ~/.mcp-auth` and reconnect (in Claude Code, `/mcp` → select `securin` → **Clear credentials**).

### Bearer token (programmatic)

Use this only when a browser can't open.

1. Generate a `client_id` / `client_secret` in **[App Access](https://documentation.securin.io/s/platform-documentation/m/platform-documentation/a/apps-api-access)** on the Securin Platform.
2. Exchange for a token:
  ```bash
   curl -X POST https://platformapi.securin.io/account-service/api/v1/oauth2/token \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "client_id=<id>&client_secret=<secret>"
  ```
3. Connect to `/api/mcp` with `Authorization: Bearer <access_token>`. Tokens expire — use the returned `refresh_token` or re-call the endpoint.

Bearer-token configs per host

**Claude Code:**

```bash
claude mcp add securin --transport http \
  --url https://mcp.securin.io/api/mcp \
  --header "Authorization: Bearer <access-token>"
```

**Claude Desktop:**

```json
{
  "mcpServers": {
    "securin": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.securin.io/api/mcp",
               "--header", "Authorization:${AUTH_TOKEN}"],
      "env": { "AUTH_TOKEN": "Bearer <access-token>" }
    }
  }
}
```

**VS Code / Cursor / other HTTP-native hosts:**

```json
{
  "servers": {
    "securin": {
      "type": "http",
      "url": "https://mcp.securin.io/api/mcp",
      "headers": { "Authorization": "Bearer <access-token>" }
    }
  }
}
```

See the [full API reference](https://docs.securin.io/panther-services/apidef/apis/public/login/login/login).



### What the agent can see

Same accounts, workspaces, and permissions you have in the Securin Platform UI. Access control is enforced server-side. The MCP server is a transparent proxy — it does not store, cache, or log your credentials or API responses.

---

## Troubleshooting

Claude Desktop: nothing happens after I open the .mcpb

Make sure you have the latest Claude Desktop. If install fails silently, fully quit and relaunch Claude Desktop, then double-click the `.mcpb` again. On macOS you may also need to right-click → **Open** the first time to bypass Gatekeeper.



Browser sign-in never opens

`mcp-remote` (used under the hood) needs to spawn a browser. If your environment is headless, look in the host's logs for a manual sign-in URL. Corporate SSO or proxies can break the OAuth callback — ask IT to allow the callback URL printed in the console.



"Authentication successful, but server reconnection failed"

Clear cached tokens and reconnect. In Claude Code: `/mcp` → select `securin` → **Clear credentials**. In other hosts: `rm -rf ~/.mcp-auth` and restart the host.



Skills not loading (Claude Code, VS Code, etc.)

- **Claude Code:** confirm `/plugin` lists `securin-platform`. If not, re-run the install command.
- **Other hosts:** verify skill folders are in the host's expected directory (e.g. `.agents/skills/`) and each has a `SKILL.md`. Restart the host so it re-indexes.



"Which account should I use?"

Expected on first query if you have multiple Securin accounts. Pick one, or say *"use account 123"* to skip the prompt next time. The choice is remembered for the conversation.



Empty results on asset queries

Your account may use the composite asset data model. The skills auto-detect this; if results look wrong, tell the agent *"use the composite asset model"* explicitly.



MCP tools not showing up

- Verify Node.js 18+: `node --version`.
- **Claude Code:** run `/mcp` and confirm `securin` is listed.
- **Claude Desktop:** fully quit and relaunch — the tray icon restart isn't enough.
- On macOS, launch the host from a terminal so it inherits your shell PATH.



---

## Learn more

- [Securin Platform Learn](https://documentation.securin.io/s/platform-documentation/m/platform-documentation/a/latest-release)
- [Securin Platform API docs](https://docs.securin.io)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Agent Skills standard](https://agentskills.io/home)

## Support

- **Issues:** [securin-public/securin-skills/issues](https://github.com/securin-public/securin-skills/issues)
- **Product support:** [support@securin.io](mailto:support@securin.io)
- **Security disclosures:** see [SECURITY.md](SECURITY.md)

---

Copyright © Securin, Inc. Licensed under the terms in [LICENSE](LICENSE).