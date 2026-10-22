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
| Claude hosted apps | `https://claude.ai/api/mcp/auth_callback` | Needed | Claude connector authentication docs: exact URI for claude.ai, Claude Desktop, Claude mobile, and Cowork |
| Claude hosted apps, alternate host | `https://claude.com/api/mcp/auth_callback` | Confirm | Named in a secondary host comparison. The Claude page cited above publishes only the `claude.ai` URI. |
| Claude Code | `http://localhost:<port>/callback` and `http://127.0.0.1:<port>/callback` | Needed | Claude docs. The port changes every session. Match the path and ignore the port, for both `localhost` and `127.0.0.1`. |
| ChatGPT and Codex, stable callback | `https://chatgpt.com/connector_platform_oauth_redirect` | Needed | `https://chatgpt.com/oauth/client.json` fetched 2026-10-22, and OpenAI authentication docs |
| ChatGPT, per connection callback | `https://chatgpt.com/connector/oauth/{callback_id}` | Needed | OpenAI authentication docs. Used when issuer identification requirements are not met. The id is assigned when the connector is created. |

## Registration can fail on one bad URI

Some clients send several redirect URIs in one dynamic registration call. If Keycloak rejects any URI in that call, the whole registration can fail before the browser opens. That is why the rejected custom scheme and the rejected generic loopback paths still matter even when the HTTPS callbacks are allowed.

The verified Grok Bot test used the two Cursor HTTPS callbacks. It did not prove desktop loopback, Claude, or ChatGPT.

## Open items for the Keycloak admin

1. Allow every row marked Needed. Keep the two Verified HTTPS callbacks.
2. Decide whether to keep rejecting `cursor://anysphere.cursor-mcp/oauth/callback`. Cursor desktop dynamic registration may still send it together with the HTTPS callback. A reject on that one URI can fail the whole call.
3. For Claude Code, accept loopback redirects on any port for `http://localhost/callback` and `http://127.0.0.1/callback`. The exact paths with no port were rejected on 2026-10-22. Port specific `8787` URIs for Cursor desktop are a separate allowlist entry.
4. Protected resource metadata lists `authorization_servers` as `https://mcp.securin.io` (the `/mcp` well known document uses a trailing slash). The authorization server issuer is `https://auth.securin.io/auth/realms/CyberSecurityWorks`. OpenAI uses the stable ChatGPT callback only when those two strings match and the authorize response returns `iss`. They do not match today, so ChatGPT may use the per connection callback instead. Confirm which callback a real ChatGPT connect sends, then allow that exact URI.
5. `client_id_metadata_document_supported` is absent. ChatGPT prefers a client metadata document and falls back to dynamic registration. Dynamic registration is advertised and should remain the fallback.
6. `token_endpoint_auth_methods_supported` does not list `none`. The Cursor client metadata document uses `none` with PKCE. Grok Bot OAuth still completed on 2026-10-22, so the register endpoint may accept a public client even though the metadata list omits `none`. Confirm that behavior and add `none` to the advertised list if public clients are intended.
7. `authorization_response_iss_parameter_supported` is true. Confirm the authorize response includes `iss` and that the value matches the issuer string with no extra slash or host change.
8. Prefer PKCE `S256`. `plain` is also advertised. Confirm that leaving `plain` enabled is acceptable.

## Optional bearer path

`https://mcp.securin.io/api/mcp` accepts a bearer token for headless jobs. That path is optional. The token comes from the host secret store or an environment variable that the user sets. Do not commit it, do not put it in a manifest, and do not write it to logs. Marketplace listings in this repository use only the OAuth URL above.
