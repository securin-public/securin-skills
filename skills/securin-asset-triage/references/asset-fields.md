# Asset Fields


> **Prefix rule:** use `compositeAsset.*` in composite-FF accounts, `asset.*` otherwise. See [_shared/composite-vs-source.md](_shared/composite-vs-source.md). The prefix change is not always exactly the same so its MANDATORY for you to refer [Composite API Fields](_shared/composite-fields.md) while using `compositeAsset.*` prefix. The fields below are **source-mode** paths; cross-reference [_shared/source-fields.md](_shared/source-fields.md) for the authoritative list.

## Identity

| Field | Type | Notes |
|---|---|---|
| `asset.assetId` | string | Internal id |
| `asset.mappedAttributes.name` | string | Primary name |
| `asset.mappedAttributes.networkInterfaces.FQDN` | string | Fully qualified |
| `asset.mappedAttributes.networkInterfaces.ipv4s` | IP | Primary IPs |
| `asset.mappedAttributes.networkInterfaces.macAddresses` | string | |

## Classification

| Field | Type | Real values |
|---|---|---|
| `asset.criticality` | **INTEGER** | Numeric scale (observed: `3` on real records). **Sort `asset.scores.overallScore:desc`** for most-critical first. Do **not** filter on string labels like `'High'` — it's a number. |
| `asset.reachability` | enum string | **`Exposed`, `NotExposed`** — binary pair. Not Internet/Internal/Isolated. |
| `asset.tags.name` | string | Free-form tags — `asset.tags` is an object array; filter/group by `.name` (or `.id`). |

> No bare `asset.type` field exists. Use `asset.assetType` (or `asset.mappedAttributes.assetType`). Verify per-account via `getApiFields(entityType=['ASSET'], searchText='type')`.

## Scanning & discovery (common; confirm per-account)

| Field | Type | Notes |
|---|---|---|
| `asset.integration.productName` | string | Scanner/integration that detected the asset (per `getTopValues` schema example) |
| `asset.lastIngestedOn` | date | Freshest record first on `desc` |
| `asset.status` | enum | Known: `active` (lowercase, unquoted in schema example) |

## Exposure rollups (cross-entity fields on asset record)

There are **no `asset.exposure.*` rollup fields** on the asset record (no `asset.exposure.count`, `asset.exposure.openCount`, `asset.exposureScore`, etc.). To answer "assets with N open critical exposures", run a separate `searchExposureData` / `aggregateExposureData` query filtered on `exposure.status = 'Open' AND exposure.scores.scoreLevel = 'Critical'`, then join back to assets via `exposure.assetId` → `asset.assetId`. The closest asset-level risk number is `asset.scores.overallScore`.

In case of **composite mode** use the `exposureQuery` tool.

## Aggregation dimensions

Call `getGroupByFields(entityType='ASSET')` for the authoritative list. For every candidate field, **verify it exists via `getApiFields` before grouping** — a field that appears in one account (e.g., from a configured integration) may be absent in another.

Examples that usually work (confirm per-account):
- `asset.criticality` (numeric — histogram buckets work better than TERMS here)
- `asset.reachability` (binary)
- `asset.workspaces.id`
- `asset.integration.productName`

## Sort keys

- `asset.scores.overallScore:desc` — most-critical first (numeric).
- `asset.scores.overallScore:desc` — most-exposed first.
- `asset.lastIngestedOn:desc` — freshest first.

Set `getSortFields: true` on a `searchAssetData` call to get the platform's canonical sortable field list for the account.

## Custom attributes

Custom attributes vary per account. Discover them via:

```text
getApiFields(entityType=['ASSET'], searchText='custom')
getCustomAttributeGroups(accountId=<>)
```

`entityType=['COMPOSITE_ASSET']` for **composite mode**

Then filter with the full path (e.g., `asset.userManagedAttributes.<name>` for built-in user-managed attributes).
