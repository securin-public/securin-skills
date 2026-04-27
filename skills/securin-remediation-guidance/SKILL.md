---
name: securin-remediation-guidance
description: >
  Use this skill when the user asks "how do I fix this exposure", "remediate
  this vulnerability", "what's the fix for...", "patch guidance for CVE-XXX",
  "workaround for this vuln", or needs an actionable fix plan for a specific
  exposure or CVE. The skill reads remediation, solution, and patch fields
  already populated in the platform (built-in, mapped, or scanner-provided)
  first, and only offers a web-search enrichment after user confirmation.
  For prioritization across many exposures use securin-exposure-triage; for
  global CVE intel use securin-cve-enrichment. Requires the Securin Platform
  MCP server.
---

# Remediation Guidance

## Purpose

Produce an **actionable fix plan** for a specific exposure or CVE — drawn primarily from the platform's own remediation content (built-in fields, mapped attributes, scanner-native fields). Web search is an opt-in enrichment, not a default step.

## When to use

- "How do I fix CVE-2024-3400?"
- "Remediate exposure `exp-abc123`"
- "Patch guidance for log4j"
- "What's the workaround while we can't patch?"
- "Compensating controls for this vuln"
- "Generate a ticket body for this exposure"

## Pre-flight

### Step 0 — Account preflight (CC-1)

See [_shared/account-preflight.md](references/_shared/account-preflight.md). Required — remediation plans read the user's exposure records.

## Suggested tools

### Pre-flight (CC-1, see shared doc)
- `getUserProfile` — resolve caller's accessible accounts + user-id
- `getEffectiveAccess` / `getEffectiveAccessWorkspaces` — per-resource access when needed

### Read remediation content (primary)
- `searchExposureData` — exposure records; **this is where most remediation content lives**, under `exposure.mappedAttributes.*` or scanner-specific fields
- `searchVulnerabilityData` — CVE record with fixed-in version and vendor references (when available)
- `searchAssetData` / `searchCompositeAssetData` — asset platform context (OS, version) so the fix advice is relevant
- `searchComponentData` — installed component / package version (for package-manager style remediation)
- `getApiFields(entityType=['EXPOSURE'], searchText='remediation')` — discover all remediation-bearing fields for this account
- `getApiFields(entityType=['EXPOSURE'], searchText='solution')` — same for scanner-native `solution` fields
- `getApiFields(entityType=['EXPOSURE'], searchText='patch')` / `'fix'` — same for patch / fix-info fields

### Integrations / actions
- `getConfiguredIntegrations` — **call early**. Returns every configured scanner + ticketing integration with `id`, `name`, `vendorName`, `type` (`SCANNER` / `TICKETING`), and **`prefix`** (e.g. `WIZ`, `Q-VMDR`, `NESSUS`, `SNYK`, `SERVICE_NOW_INCIDENT`). **Two uses:**
  1. **Find scanner-specific remediation fields.** The `prefix` maps to an integration-specific field group — pass it as `fetchGroups` to `getApiFields(entityType=['EXPOSURE'])` to retrieve that integration's remediation/solution/advisory fields (e.g., Qualys `solution`, Tenable `solution`, Rapid7 `solution`). Scanner-native fields often have richer vendor advisory text than the generic `exposure.mappedAttributes.vendorRemediation`.
  2. **Detect ticketing handoff options.** Filter `type = 'TICKETING'` to find Jira / ServiceNow / ServiceNow_Incident integrations for draft ticket output.
- `getSupportedActions` — what remediation actions are available through the platform (read-only surfacing in M1)

### Deep links (CC-2)
- See [_shared/deep-links.md](references/_shared/deep-links.md). Default: render a platform URL with the FQL filter you used. Only call `createDeepLink` if the user explicitly asks to save/share.

### Opt-in enrichment (after user confirms)
- **Web search** — vendor advisory, KB article, community workarounds. Do not run by default.

## Workflow

### Step 1 — Identify the subject

- Exposure-id → fetch the single exposure record.
- CVE → fetch all matching exposures in the account scope (filter `exposure.mappedAttributes.vulnerabilityIds = 'CVE-X' AND exposure.status = 'Open'`). If many, ask the user whether to plan for all, a subset, or give a CVE-level summary.
- Vulnerability name (no CVE) → resolve via `searchVulnerabilityData` on name/aliases; confirm with the user.

### Step 2 — Read platform remediation fields first

Fetch the exposure(s) with `searchExposureData`. Always include at minimum:

```json
"fields": [
  "exposure.exposureId",
  "exposure.title",
  "exposure.scores.scoreLevel",
  "exposure.scores.overallScore",
  "exposure.mappedAttributes.vulnerabilityIds",
  "exposure.mappedAttributes.vendorRemediation",
  "exposure.remediationTarget.status",
  "exposure.remediationTarget.dueDate",
  "exposure.remediationTarget.priority",
  "asset.criticality",
  "asset.reachability"
]
```

For richer coverage (account-specific integration fields), pre-discover via `getApiFields(entityType=['EXPOSURE'], searchText='remediation')` and append matched `apiPath`s.

**The canonical field :**

| Field | Notes |
|---|---|
| **`exposure.mappedAttributes.vendorRemediation`** | **Primary source of scanner-provided remediation text. Always request this field first.** Example real value: *(example: a vendor advisory patch instruction)* |
| `genericExposure.vulnerability.attributes.vendorRemediation` | Alternate path on generic-connector exposures |

Secondary / structured remediation fields (also populated on most accounts):

| Field | Type | Use |
|---|---|---|
| `exposure.remediationTarget.status` | enum `On Track / Overdue / Met / Missed` | SLA state |
| `exposure.remediationTarget.dueDate` | date | Due date |
| `exposure.remediationTarget.priority` | string (`P1`, `P2`, …) | Priority band |
| `exposure.remediationTarget.targetDays` | integer | SLA target window |
| `exposure.scores.remediationScore` | number | Platform-computed remediation urgency |

Account-specific integration fields may exist (Qualys, Tenable, CrowdStrike, Rapid7 — discover via `getApiFields(entityType=['EXPOSURE'], searchText='remediation')`). Present whatever is populated, **clearly labeled with the source field**.

### Step 3 — Enrich with asset + vulnerability context, and discover scanner-native remediation

Run in parallel:
- `searchAssetData` (or composite) to get the affected asset's OS, version, criticality, reachability.
- `searchVulnerabilityData` for the CVE record if not already fetched — confirm severity, KEV, exploit status.
- **`getConfiguredIntegrations`** — critical step. From the response, identify which SCANNER integration produced the exposure (match the exposure's scanner source to an integration's `prefix`). Then call:
  ```text
  getApiFields(entityType=['EXPOSURE'], fetchGroups='<PREFIX>', searchText='remediation')
  getApiFields(entityType=['EXPOSURE'], fetchGroups='<PREFIX>', searchText='solution')
  getApiFields(entityType=['EXPOSURE'], fetchGroups='<PREFIX>', searchText='fix')
  ```
  to enumerate that scanner's remediation/solution/fix fields. Add those paths to your `searchExposureData` `fields` array to pull the scanner-native remediation text. Common integrations and their typical remediation fields:
  - **Qualys VMDR/EASM** (`Q-VMDR`, `Q-EASM`, `Q-PC`, `Q-WAS`) — `solution` field
  - **Tenable Nessus / IO / SC** (`NESSUS`, `TIO_QA`, `TSC`) — `solution` field
  - **Rapid7 InsightVM / Nexpose** (`IVM`, `IVM_CLOUD`, `NEXPOSES`) — `solution` field
  - **WIZ** (`WIZ`) — remediation steps in the finding record
  - **CrowdStrike Falcon Spotlight** (`FS`) — `remediation` field
  - **Snyk** (`SNYK`) — `fixedIn` / `remediation`

  Ticketing integrations (`type = 'TICKETING'`, e.g. `SERVICE_NOW_INCIDENT`) surface draft-ticket handoff options in Step 5.

### Step 4 — Ask before web-searching

The platform remediation content is often sufficient. Before running web search, ask:

> "I found remediation guidance in the platform (sources: <list>). Want me to also search vendor advisories / KBs on the web for more depth? (Y/n)"

If the user says yes, proceed to Step 5. If no, skip to Step 6.

### Step 5 — (Opt-in) Web-search vendor advisories

Only when the user confirmed. Search for:
1. The official vendor advisory for the CVE.
2. KB article or release notes for the fixed version.
3. Known workarounds / compensating controls.

Read the content — do not just link. Quote the specific steps. See [references/patch-lookup-patterns.md](references/patch-lookup-patterns.md).

### Step 6 — Construct the fix plan

Organize findings into this structure. Fields you couldn't populate (because the platform didn't have them and web search was declined) are explicitly marked "not available".

```markdown
## Remediation Plan — <CVE or exposure id>

**Subject:** <CVE> on <asset hostname>
**Severity:** <Critical/High/Medium/Low/Info> (KEV: yes/no, overallScore: <>)
**Remediation status:** <On Track / Overdue / Met / Missed> (due <date>, priority <P1/P2/…>)
**Asset:** <hostname> — <OS + version>, criticality <numeric 1–5>, reachability <Exposed / NotExposed>

### Remediation guidance from the platform
_Source: `<field path>` (integration: `<name>`)_
> <quoted content>

_Source: `<another field>`_
> <quoted content>

### Fixed version (if known)
- <version> — source: `<field path>` or vendor advisory

### Workaround
- <quoted or "none documented in platform record">

### Compensating controls
- <quoted or "none documented; consider WAF / network segmentation">

### Pre-patch risk (from platform)
- Other open exposures on the same asset(s): <list or "none">
- Asset criticality: <>
- Reachability: <>

### Ticketing draft (copy-paste)
**Title:** Patch <CVE> on <asset>
**Body:**
> <all of the above, with platform deep link>
> — Drafted by Claude + securin-remediation-guidance. Create manually in your ticketing system (MCP M1 is read-only for write actions).

### Platform links
- Exposure record: <url>
- Vulnerability record: <url>
- All open exposures for this CVE in your account: <url>

### Additional web-sourced references (if the user opted in)
- Vendor advisory: <url> — quoted excerpt: <…>
- KB article: <url> — quoted excerpt: <…>
```

## Handoff (draft, don't create)

If `getConfiguredIntegrations` shows a ticketing integration (Jira, ServiceNow) configured:
- Draft a ticket body suitable for copy-paste.
- **Do not create the ticket.** Write actions are out of scope for MCP Milestone 1.

See [references/patch-lookup-patterns.md](references/patch-lookup-patterns.md) for platform-specific upgrade command templates and ticket boilerplate.

## Edge cases

- **Platform has zero remediation content for this exposure** — tell the user explicitly. Offer web search as an opt-in.
- **Exposure is a misconfiguration (no CVE)** — `exposure.mappedAttributes.remediation` or scanner-native `solution` is usually the best source; skip CVE queries.
- **Multi-CVE exposure** — pull remediation content per CVE; deduplicate if multiple CVEs share the same fix.
- **True zero-day (no patch yet)** — the platform likely has `vulnerabilities.tags = 'Zero Day'` set; route via `securin-zero-day-exposure-analysis` for compensating-controls guidance.
- **Asset is EOL** — flag; upgrade may not be possible, recommend isolation / replacement.

## Scope guard (CC-3)

- Global CVE intel (no specific fix plan) → `securin-cve-enrichment`.
- Prioritization across many exposures → `securin-exposure-triage`.
- "Am I affected by threat X" → `securin-threat-correlation`.
- Zero-day-specific analysis → `securin-zero-day-exposure-analysis`.
- Unknown platform capability → `securin-tool-search`.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](references/_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Patch Lookup Patterns](references/patch-lookup-patterns.md) — platform upgrade-command templates, ticket boilerplate.
- [Shared: Account Preflight](references/_shared/account-preflight.md)
- [Shared: Composite vs Source](references/_shared/composite-vs-source.md)
- [Shared: Deep Links](references/_shared/deep-links.md)
- [Shared: FQL Grammar](references/_shared/fql-grammar.md)
- [Shared: Sorting Rules](references/_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](references/_shared/brand.md)
