# Host setup guides

Per-host instructions for connecting the Securin MCP server and loading skills. See the main [README](../README.md) for Claude Code and Claude Desktop setup.

---

## VS Code (GitHub Copilot)

> **One-click:** use the install badge from the [README](../README.md#install), or use the CLI:
> ```bash
> code --add-mcp '{"name":"securin","type":"http","url":"https://mcp.securin.io/mcp"}'
> ```

**Manual setup** — add to `.vscode/mcp.json`:

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

Or copy skill subdirectories into your project's `.agents/skills/`.

---

## Cursor

> **One-click:** use the install badge from the [README](../README.md#install).

**Manual setup** — add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "securin": {
      "url": "https://mcp.securin.io/mcp"
    }
  }
}
```

**Skills** — clone this repo and copy skill subdirectories from `skills/` into your project's `.agents/skills/`.

### Cursor Marketplace

The repository root is a Cursor plugin named `securin-platform` at version `0.1.0`.

1. After the listing is approved, install Securin Platform from the Cursor Marketplace.
2. On first use, sign in with Securin OAuth in the browser.
3. The plugin loads `skills/` and the remote server in `mcp.json`.

Publisher form: https://cursor.com/marketplace/publish

Grok Bot uses this same Cursor plugin package. Submission steps for every marketplace are in [submission.md](submission.md). Redirect URIs are in [oauth-redirects.md](oauth-redirects.md).

Manual `.cursor/mcp.json` setup above remains valid before the listing is live.

---

## Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "securin": {
      "command": "npx",
      "args": ["-y", "mcp-remote@0.1.38", "https://mcp.securin.io/mcp"]
    }
  }
}
```

**Skills** — clone this repo and copy skill subdirectories from `skills/` into your project's `.agents/skills/`.

---

## Gemini CLI

Add to `.gemini/settings.json`:

```json
{
  "mcpServers": {
    "securin": {
      "url": "https://mcp.securin.io/mcp"
    }
  }
}
```

**Skills** — clone this repo and copy skill subdirectories into `.gemini/skills/` or `.agents/skills/`.

---

## OpenAI Codex CLI

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.securin]
url = "https://mcp.securin.io/mcp"
```

**Skills** — clone this repo and copy skill subdirectories into `.agents/skills/`.

---

## Any other MCP-compatible host

The endpoint `https://mcp.securin.io/mcp` uses Streamable HTTP transport. Connect directly if your host supports it, or use the `mcp-remote` bridge for stdio-only hosts:

```json
{
  "command": "npx",
  "args": ["-y", "mcp-remote@0.1.38", "https://mcp.securin.io/mcp"]
}
```

For skills, clone this repo and point the host's skill loader at the `skills/` directory.
