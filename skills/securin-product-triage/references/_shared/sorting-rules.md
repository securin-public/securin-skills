<!-- Mirrored from skills/_shared/sorting-rules.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

<!-- Mirrored from skills/_shared/sorting-rules.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

# Sorting Rules

Every skill response that lists entities MUST sort results. Randomly-ordered results waste user attention. The sort fields below are the platform's canonical score keys per entity.

## Canonical sort fields (per entity)

| Entity | Sort key | Direction | Notes |
|---|---|---|---|
| **Exposures** | `exposure.scores.score` | `desc` | **Primary risk sort for exposures.** This is the canonical built-in score path (verified against `getApiFields`). |
| **Assets** | `asset.scores.overallScore` | `desc` | **Primary risk sort for assets.** Higher = more at risk. |
| **Vulnerabilities / Weaknesses** | `riskIndex.index` | `desc` | **Primary risk sort for CVEs / CWEs.** |
| **Components** | `riskAssessment.score` | `desc` | **Primary risk sort for components.** |

## Secondary sort fields — dates, priority, enum severity

| Field | Direction | When |
|---|---|---|
| `exposure.remediationTarget.dueDate` | `asc` | SLA urgency — already breached or about to be |
| `exposure.firstIngestedOn` | `desc` | Newest detection first |
| `exposure.lastIngestedOn` | `desc` | Most recently confirmed first |
| `asset.lastIngestedOn` | `desc` | Freshest asset data first |
| `exposure.scores.scoreLevel` | `desc` (ordinal) | `Critical > High > Medium > Low > Info` — use when you want severity-first and `exposure.scores.score` isn't an option |
| `asset.criticality` | `desc` | Integer 1–5; 5 is highest. Useful tiebreaker after `asset.scores.overallScore`. |
| `riskIndex.severity` | `desc` | VULN severity enum tiebreaker |
| `cvssScore` | `desc` | CVSS tiebreaker (bare top-level path, not `vulnerability.cvss.baseScore`) |
| `vulnerabilities.isCisaKEV` | `desc` (true first) | Binary KEV signal as tiebreaker |
| `epss.probability` | `desc` | EPSS tiebreaker in Core (0.00–1.00) |

## Multi-key sorts (recommended per skill)

Comma-separated `field:direction` pairs. anonical keys only:

| Use case | Sort |
|---|---|
| **Exposure triage** (default) | `exposure.scores.score:desc,exposure.remediationTarget.dueDate:asc` |
| **Zero-day triage** | `vulnerabilities.isCisaKEV:desc,exposure.scores.score:desc` |
| **SLA breach triage** | `exposure.remediationTarget.dueDate:asc,exposure.scores.score:desc` |
| **Newest findings** | `exposure.firstIngestedOn:desc,exposure.scores.score:desc` |
| **Asset risk ranking** | `asset.scores.overallScore:desc,asset.criticality:desc` |
| **Vulnerability (Core) intel** | `riskIndex.index:desc,cvssScore:desc` |
| **Component risk** | `riskAssessment.score:desc` |

## Sort syntax

```
sort: "exposure.scores.score:desc,exposure.remediationTarget.dueDate:asc"
```

For aggregation buckets (inside `aggs[].sort`):
- `"KEY:asc"` / `"KEY:desc"` — sort by bucket key.
- `"metricName:desc"` — sort by a nested metric's value.

## Default per skill

- `securin-cve-enrichment`: N/A (single-record lookup). When listing affected products: `cvssScore:desc`.
- `securin-asset-triage`: **`asset.scores.overallScore:desc,asset.criticality:desc`**
- `securin-exposure-triage`: **`exposure.scores.score:desc,exposure.remediationTarget.dueDate:asc`**
- `securin-product-triage`: products by name asc; components by **`riskAssessment.score:desc`**
- `securin-threat-correlation`: matched exposures → `exposure.scores.score:desc`; CVEs → `riskIndex.index:desc`
- `securin-remediation-guidance`: single-exposure focus, N/A.
- `securin-zero-day-exposure-analysis`: **`exposure.scores.score:desc,exposure.firstIngestedOn:desc`**
- `securin-tool-search`: ranked by `search_tools` relevance score

## Don't

- Don't invert direction on score fields. Platform convention is uniform: higher = worse.
- Don't omit a sort — every list response declares one.
- Don't guess field names — stick to the canonical table above.

## `validateFilter` caveat

`validateFilter` returns empty (no-error) for BOTH valid and field-nonexistent filters. It verifies **syntax only**. Always cross-check paths against `getApiFields` before trusting a filter. Unsupported sort keys are rejected at query time.
