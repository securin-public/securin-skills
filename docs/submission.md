# Submission checklist

We submit each listing ourselves. We do not submit forms, upload a zip, or merge from this document.

Shared facts: name `securin-platform`, plugin version `0.1.0`, homepage `https://securin.io`, support `support@securin.io`, logo `assets/logo.svg` and `assets/logo.png` copied from `skills/_shared/securin_logos/`. License text is the root `LICENSE`. We set manifest license fields to `LicenseRef-Securin-Proprietary`, which points at that file.

## What we added

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

The icon PNG is 498 by 482 pixels. It is the existing S mark with no added background plate. We do not invent a replacement in git. If a form requires a 1:1 plate, we supply that file outside this repository.

## Cursor Marketplace

Submit: https://cursor.com/marketplace/publish

Publisher terms on that form also cover the Grok Bot form.

### Steps we follow

1. We wait until this change is on the default branch of `securin-public/securin-skills`.
2. We open the publish form and paste `https://github.com/securin-public/securin-skills`.
3. We leave the plugin path empty. The manifest is at the repository root.
4. We complete publisher verification with a Securin work mailbox.
5. We confirm the logo URL resolves to `assets/logo.svg` in the repository.
6. We install the plugin from a local checkout or from the review build. We sign in with a test account. We run one skill prompt such as `Enrich CVE-2024-3400.`
7. We reply to review notes. We treat merging as a separate maintainer action.

### Still open

Desktop redirect `http://localhost:8787/callback` and the custom scheme row in [oauth-redirects.md](oauth-redirects.md).

## Grok Bot and Grok

Submit: https://x.ai/bot/marketplace/submit-a-plugin

Grok Bot consumes the Cursor plugin. We do not keep a second manifest for that app.

xAI Grok on the web does not have a separate plugin package in this repo. The web product needs the redirect URI `https://grok.com/connectors-oauth-exchange-code/` from [oauth-redirects.md](oauth-redirects.md). The submission form has included a Grok target marked coming soon. If that target is still closed, we submit Grok Bot and Cursor, and we record the date the Grok target opened.

### Steps we follow

1. We use a work email, organization name `Securin`, and a lowercase organization handle we agree on.
2. Logo URL: the raw file `assets/logo.png` on the default branch. We replace it only after we have a 1:1 plate.
3. We select Grok Bot and Cursor. We select Grok only if the form no longer says coming soon and we have tested a Grok sign in.
4. Server or repository: `https://github.com/securin-public/securin-skills` or `https://mcp.securin.io/mcp`. We prefer the repository so the skills install with the server. If the form allows only one, we put the repository and state the MCP URL in the test notes.
5. Short description: we use the `description` string in `packaging/metadata.json`.
6. Test notes: we install in Grok Bot, complete OAuth as a test user, and ask `Enrich CVE-2024-3400.` We confirm the run does not create tickets.
7. We tick the test confirmation only after that run. A Grok Bot sign in on 2026-10-22 covered OAuth. It did not cover this package version.

### Grok Build catalog

After the commit is on the default branch, we open a pull request on `https://github.com/xai-org/plugin-marketplace` with one entry in `.grok-plugin/marketplace.json`. We replace `SHA` with the full 40 character commit. We do not guess the SHA.

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

We follow that repo `CONTRIBUTING.md`: we regenerate `.grok-plugin/plugin-index.json` with the catalog script, and we do not hand edit the index. Category `security` is a suggestion. We use a category the catalog already accepts if `security` is rejected.

## OpenAI

Docs we used on 2026-10-22:

| Topic | URL |
| --- | --- |
| Package layout | https://developers.openai.com/plugins/build/plugins |
| Upload and review | https://developers.openai.com/plugins/deploy/submission |
| OAuth | https://developers.openai.com/plugins/build/auth |
| Apps and connectors in ChatGPT | https://help.openai.com/en/articles/11487775-connecting-mcp-servers-to-chatgpt |

ChatGPT custom connectors and the public plugin directory are both in scope. A workspace admin can add `https://mcp.securin.io/mcp` as a custom connector with OAuth before the public listing exists. The public listing is the zip from this repo.

We do not include Apps SDK UI in this package. We add it later only if we want a custom panel. We do not block the skill and MCP listing on that work.

### Steps we follow

1. We run `python3 scripts/build-openai-plugin-zip.py`. The zip name comes from `name` and `version` in `packaging/metadata.json`. With the current values that file is `dist/securin-platform-openai-0.1.0.zip`.
2. In the OpenAI platform, we open Plugins, choose the verified Securin developer identity, and upload the zip.
3. We fix any portal findings. Metadata and skills require a new zip. Hosted tool changes are a rescan, not a new zip.
4. We connect the one MCP server `securin`. Authentication in the package is OAuth with dynamic registration. We do not type a client secret. The portal has no API key flow, and this package does not declare one.
5. We complete domain verification. We host the exact token as plain text at the URL the portal shows, under `https://mcp.securin.io/.well-known/openai-apps-challenge` or a parent origin the portal allows. We do not commit the token.
6. We enter reviewer credentials in the portal only. We do not put them in git. The account must work without a person approving MFA during the review window.
7. We record a video of the five positive cases and three negative cases in `packaging/openai/plugin.json`. We put the video URL in the portal. We add `demo_recording_url` to the manifest only after the URL exists.
8. We set country availability in the portal. The manifest does not set a country list.
9. We confirm category `Developer Tools` against the dashboard list. We change it in both OpenAI manifests if the dashboard uses another title.
10. We submit for review. We publish only after approval. We do not publish from this repository.

### Still open

ChatGPT redirect rows in [oauth-redirects.md](oauth-redirects.md), domain verification, a reviewer account, a video, and country availability.

Codex users who only need the server can skip the zip and use the HTTPS block in [host-setup.md](host-setup.md). Skills for that path are the `skills/` tree in this repo.

## Anthropic

### Claude Code marketplace

We can install from git after this change is on the default branch:

```bash
/plugin marketplace add securin-public/securin-skills
/plugin install securin-platform@securin-skills
```

We do not file an extra form for a team that adds the marketplace by repository. We test with a real sign in, not only a check that `npx` is absent:

1. `/plugin marketplace add securin-public/securin-skills`
2. `/plugin install securin-platform@securin-skills`
3. In `/mcp`, we select `securin` and complete Securin sign in.
4. We run `Enrich CVE-2024-3400` and confirm the tool call uses the signed in session.

We keep `.mcp.json` at `https://mcp.securin.io/mcp` with no `npx` process. That check is not a substitute for step 3.

Claude Code redirect URIs are `http://localhost:<port>/callback` and `http://127.0.0.1:<port>/callback`. We list them as Needed in [oauth-redirects.md](oauth-redirects.md).

### Claude directory

Portal: https://claude.ai/directory/manage

Checklist: https://claude.com/docs/plugins/pre-submission-checklist

Submit guide: https://claude.com/docs/plugins/submit

### Steps we follow

1. We connect a GitHub account that can push to `securin-public/securin-skills`.
2. We submit a plugin bundle. Repository `securin-public/securin-skills`. Plugin path empty. We track the default branch.
3. We run Validate in the portal. If Claude Code is installed, we also run `claude plugin validate . --strict` and fix blocking findings.
4. We submit the remote MCP server again as an MCP connector if the portal still requires a separate connector listing. URL `https://mcp.securin.io/mcp`. Auth is OAuth, not a static header.
5. We answer data handling: the plugin sends prompts to the Securin MCP server over HTTPS; the server applies the signed in user permissions; this repo does not store customer data.
6. We use `support@securin.io` as the contact on the form.
7. The official Anthropic marketplace `claude-plugins-official` does not take this portal submission. A partner listing is a separate conversation with Anthropic.

### Claude Desktop bundle

We install `securin-platform.mcpb` by opening the file. We set the manifest inside the archive to version `1.2.3`. We do not see a Desktop store upload in the docs cited above.

### Still open

Redirect rows in [oauth-redirects.md](oauth-redirects.md), including the Claude Code `/callback` URIs and the mcp-remote Keep rows. We run `claude plugin validate` where the CLI is installed, and we run Validate in the directory portal. We no longer use `npx` as the Claude Code default. If a reviewer still requires stdio, we use the MCPB bundle rather than putting `npx` back into `.mcp.json`.

## How we test

1. Cursor desktop: we add `mcp.json`, complete OAuth, and run a skill prompt.
2. Grok Bot: we repeat the 2026-10-22 sign in against this package.
3. Claude Code: we run `/plugin marketplace add securin-public/securin-skills`, then `/plugin install securin-platform@securin-skills`, then we authenticate `securin` in `/mcp`, then we use the same prompt. We do not stop at "no npx process".
4. Claude hosted: custom connector URL `https://mcp.securin.io/mcp`. The UI is in the README. Sign in for that connector uses `https://claude.ai/api/mcp/auth_callback`, which we mark Needed. We do not treat the README steps as a completed sign in.
5. ChatGPT: custom connector or the uploaded zip, OAuth, same prompt, then a negative prompt that asks to delete exposures.
6. We confirm no token appears in git, in screenshots, or in uploaded logs.
