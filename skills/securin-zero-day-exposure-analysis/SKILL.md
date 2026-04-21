---
name: securin-zero-day-exposure-analysis
description: >
  Use this skill when the user asks to "analyze zero-day exposure", "am I
  exposed to zero-days", "show me my zero-day risk", "what zero-days affect
  my environment", "check if we're exposed to [named zero-day like Regresshell
  or Citrix Bleed]", or needs a report of zero-day vulnerabilities correlated
  to the user's assets/exposures. Requires the Securin Platform MCP server.
---

# Zero-Day Exposure Analysis

## Purpose

Identify the user's exposure to **zero-day vulnerabilities** — CVEs that are actively exploited in the wild before a patch is widely available. Two modes:

1. **Broad scan** — "what zero-days am I exposed to right now?" Enumerate all open exposures whose linked vulnerability carries the `Zero Day` tag.
2. **Named zero-day** — "am I affected by [name, e.g., Regresshell / Citrix Bleed]?" Resolve the name to CVE IDs via Core, then correlate to the user's environment.

Zero-days often lack a vendor patch at discovery time, so remediation emphasis shifts to **compensating controls**, **detection rules**, and **scope containment**.

## When to use

- "Am I exposed to any zero-days?"
- "Show me my open zero-day exposures"
- "Am I affected by [named zero-day]?"
- "List zero-day vulnerabilities in my environment"
- "Zero-day risk report for my account"

## Pre-flight

### Step 0 — Account preflight (CC-1)

See [_shared/account-preflight.md](../_shared/account-preflight.md). Required — exposure matches are scoped to the resolved account-id.

### Step 0.5 — Composite vs source (if asset pivot is needed)

See [_shared/composite-vs-source.md](../_shared/composite-vs-source.md). Only matters when the report includes affected-asset context.

## Suggested tools

### Pre-flight
- `getUserProfile`, `getEffectiveAccess`, `getEffectiveAccessWorkspaces`

### Core intelligence
- `searchVulnerabilityData` — Core index; filter by `tags = 'Zero Day'` or name/alias
- `searchThreatActorData` — threat actors behind the zero-day (pass `fields: ['threatActor']`)

### Environment correlation
- `searchExposureData` / `aggregateExposureData` / `hybridExposureData` — match CVEs to open exposures
- `searchAssetData` / `hybridAssetData` (or composite variants) — pivot to affected assets
- `searchComponentData` — component-level matches

### Field discovery
- `getApiFields(entityType=['VULNERABILITY'], searchText='tag')` — confirm tag field path
- `getTopValues(field='vulnerabilities.tags', entityType='VULNERABILITY')` — see what tags exist in this account's Core index

### Deep links (CC-2)
- `filterToChipPost` — convert FQL filter → chip form for a platform URL (default, Strategy A).
- `createDeepLink` — only if the user explicitly asks to save/share the view (Strategy B; write op, needs `x-user-id` + `shareWith`).
- `getDeepLink` / `aggregateByDeepLink` — retrieve a saved short-code.
- See [_shared/deep-links.md](../_shared/deep-links.md).

### Outside
- **Web search** — resolve named zero-days (e.g., "Regresshell", "Citrix Bleed", "MOVEit") to CVE IDs when Core doesn't match on alias.

## Mode A — Broad zero-day scan

User asks "am I exposed to any zero-day?" / "show me my zero-day risk".

### Step A.1 — Inventory your environment's zero-day exposures

```text
hybridExposureData
filter: exposure.status = 'Open'
        AND vulnerabilities.tags = 'Zero Day'
groupByField: exposure.scores.scoreLevel
aggs: [{function: TERMS, field: exposure.scores.scoreLevel, name: 'bySeverity', size: 10}]
sort: "exposures.scores.score:desc,exposure.remediationTarget.dueDate:asc"
limit: 100
page: 1
```

The `vulnerabilities.tags = 'Zero Day'` cross-entity join pulls from the vulnerability index (bare path `tags = 'Zero Day'` in Core).

### Step A.2 — Enrich with CVE-level signals

Collect distinct CVE IDs from Step A.1 results. For each (or batched):

```text
searchVulnerabilityData
filter: vulnerabilityId in ['CVE-…','CVE-…']
fields: ['vulnerability']
sort: "riskIndex.index:desc"
```

Capture: KEV status, exploitation status, risk index, published date, affected products.

### Step A.3 — Pivot to affected assets

```text
searchAssetData   # or searchCompositeAssetData
filter: asset.assetId in [<ids from A.1>]
sort: "asset.scores.overallScore:desc,asset.criticality:desc"
fields: ['asset']
limit: 50
```

### Step A.4 — Emit report

```markdown
## Zero-Day Exposure Assessment — <account>

**Verdict:** <N open zero-day exposures across M assets; K CVEs; J KEV-tagged>

### Zero-day CVEs in your environment
| CVE | Risk Index | KEV | Exploited | # Exposures | # Assets | Platform link |
|---|---|---|---|---|---|---|
| … | … | ✓/✗ | ✓/✗ | … | … | <url> |

### Open zero-day exposures — by severity
- Critical: <count> — <platform filter url>
- High: <count> — <url>
- Medium: <count> — <url>
- Low: <count> — <url>

### Top affected assets
| Asset | Criticality | Reachability | Workspace | # Zero-day exposures | Platform link |
|---|---|---|---|---|---|
| … | … | … | … | … | <url> |

### Recommended next steps
- Remediation planning: `securin-remediation-guidance` for each CVE — zero-days often have no patch yet, so expect compensating-control emphasis.
- Threat actor context: `securin-threat-correlation` if you want to know who's exploiting these.
- Detailed CVE intel: `securin-cve-enrichment` for any single zero-day.
```

## Mode B — Named zero-day

User asks "am I affected by Regresshell / Citrix Bleed / MOVEit / <named event>?"

### Step B.1 — Resolve the name to CVE IDs

Try Core first:

```text
searchVulnerabilityData
filter: tags = 'Zero Day' AND (aliases like '<name>' OR title like '<name>')
fields: ['vulnerability']
limit: 10
```

If Core matches → use the returned `vulnerabilityId`s.

If Core doesn't match (very new or informal name):
1. Web search for the event + "CVE".
2. Present the resolved CVE list to the user: *"I found <CVE list> for '<name>'. Confirm before I correlate to your environment."*
3. Only correlate after confirmation.

### Step B.2 — Correlate to environment

```text
hybridExposureData
filter: exposure.mappedAttributes.vulnerabilityIds in [<cve list>]
        AND exposure.status = 'Open'
groupByField: asset.workspaceId
aggs: [{function: TERMS, field: asset.workspaceId, name: 'byWorkspace', size: 20},
       {function: COUNT, field: exposure.exposureId, name: 'totalExposures'}]
limit: 100
page: 1
sort: "exposures.scores.score:desc"
```

### Step B.3 — Enrich and report

Run the affected-assets pivot as in Mode A.3, then emit a named-zero-day report:

```markdown
## Zero-Day Exposure — <Named Event>

**Mapped CVEs:** <list>
**Verdict:** AFFECTED / NOT AFFECTED / PARTIAL — <N exposures, M assets>

### Matched exposures
| CVE | Severity | Asset | Workspace | SLA | Platform link |
|---|---|---|---|---|---|

### Recommended next steps
- Remediation (likely compensating controls): `securin-remediation-guidance`
- Global intel on the event: `securin-cve-enrichment` for each CVE
```

## FQL patterns

### Zero-day tag filter in exposure context
```text
exposure.status = 'Open' AND vulnerabilities.tags = 'Zero Day'
```

### Zero-day filter in Core (bare path — no `vulnerabilities.` prefix)
```text
tags = 'Zero Day'
```

### Zero-day + KEV (most urgent subset)
```text
exposure.status = 'Open'
AND vulnerabilities.tags = 'Zero Day'
AND vulnerabilities.exploitation.isCisaKev = true
```

### Zero-day on exposed-to-internet prod assets (compound)
```text
exposure.status = 'Open'
AND vulnerabilities.tags = 'Zero Day'
AND asset.reachability = 'Exposed'                      # source-model
AND asset.workspaceId in [<prod-ws-ids>]
```

Substitute `compositeAsset.*` in composite-data accounts — see [_shared/composite-vs-source.md](../_shared/composite-vs-source.md).

## Sorting

Default: `exposures.scores.score:desc, exposure.remediationTarget.dueDate:asc` — worst first, SLA tiebreaker.

Alternative for "worst externally-facing first":
`asset.reachability:desc, exposures.scores.score:desc` (if the platform supports ordinal sort on reachability; confirm via `getSortFields=true` 🧪).

## Scope guard (CC-3)

- Single-CVE deep dive with no environment angle → `securin-cve-enrichment`.
- Broad exposure triage beyond zero-days → `securin-exposure-triage`.
- Remediation plan for a specific zero-day → `securin-remediation-guidance`.
- Threat actor attribution for a zero-day → `securin-threat-correlation`.

## Edge cases

- **No zero-day tag in the account** — Core may tag these differently (`"0-day"`, `"zero day"`). Call `getTopValues(field='vulnerabilities.tags')` to enumerate actual values and adjust the filter.
- **User's named event has no CVE yet** — tell them; offer to set up a follow-up check once a CVE is published.
- **Zero-day with patch now available** — still tagged zero-day in Core; route remediation normally.
- **False positives** — some scanners over-detect; surface the scanner source in the report so the user can filter.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](../_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Shared: Account Preflight](../_shared/account-preflight.md)
- [Shared: Composite vs Source](../_shared/composite-vs-source.md)
- [Shared: Deep Links](../_shared/deep-links.md)
- [Shared: FQL Grammar](../_shared/fql-grammar.md)
- [Shared: Sorting Rules](../_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](../_shared/brand.md)
