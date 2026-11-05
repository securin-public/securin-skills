# OAuth redirect URIs

Each person signs in to the Securin MCP server as that person. The default path is OAuth 2.1 with PKCE and dynamic client registration. Do not ship a shared bearer token, a client secret, or an App Access key in a marketplace package.

Public discovery was read on 2026-10-22 from `https://mcp.securin.io/.well-known/oauth-authorization-server` and `https://mcp.securin.io/.well-known/oauth-protected-resource`.

| Item | Value |
| --- | --- |
| MCP endpoint | `https://mcp.securin.io/mcp` |
| Issuer | `https://auth.securin.io/auth/realms/CyberSecurityWorks` |
| Authorize | `https://auth.securin.io/auth/realms/CyberSecurityWorks/protocol/openid-connect/auth` |
| Token | `https://mcp.securin.io/token` |
| Register | `https://mcp.securin.io/register` |
| Realm | `CyberSecurityWorks` |
| Existing realm client name | `securin-java-ai-mcp` |
| Scope advertised | `openid` |
| PKCE methods advertised | `S256`, `plain` |
| Issuer identification advertised | `authorization_response_iss_parameter_supported: true` |
| Client metadata documents | field absent |

Marketplace installs must use dynamic registration. The realm client name above is for the Keycloak admin. Do not paste a client secret into a manifest, a skill, or a log.

## Redirect URIs

Status values:

| Status | Meaning |
| --- | --- |
| Verified | Securin confirmed on 2026-10-22 that Keycloak accepts this exact URI, and Grok Bot completed OAuth as a real user. |
| Needed | A host publishes this URI. Keycloak still needs to allow it. This PR did not complete a live sign in for that host. |
| Keep | A client that already ships in this repo registers this URI. Leave it on the allowlist when tightening. This change did not repeat a live sign in for it. |
| Rejected | Securin confirmed on 2026-10-22 that Keycloak does not accept this URI. |
| Confirm | A secondary writeup names this URI. It is not in the Claude page cited below. Confirm with a live connect before relying on it. |

| Host | Redirect URI | Status | Source |
| --- | --- | --- | --- |
| Cursor Agents and Grok Bot web | `https://www.cursor.com/agents/mcp/oauth/callback` | Verified | Securin test on 2026-10-22; also listed in `https://cursor.com/oauth/mcp-client.json` |
| Cursor Agents apex host | `https://cursor.com/agents/mcp/oauth/callback` | Verified | Securin test on 2026-10-22 |
| Grok Bot on cursor.com | `https://www.cursor.com/bot/mcp/oauth/callback` | Needed | `https://cursor.com/oauth/mcp-client.json` fetched 2026-10-22 |
| Grok on the web | `https://grok.com/connectors-oauth-exchange-code/` | Needed | Same Cursor client metadata document; also published as the Grok web callback at `https://docs.x.com/x-ads-api/mcp` |
| Cursor desktop loopback | `http://localhost:8787/callback` | Needed | Cursor MCP docs and the Cursor client metadata document |
| Cursor desktop loopback, IP form | `http://127.0.0.1:8787/callback` | Needed | Cursor client metadata document |
| Cursor desktop custom scheme | `cursor://anysphere.cursor-mcp/oauth/callback` | Rejected | Securin test on 2026-10-22. Some Cursor builds still send it during registration. |
| Generic loopback | `http://localhost/callback` | Rejected | Securin test on 2026-10-22 |
| Generic loopback, IP form | `http://127.0.0.1/callback` | Rejected | Securin test on 2026-10-22 |
| Claude hosted apps | `https://claude.ai/api/mcp/auth_callback` | Needed | Official Claude connector docs name this exact URI for claude.ai, Claude Desktop, Claude mobile, and Cowork. The README custom connector section shows that UI only. This repository has no live sign in record for this URI, so the status stays Needed. Do not read the README as proof that Keycloak already accepts it. |
| Claude hosted apps, alternate host | `https://claude.com/api/mcp/auth_callback` | Confirm | Named in a secondary host comparison. The Claude page cited above publishes only the `claude.ai` URI. |
| Claude Code | `http://localhost:<port>/callback` and `http://127.0.0.1:<port>/callback` | Needed | Claude docs. The port changes every session. Match the path and ignore the port, for both `localhost` and `127.0.0.1`. Claude Code sign in is not safe for users who update the plugin until Keycloak allows these URIs. This repository does not record a live Claude Code sign in. |
| mcp-remote 0.1.38 (MCPB and pinned npx) | `http://localhost:<port>/oauth/callback` | Keep | Default redirect in vendored mcp-remote 0.1.38 (`securin-platform.mcpb` and the README `npx` examples). The CLI host defaults to `localhost` and the path is `/oauth/callback`, which is not the Claude Code path. Leave this URI in place when tightening the allowlist. |
| mcp-remote 0.1.38, IP host | `http://127.0.0.1:<port>/oauth/callback` | Keep | Used when the process is started with `--host 127.0.0.1`. The callback listener binds `127.0.0.1`, but the registered redirect uses the host flag. Keep this form as well so a tighter allowlist does not drop the Desktop bundle. |
| ChatGPT and Codex, stable callback | `https://chatgpt.com/connector_platform_oauth_redirect` | Needed | `https://chatgpt.com/oauth/client.json` fetched 2026-10-22, and OpenAI authentication docs |
| ChatGPT, per connection callback | `https://chatgpt.com/connector/oauth/{callback_id}` | Needed | OpenAI authentication docs. Used when issuer identification requirements are not met. The id is assigned when the connector is created. |

## Registration can fail on one bad URI

Some clients send several redirect URIs in one dynamic registration call. If Keycloak rejects any URI in that call, the whole registration can fail before the browser opens. That is why the rejected custom scheme and the rejected generic loopback paths still matter even when the HTTPS callbacks are allowed.

The verified Grok Bot test used the two Cursor HTTPS callbacks. It did not prove desktop loopback, the claude.ai callback, Claude Code loopback, the mcp-remote `/oauth/callback` path, or ChatGPT. The README custom connector section shows the claude.ai UI. It is not a live sign in record, so that callback stays Needed.

## Open items for the Keycloak admin

1. Allow every row marked Needed. Leave every row marked Keep on the allowlist, including both mcp-remote `/oauth/callback` URIs. Leave the two Verified HTTPS callbacks in place.
2. Decide whether to keep rejecting `cursor://anysphere.cursor-mcp/oauth/callback`. Cursor desktop dynamic registration may still send it together with the HTTPS callback. A reject on that one URI can fail the whole call.
3. For Claude Code, accept loopback redirects on any port for `http://localhost:<port>/callback` and `http://127.0.0.1:<port>/callback`. The exact paths with no port were rejected on 2026-10-22. Port specific `8787` URIs for Cursor desktop are a separate allowlist entry. Claude Code sign in is not safe for users who update the plugin until the port specific loopback URIs are allowed. This document does not record a live Claude Code sign in.
4. Leave `http://localhost:<port>/oauth/callback` on the allowlist for mcp-remote 0.1.38 (the Desktop `.mcpb` bundle and the pinned `npx` examples). Also leave `http://127.0.0.1:<port>/oauth/callback` for a host flag of `127.0.0.1`. That path is different from the Claude Code `/callback` path and from the rejected generic `http://localhost/callback` row. Do not drop it when tightening the list.
5. Protected resource metadata lists `authorization_servers` as `https://mcp.securin.io` (the `/mcp` well known document uses a trailing slash). The authorization server issuer is `https://auth.securin.io/auth/realms/CyberSecurityWorks`. OpenAI uses the stable ChatGPT callback only when those two strings match and the authorize response returns `iss`. They do not match today, so ChatGPT may use the per connection callback instead. Confirm which callback a real ChatGPT connect sends, then allow that exact URI.
6. `client_id_metadata_document_supported` is absent. ChatGPT prefers a client metadata document and falls back to dynamic registration. Dynamic registration is advertised and should remain the fallback.
7. `token_endpoint_auth_methods_supported` does not list `none`. The Cursor client metadata document uses `none` with PKCE. Grok Bot OAuth still completed on 2026-10-22, so the register endpoint may accept a public client even though the metadata list omits `none`. Confirm that behavior and add `none` to the advertised list if public clients are intended.
8. `authorization_response_iss_parameter_supported` is true. Confirm the authorize response includes `iss` and that the value matches the issuer string with no extra slash or host change.
9. Prefer PKCE `S256`. `plain` is also advertised. Confirm that leaving `plain` enabled is acceptable.

## Optional bearer path

`https://mcp.securin.io/api/mcp` accepts a bearer token for headless jobs. That path is optional. The token comes from the host secret store or an environment variable that the user sets. Do not commit it, do not put it in a manifest, and do not write it to logs. Marketplace listings in this repository use only the OAuth URL above.
