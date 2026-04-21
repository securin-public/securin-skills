# Composite vs. Source Data Model

The Securin Platform has two asset data models that are toggled per account by a feature flag. **Choosing the wrong one returns empty results or stale data.** This doc tells you how to detect which model is active and which tools/fields to use.

## Why two models

- **Source model (legacy):** one record per asset per source/scanner. The same machine scanned by Nessus *and* Qualys shows up as two asset rows.
- **Composite model (newer):** one deduplicated record per logical asset, merging data across sources. The same machine is a single row with attributes from all scanners.

Accounts with the **Composite Data feature flag ON** must use the composite tools and field paths. Accounts with it OFF must use the source tools.

## Detect the active model

Call `getAccountSettings` for the resolved account-id (from the CC-1 preflight). Inspect the response for a feature flag named `compositeDataEnabled`, `compositeAsset`, or similar (the exact field depends on the account's settings shape — check and cache).

Alternatively, call `getAccountPreferences` — the same flag may live there.

Cache the result for the turn; the flag rarely changes within a conversation.

## Tool routing

| If FF is… | Use for asset search | Use for asset aggregation | Use for hybrid (compound + agg) | FQL asset prefix |
|---|---|---|---|---|
| **ON (composite)** | `searchCompositeAssetData` | `aggregateCompositeAssetData` | *(no composite hybrid tool — use `searchCompositeAssetData` + `aggregateCompositeAssetData` sequentially, or client-side combine)* | `compositeAsset.*` |
| **OFF (source)** | `searchAssetData` / `sourceAssetQuery` | `aggregateAssetData` | `hybridAssetData` | `asset.*` |

> **Note:** The MCP server currently does not expose a `hybridCompositeAssetData` tool. In composite accounts that need a compound-filter + aggregation shape, run `searchCompositeAssetData` for the list and a separate `aggregateCompositeAssetData` for the bucket counts.

Exposures, vulnerabilities, components, threats, and threat actors are **not** affected by this flag — they have a single model.

## Field path differences

| Composite | Source |
|---|---|
| `compositeAsset.criticality` | `asset.criticality` |
| `compositeAsset.hostname` | `asset.hostname` |
| `compositeAsset.reachability` | `asset.reachability` |
| `compositeAsset.assetId` | `asset.assetId` |
| `compositeAsset.exposure.severity` | `asset.exposure.severity` |

When cross-referencing from exposures to assets, the prefix changes too: in `searchExposureData`, use `compositeAsset.*` if the account is composite, otherwise `asset.*`.

## In cross-entity queries

`searchExposureData` can filter by asset attributes. Use the correct prefix based on the account's flag:

```text
# Composite account
exposure.status = 'Open' AND compositeAsset.criticality >= 4

# Source account
exposure.status = 'Open' AND asset.criticality >= 4
```

## When to clarify with the user

If `getAccountSettings` doesn't clearly show the flag, or returns an error, ask the user directly:

> "I couldn't determine your account's data model. Is this a **composite** account (deduplicated assets across sources) or a **source** account (one record per scanner)?"

Don't guess — cross-model queries return zero results silently.

## Quick decision tree

```
Does the question involve assets?
├─ No → ignore this doc (exposures/vulns/products are flag-agnostic)
└─ Yes → getAccountSettings for account-id
         ├─ compositeDataEnabled = true  → use searchCompositeAssetData + compositeAsset.*
         └─ compositeDataEnabled = false → use searchAssetData + asset.*
```
