# Exposure Fields


## Identity

| Field | Type | Notes |
|---|---|---|
| `exposure.exposureId` | string | Internal id (e.g., `"<account-id>/8609/~NessusFinding:201010202"`) |
| `exposure.title` | string | Human-readable title |
| `exposure.description` | string | Long-form description |

## Severity & scoring

| Field | Type | Real values |
|---|---|---|
| `exposure.scores.scoreLevel` | enum string | **`Critical`, `High`, `Medium`, `Low`, `Info`** |
| `exposure.scores.overallScore` | number | Higher = worse |
| `exposure.scores.remediationScore` | number | |

> ❌ `exposure.severity` and `exposure.severityScore` are NOT valid paths. Use `exposure.scores.scoreLevel` and `exposure.scores.overallScore`.

## Status

| Field | Type | Real values |
|---|---|---|
| `exposure.status` | enum string | **`Open`, `Closed`** — **only two values**. No `InProgress`/`Accepted`/`FalsePositive` enum members. |

## Remediation — canonical fields

| Field | Type | Real values / notes |
|---|---|---|
| `exposure.mappedAttributes.vendorRemediation` | string | **Primary source of scanner-provided remediation text.** Example from a real record: *(example: a vendor advisory patch instruction)* |
| `exposure.remediationTarget.status` | enum string | **`On Track`, `Overdue`, `Met`, `Missed`** |
| `exposure.remediationTarget.dueDate` | date | |
| `exposure.remediationTarget.priority` | string | `P1`, `P2`, … (customizable) |
| `exposure.remediationTarget.targetDays` | integer | |
| `exposure.remediationTarget.isDefaultPolicyUsed` | boolean | |
| `exposure.remediationTarget.dueDateCreatedOn` | date | |
| `exposure.remediationTarget.dueDateUpdatedOn` | date | |
| `genericExposure.vulnerability.attributes.vendorRemediation` | string | Alt remediation path on generic-connector exposures |

### Pre-built remediation aggregates (alias fields, ready to COUNT)

These aliases are defined on the server and surface as aggregation fields:

| Alias | Filter applied server-side |
|---|---|
| `REMEDIATION_MET` | `exposure.remediationTarget.status = 'Met'` |
| `REMEDIATION_MISSED` | `exposure.remediationTarget.status = 'Missed'` |
| `REMEDIATION_ON_TRACK` | `exposure.remediationTarget.status = 'On Track'` |
| `REMEDIATION_OVERDUE` | `exposure.remediationTarget.status = 'Overdue'` |
| `REMEDIATION_P1_OPEN` | `exposure.remediationTarget.priority = 'P1' AND exposure.status = 'Open'` |

These are powerful for dashboards — call `aggregateExposureData` with a TERMS/COUNT using these aliases.

## Mapped attributes

| Field | Type | Real values |
|---|---|---|
| `exposure.mappedAttributes.type` | string | **`Vulnerability`, `Contact`, `Network`**. More may exist in other accounts — `getTopValues` to enumerate. |
| `exposure.mappedAttributes.vulnerabilityIds` | string[] | CVE IDs tied to this exposure |
| `exposure.mappedAttributes.cweIds` | string[] | CWE-XXX (where populated) |

## Timing

| Field | Type | Notes |
|---|---|---|
| `exposure.firstSeenAt` / `exposure.lastSeenAt` | date | Confirm paths per account via `getApiFields`. |

## Cross-entity joins (from `searchExposureData` / aggregate)

| Path | Joined entity | Example |
|---|---|---|
| `vulnerabilities.id` | VULNERABILITY | `vulnerabilities.id = 'CVE-2024-3400'` |
| `vulnerabilities.tags` | VULNERABILITY | `vulnerabilities.tags = 'Zero Day'` |
| `vulnerabilities.exploitation.isCisaKev` | VULNERABILITY | `vulnerabilities.exploitation.isCisaKev = true` |
| `asset.criticality` / `compositeAsset.criticality` | ASSET | integer (1–5 scale) |
| `asset.reachability` / `compositeAsset.reachability` | ASSET | `'Exposed'` / `'NotExposed'` |
| `asset.workspaceId` / `compositeAsset.workspaceId` | ASSET | `in [...]` |

> **Namespace reminder:** `vulnerabilities.*` is valid **only** in exposure queries. In `searchVulnerabilityData`, use bare paths (`vulnerabilityId`, `tags`, `exploitation.isCisaKev`). See [_shared/fql-grammar.md](_shared/fql-grammar.md).

## Aggregation dimensions (common)

- `exposure.scores.scoreLevel`
- `exposure.status`
- `exposure.workspaceId`
- `exposure.mappedAttributes.type`
- `exposure.remediationTarget.status`
- `exposure.remediationTarget.priority`

Call `getGroupByFields(entityType='EXPOSURE')` for the canonical list.

## Sort keys

Default: `exposures.scores.score:desc`. Other useful sorts:
- `exposure.remediationTarget.dueDate:asc` (closest breach first)
- `exposures.scores.score:desc,exposure.remediationTarget.dueDate:asc` (risk-primary, SLA-tiebreak)

Use `getSortFields: true` on any search/hybrid call to list valid sortable paths.

## Custom attributes

Discover with:
```text
getApiFields(entityType=['EXPOSURE'])
```
Then filter with the full path.
