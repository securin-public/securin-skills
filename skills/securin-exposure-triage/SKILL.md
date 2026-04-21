---
name: securin-exposure-triage
description: >
  Use this skill when the user asks to "find exposures where...", "show open
  critical exposures", "how many exposures...", "break down exposures by
  severity/status/SLA", "list exposures in my environment matching...",
  "exposure distribution", "exposures over time", or any ad-hoc exposure search /
  filter / aggregation. Use this for exposure records specifically (instances
  found in the user's environment); for global CVE intelligence use
  securin-cve-enrichment. Requires the Securin Platform MCP server.
---

# Exposure Triage

## Purpose

Ad-hoc search, filtering, and aggregation of the user's **exposures** — instances of vulnerabilities, misconfigurations, or findings discovered in their environment. Translate questions like "show me all open critical exposures breaching SLA" into the correct `search*Data` / `aggregate*Data` / `hybrid*Data` call with proper scoping and deep links.

An *exposure* is an instance (e.g., "CVE-2024-3400 on host web-01"). A *vulnerability* is the global CVE record. This skill is about exposures; use `securin-cve-enrichment` for vulnerability intel.

## When to use

- "Show me all open critical exposures"
- "How many exposures are breaching SLA?"
- "Break down exposures by severity and workspace"
- "List exposures older than 90 days"
- "Exposure volume over time" / "new vs closed exposures"
- "Show me exposures tied to CVE-2024-3400"
- "Which exposures are on exposed-to-internet assets?"

## Pre-flight

### Step 0 — Account preflight (CC-1)

See [_shared/account-preflight.md](../_shared/account-preflight.md). Resolve account-id(s) and validate access before any query. If the question implies a workspace subset, resolve workspace-ids too.

> Note: the exposure index is **not** affected by the composite-vs-source data model (that flag only affects assets). But cross-entity exposure filters that reference asset fields still need the correct asset prefix — see [_shared/composite-vs-source.md](../_shared/composite-vs-source.md).

## Suggested tools

### Primary
- `searchExposureData` — flat list
- `aggregateExposureData` — single-field bucketed count
- `hybridExposureData` — compound-filter + aggregation (requires `groupByField`)
- `searchViStatsData` — vulnerability-instance stats (time series, trend aggregations)
- `aggregateVulnerabilityTimelineData` / `searchVulnerabilityTimelineData` / `hybridVulnerabilityTimelineData` — time-series shape

### Supporting
- `getApiFields` with `entityType: ["EXPOSURE"]` — field discovery
- `getGroupByFields` — valid aggregation dimensions
- `getTopValues` — enum values for a field
- `getDefaultViewForGroupByField` — platform's default column set for a grouping
- `filterToChip` / `filtersToChip` / `validateFilter` — FQL construction + validation
- `getEffectiveAccessWorkspaces` — workspace scoping

### Deep links (CC-2)
- `createDeepLink` (preferred)
- `aggregateByDeepLink` — aggregation + per-bucket URLs
- `getDeepLink` — URL for a known exposure-id

See [_shared/deep-links.md](../_shared/deep-links.md).

## Workflow

### Step 1 — Classify the ask

| Shape | Example | Tool |
|---|---|---|
| Flat list | "List open critical exposures" | `searchExposureData` |
| Single-field bucket | "Exposures by severity" | `aggregateExposureData` |
| Compound filter + aggregation | "Open critical on prod, grouped by workspace" | `hybridExposureData` + `groupByField` |
| Time series | "Exposures created per week over 6 months" | `searchViStatsData` / `*VulnerabilityTimelineData` |
| Aggregation with per-bucket deep links | "Bucket counts, clickable" | `aggregateByDeepLink` |

### Step 2 — Discover fields if uncertain

```text
getApiFields(entityType=["EXPOSURE"])
getTopValues(field="exposure.status")
getGroupByFields(entityType="EXPOSURE")
```

### Step 3 — Compose FQL

See [_shared/fql-grammar.md](../_shared/fql-grammar.md). Exposure-specific patterns:

```text
exposure.status = 'Open'
exposure.scores.scoreLevel = 'Critical'
"exposure.scores.overallScore" >= 7.0
"exposure.firstSeenAt" >= "2026-01-01T00:00:00Z"
exposure.remediationTarget.status = 'Overdue'
exposure.assignedTo = 'team:remediation'
exposure.mappedAttributes.vulnerabilityIds = 'CVE-2024-3400'
exposure.mappedAttributes.type like 'Vulnerability'
```

Cross-entity filters (exposure → vuln / asset):

```text
# Exposures tied to exploited vulnerabilities
vulnerabilities.exploitation.isCisaKev = true

# Exposures on exposed-to-internet assets (source-model account)
asset.reachability = 'Exposed'

# Same, composite-model account
compositeAsset.reachability = 'Exposed'
```

### Step 4 — Pick and call the right tool

Classification from Step 1. Key rules:

- For time series: `searchViStatsData` exposes pre-aggregated stats; for flexible time buckets use the `*VulnerabilityTimelineData` family.
- For per-bucket deep links, prefer `aggregateByDeepLink`.

### Step 5 — Deep links (CC-2)

Every result table adds a `View in Platform` column. Every bucket in an aggregation gets its own URL. Call `createDeepLink` once per reported scope; `getDeepLink(exposureId)` for individual drill-downs.

### Step 6 — Emit response

```markdown
**Query:** <plain-English restatement>
**Account:** <account name + id>
**Filter:** `<FQL>`

<results table with View-in-Platform links>

[View full list in Platform](<top-level deep link>)

**Observations:**
- <Pattern noted — e.g., "70% of critical exposures are in one workspace">
- <Suggested next step — e.g., "Drill into remediation: use securin-remediation-guidance for the top 3">
```

## Common recipes

### "Open critical exposures breaching SLA"
```text
searchExposureData
filter: exposure.status = 'Open'
        AND exposure.scores.scoreLevel = 'Critical'
        AND exposure.remediationTarget.status = 'Overdue'
sort: "exposures.scores.score:desc"
```

### "Break down exposures by severity and workspace"

Compound filter + two dimensions → `hybridExposureData`:
```text
hybridExposureData
filter: exposure.status = 'Open'
groupByField: exposure.workspaceId   # primary
aggs: [{type: "count", by: "exposure.scores.scoreLevel"}]
```

### "Exposures tied to CISA KEV CVEs in prod"
```text
hybridExposureData
filter: exposure.status = 'Open'
        AND vulnerabilities.exploitation.isCisaKev = true
        AND exposure.workspaceId in [<prod-ws-ids>]
groupByField: "exposure.scores.scoreLevel"
```

### "New vs closed exposures over time"

Use `*VulnerabilityTimelineData` or `searchViStatsData`:
```text
hybridVulnerabilityTimelineData
filter: exposure.firstSeenAt >= today() - 180
groupByField: "exposure.state"   # created vs closed
```

### "MTTR by severity"

Exposures have `remediationDate - firstSeenAt` → query both, compute client-side, or check if the platform exposes an `exposure.timeToRemediate` field via `getApiFields`.

## Scope guard (CC-3)

- Global CVE details → hand off to `securin-cve-enrichment`.
- "Am I affected by threat X" → hand off to `securin-threat-correlation`.
- "How do I fix this exposure" → hand off to `securin-remediation-guidance`.
- Pure asset questions → hand off to `securin-asset-triage`.
- Unknown tool needed → `securin-tool-search`.

## Edge cases

- **Empty result on cross-entity filter** — check asset prefix (`asset.*` vs `compositeAsset.*`) matches the account's data model.
- **Custom statuses** — accounts can customize the exposure state machine; use `getTopValues(field="exposure.status")` to enumerate.
- **Very wide time windows** — lean on `searchViStatsData` or aggregation rather than raw listing.
- **Tags / custom attributes** — `exposure.tags`, `exposure.customAttributes.*` are discoverable via `getApiFields`.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](../_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Exposure Fields Quickref](references/exposure-fields.md)
- [Shared: Account Preflight](../_shared/account-preflight.md)
- [Shared: Composite vs Source](../_shared/composite-vs-source.md)
- [Shared: Deep Links](../_shared/deep-links.md)
- [Shared: FQL Grammar](../_shared/fql-grammar.md)
- [Shared: Sorting Rules](../_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](../_shared/brand.md)
