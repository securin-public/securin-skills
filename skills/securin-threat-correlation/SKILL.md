---
name: securin-threat-correlation
description: >
  Use this skill when the user asks "am I affected by this CVE", "does this
  threat affect my environment", "check if we're vulnerable to [ransomware /
  threat actor]", "correlate threats with my exposures", "what threats target
  my vulnerabilities", "show me the intersection of <threat> and my environment",
  or any question that bridges external threat intelligence with the user's
  specific assets and exposures. For pure CVE intelligence without environment
  matching use securin-cve-enrichment. Requires the Securin Platform MCP server.
---

# Threat Correlation

## Purpose

Bridge **external threat intelligence** (CVEs, ransomware families, threat actors, campaigns) with the **user's environment** (assets, exposures, components). Answer the core question: *"Does this threat matter to me right now?"*

This skill is the inverse of `securin-cve-enrichment`: enrichment produces a global report on a CVE; correlation intersects that CVE (or a threat, or an actor's TTPs) with the user's real data.

## When to use

- "Am I affected by CVE-2024-3400?"
- "Does this ransomware campaign hit my environment?"
- "Check if we're vulnerable to Lazarus Group"
- "Show me exposures tied to CISA KEV entries"
- "Which of my open exposures are exploited in the wild?"
- "What threats target the CVEs in my environment?" *(outbound direction)*

## Pre-flight

### Step 0 — Account preflight (CC-1)

See [_shared/account-preflight.md](../_shared/account-preflight.md). Correlation queries always touch the user's environment — you must resolve account-id(s) and validate access before any exposure/asset query. Also detect the composite-vs-source data model (see [_shared/composite-vs-source.md](../_shared/composite-vs-source.md)) to use the correct asset prefix.

## Suggested tools

### Threat intel (global)
- `searchVulnerabilityData` — CVE record + exploitation signals
- `searchThreatActorData` — threat actor → CVE list. Pass `fields: ['threatActor']` in the request
- `searchWeaknessData` — CWE root cause

### User environment
- `searchExposureData` / `aggregateExposureData` / `hybridExposureData` — match CVEs to open exposures
- `searchAssetData` / `hybridAssetData` (or composite variants) — pivot exposures → affected assets
- `searchComponentData` / `hybridComponentData` — component-level matches (SBOM-style)

### Scoping + access
- `getEffectiveAccessWorkspaces`
- `getAccountSettings` — composite FF check
- `getApiFields` — field discovery

### Deep links (CC-2)
- `createDeepLink` (preferred)
- `aggregateByDeepLink`
- `getDeepLink`

### Outside
- **Web search** — resolve named campaigns / news events to CVE lists when the user's input is a name, not a CVE.

## Core concept — two-step correlation

```
Step 1: Threat Intelligence  →  Extract CVEs / indicators
Step 2: Your Environment     →  Find matching exposures / assets / components
Result: Threat Exposure Assessment
```

Two strategies based on direction.

## Strategy A — Inbound (Threat → You)

The user starts with a threat and wants to know if they're affected.

### A.1 Resolve threat → CVE list

| If the user said… | Do |
|---|---|
| `CVE-XXXX-YYYY` | Already a CVE — skip to A.2 |
| A threat-actor name (e.g., "Lazarus") | `searchThreatActorData` with bare-path filter `name like 'Lazarus'`, `fields: ['threatActor']` → collect `mappedAttributes.cveIds` |
| A ransomware family (e.g., "LockBit") | **Use web search** — resolve the family to a CVE list via published threat-intel and confirm with the user|
| A campaign / news event | Web search to resolve to CVE list, then confirm with the user before proceeding |

### A.2 Query exposures for the CVE set

```text
hybridExposureData
filter: exposure.mappedAttributes.vulnerabilityIds in [<cve-list>]
        AND exposure.status = 'Open'
        AND "<account/workspace scope>"
groupByField: "exposure.scores.scoreLevel"
aggs: [{type: "count"}]
```

If the set is small, also call `searchExposureData` for an itemized list.

### A.3 Pivot to affected assets

Using `assetId`s from the exposures (or a separate join):

```text
searchAssetData                          # or searchCompositeAssetData
filter: asset.assetId in [<asset-ids from A.2>]
sort: "asset.scores.overallScore:desc"
```

### A.4 Generate deep links (CC-2)

- One top-level filter link (Exposures view with the CVE-list filter).
- Per-row link for each affected asset / exposure.
- Per-bucket link in the severity breakdown.

### A.5 Emit "Threat Exposure Assessment"

```markdown
## Threat Exposure Assessment — <threat name or CVE>

**Verdict:** AFFECTED / NOT AFFECTED / PARTIAL — <N matched exposures across M assets>

### Matched CVEs
| CVE | Severity | KEV | # Exposures | Link |
|---|---|---|---|---|
| … | … | … | … | [View](<deep link>) |

### Affected Assets
| Asset | Criticality | Reachability | Workspace | # Matched Exposures | Link |
|---|---|---|---|---|---|
| … | … | … | … | … | [View](<deep link>) |

### Severity Breakdown
- Critical: 3 → [View](…)
- High: 11 → [View](…)
- Medium: 27 → [View](…)

### Recommended next steps
- Top-priority remediation: hand off to **securin-remediation-guidance** for CVE-XXXX
- Triage the full list: hand off to **securin-exposure-triage** for SLA review
```

## Strategy B — Outbound (You → Threats)

The user starts with an asset or exposure and wants to know what threats target them.

### B.1 Collect CVEs in the user's scope

```text
aggregateExposureData                    # or hybrid for compound
groupByField: "exposure.mappedAttributes.vulnerabilityIds"
filter: exposure.status = 'Open' AND "<scope>"
```

### B.2 Enrich each CVE with threat signals

For each CVE (or batched):

```text
searchThreatActorData  filter: ...mappedAttributes.cveIds = "CVE-X", fields: ["threatActor"]
searchVulnerabilityData filter: vulnerabilityId = 'CVE-X'
```

### B.3 Emit "What Hunts Me" report

```markdown
## What Hunts Me — <account / workspace scope>

**Top threats targeting your open exposures:**

| Threat / Actor | Type | Your exposed CVEs | # Affected Assets | Link |
|---|---|---|---|---|
| LockBit 3.0 | Ransomware | CVE-…, CVE-… | 14 | [View](…) |
| APT29 | State actor | CVE-…, CVE-… | 3 | [View](…) |

### Recommended next steps
- Deep-dive a specific threat → **securin-cve-enrichment** for the CVE
- Remediation planning → **securin-remediation-guidance**
```

## FQL patterns

See [_shared/fql-grammar.md](../_shared/fql-grammar.md) for full grammar. Correlation-specific:

```text
# Exposures matching a CVE set
"exposure.mappedAttributes.vulnerabilityIds" in ['CVE-X','CVE-Y','CVE-Z']

# Exposures on exposed-to-internet assets (source-model)
asset.reachability = 'Exposed'
# Same, composite-model
compositeAsset.reachability = 'Exposed'

# Exposures tied to CISA KEV CVEs (cross-entity to vuln index from exposures)
vulnerabilities.exploitation.isCisaKev = true

# In searchVulnerabilityData — bare path, no "vulnerabilities." prefix
vulnerabilityId = 'CVE-X'
exploitation.isCisaKev = true
```

- `searchThreatActorData` with no `filters` → an error. Always pass a filter + `fields: ['threatActor']`.
- THREATACTOR field namespace is bare (`name`, `description`, `vulnerabilityCount`, `originCountry`, `targetedCountries`, `targetedIndustries`, `associatedGroups`) — no `threatActor.` prefix.
- `validateFilter` only checks FQL syntax — it does not verify field existence. Always cross-check paths against `getApiFields`.

## Scope guard (CC-3)

- Global CVE intel only (no environment match) → `securin-cve-enrichment`.
- Raw exposure triage (no external threat angle) → `securin-exposure-triage`.
- Asset inventory only → `securin-asset-triage`.
- Remediation planning → `securin-remediation-guidance`.
- Unknown capability → `securin-tool-search`.

## Edge cases

- **Named campaign doesn't map cleanly to CVEs** — ask the user to confirm the CVE list from web search before correlating.
- **Zero matches** — sanity-check composite vs source prefix (#1 cause of silent empties), verify account/workspace scope, verify the `exposure.status` filter isn't too narrow.
- **Threat actor with 200+ CVEs** — don't match all 200 blindly. Prioritize by CISA KEV / `exploitedInWild` first, then correlate.
- **New zero-day before it's in the platform** — web search may find the CVE before it's indexed; tell the user it's not yet in Core and offer to check back later.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](../_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Correlation Patterns](references/correlation-patterns.md)
- [Shared: Account Preflight](../_shared/account-preflight.md)
- [Shared: Composite vs Source](../_shared/composite-vs-source.md)
- [Shared: Deep Links](../_shared/deep-links.md)
- [Shared: FQL Grammar](../_shared/fql-grammar.md)
- [Shared: Sorting Rules](../_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](../_shared/brand.md)
