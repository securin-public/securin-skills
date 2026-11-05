# OAuth redirect URIs

Each person signs in to the Securin MCP server as that person. We use OAuth 2.1 with PKCE and dynamic client registration. We do not ship a shared bearer token, a client secret, or an App Access key in a marketplace package.

We read public discovery on 2026-10-22 from `https://mcp.securin.io/.well-known/oauth-authorization-server` and `https://mcp.securin.io/.well-known/oauth-protected-resource`.

| Item | Value |
| --- | --- |
| MCP endpoint | `https://mcp.securin.io/mcp` |
| Issuer | `https://auth.securin.io/auth/realms/CyberSecurityWorks` |
| Authorize | `https://auth.securin.io/auth/realms/CyberSecurityWorks/protocol/openid-connect/auth` |
| Token | `https://mcp.securin.io/token` |
| Register | `https://mcp.securin.io/register` |
| Realm | `CyberSecurityWorks` |
| Scope advertised | `openid` |
| PKCE methods advertised | `S256`, `plain` |
| Issuer identification advertised | `authorization_response_iss_parameter_supported: true` |
| Client metadata documents | field absent |

We use dynamic registration for marketplace installs. We do not paste a client secret into a manifest, a skill, or a log.

## Redirect URIs

Status values:

| Status | Meaning |
| --- | --- |
| Verified | We confirmed on 2026-10-22 that this exact URI is accepted. Grok Bot completed OAuth as a real user on the two Cursor HTTPS callbacks. |
| Needed | The host publishes this URI. We list it for that host. We do not mark it Verified. |
| Keep | A client we already ship registers this URI. We leave it in place when the allowlist changes. |
| Rejected | We confirmed on 2026-10-22 that this URI is not accepted. |
| Confirm | A secondary writeup names this URI. The Claude page we cite publishes only the `claude.ai` URI. |

| Host | Redirect URI | Status | Source |
| --- | --- | --- | --- |
| Cursor Agents and Grok Bot web | `https://www.cursor.com/agents/mcp/oauth/callback` | Verified | Our test on 2026-10-22; also listed in `https://cursor.com/oauth/mcp-client.json` |
| Cursor Agents apex host | `https://cursor.com/agents/mcp/oauth/callback` | Verified | Our test on 2026-10-22 |
| Grok Bot on cursor.com | `https://www.cursor.com/bot/mcp/oauth/callback` | Needed | `https://cursor.com/oauth/mcp-client.json` fetched 2026-10-22 |
| Grok on the web | `https://grok.com/connectors-oauth-exchange-code/` | Needed | Same Cursor client metadata document; also published as the Grok web callback at `https://docs.x.com/x-ads-api/mcp` |
| Cursor desktop loopback | `http://localhost:8787/callback` | Needed | Cursor MCP docs and the Cursor client metadata document |
| Cursor desktop loopback, IP form | `http://127.0.0.1:8787/callback` | Needed | Cursor client metadata document |
| Cursor desktop custom scheme | `cursor://anysphere.cursor-mcp/oauth/callback` | Rejected | Our test on 2026-10-22. Some Cursor builds still send it during registration. |
| Generic loopback | `http://localhost/callback` | Rejected | Our test on 2026-10-22 |
| Generic loopback, IP form | `http://127.0.0.1/callback` | Rejected | Our test on 2026-10-22 |
| Claude hosted apps | `https://claude.ai/api/mcp/auth_callback` | Needed | Official Claude connector docs name this exact URI for claude.ai, Claude Desktop, Claude mobile, and Cowork. Our README shows the custom connector UI only. We do not treat that UI as proof the redirect already succeeds. |
| Claude hosted apps, alternate host | `https://claude.com/api/mcp/auth_callback` | Confirm | Named in a secondary host comparison. The Claude page we cite publishes only the `claude.ai` URI. |
| Claude Code | `http://localhost:<port>/callback` and `http://127.0.0.1:<port>/callback` | Needed | Claude docs. The port changes every session. We match the path and ignore the port, for both `localhost` and `127.0.0.1`. This path is `/callback`, not `/oauth/callback`. |
| mcp-remote 0.1.38 (MCPB and pinned npx) | `http://localhost:<port>/oauth/callback` | Keep | Default redirect in vendored mcp-remote 0.1.38 (`securin-platform.mcpb` and the README `npx` examples). The CLI host defaults to `localhost` and the path is `/oauth/callback`. |
| mcp-remote 0.1.38, IP host | `http://127.0.0.1:<port>/oauth/callback` | Keep | Used when the process is started with `--host 127.0.0.1`. The callback listener binds `127.0.0.1`, but the registered redirect uses the host flag. We keep this form so a tighter allowlist does not drop the Desktop bundle. |
| ChatGPT and Codex, stable callback | `https://chatgpt.com/connector_platform_oauth_redirect` | Needed | `https://chatgpt.com/oauth/client.json` fetched 2026-10-22, and OpenAI authentication docs |
| ChatGPT, per connection callback | `https://chatgpt.com/connector/oauth/{callback_id}` | Needed | OpenAI authentication docs. Used when issuer identification requirements are not met. The id is assigned when the connector is created. |

## Registration can fail on one bad URI

Some clients send several redirect URIs in one dynamic registration call. If any URI in that call is rejected, the whole registration can fail before the browser opens. That is why we still list the rejected custom scheme and the rejected generic loopback paths.

## Optional bearer path

`https://mcp.securin.io/api/mcp` accepts a bearer token for headless jobs. We treat that path as optional. The token comes from the host secret store or an environment variable that the user sets. We do not commit it, we do not put it in a manifest, and we do not write it to logs. Our marketplace listings use only the OAuth URL above.
