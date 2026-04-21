# Security Policy

Securin takes security seriously. This document describes how to report
vulnerabilities in the **Securin Platform Skills Plugin** and what to expect
from our response.

## Reporting a vulnerability

If you believe you have found a security vulnerability in this plugin,
its shipped MCP configuration, or its skill content, please report it
responsibly so we can fix it before it is publicly disclosed.

**Preferred channel — email:**

Send a detailed report to **security@securin.io**. Encrypt with Securin's
PGP key if your finding is sensitive (key fingerprint and published key
available at <https://securin.io/.well-known/security.txt>).

**Alternate channel — private GitHub advisory:**

Open a private security advisory against this repository:
<https://github.com/securin-public/securin-skills/security/advisories/new>

Please include:

- A description of the vulnerability and its potential impact
- Step-by-step reproduction instructions, including the affected version /
  commit hash
- Any proof-of-concept code, logs, or screenshots that demonstrate the issue
- Your name / handle (optional, for acknowledgment)

**Do not** disclose the vulnerability publicly — including in public GitHub
issues, social media, or blog posts — until Securin has confirmed a fix or
explicitly asked you to proceed.

## Scope

In scope:

- The plugin manifest (`.claude-plugin/plugin.json`)
- The MCP configuration (`.mcp.json`)
- All files under `skills/` — including skill content, shared references,
  and example FQL / prompt strings that could be abused
- The brand pipeline in `skills/_shared/brand.md` and its example code
  snippets

Out of scope (report to the relevant upstream project):

- The Securin Platform MCP Server itself →
  <https://github.com/securin-inc/securin-mcp>
- The Securin Platform API and UI → security@securin.io
- Claude Code / Cowork / Desktop / other host clients → the respective
  vendor (Anthropic, Microsoft, etc.)

## Our response

When you report a vulnerability through one of the preferred channels,
you can expect:

| Stage | Timeline |
|---|---|
| Acknowledgment that we received the report | Within 2 business days |
| Initial triage and severity assessment | Within 5 business days |
| Status update or fix plan | Within 14 days of triage |
| Coordinated disclosure (if applicable) | Mutually agreed |

We may ask follow-up questions as we investigate. Once a fix is released,
we'll credit you in the release notes and — if you want — in a public
security advisory, unless you prefer to remain anonymous.

## Safe-harbor

Securin will not take legal action against researchers who:

- Make a good-faith effort to avoid privacy violations, destruction of
  data, and interruption or degradation of our service during their
  research.
- Report vulnerabilities through the channels above and give us a
  reasonable opportunity to fix the issue before public disclosure.
- Do not exfiltrate data beyond what is necessary to prove the
  vulnerability.
- Comply with all applicable laws.

## Questions

Non-security product questions: support@securin.io
Security-specific inquiries: security@securin.io
