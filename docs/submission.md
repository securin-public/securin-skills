# Submission checklist

Humans submit each listing. This pull request does not submit forms, does not upload a zip, and does not merge.

Shared facts: name `securin-platform`, plugin version `0.1.0`, homepage `https://securin.io`, support `support@securin.io`, logo `assets/logo.svg` and `assets/logo.png` copied from `skills/_shared/securin_logos/`. License text is the root `LICENSE`. Manifests use `LicenseRef-Securin-Proprietary` until legal picks the identifier.

## Done in this pull request

| Item | State |
| --- | --- |
| Cursor manifest `.cursor-plugin/plugin.json` and root `mcp.json` | Done |
| Grok Bot uses that Cursor package; Grok Build manifest `.grok-plugin/plugin.json` | Done |
| OpenAI zip sources under `packaging/openai/` and `scripts/build-openai-plugin-zip.py` | Done |
| Claude `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, HTTPS `.mcp.json` | Done |
| MCPB manifest aligned to the root license; bundle version `1.2.3` | Done |
| OAuth redirect page | Done |
| CI schema check and secret scan | Done |
| Logo files copied from existing assets | Done |

## Blocked for every listing

| Blocker | Owner |
| --- | --- |
| Brand sign off for the logo on a public listing, including a square plate if a form requires one | Brand |
| Legal sign off on the root `LICENSE`, on `LicenseRef-Securin-Proprietary`, and on any marketplace that requires an OSI license | Legal |
| Terms URL. `https://www.securin.io/terms`, `/terms-of-service`, and `/terms-of-use` returned the marketing homepage on 2026-10-22, so no terms URL is set | Legal |
| Privacy URL in manifests is `https://www.securin.io/privacy-policy`. Confirm it is the policy legal wants cited | Legal |
| Redirect URIs in [oauth-redirects.md](oauth-redirects.md) | Keycloak admin |
| Reviewer account with sample data, no real customer data, and a sign in path a reviewer can finish | Securin account admin |
| Screenshots and a video where a portal requires them | Listing owner |
| End to end sign in on Cursor desktop, Claude, and ChatGPT after the allowlist changes | Listing owner |

The icon PNG is 498 by 482 pixels. It is the existing S mark with no added background plate. The Grok Bot form asks for a 1:1 SVG or PNG on a background plate. Do not invent art in git. Brand supplies a plate if the form rejects this file.

## Cursor Marketplace

Submit: https://cursor.com/marketplace/publish

Publisher terms on that form also cover the Grok Bot form.

### Human steps

1. Wait until this change is on the default branch of `securin-public/securin-skills`.
2. Open the publish form and paste `https://github.com/securin-public/securin-skills`.
3. Leave the plugin path empty. The manifest is at the repository root.
4. Complete publisher verification with a Securin work mailbox.
5. Confirm the logo URL resolves to `assets/logo.svg` in the repository.
6. Install the plugin from a local checkout or from the review build. Sign in with a test account. Run one skill prompt such as `Enrich CVE-2024-3400.`
7. Reply to review notes. Do not merge this packaging pull request as part of the form; merging is a separate maintainer action.

### Still blocked

Brand, legal, desktop redirect `http://localhost:8787/callback`, and the custom scheme decision in [oauth-redirects.md](oauth-redirects.md).

## Grok Bot and Grok

Submit: https://x.ai/bot/marketplace/submit-a-plugin

Grok Bot consumes the Cursor plugin. There is no second manifest to maintain for that app.

xAI Grok on the web does not have a separate plugin package in this repo. The web product needs the redirect URI `https://grok.com/connectors-oauth-exchange-code/` from [oauth-redirects.md](oauth-redirects.md). The submission form has included a Grok target marked coming soon. If that target is still closed, submit Grok Bot and Cursor, and record the date the Grok target opened.

### Human steps

1. Use a work email, organization name `Securin`, and a lowercase organization handle the team agrees on.
2. Logo URL: the raw file `assets/logo.png` on the default branch. Replace it only after brand supplies a 1:1 plate.
3. Select Grok Bot and Cursor. Select Grok only if the form no longer says coming soon and a Grok sign in has been tested.
4. Server or repository: `https://github.com/securin-public/securin-skills` or `https://mcp.securin.io/mcp`. Prefer the repository so the skills install with the server. If the form allows only one, put the repository and state the MCP URL in the test notes.
5. Short description: use the `description` string in `packaging/metadata.json`.
6. Test notes: install in Grok Bot, complete OAuth as a test user, ask `Enrich CVE-2024-3400.` Confirm the agent does not create tickets.
7. Tick the test confirmation only after that run. The 2026-10-22 Grok Bot OAuth test covered sign in. It did not cover this package version.

### Grok Build catalog

After the commit is on the default branch, open a pull request on `https://github.com/xai-org/plugin-marketplace` with one entry in `.grok-plugin/marketplace.json`. Replace `SHA` with the full 40 character commit. Do not guess the SHA.

```json
{
  "name": "securin-platform",
  "description": "Securin Platform skills for exposure triage, CVE enrichment, threat correlation, and remediation guidance. Connects to the Securin MCP server with per user OAuth single sign on. A Securin account is required.",
  "version": "0.1.0",
  "author": {"name": "Securin", "email": "support@securin.io"},
  "homepage": "https://securin.io",
  "keywords": ["securin", "vulnerability", "exposure", "cve", "remediation"],
  "category": "security",
  "source": {
    "source": "url",
    "url": "https://github.com/securin-public/securin-skills.git",
    "sha": "SHA"
  }
}
```

Follow that repo `CONTRIBUTING.md`: regenerate `.grok-plugin/plugin-index.json` with the catalog script, and do not hand edit the index. Category `security` is a suggestion. Use a category the catalog already accepts if `security` is rejected.

## OpenAI

Docs used on 2026-10-22:

| Topic | URL |
| --- | --- |
| Package layout | https://developers.openai.com/plugins/build/plugins |
| Upload and review | https://developers.openai.com/plugins/deploy/submission |
| OAuth | https://developers.openai.com/plugins/build/auth |
| Apps and connectors in ChatGPT | https://help.openai.com/en/articles/11487775-connecting-mcp-servers-to-chatgpt |

ChatGPT custom connectors and the public plugin directory are both in scope. A workspace admin can add `https://mcp.securin.io/mcp` as a custom connector with OAuth before the public listing exists. The public listing is the zip from this repo.

Apps SDK UI is not in this package. Add it later only if product wants a custom panel. Do not block the skill and MCP listing on that work.

### Human steps

1. Run `python3 scripts/build-openai-plugin-zip.py`. The zip is `dist/securin-platform-openai-0.1.0.zip`.
2. In the OpenAI platform, open Plugins, choose the verified Securin developer identity, and upload the zip.
3. Fix any portal findings. Metadata and skills require a new zip. Hosted tool changes are a rescan, not a new zip.
4. Connect the one MCP server `securin`. Authentication in the package is OAuth with dynamic registration. Do not type a client secret. The portal has no API key flow, and this package does not declare one.
5. Complete domain verification. Host the exact token as plain text at the URL the portal shows, under `https://mcp.securin.io/.well-known/openai-apps-challenge` or a parent origin the portal allows. Do not commit the token.
6. Enter reviewer credentials in the portal only. Do not put them in git. The account must work without a human approving MFA during the review window.
7. Record a video of the five positive cases and three negative cases in `packaging/openai/plugin.json`. Put the video URL in the portal. Add `demo_recording_url` to the manifest only after the URL exists.
8. Set country availability with legal. The manifest does not set a country list.
9. Confirm category `Developer Tools` against the dashboard list. Change it in both OpenAI manifests if the dashboard uses another title.
10. Submit for review. Publish only after approval. Publishing is not part of this pull request.

### Still blocked

Redirect rows for ChatGPT in [oauth-redirects.md](oauth-redirects.md), the issuer mismatch noted there, domain verification, reviewer account, video, countries, brand, and legal.

Codex users who only need the server can skip the zip and use the HTTPS block in [host-setup.md](host-setup.md). Skills for that path are the `skills/` tree in this repo.

## Anthropic

### Claude Code marketplace

Already installable from git after this change is on the default branch:

```bash
/plugin marketplace add securin-public/securin-skills
/plugin install securin-platform@securin-skills
```

No extra form is required for a team that adds the marketplace by repository. Test: install, sign in, run `Enrich CVE-2024-3400.` Confirm `.mcp.json` connects to `https://mcp.securin.io/mcp` and does not spawn `npx`.

### Claude directory

Portal: https://claude.ai/directory/manage

Checklist: https://claude.com/docs/plugins/pre-submission-checklist

Submit guide: https://claude.com/docs/plugins/submit

### Human steps

1. Connect a GitHub account that can push to `securin-public/securin-skills`.
2. Submit a plugin bundle. Repository `securin-public/securin-skills`. Plugin path empty. Track the default branch.
3. Run Validate in the portal. If Claude Code is installed, also run `claude plugin validate . --strict` and fix blocking findings.
4. Submit the remote MCP server again as an MCP connector if the portal still requires a separate connector listing. URL `https://mcp.securin.io/mcp`. Auth is OAuth, not a static header.
5. Answer data handling: the plugin sends prompts to the Securin MCP server over HTTPS; the server applies the signed in user permissions; this repo does not store customer data.
6. Use `support@securin.io` as the contact on the form.
7. The official Anthropic marketplace `claude-plugins-official` does not take this portal submission. A partner listing is a separate conversation with Anthropic.

### Claude Desktop bundle

`securin-platform.mcpb` is installed by opening the file. This pull request updates the manifest inside the archive to version `1.2.3`. There is no Desktop store upload in the docs cited above.

### Still blocked

Claude redirect URIs, `claude plugin validate` on a machine that has the CLI, directory portal Validate, brand, and legal. A pinned `npx` path is no longer the Claude Code default. If a reviewer still requires stdio, use the MCPB bundle rather than putting `npx` back into `.mcp.json`.

## Test steps after allowlist updates

1. Cursor desktop: add `mcp.json`, complete OAuth, run a skill prompt.
2. Grok Bot: repeat the 2026-10-22 sign in against this package.
3. Claude Code: `/plugin install securin-platform@securin-skills`, then the same prompt.
4. Claude hosted: custom connector URL `https://mcp.securin.io/mcp`.
5. ChatGPT: custom connector or the uploaded zip, OAuth, same prompt, then a negative prompt that asks to delete exposures.
6. Confirm no token appears in git, in screenshots, or in uploaded logs.
