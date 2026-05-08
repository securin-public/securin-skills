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

Ad-hoc search, filtering, and aggregation of the user's **exposures** — instances of vulnerabilities, misconfigurations, or findings discovered in their environment. Translate questions like "show me all open critical exposures breaching SLA" into the correct `search*Data` / `aggregate*Data` call with proper scoping and deep links.

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

See [_shared/account-preflight.md](references/_shared/account-preflight.md). Resolve account-id(s) and validate access before any query. If the question implies a workspace subset, resolve workspace-ids too.

> Note: the exposure index is **not** affected by the composite-vs-source data model (that flag only affects assets). But cross-entity exposure filters that reference asset fields still need the correct asset prefix — see [_shared/composite-vs-source.md](references/_shared/composite-vs-source.md).

## Suggested tools

### Primary
- `searchExposureData` — flat list
- `aggregateExposureData` — bucketed count (TERMS) and time-bucketed histogram (DATE_HISTOGRAM)
- `aggregateVulnerabilityTimelineData` / `searchVulnerabilityTimelineData` — historical vulnerability state changes over time (if available for account; fall back to DATE_HISTOGRAM if 404)

### Supporting
- `getApiFields` with `entityType: ["EXPOSURE"]` — field discovery
- `getGroupByFields` — valid aggregation dimensions
- `getTopValues` — enum values for a field
- `getDefaultViewForGroupByField` — platform's default column set for a grouping
- `validateFilter` — FQL construction + validation
- `getEffectiveAccessWorkspaces` — workspace scoping

### Deep links (CC-2)
- `createDeepLink` (preferred)
- `aggregateByDeepLink` — aggregation + per-bucket URLs
- `getDeepLink` — URL for a known exposure-id

See [_shared/deep-links.md](references/_shared/deep-links.md).

## Workflow

### Step 1 — Classify the ask

| Shape | Example | Tool |
|---|---|---|
| Flat list | "List open critical exposures" | `searchExposureData` |
| Single-field bucket | "Exposures by severity" | `aggregateExposureData` |
| Time series | "Exposures created per week over 6 months" | `aggregateVulnerabilityTimelineData` or `aggregateExposureData` DATE_HISTOGRAM |
| Aggregation with per-bucket deep links | "Bucket counts, clickable" | `aggregateByDeepLink` |

### Step 2 — Discover fields if uncertain

```text
getApiFields(entityType=["EXPOSURE"])
getTopValues(field="exposure.status")
getGroupByFields(entityType="EXPOSURE")
```

### Step 3 — Compose FQL

See [_shared/fql-grammar.md](references/_shared/fql-grammar.md). Exposure-specific patterns:

```text
exposure.status = 'Open'
exposure.scores.scoreLevel = 'Critical'
"exposure.scores.overallScore" >= 7.0  # filter-only — NOT a valid sort key; sort uses exposures.scores.score:desc
"exposure.firstSeenAt" >= "2026-01-01T00:00:00Z"
exposure.remediationTarget.status = 'Overdue'
exposure.assignments.assignedTo.name = 'team:remediation'
exposure.mappedAttributes.vulnerabilityIds = 'CVE-2024-3400'
exposure.mappedAttributes.type like 'Vulnerability'
```

Cross-entity filters (exposure → vuln / asset):

```text
# Exposures tied to a specific CVE — correct cross-entity field is vulnerabilities.id
vulnerabilities.id = 'CVE-2024-3400'
# ❌ vulnerabilities.vulnerabilityId  → 400 Invalid field
# ❌ vulnerabilities.cveId           → 400 Invalid field

# Exposures tied to exploited vulnerabilities
vulnerabilities.isCisaKEV = true

# Exposures on exposed-to-internet assets (source-model account)
asset.reachability = 'Exposed'

# Same, composite-model account
compositeAsset.reachability = 'Exposed'
```

### Step 4 — Pick and call the right tool

- For time series: try `aggregateVulnerabilityTimelineData` / `searchVulnerabilityTimelineData` first. If those return 404, fall back to `aggregateExposureData` with `DATE_HISTOGRAM`.
- For per-bucket deep links, prefer `aggregateByDeepLink`.

#### `aggregateExposureData` — correct request shape

`function` is a **string**, `field` is the key (not `apiPath`), and a `subAggs` COUNT is required:

```json
{
  "filters": "exposure.status = 'Open'",
  "aggs": [{
    "name": "bySeverity",
    "function": "TERMS",
    "field": "exposure.scores.scoreLevel",
    "size": 10,
    "subAggs": [{"name": "count", "function": "COUNT", "field": "exposure.exposureId"}]
  }]
}
```

Common mistakes that cause 400/500:
- ❌ `"function": {"type": "TERMS", "field": "..."}` — function must be a string, not an object
- ❌ `"apiPath": "..."` — key must be `"field"`, not `"apiPath"`
- ❌ `"field": "exposure.workspaceId"` — returns 500; use `"asset.workspaces.name"` for workspace grouping

#### `aggregateExposureData` with `DATE_HISTOGRAM` — time series shape

Different structure from TERMS: nested aggs use `"aggs"` (not `"subAggs"`), and `interval` must be **Title Case**. `isFixedInterval`, `extendedBounds`, and `hardBounds` are required:

```json
{
  "aggs": [{
    "function": "DATE_HISTOGRAM",
    "name": "openedByMonth",
    "field": "exposure.firstDiscoveredOn",
    "interval": "Month",
    "isFixedInterval": false,
    "extendedBounds": {"min": "2025-11-01T00:00:00Z", "max": "now"},
    "hardBounds": {"min": "2025-11-01T00:00:00Z"},
    "aggs": [{"function": "COUNT", "name": "count", "field": "exposure.exposureId"}]
  }]
}
```

Valid `interval` values (Title Case only): `"Day"`, `"Week"`, `"Month"`, `"Quarter"`, `"Year"`.
❌ `"month"`, `"MONTH"`, `"1M"`, `"MONTHLY"` all return 400.

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

Run `aggregateExposureData` once per dimension (two calls):
```json
// Call 1 — by severity
{
  "filters": "exposure.status = 'Open'",
  "aggs": [{"name": "bySeverity", "function": "TERMS", "field": "exposure.scores.scoreLevel", "size": 10,
            "subAggs": [{"name": "count", "function": "COUNT", "field": "exposure.exposureId"}]}]
}

// Call 2 — by workspace (use asset.workspaces.name — exposure.workspaceId returns 500)
{
  "filters": "exposure.status = 'Open'",
  "aggs": [{"name": "byWorkspace", "function": "TERMS", "field": "asset.workspaces.name", "size": 25,
            "subAggs": [{"name": "count", "function": "COUNT", "field": "exposure.exposureId"}]}]
}
```



## Scope guard (CC-3)

- Global CVE details → hand off to `securin-cve-enrichment`.
- "Am I affected by threat X" → hand off to `securin-threat-correlation`.
- "How do I fix this exposure" → hand off to `securin-remediation-guidance`.
- Pure asset questions → hand off to `securin-asset-triage`.
- Unknown tool needed → `securin-tool-search`.

## Edge cases

- **Empty result on cross-entity filter** — check asset prefix (`asset.*` vs `compositeAsset.*`) matches the account's data model.
- **Custom statuses** — accounts can customize the exposure state machine; use `getTopValues(field="exposure.status")` to enumerate.
- **Very wide time windows** — lean on `aggregateExposureData` (TERMS or DATE_HISTOGRAM) rather than raw listing.
- **Tags / custom attributes** — `exposure.tags`, `exposure.customAttributes.*` are discoverable via `getApiFields`.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](references/_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Exposure Fields Quickref](references/exposure-fields.md)
- [Shared: Account Preflight](references/_shared/account-preflight.md)
- [Shared: Composite vs Source](references/_shared/composite-vs-source.md)
- [Shared: Deep Links](references/_shared/deep-links.md)
- [Shared: FQL Grammar](references/_shared/fql-grammar.md)
- [Shared: Sorting Rules](references/_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](references/_shared/brand.md)
