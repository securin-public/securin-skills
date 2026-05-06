---
name: securin-filter
description: >
  Converts natural language queries into valid Securin QL filter expressions for assets,
  exposures, vulnerabilities, and weaknesses on the Securin platform (both Source and
  Composite modes). Use whenever the user asks to filter, search, or list this data — or
  pastes a broken/partial filter to fix. Always use before writing any Securin filter from
  scratch. Do NOT use for Securin Core / global threat intelligence (CVEs, threat actors,
  tactics, techniques) — those are not customer-scoped and have their own search endpoints.
---

## Step 0 — Account Mode

Call `Securin__getAccountSettings(account-id, settings: ["COMPOSITE_ASSET_LIST_VIEW"])`.
- `"true"` → **Composite Mode** · missing/other → **Source Mode** · no ID → **Source Mode**
- If Composite but user asks for source/raw/unmerged data → use **Source Mode**.

## Step 1 — Parse

Identify: entities · conditions · scope intent (co-occurrence vs independent) · ambiguity (ask one question if entity type unclear).

## Step 2 — Resolve Fields

> ⚠️ **MANDATORY: `view` the cache file before any API call. Skipping this is an error.**
> - Source Mode → `references/_shared/source-fields.md`
> - Composite Mode → `references/_shared/composite-fields.md`
>
> Search the cache for every field mentioned — including ambiguous terms like "score", "status", "date". Only proceed to live lookup if the field is **confirmed missing** or behaves unexpectedly. Never guess an alias.

**Live lookup** — extract only these 8 fields from every response, discard rest:
`apiPath` `aliasName` `aliasDisplayName` `entityType` `dataType` `group` `groupId` `isArray`
Use `dataType` for operator selection (see `grammar.md` operator-by-type table).

**Tier 1 — Targeted**
```
Securin__getApiFields(account-id, searchText: "<keyword>",
  fetchOnlyAliasedFields: true, groupByGroupId: false, limit: 10, entityType: <Step 1>)
```
1 result → use it · Multiple → show options, ask user · 0 → Tier 2.

**Tier 2 — Broad** (Tier 1 empty, or user says "custom attributes"/"all fields")
```
Securin__getApiFields(account-id, fetchOnlyAliasedFields: false,
  groupByGroupId: false, entityType: <Step 1>, fetchGroups: <see Entity scoping below>)
```
Pick closest. Still not found → suggest nearest, ask user to confirm.

**Entity scoping:**
- Source: `[ASSET, EXPOSURE, VULNERABILITY, WEAKNESS]`
  - Standard fetchGroups: `BUILT_IN,MAPPED_ATTRIBUTES,USER_MANAGED_ATTRIBUTES`
  - Custom attributes: also add `CUSTOM_MAPPED_ATTRIBUTES,CUSTOM_USER_MANAGED_ATTRIBUTES`
  - Scanner-specific fields: call `Securin__getConfiguredIntegrations(account-id)` first to get the `integrationId`, then add it as an additional fetchGroup (e.g. `AZURE_AI_FOUNDRY`)
- Composite: `[COMPOSITE_ASSET, COMPOSITE_EXPOSURE, COMPOSITE_EXPOSURE_VULNERABILITY, COMPOSITE_EXPOSURE_WEAKNESS, COMPOSITE_EXPOSURE_TICKETINFO]`
  - Standard fetchGroups: `COMPOSITE_BUILT_IN,COMPOSITE_MAPPED_ATTRIBUTES_SOURCES`
  - Custom attributes: also add `COMPOSITE_CUSTOM_MAPPED_ATTRIBUTES_SOURCES,COMPOSITE_CUSTOM_USER_MANAGED_ATTRIBUTES_SOURCES`

## Step 3 — Build Filter

Read **`references/grammar.md`** for scope decisions, operators, and examples.

- Use aliases when available (quote if they contain spaces). Use full field paths inside scope wrappers.
- For fields with `isArray: true`, use `in` / `like` / `matches` — not bare `=`.

## Step 4 — Validate (conditional)

Validate when: scope wrappers used · multiple AND/OR conditions · field came from live lookup.
Skip when: no account ID · single condition on a cached field.

```
Securin__validateFilter(account-id, entityTypes: <Step 1>, filter: <filter>)
```
On 400 → parse `message`, self-correct, re-validate once. Still failing → return the filter with the error noted.

## Step 5 — Respond

Output the filter (copy-paste ready) + 2–4 sentence explanation + caveats if ambiguous.

## Edge Cases

| Situation | Action |
|---|---|
| Broken/partial filter | Identify error, output corrected version |
| Auth 401/403 | Stop and tell the user their token may be expired |
| API unreachable | Best-effort from grammar; note that fields could not be verified |
| Assets seen by A but not B | Composite Mode only — `"Asset Source Connector" like "A" AND NOT("Asset Source Connector" like "B")`. Confirm `COMPOSITE_ASSET_LIST_VIEW = true`. |


# Securin QL Filter Grammar

Full syntax reference. Read when building any non-trivial filter.

---

## Entity Hierarchy

```
ASSET
├── EXPOSURE                   (child of ASSET)
│   ├── EXPOSUREIMPORTHISTORY  (Source Mode only)
│   ├── VULNERABILITY
│   ├── WEAKNESS
│   └── TICKETINFO
└── ASSETIMPORTHISTORY         (Source Mode only)
```

> Composite Mode uses the same hierarchy minus `EXPOSUREIMPORTHISTORY` and `ASSETIMPORTHISTORY`, and uses different field prefixes (see table below).

**Source Mode:**

| Field prefix | Belongs to |
|---|---|
| `asset.*` | ASSET |
| `assetImportHistory.*` | ASSETIMPORTHISTORY |
| `exposure.*` | EXPOSURE |
| `exposureImportHistory.*` | EXPOSUREIMPORTHISTORY |
| `vulnerabilities.*` | VULNERABILITY |
| `weaknesses.*` | WEAKNESS |
| `ticketInfo.*` | TICKETINFO |

**Composite Mode:**

| Field prefix | Belongs to |
|---|---|
| `compositeAsset.*` | COMPOSITE_ASSET |
| `compositeExposure.*` | COMPOSITE_EXPOSURE |
| `vulnerabilities.*` | VULNERABILITY |
| `weaknesses.*` | WEAKNESS |
| `ticketInfo.*` | TICKETINFO |

---

## Implicit vs Explicit Scope

Default — no wrapper needed. Each condition auto-scopes to the entity that owns the field. Only use a wrapper when co-occurrence on the same record is required.

### Scope Wrappers

| Wrapper | Meaning |
|---|---|
| `ASSET(...)` | Asset must have at least one exposure matching all conditions |
| `EXPOSURE(...)` | All conditions true within the **same single** exposure record |
| `VULNERABILITY(...)` | All conditions true within the **same single** vulnerability record |

### Scope Decision Guide

| Intent | Scope |
|---|---|
| Asset has any exposure with all conditions | `ASSET(exposure.* conditions)` |
| Single exposure matches all conditions simultaneously | `EXPOSURE(...)` |
| Single vulnerability matches multiple conditions | `VULNERABILITY(...)` |
| Asset-level field only | No wrapper |
| Mix of asset-level + exposure-level | `asset.*` outside, `ASSET(exposure.* ...)` inside |

**Requiring ALL values on the same asset (not just either):**
```
# ✅ Asset must have BOTH tags
ASSET(exposure.tags.name = "PCI" AND exposure.tags.name = "HIPAA")

# ❌ Returns assets with EITHER tag
exposure.tags.name in ("PCI", "HIPAA")
```

---

## Syntax Reference

Conditions joined with `AND`, `OR`, `NOT`. Filtering is **case-sensitive**.

Parentheses control precedence:
```
("Status" = "Open" OR "Lifecycle State" = "Suppressed") AND "Last Discovered On" > today() - 7
```

### Comparison Operators

| Operator | Description | Example |
|---|---|---|
| `=` | Exact match | `"Score" = 9.3` |
| `!=` | Does not match | `"Score" != 9.3` |
| `in` | Any of these values | `"Tags" in ("PCI", "HIPAA")` |
| `not in` | None of these values | `"Asset Name" not in ("A", "B")` |
| `like` | Substring match | `"Asset Name" like "WIN10"` |
| `not like` | Not a substring | `"Title" not like "10DETECT"` |
| `matches` | Wildcard (`*`) match | `"Title" matches "*DETECTION"` |
| `does not match` | Not a wildcard match | `"Title" does not match "WIN*"` |
| `>` `<` `>=` `<=` | Numeric/date comparison | `"Score" > 7.5` |
| `between` | Inclusive range | `"Score" between (4.3 - 6.8)` |
| `not between` | Outside range | `"Score" not between (5 - 7)` |
| `exists` | Field is present | `"Routing Score" exists` |
| `does not exist` | Field is absent | `"Routing Score" does not exist` |

### Operators by Data Type

| Type | Supported Operators |
|---|---|
| STRING | `=`, `!=`, `in`, `not in`, `like`, `not like`, `matches`, `does not match`, `exists`, `does not exist` |
| NUMBER (INT/DOUBLE) | `=`, `!=`, `>`, `<`, `>=`, `<=`, `between`, `not between`, `exists`, `does not exist` |
| DATE | `in`, `not in`, `=`, `!=`, `<`, `<=`, `>`, `>=`, `like`, `between`, `not between`, `exists`, `does not exist` |
| IP | `=`, `!=`, `in`, `not in`, `like`, `not like`, `matches`, `does not match`, `>`, `<`, `>=`, `<=`, `between`, `not between`, `exists`, `does not exist` |
| BOOLEAN | `=`, `!=`, `exists`, `does not exist` |

### Count Functions (Child Cardinality)

Filter a parent by number of matching child records. Uses square brackets `[...]` on the parent. Conditions inside use full field paths, not aliases. Not applicable to non-child multi-valued fields like tags.

**Syntax:** `PARENT[CHILDCOUNT(<filter>) <operator> <number>]`

| Parent | Count Function | Counts |
|---|---|---|
| `ASSET[...]` | `EXPOSURECOUNT(...)` | Exposures on the asset |
| `ASSET[...]` | `VULNERABILITYCOUNT(...)` | Vulnerabilities on the asset |
| `ASSET[...]` | `WEAKNESSCOUNT(...)` | Weaknesses on the asset |
| `EXPOSURE[...]` | `VULNERABILITYCOUNT(...)` | Vulnerabilities on the exposure |
| `EXPOSURE[...]` | `WEAKNESSCOUNT(...)` | Weaknesses on the exposure |

Operators: `>`, `<`, `>=`, `<=` only — **`= 0` is not supported**

> ⚠️ Parentheses must never be empty — a filter condition is always required.
> - ❌ `ASSET[EXPOSURECOUNT() > 1000]`
> - ✅ `ASSET[EXPOSURECOUNT(exposure.exposureId exists) > 1000]`

> ⚠️ Cannot use `= 0` to find assets with no matching exposures. Use `ASSET(NOT(...))` instead:
> - ❌ `ASSET[EXPOSURECOUNT(exposure.status = "Open") = 0]`
> - ✅ `ASSET(NOT(exposure.status = "Open"))`

### Dynamic Functions

```
asset.firstIngestedOn > today() - 30          # last 30 days
exposure.remediationTarget.dueDate < today() + 7   # due in next 7 days
exposure.assignments.assignedTo.name = me()   # current user
```

### Date Formats (ISO 8601)
```
YYYY-MM-DDTHH:mm:ssZ  |  YYYY-MM-DD  |  YYYY-MM  |  YYYY
```

---

## Annotated Examples

```
# Assets with ONLY informational exposures
ASSET(exposure.scores.scoreLevel = "Info" AND NOT(exposure.scores.scoreLevel IN ('Critical', 'High', 'Medium', 'Low')))

# Two CVEs across any exposures on the same asset (ASSET scope)
ASSET(vulnerabilities.id = "CVE-2024-38475" AND vulnerabilities.id = "CVE-2019-0211")

# Single exposure containing both CVEs simultaneously (EXPOSURE scope)
EXPOSURE(vulnerabilities.id = 'CVE-2025-13019' AND vulnerabilities.id = 'CVE-2025-13020')

# Assets with no exposures at all
ASSET(exposure.exposureId does not exist)

# Assets with no open exposures
ASSET(NOT(exposure.status = "Open"))

# Assets with more than 100 open exposures
ASSET[EXPOSURECOUNT(exposure.status = "Open") > 100]

# Active assets with open ransomware exposures OR open exposures assigned to current user
"Asset Status" = "Active" AND ASSET(EXPOSURE((vulnerabilities.hasRansomware = true AND exposure.status = "Open") OR (exposure.assignments.assignedTo.name = me() AND exposure.status = "Open")))

# Critical exposures past due, assigned to me
exposure.scores.scoreLevel = "Critical" AND exposure.remediationTarget.dueDate < today() AND exposure.assignments.assignedTo.name = me()
```

---

## Known Enum Values

| Field | Values |
|---|---|
| Score Level | `"Critical"`, `"High"`, `"Medium"`, `"Low"`, `"Info"` |
| Asset Criticality | Integer 1–5 (5 = Critical) |
| Asset Lifecycle State | `"Monitored"`, `"Decommissioned"`, `"Dormant"`, `"Suppressed"` |
| Exposure Lifecycle State | `"New"`, `"Persistent"`, `"User Resolved"`, `"Resolved"`, `"Mixed"` |
| Exposure Status | `"Open"`, `"Closed"` |
| Asset Status | `"Active"`, `"Inactive"` |
| Remediation / Routing Status | `"Met"`, `"Missed"`, `"Overdue"`, `"On Track"` |

---

## Dynamic Value Lookup

Some fields have values that vary by account or integration and **must not be hardcoded**. For these fields, always call `Securin__getTopValues` at query time to discover valid values before building the filter.

**When to use dynamic lookup:**
- The field is a categorical STRING whose values depend on what data is present in the account (e.g., scanner-specific fields, EASM metric categories, breach types).
- The user refers to a value by a partial or informal name (e.g., "high risk services", "expired certs") — use `getTopValues` to find the exact string to match.
- You are unsure whether a value exists in the account.

**Sample Fields that require dynamic lookup:**

| Field | entityType | Why dynamic |
|---|---|---|
| `sentryExposure.exposure.keyMetricData` | EXPOSURE | EASM metric categories depend on which Sentry modules are active |
| `asset.integration.productName` | ASSET | Depends on which connectors are configured |
| `exposure.integration.productName` | EXPOSURE | Depends on which connectors are configured |

**Pattern:**
```
# Step 1 — discover valid values
Securin__getTopValues(account-id, entityType: "EXPOSURE",
  field: "sentryExposure.exposure.keyMetricData")
→ ["High Risk Services", "High Risk Vulnerabilities", ...]

# Step 2 — pick the matching value and build the filter
sentryExposure.exposure.keyMetricData = 'High Risk Services'
```

---

## Custom Attributes & Scanner-Specific Fields

Custom attributes and scanner-specific fields are account-specific and not in the common-fields cache. Discover them via live lookup with the appropriate fetchGroups.

**Source Mode:**
```
Securin__getApiFields(account-id, entityType: [...],
  fetchGroups: "BUILT_IN,MAPPED_ATTRIBUTES,USER_MANAGED_ATTRIBUTES,
               CUSTOM_MAPPED_ATTRIBUTES,CUSTOM_USER_MANAGED_ATTRIBUTES")
```

For scanner-specific fields, first call `Securin__getConfiguredIntegrations(account-id)` to get the `integrationId`, then include it as an additional fetchGroup:
```
Securin__getApiFields(account-id, entityType: [...],
  fetchGroups: "BUILT_IN,MAPPED_ATTRIBUTES,USER_MANAGED_ATTRIBUTES,
               CUSTOM_MAPPED_ATTRIBUTES,CUSTOM_USER_MANAGED_ATTRIBUTES,
               AZURE_AI_FOUNDRY")   # integrationId from getConfiguredIntegrations
```

**Composite Mode:**
```
Securin__getApiFields(account-id, entityType: [...],
  fetchGroups: "COMPOSITE_BUILT_IN,COMPOSITE_MAPPED_ATTRIBUTES_SOURCES,
               COMPOSITE_CUSTOM_MAPPED_ATTRIBUTES_SOURCES,
               COMPOSITE_CUSTOM_USER_MANAGED_ATTRIBUTES_SOURCES")
```