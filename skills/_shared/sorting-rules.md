# Sorting Rules

Every skill response that lists entities MUST sort results. Randomly-ordered results waste user attention. The sort fields below are the platform's canonical score keys per entity.

## Canonical sort fields (per entity)

| Entity | Sort key | Direction | Notes |
|---|---|---|---|
| **Exposures** | `exposures.scores.score` | `desc` | **Primary risk sort for exposures.** Note the plural `exposures.` — this is the canonical path. Use `exposures.scores.score` for sort; `exposure.scores.overallScore` can still be used as a **filter** field (`>=`, `between`). |
| **Assets** | `asset.scores.overallScore` | `desc` | **Primary risk sort for assets.** Higher = more at risk. |
| **Vulnerabilities / Weaknesses** | `riskIndex.index` | `desc` | **Primary risk sort for CVEs / CWEs.** |
| **Components** | `riskAssessment.score` | `desc` | **Primary risk sort for components.** |

## Secondary sort fields — dates, priority, enum severity

| Field | Direction | When |
|---|---|---|
| `exposure.remediationTarget.dueDate` | `asc` | SLA urgency — already breached or about to be |
| `exposure.firstSeenAt` | `desc` | Newest detection first |
| `exposure.lastSeenAt` | `desc` | Most recently confirmed first |
| `asset.lastIngestedOn` | `desc` | Freshest asset data first |
| `exposure.scores.scoreLevel` | `desc` (ordinal) | `Critical > High > Medium > Low > Info` — use when you want severity-first and `exposures.scores.score` isn't an option |
| `asset.criticality` | `desc` | Integer 1–5; 5 is highest. Useful tiebreaker after `asset.scores.overallScore`. |
| `riskIndex.severity` | `desc` | VULN severity enum tiebreaker |
| `cvssScore` | `desc` | CVSS tiebreaker (bare top-level path, not `vulnerability.cvss.baseScore`) |
| `vulnerabilities.exploitation.isCisaKev` | `desc` (true first) | Binary KEV signal as tiebreaker |
| `epss.probability` | `desc` | EPSS tiebreaker in Core (0.00–1.00) |

## Multi-key sorts (recommended per skill)

Comma-separated `field:direction` pairs. anonical keys only:

| Use case | Sort |
|---|---|
| **Exposure triage** (default) | `exposures.scores.score:desc,exposure.remediationTarget.dueDate:asc` |
| **Zero-day triage** | `vulnerabilities.exploitation.isCisaKev:desc,exposures.scores.score:desc` |
| **SLA breach triage** | `exposure.remediationTarget.dueDate:asc,exposures.scores.score:desc` |
| **Newest findings** | `exposure.firstSeenAt:desc,exposures.scores.score:desc` |
| **Asset risk ranking** | `asset.scores.overallScore:desc,asset.criticality:desc` |
| **Vulnerability (Core) intel** | `riskIndex.index:desc,cvssScore:desc` |
| **Component risk** | `riskAssessment.score:desc` |

## Sort syntax

```
sort: "exposures.scores.score:desc,exposure.remediationTarget.dueDate:asc"
```

For aggregation buckets (inside `aggs[].sort`):
- `"KEY:asc"` / `"KEY:desc"` — sort by bucket key.
- `"metricName:desc"` — sort by a nested metric's value.

## Default per skill

- `securin-cve-enrichment`: N/A (single-record lookup). When listing affected products: `cvssScore:desc`.
- `securin-asset-triage`: **`asset.scores.overallScore:desc,asset.criticality:desc`**
- `securin-exposure-triage`: **`exposures.scores.score:desc,exposure.remediationTarget.dueDate:asc`**
- `securin-product-triage`: products by name asc; components by **`riskAssessment.score:desc`**
- `securin-threat-correlation`: matched exposures → `exposures.scores.score:desc`; CVEs → `riskIndex.index:desc`
- `securin-remediation-guidance`: single-exposure focus, N/A.
- `securin-zero-day-exposure-analysis`: **`exposures.scores.score:desc,exposure.firstSeenAt:desc`**
- `securin-tool-search`: ranked by `search_tools` relevance score

## Don't

- Don't use `exposure.scores.overallScore` as a **sort** key — it's not a valid sort key. As a **filter** it's fine (`>=`, `between`).
- Don't invert direction on score fields. Platform convention is uniform: higher = worse.
- Don't omit a sort — every list response declares one.
- Don't guess field names — stick to the canonical table above.

## `validateFilter` caveat

`validateFilter` returns empty (no-error) for BOTH valid and field-nonexistent filters. It verifies **syntax only**. Always cross-check paths against `getApiFields` before trusting a filter. Unsupported sort keys are rejected at query time.
