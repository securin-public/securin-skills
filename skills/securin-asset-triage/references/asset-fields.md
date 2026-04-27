# Asset Fields


> **Prefix rule:** use `compositeAsset.*` in composite-FF accounts, `asset.*` otherwise. See [_shared/composite-vs-source.md](_shared/composite-vs-source.md).

## Identity

| Field | Type | Notes |
|---|---|---|
| `asset.assetId` | string | Internal id |
| `asset.hostname` | string | Primary name |
| `asset.fqdn` | string | Fully qualified |
| `asset.ipAddress` | string | Primary IP |
| `asset.macAddress` | string | |

## Classification

| Field | Type | Real values |
|---|---|---|
| `asset.criticality` | **INTEGER** | Numeric scale (observed: `3` on real records). **Sort `asset.scores.overallScore:desc`** for most-critical first. Do **not** filter on string labels like `'High'` — it's a number. |
| `asset.reachability` | enum string | **`Exposed`, `NotExposed`** — binary pair. Not Internet/Internal/Isolated. |
| `asset.tags` | string[] | Free-form tags |

> `asset.type` returns an error. If you need a "type" dimension, discover the correct field via `getApiFields(entityType=['ASSET'], searchText='type')`.

## Scanning & discovery (common; confirm per-account)

| Field | Type | Notes |
|---|---|---|
| `asset.integration.productName` | string | Scanner/integration that detected the asset (per `getTopValues` schema example) |
| `asset.lastIngestedOn` | date | Freshest record first on `desc` |
| `asset.status` | enum | Known: `active` (lowercase, unquoted in schema example) |

## Exposure rollups (cross-entity fields on asset record)

| Field | Type | Notes |
|---|---|---|
| `asset.exposure.count` | int | Total exposures on the asset |
| `asset.exposure.criticalCount` | int | |
| `asset.exposure.highCount` | int | |
| `asset.exposure.openCount` | int | `status = Open` |
| `asset.exposureScore` | number | Asset-level risk score (higher = worse) |

## Aggregation dimensions

Call `getGroupByFields(entityType='ASSET')` for the authoritative list. For every candidate field, **verify it exists via `getApiFields` before grouping** — a field that appears in one account (e.g., from a configured integration) may be absent in another.

Examples that usually work (confirm per-account):
- `asset.criticality` (numeric — histogram buckets work better than TERMS here)
- `asset.reachability` (binary)
- `asset.workspaceId`
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

Then filter with the full path (e.g., `asset.customAttributes.<name>`).
