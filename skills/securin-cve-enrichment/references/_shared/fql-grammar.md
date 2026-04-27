<!-- Mirrored from skills/_shared/fql-grammar.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

# FQL Grammar — Authoritative Reference

The Securin Platform uses a filter query language (FQL) across all `search*Data`, `aggregate*Data`, and `hybrid*Data` tools. **This doc reflects the canonical syntax per the MCP tool schemas — not prior-version claims.**

## Syntax essentials

**From the `searchExposureData.filters` schema (authoritative):**

> Syntax: `fieldPath operator value` connected with AND/OR. Operators vary by data type (check each field's `supportedFQLOperators` from the API Fields endpoint): equality (=, !=), comparison (>, >=, <, <=), range (between), text (like, matches), list (in, not in), existence (exists, does not exist). **String values must be quoted with single quotes.** Date values use ISO format or relative functions like `today() - 30`. Examples: `asset.status = active`, `exposure.status = 'Open' AND exposure.scores.scoreLevel = 'Critical'`.

### The three rules

1. **Field paths on the LHS are bare (unquoted) dot-notation.** `exposure.status`, not `"exposure.status"`.
2. **String values on the RHS use single quotes.** `'Open'`, `'Critical'`. Enums that are lowercase single-word (e.g. `active`) may work unquoted, but **always single-quote for safety**.
3. **Booleans, numbers, and relative date functions are bare.** `true`, `42`, `today() - 30`.

## Operators

| Operator | Meaning | Example |
|---|---|---|
| `=` | Equal | `asset.status = 'active'` |
| `!=` | Not equal | `exposure.status != 'Closed'` |
| `>`, `<`, `>=`, `<=` | Numeric / date comparison | `exposure.scores.overallScore >= 7.0` |
| `between` | Inclusive range | `exposure.scores.overallScore between 7 and 10` |
| `like` | Substring (case-insensitive) | `asset.hostname like 'prod-'` |
| `matches` | Regex / glob — confirm via `validateFilter` 🧪 | `asset.hostname matches '.*-prod$'` |
| `in` | Set membership | `exposure.scores.scoreLevel in ['Critical','High']` |
| `not in` | Inverse set | `asset.type not in ['Container']` |
| `exists` / `does not exist` | Null check | `exposure.remediationDate does not exist` |
| `AND`, `OR` | Boolean combinators | `a = 1 AND (b = 2 OR c = 3)` |

- Exact operator support varies by field. Call `getApiFields(entityType=[…])` and read each field's `supportedFQLOperators` array before guessing.
- Use `validateFilter` on a composed expression to get a server-side OK before firing the real query.
- Use `filterToChipPost(filter=…, entityTypes=[…])` to parse an FQL expression into a structured chip form — handy for both verification and for reconstructing UI state.

## Canonical field paths (schema-verified)

### EXPOSURE

| Path | Type | Notes |
|---|---|---|
| `exposure.status` | enum string | Run `getTopValues(field='exposure.status', entityType='EXPOSURE')` for the active set — known examples: `Open`, `Closed` (exact enum is account-dependent; confirm per account) 🧪 |
| `exposure.scores.scoreLevel` | enum string | `Critical, High, Medium, Low, Info` (per schema agg examples) |
| `exposure.scores.overallScore` | number | Higher = worse |
| `exposure.mappedAttributes.vulnerabilityIds` | string[] | CVE IDs |
| `exposure.mappedAttributes.type` | string | `Vulnerability`, `Misconfiguration`, `WebVulnerability`, … |
| `exposure.remediationTarget.dueDate` | date | Lower (closer) = more urgent |
| `exposure.remediationTarget.status` | enum | Confirm values 🧪 |

### Cross-entity fields in EXPOSURE queries

| Path | Joined entity | Example |
|---|---|---|
| `vulnerabilities.id` | VULNERABILITY | `vulnerabilities.id = 'CVE-2024-3400'` |
| `vulnerabilities.tags` | VULNERABILITY | `vulnerabilities.tags = 'Zero Day'` |
| `vulnerabilities.exploitation.isCisaKev` | VULNERABILITY | `vulnerabilities.exploitation.isCisaKev = true` |
| `asset.criticality` | ASSET (source-model) | — |
| `compositeAsset.criticality` | ASSET (composite-model) | — |

> **Namespace rule:** `vulnerabilities.*` is only valid inside exposure queries. In `searchVulnerabilityData` (Core), use **bare paths** like `vulnerabilityId`, not `vulnerabilities.id`.

### VULNERABILITY (Core, bare paths)

| Path | Type |
|---|---|
| `vulnerabilityId` | string |
| `riskIndex.severity` | enum |
| `riskIndex.index` | number |
| `exploitation.isCisaKev` | bool |
| `exploitation.exploitedInWild` | bool |
| `tags` | string[] |

### ASSET 

| Path | Type | Real values |
|---|---|---|
| `asset.status` | enum | `active` (lowercase, unquoted OK) |
| `asset.criticality` | **integer** | Numeric scale (observed `3`). Filter with numbers: `asset.criticality >= 3`. **Not a string enum** — don't write `asset.criticality = 'High'`. |
| `asset.reachability` | enum string | `'Exposed'` / `'NotExposed'` (binary pair, NOT Internet/Internal/Isolated) |
| `asset.integration.productName` | string | Scanner/integration name |

> ⚠ `asset.type` returns an error. Run `getApiFields(entityType=['ASSET'])` before assuming any asset field exists.

For the **authoritative account-specific** field list always call `getApiFields(account-id=<>, entityType=['ASSET'])` — fields differ per configured integration.

### THREAT / THREAT_ACTOR 

**Critical:** THREATACTOR field paths are **bare**, not prefixed. Use `name`, `description`, `vulnerabilityCount`, `originCountry`, `targetedCountries`, `targetedIndustries`, `associatedGroups`. Using `threatActor.name` returns an error.

`searchThreatActorData` with **no filters** returns an error. Always pass at least one filter **and** `fields: ['threatActor']`.

Example (correct):
```
searchThreatActorData
  filters: "name like 'Lazarus'"
  fields: ['threatActor']
```

## Threat / zero-day filtering (user-provided pattern)

```text
# Zero-day exposures in my environment:
exposure.status = 'Open' AND vulnerabilities.tags = 'Zero Day'

# Global zero-day CVE catalog search (Core, bare path):
tags = 'Zero Day'
```

## Date handling

- ISO-8601 UTC: `'2026-01-01T00:00:00Z'`.
- Relative: `today() - 30` → 30 days ago.
- Between two dates: `exposure.firstSeenAt between today() - 90 and today()`.

## Discovery workflow

Before writing an FQL expression:

1. `getApiFields(account-id=<>, entityType=[<entity>])` — canonical paths + `supportedFQLOperators` + data types per field.
2. `getTopValues(field=<>, entityType=<>, limit=20)` — enum/top-N values for that field.
3. `getGroupByFields(entityType=<>)` — which fields are valid for aggregation.
4. `validateFilter(...)` — verify the FQL string parses.
5. `filterToChipPost(filter=..., entityTypes=[...])` — get the structured chip representation (useful when you want to hand the user a URL they can load in the UI).

## Tool selection by filter shape

| Filter shape | Tool |
|---|---|
| Flat list, no aggregation | `search*Data` |
| Aggregation only (no paginated list) | `aggregate*Data` — with a `TERMS`, `DATE_HISTOGRAM`, etc. aggregation |
| List + per-group aggregation in one response | `hybrid*Data` — requires `groupByField`, `page`, `limit` |
| Per-bucket saved view | `createDeepLink` (with `view.filters`) then `aggregateByDeepLink(shortCode=…)` |

## Aggregation DSL (for `aggregate*Data` / `hybrid*Data`)

`aggs` is an array of aggregation objects. Each has `function` (discriminator) + `name` (label) + function-specific fields:

| `function` | Purpose | Key fields |
|---|---|---|
| `TERMS` | GROUP BY distinct values | `field`, `size` (≤300), `sort`, nested `aggs` |
| `DATE_HISTOGRAM` | Time-bucket | `field`, `interval` (`1d`, `week`, `month`), `isFixedInterval` |
| `HISTOGRAM` | Numeric-bucket | `field`, `interval` (width) |
| `COMPOSITE` | Paginate every group bucket | `field`, `size`, `searchAfter` |
| `FILTER` | Sub-filter then nest metrics | `field` (the FQL filter) + `aggs` |
| `COUNT` | Doc count | `field`, optional `filters` |
| `CARDINALITY` | Distinct count | `field` |
| `SUM`, `MIN`, `MAX`, `AVG` | Numeric metric | `field` |
| `FIRST` | Sample doc per bucket | `field`, `sort` |
| `TOP_HITS` | N sample docs per bucket | `field` (array of paths), `sort`, `size` |

> Every aggregation can carry its own `filters` — e.g. a `COUNT` named "Critical Open" with `filters: "exposure.status = 'Open' AND exposure.scores.scoreLevel = 'Critical'"` inside a larger aggregation that groups by workspace.

## Caveats to probe at runtime 🧪

- Whether `matches` works with Elasticsearch / Lucene regex or POSIX regex.
- Whether `in [...]` accepts numeric arrays unquoted.
- Whether mixing `AND` and `OR` without parentheses is left-associative or errors.
- Whether per-account custom attributes use `asset.customAttributes.<name>` or a different namespace — use `getApiFields` to discover.
