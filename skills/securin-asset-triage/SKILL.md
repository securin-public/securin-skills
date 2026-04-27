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

Ad-hoc asset search, filtering, and aggregation. Translate natural-language questions about the user's asset inventory ("show me exposed-to-internet prod assets with critical exposures") into the correct Securin MCP `search*Data` / `aggregate*Data` / `hybrid*Data` call, with proper account scoping and deep links back to the platform.

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

### Step 0.5 — Detect composite vs source data model (critical)

See [_shared/composite-vs-source.md](references/_shared/composite-vs-source.md). Call `getAccountSettings` and determine whether `compositeDataEnabled` is on. This determines:

- Tool to call: `searchCompositeAssetData` (composite) or `searchAssetData` (source).
- Field prefix: `compositeAsset.*` vs `asset.*`.

Cache the flag for the turn. **Picking the wrong model returns empty results with no error.**

## Suggested tools

### Primary (pick one triad based on data model)

**Composite accounts:**
- `searchCompositeAssetData` — flat list
- `aggregateCompositeAssetData` — single-field bucketed count
- *(no `hybridCompositeAssetData` tool today — if you need compound-filter + aggregation, run `searchCompositeAssetData` and `aggregateCompositeAssetData` as two calls)*

**Source accounts:**
- `searchAssetData` — flat list
- `aggregateAssetData` — single-field bucketed count
- `hybridAssetData` — compound-filter + aggregation (requires `groupByField`)
- `sourceAssetQuery` / `assetQuery` — lower-level query endpoints if the search tools don't fit

### Supporting
- `getApiFields` with `entityType: ["ASSET"]` — field discovery when unsure of the field name
- `getGroupByFields` — valid aggregation dimensions
- `getTopValues` — enum-like value discovery for a field (build `in [...]` sets)
- `getAccountSettings` / `getAccountPreferences` — composite FF detection
- `getEffectiveAccessWorkspaces` / `getWorkspacesByAccountId` — workspace scoping
- `filterToChip` / `filtersToChip` / `validateFilter` — FQL construction + validation

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
| Flat list | "Show me all assets where X" | `search*Data` |
| Bucketed count (one group-by) | "How many assets by type?" | `aggregate*Data` |
| Compound filter + aggregation | "Exposed-to-internet AND critical, grouped by workspace" | `hybrid*Data` + `groupByField` |
| Aggregation + deep links per bucket | "Bucketed counts I can click into" | `aggregateByDeepLink` |

### Step 2 — Discover fields if uncertain

If you're unsure of a field path or acceptable value:

```text
getApiFields(entityType=["ASSET"])
getTopValues(field="asset.cloudProvider")   # or compositeAsset.cloudProvider
getGroupByFields(entityType="ASSET")
```

### Step 3 — Compose FQL

Follow [_shared/fql-grammar.md](references/_shared/fql-grammar.md). Critical rules:

- Use the correct prefix (`asset.*` or `compositeAsset.*`) based on Step 0.5.
- Compound filters use parentheses and explicit `AND`/`OR`.
- Bare field names on LHS, single-quoted string values on RHS. `asset.criticality` is **numeric** — compare with `>=`, `=`, `<` using integers (e.g., `asset.criticality >= 4`).

Optional sanity check: `validateFilter` before firing the actual query.

### Step 4 — Pick and call the right tool

Apply the Step 1 classification. For compound filters + aggregation, `hybrid*Data` **requires** `groupByField` — without it, the tool behaves like a plain search.

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
| `asset.reachability = 'Exposed' AND asset.criticality >= 4` (compound, numeric criticality) | `searchAssetData` | **`hybridAssetData` (required)** |

Replace `searchAssetData` with `searchCompositeAssetData` if the account uses composite data.

## Common recipes

### "Asset distribution by business unit / workspace"

```text
aggregateAssetData | aggregateCompositeAssetData
groupByField: "asset.workspaceId"  (or compositeAsset.workspaceId)
```

Enrich workspace-ids → names via `getWorkspacesByAccountId`.

### "Exposed-to-internet prod assets with open critical exposures"

Compound + aggregation → `hybridAssetData` (or composite variant):

```text
filter: asset.reachability = 'Exposed'
        AND asset.workspaceId in [<prod-workspace-ids>]
        AND "asset.exposure.scores.scoreLevel" = 'Critical'
        AND "asset.exposure.status" = "Open"
groupByField: "asset.type"
aggs: [{type: "count"}]
```

### "Assets discovered in last 30 days"

```text
searchAssetData
filter: "asset.discoveredAt" >= "<ISO-8601 30 days ago>"
sort: "asset.discoveredAt:desc"
```

### "Credentialed vs non-credentialed scan coverage"

```text
aggregateAssetData
groupByField: "asset.scanCredentialed"   # confirm field name via getApiFields
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
