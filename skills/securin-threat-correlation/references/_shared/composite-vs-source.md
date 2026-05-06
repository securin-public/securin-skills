<!-- Mirrored from skills/_shared/composite-vs-source.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

# Composite vs. Source Data Model

The Securin Platform has two data models for assets and exposures that are toggled per account by a feature flag. **Choosing the wrong one returns empty results or stale data.** This doc tells you how to detect which model is active and which tools/fields to use.

## Why two models

- **Source model (legacy):** one record per asset or exposure per source/scanner. The same machine scanned by Nessus *and* Qualys shows up as two asset rows.
- **Composite model (newer):** one deduplicated record per logical asset or exposure, merging data across sources. The same machine is a single row with attributes from all scanners.

Accounts with the **Composite Data feature flag ON** must use the composite tools and field paths. Accounts with it OFF must use the source tools.

## Detect the active model

The agent must call `getAccountSettings` for the resolved account-id (from the CC-1 preflight) and run the exact same payload:

```json
{
  "settings": [
    "COMPOSITE_ASSET_LIST_VIEW"
  ],
  "account-id": "<resolved_account_id>",
  "settings-type": [
    "Feature Flag"
  ]
}
```

Inspect the response and check the `merged.value` field:
- If `merged.value` is `'true'`, the **Composite Data** feature flag is **ON** (composite model).
- If `merged.value` is `'false'` (or missing), the feature flag is **OFF** (source model).

Cache the result for the turn; the flag rarely changes within a conversation.

## Tool routing

| Entity | If FF is… | Search & Aggregate Tools | FQL prefix |
|---|---|---|---|
| **Assets** | **ON (composite)** | `assetQuery` (performs both search and aggregation simultaneously) | `compositeAsset.*` |
| **Assets** | **OFF (source)** | `searchAssetData` for search, `aggregateAssetData` for aggregation | `asset.*` |
| **Exposures** | **ON (composite)** | `exposureQuery` (performs both search and aggregation simultaneously) | `compositeExposure.*` |
| **Exposures** | **OFF (source)** | `searchExposureData` for search, `aggregateExposureData` for aggregation | `exposure.*` |

> **Note for Source Data:** For source accounts (FF OFF), there is no compound-filter + aggregation tool. When you need both a filtered list and bucket counts, you must run the search and the aggregate tools as two sequential calls and combine the results client-side. This limitation does **not** apply to composite accounts, as `assetQuery` and `exposureQuery` can perform both operations at the same time.

Vulnerabilities, threats, and threat actors are **not** affected by this flag — they have a single model.

## Field path differences

| Composite | Source |
|---|---|
| `compositeAsset.criticality` | `asset.criticality` |
| `compositeAsset.hostname` | `asset.hostname` |
| `compositeAsset.reachability` | `asset.reachability` |
| `compositeAsset.assetId` | `asset.assetId` |
| `compositeExposure.severity` | `exposure.severity` |
| `compositeExposure.status` | `exposure.status` |

When cross-referencing from exposures to assets, ensure you use the correct prefixes for both entities based on the account type.

## In cross-entity queries

`exposureQuery` (composite) and `searchExposureData` (source) can filter by asset attributes. Use the correct prefixes based on the account's flag:

```text
# Composite account
compositeExposure.status = 'Open' AND compositeAsset.criticality >= 4

# Source account
exposure.status = 'Open' AND asset.criticality >= 4
```

## When to clarify with the user

If `getAccountSettings` doesn't clearly show the flag, or returns an error, ask the user directly:

> "I couldn't determine your account's data model. Is this a **composite** account (deduplicated data across sources) or a **source** account (one record per scanner)?"

Don't guess — cross-model queries return zero results silently.

## Quick decision tree

```text
Does the question involve assets or exposures?
├─ No → ignore this doc (vulns/products/threats are flag-agnostic)
└─ Yes → getAccountSettings for account-id
         ├─ compositeDataEnabled = true  → use assetQuery / exposureQuery + compositeAsset.* / compositeExposure.*
         └─ compositeDataEnabled = false → use search/aggregate source tools + asset.* / exposure.*
```
