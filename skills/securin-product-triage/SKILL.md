---
name: securin-product-triage
description: >
  Use this skill when the user asks to "find products...", "list components...",
  "which software runs version X", "software inventory matching...", "product
  catalog search", "list packages affected by CVE-XXX", "which vendors...", or
  any ad-hoc search / filter / aggregation of products (global catalog) or
  components (instances installed in the user's environment). Requires the
  Securin Platform MCP server.
---

# Product & Component Triage

## Purpose

Ad-hoc search, filtering, and aggregation of **products** (global catalog entries from Securin Core — e.g., "Palo Alto PAN-OS 10.2.3") and **components** (the user's installed instances — e.g., "log4j-core 2.14.1 on host web-01"). Translate questions like "list all components running log4j < 2.17" or "which vendors are in my software inventory" into the correct MCP call.

## Products vs. components — read this first

| | Product | Component |
|---|---|---|
| Scope | Global catalog (Core) | User's environment |
| Examples | "Ubuntu 22.04", "Apache httpd 2.4.52" | "libxml2-2.9.10 on server-01" |
| Tool | `getProducts`, `getVendors` | `searchComponentData`, `aggregateComponentData`, `hybridComponentData` |
| Account-scoped? | No | Yes (needs CC-1 preflight) |
| Deep link target | Product detail page (catalog) | Filtered components view |

**Clarify with the user** when the question is ambiguous. "What versions of log4j do we have?" is components. "What versions of log4j exist?" is products.

## When to use

- "List all products by <vendor>" → products
- "Which components run `openssl < 3.0.8`?" → components
- "Show my software inventory, grouped by vendor" → components
- "Count components affected by CVE-2024-3400 in prod" → components
- "Is PAN-OS 10.2.3 in the Securin catalog?" → products

## Pre-flight

### Step 0 — Account preflight (CC-1)

See [_shared/account-preflight.md](../_shared/account-preflight.md). Required for **component** queries. For pure product-catalog queries (`getProducts`, `getVendors`), the preflight still runs so that deep links (CC-2) resolve to the correct account's UI context.

## Suggested tools

### Products (global catalog)
- `getProducts` — catalog listing
- `getVendors` — vendor listing
- `getApiFields` with `entityType: ["PRODUCT"]` — product field discovery

### Components (user's environment)
- `searchComponentData` — flat list
- `aggregateComponentData` — single-field bucket count
- `hybridComponentData` — compound-filter + aggregation (requires `groupByField`)
- `searchViStatsData` — vulnerability-instance stats over components
- `getApiFields` with `entityType: ["COMPONENT"]` — component field discovery
- `getGroupByFields` / `getTopValues` — aggregation dimensions + enum values

### Shared utilities
- `filterToChip` / `filtersToChip` / `validateFilter` — FQL construction
- `getEffectiveAccessWorkspaces` — workspace scoping

### Deep links (CC-2)
- `createDeepLink`
- `aggregateByDeepLink`
- `getDeepLink`

## Workflow

### Step 1 — Decide products vs components

Ask yourself (and the user if unclear): catalog question or environment question?

### Step 2 — For components, classify the filter shape

| Shape | Example | Tool |
|---|---|---|
| Flat list | "Components with `log4j-core` in name" | `searchComponentData` |
| Single-field bucket | "Components by vendor" | `aggregateComponentData` |
| Compound + aggregation | "Log4j components on prod assets, grouped by version" | `hybridComponentData` + `groupByField` |

### Step 3 — Discover fields

```text
getApiFields(entityType=["COMPONENT"])   # or PRODUCT
getTopValues(field="component.vendor")
getGroupByFields(entityType="COMPONENT")
```

### Step 4 — Compose FQL

Common component filter patterns:

```text
"component.name" like "log4j"
"component.vendor" = "Apache"
"component.version" < "2.17.0"             # string compare; use cautiously
"component.assetId" in [<asset ids>]
"component.mappedAttributes.cveIds" = "CVE-2024-3400"
asset.workspaceId in [<prod-ws-ids>]      # cross-entity to asset
compositeAsset.reachability = 'Exposed'  # composite-FF account
```

> **Version comparison gotcha:** semver strings don't sort lexicographically. If you need proper version comparison, filter to a product family first and compare client-side, or use `getTopValues` to enumerate distinct versions and build an explicit `in [...]` set.

### Step 5 — Call the right tool

Step 2 classification. `hybridComponentData` requires `groupByField` when `aggs` is set.

### Step 6 — Deep links (CC-2)

- For components: `createDeepLink(entityType="component", filter=...)` → filtered Components view.
- For products: `getDeepLink(productId=...)` or `createDeepLink(entityType="product", filter=...)`.
- For each aggregation bucket: one URL per row.

### Step 7 — Emit response

```markdown
**Query:** <plain-English restatement> (products | components)
**Account:** <account name + id> (for component queries)
**Filter:** `<FQL>`

<results table with View-in-Platform column>

[View full list in Platform](<top-level deep link>)
```

## Common recipes

### "Which components in my env run log4j < 2.17?"
```text
searchComponentData
filter: "component.name" like "log4j"
        AND "component.version" in [<explicit version list from getTopValues>]
sort: "asset.scores.overallScore:desc"
```

### "Component vendors I have, ranked by count"
```text
aggregateComponentData
groupByField: "component.vendor"
sort: [{type: "count", order: "desc"}]
```

### "Components affected by CVE-2024-3400 on exposed-to-internet prod"
```text
hybridComponentData
filter: "component.mappedAttributes.cveIds" = "CVE-2024-3400"
        AND asset.reachability = 'Exposed'           # or compositeAsset.*
        AND asset.workspaceId in [<prod-ws-ids>]
groupByField: "component.name"
aggs: [{type: "count"}]
```

### "List all Apache products in the Securin catalog"
```text
getProducts
filter: "product.vendor" = "Apache"
```

## Scope guard (CC-3)

- CVE / vulnerability global intel (no inventory angle) → `securin-cve-enrichment`.
- "Am I affected by threat X" → `securin-threat-correlation`.
- Asset-centric questions (hosts, not the software on them) → `securin-asset-triage`.
- Exposure records (findings with severity/SLA) → `securin-exposure-triage`.
- Unknown capability → `securin-tool-search`.

## Edge cases

- **SBOM ingest not enabled** — component data may be sparse. Tell the user and suggest which integrations populate it.
- **Duplicate components** across scanners — results may show the same `<name,version>` with different `source` values. Offer to dedupe via aggregation.
- **CPE vs human-readable** — `getProducts` uses normalized CPE strings; surface both CPE and the readable label.
- **Products without components in user env** — fine for catalog questions; flag if the user expected them to match their inventory.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](../_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Product & Component Fields Quickref](references/product-fields.md)
- [Shared: Account Preflight](../_shared/account-preflight.md)
- [Shared: Composite vs Source](../_shared/composite-vs-source.md)
- [Shared: Deep Links](../_shared/deep-links.md)
- [Shared: FQL Grammar](../_shared/fql-grammar.md)
- [Shared: Sorting Rules](../_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](../_shared/brand.md)
