---
name: securin-asset-triage
description: >
  Use this skill when the user asks to "find assets where...", "list my assets
  matching...", "how many assets...", "break down assets by...", "aggregate
  assets by type/criticality/workspace/cloud provider", "show asset distribution",
  "search my asset inventory", or any ad-hoc asset search / filter / aggregation
  against the Securin Platform. Requires the Securin Platform MCP server.
---

# Asset Triage

## Purpose

Ad-hoc asset search, filtering, and aggregation. Translate natural-language questions about the user's asset inventory ("show me exposed-to-internet prod assets with critical exposures") into the correct Securin MCP `search*Data` / `aggregate*Data` call, with proper account scoping and deep links back to the platform.

## When to use

- "Find all Linux servers in `prod-cloud` workspace"
- "How many assets do I have by cloud provider?"
- "Break down assets by criticality and workspace"
- "Show assets discovered in the last 30 days"
- "List credentialed vs non-credentialed scan coverage"
- "Which assets are exposed-to-internet AND have open critical exposures?" *(compound filter)*

## Pre-flight

### Step 0 — Account preflight (CC-1)

See [_shared/account-preflight.md](references/_shared/account-preflight.md). Resolve the account-id(s), validate access, and hold them for the rest of the turn. If the question implies a workspace subset ("prod", "EU BU"), also resolve workspace-ids via `getEffectiveAccessWorkspaces`.

Also before you use this SKILL, its MANDATORY for you to read through all the files inside [Referances folder](references/). This also includes all the files inside [Shared referances folder](references/_shared/). It is also COMPELSORY to try and use [Source data API Fields](references/_shared/source-fields.md) or [Composite data API Fields](references/_shared/composite-fields.md) instead of calling the `getApiFields` tool. ONLY use the tool as a fall back mechanism. 

### Step 0.5 — Detect composite vs source data model (critical)

See [_shared/composite-vs-source.md](references/_shared/composite-vs-source.md). Call `getAccountSettings` and determine whether `compositeDataEnabled` is on. This determines:

- Tool to call: `assetQuery` (composite) or `searchAssetData` (source).
- Field prefix: `compositeAsset.*` vs `asset.*`.

Cache the flag for the turn. **Picking the wrong model returns empty results with no error.**

## Suggested tools

### Primary (pick one pair based on data model)

**Composite accounts:**
- `assetQuery` — flat list and single-field bucketed count

**Source accounts:**
- `searchAssetData` — flat list
- `aggregateAssetData` — single-field bucketed count

> There is no compound-filter + aggregation tool. For "filtered list **and** bucket counts", run the search and the aggregate as two sequential calls and combine client-side.

### Supporting
- `getApiFields` with `entityType: ["ASSET"]` — field discovery when unsure of the field name
- `getGroupByFields` — valid aggregation dimensions
- `getTopValues` — enum-like value discovery for a field (build `in [...]` sets)
- `getAccountSettings` / `getAccountPreferences` — composite FF detection
- `getEffectiveAccessWorkspaces` / `getWorkspacesByAccountId` — workspace scoping
- `validateFilter` — FQL syntax validation

### Deep links (CC-2)
- `createDeepLink` (preferred) — build a URL from entity type + filter
- `aggregateByDeepLink` — one-shot aggregation with per-bucket URLs
- `getDeepLink` — URL for a known assetId

See [_shared/deep-links.md](references/_shared/deep-links.md).

## Workflow

### Step 1 — Understand the ask

Classify the question into one of:

| Shape | Example | Tool |
|---|---|---|
| Flat list | "Show me all assets where X" | `search*Data` / `assetQuery` |
| Bucketed count (one group-by) | "How many assets by type?" | `aggregate*Data` /`assetQuery` |
| Compound filter + aggregation | "Exposed-to-internet AND critical, grouped by workspace" | `search*Data` **and** `aggregate*Data` (two calls; combine client-side) **or** `assetQuery` in case of composite mode |
| Aggregation + deep links per bucket | "Bucketed counts I can click into" | `createDeepLink` |

### Step 2 — Discover fields if uncertain

If you're unsure of a field path or acceptable value:

```text
getApiFields(entityType=["ASSET"])
getTopValues(field="asset.mappedAttributes.cloudProperties.provider")   # or compositeAsset equivalent
getGroupByFields(entityType="ASSET")
```

### Step 3 — Compose FQL

Follow [_shared/fql-grammar.md](references/_shared/fql-grammar.md). Critical rules:

- Use the correct prefix (`asset.*` or `compositeAsset.*`) based on Step 0.5.
- Compound filters use parentheses and explicit `AND`/`OR`.
- Bare field names on LHS, single-quoted string values on RHS. `asset.criticality` is **numeric** — compare with `>=`, `=`, `<` using integers (e.g., `asset.criticality >= 4`).

Optional sanity check: `validateFilter` before firing the actual query.

### Step 4 — Pick and call the right tool

Apply the Step 1 classification. For compound filters + aggregation, fire `search*Data` and `aggregate*Data` with the same `filters` string — the search returns the row list, the aggregate returns the bucket counts.

Use `*Query` in case of composite mode. 

### Step 5 — Deep link every result (CC-2)

- For each list: one `createDeepLink` for the filtered Assets view.
- For aggregations: one link per bucket. Prefer `aggregateByDeepLink` which returns these inline.
- For a single asset drill-down: `getDeepLink(assetId)`.

### Step 6 — Emit response

```markdown
**Query:** <plain-English restatement>
**Account:** <account name + id> (composite / source)
**Filter:** `<FQL>`

<table of results with a "View in Platform" column>

[View full list in Platform](<top-level deep link>)
```

## Tool-selection cheat sheet

| Filter shape | No aggs | With aggs |
|---|---|---|
| `asset.status = 'active'` (single) | `searchAssetData` | `aggregateAssetData` |
| `asset.reachability = 'Exposed' AND asset.criticality >= 4` (compound, numeric criticality) | `searchAssetData` | `searchAssetData` + `aggregateAssetData` (two calls, same filter) |

Replace `searchAssetData` with `searchCompositeAssetData` and `aggregateAssetData` with `aggregateCompositeAssetData` if the account uses composite data.

## Common recipes

### "Asset distribution by business unit / workspace"

```text
aggregateAssetData | aggregateCompositeAssetData
groupByField: "asset.workspaces.id"  (or composite equivalent — see composite-fields.md)
```

Enrich workspace-ids → names via `getWorkspacesByAccountId`.

### "Exposed-to-internet prod assets with open critical exposures"

There are no `asset.exposure.*` rollup fields — the asset record does not carry exposure counts/severity. Run a two-step pattern: query EXPOSURE first, then ASSET (use composite variants if the account is composite):

```text
# 1) Find exposures matching the criteria, collect assetIds
searchExposureData
filters: exposure.status = 'Open'
         AND exposure.scores.scoreLevel = 'Critical'
fields: ["exposure.assetId"]

# 2) Pull the asset records for those ids, scoped to prod workspaces and exposed-to-internet
#    NOTE: FQL list literals use parentheses, not square brackets.
searchAssetData
filters: asset.assetId in ('<id1>','<id2>',...)
         AND asset.reachability = 'Exposed'
         AND asset.workspaces.id in (<prod-ws-id-1>, <prod-ws-id-2>)

# 3) Bucket counts on the same asset filter (e.g., by asset type).
#    aggs entries require {name, function, field}. `function` (not `type`) is
#    the operation key — TERMS for bucketing, COUNT/SUM/MIN/MAX/AVG for metrics.
aggregateAssetData
filters: <same as step 2>
aggs: [{ name: "by_type", function: "TERMS", field: "asset.assetType" }]
```

### "Assets discovered in last 30 days"

```text
searchAssetData
filter: "asset.firstDiscoveredOn" >= "<ISO-8601 30 days ago>"
sort: "asset.firstDiscoveredOn:desc"
```

### "Credentialed vs non-credentialed scan coverage"

```text
aggregateAssetData
groupByField: "asset.mappedAttributes.isCredentialed"   # or asset.isCredentialedAsset; confirm via getApiFields
```

## Scope guard (CC-3)

- If the user asks about threat actors, ransomware, or CVE-level intel → hand off to `securin-cve-enrichment` or `securin-threat-correlation`.
- If the user asks about specific exposure records (as opposed to assets with exposures) → hand off to `securin-exposure-triage`.
- If no skill fits and the user needs a capability we don't cover → hand off to `securin-tool-search`.

## Edge cases

- **Zero results** — double-check the composite/source routing (most common cause) before reporting empty.
- **Very large result sets** — paginate. Ask the user if they want aggregate instead of listing.
- **Field name ambiguity** — always confirm via `getApiFields`. Don't guess field paths across accounts; custom attributes differ.
- **Workspace access mismatch** — if the user asks about a workspace they can't see, `getEffectiveAccessWorkspaces` will omit it; surface the gap.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](references/_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Asset Fields Quickref](references/asset-fields.md) — common asset fields + aggregation dimensions
- [Shared: Account Preflight](references/_shared/account-preflight.md)
- [Shared: Composite vs Source](references/_shared/composite-vs-source.md)
- [Shared: Deep Links](references/_shared/deep-links.md)
- [Shared: FQL Grammar](references/_shared/fql-grammar.md)
- [Shared: Sorting Rules](references/_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](references/_shared/brand.md)
