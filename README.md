<!-- prettier-ignore-start -->
<p align="center">
  <img src="skills/_shared/securin_logos/Securin_logo_rounded.png" alt="Securin" height="48">
</p>

<h3 align="center">Securin Platform — Skills & MCP Server</h3>

<p align="center">
  Bring your Securin data into your AI tools. 6 ready-made workflows + 50+ MCP tools<br>
  for vulnerability triage, exposure analysis, threat correlation, and remediation.
</p>

<p align="center">
  <a href="https://github.com/securin-public/securin-skills/raw/main/securin-platform.mcpb"><img src="https://img.shields.io/badge/Claude_Desktop-Download_.mcpb-D97757?style=flat-square&logo=anthropic&logoColor=white" alt="Install in Claude Desktop"></a>
</p>

<p align="center">
  <sub>Also works with Claude Code, Windsurf, Gemini CLI, Codex CLI, and any MCP-compatible host.</sub>
</p>
<!-- prettier-ignore-end -->

---

## What you get

**6 skills** — guided workflows your agent runs end-to-end. No prompt engineering required.

| Skill | What you can ask |
| --- | --- |
| `securin-cve-enrichment` | *"Enrich CVE-2024-3400."* — CVSS, EPSS, KEV, exploitation history, threat actors. |
| `securin-zero-day-exposure-analysis` | *"Am I exposed to any zero-days?"* — Open zero-day exposures in your environment with affected assets and remediation pointers. |
| `securin-threat-correlation` | *"Am I affected by LockBit?"* — Maps a CVE, threat actor, or ransomware group to your environment with a clear verdict. |
| `securin-asset-triage` | *"Break down assets by criticality and workspace."* — Search, filter, and aggregate your asset inventory. |
| `securin-exposure-triage` | *"Show open criticals breaching SLA."* — Ranked exposure lists or aggregated views. |
| `securin-remediation-guidance` | *"How do I fix exposure 12345?"* — Actionable fix plans with vendor advisories and ticket bodies. |

When no skill matches the ask, fall back to the built-in `Securin__search_tools` MCP meta-tool to look up the right tool by description.

**50+ MCP tools** — direct API access for everything else. All tools are prefixed with `Securin__` (e.g. `Securin__searchVulnerabilityData`). Two meta-tools are unprefixed: `ping` (health check) and `search_tools` (find a tool by description).

---

## Install

Pick your AI tool:

<!-- prettier-ignore -->
### <img src="https://cdn.simpleicons.org/claude/D97757" height="16" alt="Claude"> Claude Desktop/Cowork

1. **[Download `securin-platform.mcpb`](https://github.com/securin-public/securin-skills/raw/main/securin-platform.mcpb)** (or click the button at the top).
2. Open the file. Claude Desktop installs it automatically.
3. Sign in to Securin when the browser opens. Done.

> Skills are not loaded by Claude Desktop. For full skills + MCP, use Claude Code.

<!-- prettier-ignore-start -->
<details>
<summary>Manual setup (config file)</summary>

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

</details>
<!-- prettier-ignore-end -->

**Claude Teams & Enterprise — add via UI**

Organization owners can add the connector directly from [claude.ai](https://claude.ai) — no file editing or restart needed:

1. Go to **Organization Settings → Connectors → Add → Custom → Web**
2. Enter name: `Securin Platform`
3. Enter URL: `https://mcp.securin.io/mcp`
4. Click **Add**
<img width="959" height="399" alt="1" src="https://github.com/user-attachments/assets/0f3e45fd-5912-416e-ad45-1a31726fc851" />

<img width="959" height="398" alt="2" src="https://github.com/user-attachments/assets/ee85cba1-0159-4f55-863e-e56e218d73d0" />

Team members then go to **Customize → Connectors**, find **Securin Platform**, and click **Connect** — the browser redirects to Securin for sign-in automatically.

<img width="958" height="394" alt="3" src="https://github.com/user-attachments/assets/e256701d-e54d-446d-9159-7be56e6d11f5" />

See the [Claude docs on custom connectors](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp) for more detail.

**Claude Cowork — Skills Plugin**

After adding the MCP connector, each team member can also install the Securin Skills Plugin to access the 6 guided workflows directly within Claude Cowork:

1. In Claude Cowork, open **Customize** from the left sidebar.
2. Under **Personal Plugins**, click the **+** icon and select **Create Plugin**.
3. Choose **Add Marketplace**, enter the skills repository URL:
   ```
   https://github.com/securin-public/securin-skills
   ```
   Then click **Sync**.
4. The **Securin Platform** plugin will appear under **Personal** in the plugins directory.
5. Click **+** next to **Securin Platform** to activate it.
6. The skills are now active — start asking questions in any conversation.

---

<!-- prettier-ignore -->
### <img src="https://cdn.simpleicons.org/claude/D97757" height="16" alt="Claude"> Claude Code

The plugin marketplace installs both the MCP server and all 6 skills:

```bash
/plugin marketplace add securin-public/securin-skills
/plugin install securin-platform@securin-skills
```

To update later: `/plugin marketplace update securin-skills`.

<!-- prettier-ignore-start -->
<details>
<summary>Pre-configure for your team</summary>

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

</details>
<!-- prettier-ignore-end -->

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

| Endpoint | URL | Auth | Use when |
|---|---|---|---|
| `/mcp` | `https://mcp.securin.io/mcp` | OAuth (browser SSO) | You're a person using an AI tool — **default for everything above**. |
| `/api/mcp` | `https://mcp.securin.io/api/mcp` | Bearer token | Headless: CI/CD, scripts, server-to-server. |

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

<!-- prettier-ignore-start -->
<details>
<summary>Bearer-token configs per host</summary>

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

**Other HTTP-native hosts:**
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

</details>
<!-- prettier-ignore-end -->

### What the agent can see

Same accounts, workspaces, and permissions you have in the Securin Platform UI. Access control is enforced server-side. The MCP server is a transparent proxy — it does not store, cache, or log your credentials or API responses.

---

## Troubleshooting

<!-- prettier-ignore-start -->
<details>
<summary>Claude Desktop: nothing happens after I open the .mcpb</summary>

Make sure you have the latest Claude Desktop. If install fails silently, fully quit and relaunch Claude Desktop, then double-click the `.mcpb` again. On macOS you may also need to right-click → **Open** the first time to bypass Gatekeeper.

</details>

<details>
<summary>Browser sign-in never opens</summary>

`mcp-remote` (used under the hood) needs to spawn a browser. If your environment is headless, look in the host's logs for a manual sign-in URL. Corporate SSO or proxies can break the OAuth callback — ask IT to allow the callback URL printed in the console.

</details>

<details>
<summary><code>Error: listen EADDRINUSE: address already in use 127.0.0.1:&lt;port&gt;</code></summary>

This is a **local port collision** on your machine — not a server issue. `mcp-remote` opens a tiny HTTP listener on `127.0.0.1:<random-port>` to receive the OAuth redirect after sign-in. If a previous `mcp-remote` process didn't shut down cleanly (most common cause), the port is still held and the new connection can't bind.

**Fix it:**

```bash
# macOS / Linux — find what's holding the port (replace 37040 with your port)
lsof -i :37040

# Kill any orphaned mcp-remote / node processes
pkill -f mcp-remote

# Fully quit and reopen Claude — quit the app, don't just close the window
```

```powershell
# Windows (PowerShell) — find and kill the process holding the port
Get-NetTCPConnection -LocalPort 37040 | Select-Object OwningProcess
Stop-Process -Id <pid-from-above> -Force

# Then fully quit and reopen Claude
```

If it recurs, clear `mcp-remote`'s OAuth cache too — a stale state file can make the client retry and collide with itself:

```bash
# macOS / Linux
rm -rf ~/.mcp-auth

# macOS (alternative location used by some versions)
rm -rf "$HOME/Library/Application Support/mcp-remote"

# Windows (PowerShell)
Remove-Item -Recurse -Force $HOME\.mcp-auth
```

Also worth checking: are two AI hosts (e.g. Claude Desktop + Claude Code) racing to launch the same `mcp-remote` instance at the same time? Stagger their startup or pick one host per machine.

</details>

<details>
<summary>"Authentication successful, but server reconnection failed"</summary>

Clear cached tokens and reconnect. In Claude Code: `/mcp` → select `securin` → **Clear credentials**. In other hosts: `rm -rf ~/.mcp-auth` and restart the host.

</details>

<details>
<summary>Skills not loading</summary>

- **Claude Code:** confirm `/plugin` lists `securin-platform`. If not, re-run the install command.
- **Other hosts:** verify skill folders are in the host's expected directory (e.g. `.agents/skills/`) and each has a `SKILL.md`. Restart the host so it re-indexes.

</details>

<details>
<summary>"Which account should I use?"</summary>

Expected on first query if you have multiple Securin accounts. Pick one, or say *"use account 123"* to skip the prompt next time. The choice is remembered for the conversation.

</details>

<details>
<summary>Empty results on asset queries</summary>

Your account may use the composite asset data model. The skills auto-detect this; if results look wrong, tell the agent *"use the composite asset model"* explicitly.

</details>

<details>
<summary>MCP tools not showing up</summary>

- Verify Node.js 18+: `node --version`.
- **Claude Code:** run `/mcp` and confirm `securin` is listed.
- **Claude Desktop:** fully quit and relaunch — the tray icon restart isn't enough.
- On macOS, launch the host from a terminal so it inherits your shell PATH.

</details>
<!-- prettier-ignore-end -->

---

## Contributing

Contributions are welcome — whether you're improving an existing skill, fixing a bug, or adding a new workflow.

### Reporting issues

Open an issue at [securin-public/securin-skills/issues](https://github.com/securin-public/securin-skills/issues) with a clear description and steps to reproduce.

### Improving an existing skill

Each skill lives in `skills/<skill-name>/SKILL.md`. To improve one:

1. Fork the repository and create a feature branch.
2. Edit `SKILL.md` — instructions are plain Markdown. Preserve the frontmatter block (`name`, `description`) and the standard section headings (`## Purpose`, `## When to use`, `## Steps`, `## Output format`).
3. Shared reference material (FQL grammar, deep links, brand guidelines, etc.) lives in `skills/_shared/` and is mirrored into each skill's `references/_shared/`. Update it there if a change applies across all skills.
4. Open a pull request with a clear description of what changed and why.

### Adding a new skill

1. Copy an existing skill directory as a starting point:
   ```bash
   cp -r skills/securin-cve-enrichment skills/securin-your-skill-name
   ```
2. Update `SKILL.md`:
   - **Frontmatter:** Set `name` (kebab-case, matching the directory name) and a precise one-line `description` — this is what the agent reads to decide when to invoke the skill.
   - **Purpose:** One paragraph on what the skill produces.
   - **When to use:** Bullet list of example user queries that should trigger this skill.
   - **Steps:** Numbered agent instructions referencing specific MCP tools (`Securin__<toolName>`).
   - **Output format:** Describe the exact structure the skill should return.
3. Verify that every MCP tool referenced in your skill exists — use `search_tools` or `ping` in Claude Code to confirm.
4. Test the skill end-to-end with Claude Code before submitting. Include a sample query and its expected output in the pull request description.

### Standards

- Skill directory names use the `securin-` prefix and kebab-case (e.g. `securin-my-new-skill`).
- Keep each skill focused on a single job. If a skill requires many conditional branches, consider splitting it into two distinct skills.
- Do not duplicate shared reference files — keep them in `skills/_shared/` and reference them from there.
- Do not commit credentials, tokens, API keys, or personal data of any kind.
- Match the formatting and tone of existing skills for consistency.

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

<sub>Copyright &copy; Securin, Inc. Licensed under the terms in <a href="LICENSE">LICENSE</a>.</sub>
