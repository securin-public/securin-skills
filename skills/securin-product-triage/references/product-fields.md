# Product & Component Fields — Quickref

Common field paths. For the authoritative list, call:
- `getApiFields(entityType=["PRODUCT"])`
- `getApiFields(entityType=["COMPONENT"])`

## Products (global catalog)

| Field | Type | Notes |
|---|---|---|
| `product.productId` | string | Internal id |
| `product.name` | string | Human-readable |
| `product.vendor` | string | Vendor name |
| `product.version` | string | |
| `product.cpe` | string | CPE URI (e.g., `cpe:2.3:a:apache:log4j:*:*:*:*:*:*:*:*`) |
| `product.category` | string | `Software`, `OS`, `Library`, `Firmware`, … |
| `product.affectedByCveCount` | int | How many CVEs affect this product |
| `product.latestCveDate` | date | Most recent CVE publish date |

## Components (user's environment)

### Identity
| Field | Type |
|---|---|
| `component.componentId` | string |
| `component.name` | string |
| `component.vendor` | string |
| `component.version` | string |
| `component.cpe` | string |
| `component.packageType` | enum (`deb`, `rpm`, `maven`, `npm`, `pypi`, `nuget`, …) |
| `component.source` | string[] | Scanner/integration that detected it |

### Placement
| Field | Type | Notes |
|---|---|---|
| `component.assetId` | string | Which asset it's installed on |
| `component.assetHostname` | string | Denormalized for convenience |
| `component.path` | string | Installed path (when available) |

### Risk signals (cross-entity)
| Field | Type |
|---|---|
| `component.mappedAttributes.cveIds` | string[] |
| `component.mappedAttributes.exploitedInWild` | bool |
| `component.exposure.count` | int |
| `component.exposure.criticalCount` | int |

## Cross-entity joins on component queries

From `searchComponentData`, you can filter by:

| Field | Joined entity |
|---|---|
| `asset.criticality` / `compositeAsset.criticality` | ASSET |
| `asset.reachability` / `compositeAsset.reachability` | ASSET |
| `asset.workspaceId` / `compositeAsset.workspaceId` | ASSET |
| `vulnerabilities.id` | VULNERABILITY |
| `vulnerabilities.exploitation.isCisaKev` | VULNERABILITY |

Remember the composite-vs-source prefix rule for asset fields.

## Aggregation dimensions (common)

### Products
- `product.vendor`
- `product.category`

### Components
- `component.name`
- `component.vendor`
- `component.version`
- `component.packageType`
- `component.source`
- `asset.workspaceId` (via cross-entity)

Call `getGroupByFields(entityType="COMPONENT")` for the canonical list.

## Sort keys

- `component.exposure.criticalCount` desc — most-exposed first
- `component.mappedAttributes.cveIds.length` desc — most-vulnerable component-version first
- `component.name` asc — alphabetic

## Gotchas

- **Version sorting** — lexicographic sort is wrong for semver. Use `getTopValues` to enumerate distinct versions and build `in [...]` sets for ranges.
- **CPE matching** — CPE strings are exact. For fuzzy product matching use `component.name like ...` on the human label.
- **Dedup** — same component can appear multiple times with different `source`. Aggregate or dedupe in post.
- **Missing data** — components are populated by SBOM, package-manager scans, or SCA integrations; absence of data may mean the integration isn't configured.
