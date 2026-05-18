## Deep Link Generation (MANDATORY for Every List/Table/Aggregation of Customer Data)

You MUST call `Securin__createDeepLink` to mint a real `shortCode` and build the
deep-link URL from the tool's response. You MUST NOT fabricate a URL or a
shortCode. If the tool call is not made, the link is omitted entirely — there
is no third option.

**Call-order rule** — within a single turn:
1. Run all search / aggregate queries needed to answer the question.
2. For EACH list/table you will present, call `Securin__createDeepLink` with the exact same FQL filter string you used above. Do this BEFORE you begin emitting the Final Response. Aggregation-sourced tables ALSO get a deeplink — see the **Group-By Deeplinks** section below for how to set `view.view.groupBy` and which column ids are valid.
3. Only after every `createDeepLink` call has returned do you start the Final
   Response section.

The URL you embed in the response is built ONLY from the tool's returned
`shortCode` — never from pattern matching, prior turns, or guessing.

Whenever your Final Response presents a **list, table, or aggregation of customer data** (assets, exposures, vulnerabilities, weaknesses, components, threat actors, VI stats, dashboards), generate a deep link back into the Securin Platform UI so the user can open the exact same filtered view there. Render the link directly under the relevant table/list — not at the bottom of the response.

### When to Generate

- One deep link per logical list. If the response contains multiple distinct lists (e.g. critical exposures table + affected assets table), generate one link per list.
- **Skip** the deep link when the response is purely conceptual (CVE explanation, threat actor profile from VI, "what is X" answers) with no customer data list.
- **Skip** if the response is a single-record drilldown rather than a list.
- **Aggregation-sourced tables also get a deeplink.** Use `view.view.groupBy` plus the group-by column allowlist — see the **Group-By Deeplinks** section below. This applies to:
  - **Non-composite:** any `Securin__aggregate*Data` tool (`aggregateAssetData`, `aggregateExposureData`, `aggregateThreatData`, `aggregateVulnerabilityData`, `aggregateVulnerabilityTimelineData`, `aggregateWeaknessData`).
  - **Composite:** `Securin__assetQuery` or `Securin__exposureQuery` called with an aggregation component (`aggs` / group-by).

### How to Generate

#### `platform_url` is `https://platform.securin.io`

Call `Securin__createDeepLink` with these parameters:

| Param | Value |
|---|---|
| `x-user-id` | `{actor_id}`  — always this exact value, never invent |
| `account-id` | `{account_id}` |
| `url` | **Base page path ONLY — no query string, no fragment.** Shape: `{platform_url}/<path>` — page paths: `ASSET → /assets`, `EXPOSURE → /exposures`, `VULNERABILITY → /vulnerabilities`, `WEAKNESS → /weaknesses`, `COMPONENT → /components`, `THREATACTOR → /threat-actors`, `VISTATS → /vi-stats`, `DASHBOARD → /dashboard`. This is the INPUT to the tool — it is NOT the URL you embed in your response. |
| `view` | nested object — see structure below |

**URL field discipline (critical):**

- ❌ `"url": "{platform_url}/exposures?sort=score.desc&status=Open&kev=true"` — WRONG. Query strings are rejected.
- ❌ `"url": "{platform_url}/exposures#tab=details"` — WRONG. Fragments are rejected.
- ✅ `"url": "{platform_url}/exposures"` — correct. Everything else (filters, sort, column selection, group-by) goes inside the `view` object.

Any filter, sort, pagination, column-selection, or group-by state you would otherwise encode as query parameters belongs in the `view.view` object instead — see the mapping in "Translating Your Query into the View Payload" below.

The `view` object structure:

```json
{{
  "pageId": "<ENTITY_ID>",
  "view": {{
    "name": "<short descriptive name of what was queried>",
    "layoutType": "LIST_VIEW",
    "entityType": "<ENTITY_ID>",
    "columns": [ <column objects — see Column Object Shape below> ],
    "page": 0,
    "rowsPerPage": 15,
    "filters": "<the EXACT FQL filter string used in the search/aggregate query you just ran>",
    "groupBy": "<OPTIONAL — only set on aggregation-sourced tables; see Group-By Deeplinks>"
  }},
  "shareWith": {{ "teams": [], "users": ["{actor_id}"] }},
  "type": "createViewRequest"
}}
```

**`layoutType` is always `"LIST_VIEW"`** for every deep link you generate — lists, tables, and aggregations (including group-by views) all use `"LIST_VIEW"`. This is the ONLY valid value for this agent's use case. Group-by behavior comes from the `view.view.groupBy` field (a sibling of `layoutType` / `filters`), not from a different `layoutType`. Do not set `layoutType` to anything else, and do not omit it.

**`view.type` is always `"createViewRequest"`** — this is the top-level `type` field inside the outer `view` object (sibling of `pageId`, `view`, `shareWith`), not inside `view.view`. It is the ONLY valid value for this agent's use case. Do not set it to anything else, and do not omit it.

### Schema-Override Notice — READ THIS FIRST

The MCP tool schema for `Securin__createDeepLink` is **incomplete**. Do NOT rely on it alone — the backend HTTP API accepts more fields than the MCP schema lists, and the schema's enums are missing. When the tool schema and this document disagree, **this document wins**. Specifically:

1. **`view.view.columns` is REQUIRED even though the tool schema does not list it as a property.** The backend rejects deep-link calls that do not include a columns array. Always include it, composed per the **Column Object Shape** section below.
2. **`view.view.page` and `view.view.rowsPerPage` are REQUIRED even though the tool schema does not list them.** Always include `page: 0` and `rowsPerPage: 15` (or whatever pagination matches your query).
3. **`view.type` accepts only `"createViewRequest"`** for this agent. The tool schema declares `type` as an unconstrained string — ignore that; only `"createViewRequest"` is valid.
4. **`view.view.layoutType` accepts only `"LIST_VIEW"`** for this agent. The tool schema declares `layoutType` as an unconstrained string — ignore that; only `"LIST_VIEW"` is valid.
5. **Do NOT set `view.view.viewType`.** The tool schema lists a separate field called `viewType` with enum `["DEEP_LINK", "SAVED", "SYSTEM", "WIDGET"]`. This is a DIFFERENT field from `view.type`, and you should leave it unset. In particular, do NOT put `"DEEP_LINK"` into `view.type` — `"DEEP_LINK"` is a value that belongs to the `viewType` enum, which you are not using. The only value for `view.type` is `"createViewRequest"`.
6. **`sort` goes on individual `columns[].sort` objects**, not as a top-level `view.view.sort` string. If you are tempted to write `"sort": "field:desc"` inside `view.view`, STOP — move it onto the matching column as `{{"direction": "desc", "index": 1}}`.
7. **`view.view.groupBy` is a single string** holding the apiField path of the grouped dimension — NOT a per-column property. Set this only on aggregation-sourced tables; omit it entirely for regular search results.

If the LLM-visible tool schema seems to contradict any of the above, the schema is wrong and this document is right. The backend validates against its own (stricter, more complete) contract, not the MCP schema.

### Column Object Shape (Hardcoded — Source of Truth)

Every entry in `view.view.columns` is an object with these keys. Compose the
columns list fresh per call — pick field IDs from the **Available API Fields**
section above so they match the fields returned by the search/aggregate query
you just ran.

| Key | Type | Required? | Description |
|---|---|---|---|
| `id` | string | **required** | Field path from **Available API Fields** (e.g. `exposure.scores.score`, `asset.mappedAttributes.name`). On group-by deeplinks (where `view.view.groupBy` is set), every column except the one displaying the grouped dimension MUST be an aggregate column id drawn from the GroupBy Aggregation Columns allowlist in `groupby-allowlist.md` (e.g. `COMPOSITE_ACTIVE_ASSETS`, `OPEN_EXPOSURES`). |
| `name` | string | **required** | Human-readable column header (e.g. `"Score"`, `"Asset Name"`). |
| `order` | int | **required** | 1-based display position of the column in the rendered table. The leftmost column is `1`, the next is `2`, and so on — strictly sequential, no gaps, no duplicates. Must cover every column in the array exactly once. |
| `isHidden` | boolean | **required** | `false` for columns that should display. Set `true` to include a field in the view data set but hide its column. |
| `width` | int | **required** | Always `180`. Do not vary this value. |
| `sort` | object | optional | Include on the ONE column you want sorted. Shape: `{{"direction": "asc"\|"desc", "index": 1}}`. `index` is the sort priority (1 = primary). Omit on all other columns. |
| `onClickViewId` | string | optional | Rare — only when the column drills into another system view on click. Leave out unless you have a specific view id to target. |

**Hard rules for the columns array:**

1. Every `id` MUST come from the **Available API Fields** section above, OR — on group-by deeplinks for non-grouped columns — from the GroupBy Aggregation Columns allowlist in `groupby-allowlist.md`. No guessing.
2. The column set you send MUST match (be a superset of) the fields your search/aggregate tool call actually returned for the rendered table — this is what ties the deep link to the table the user sees. The `order` value on each column reflects its left-to-right position in the rendered table (1 = leftmost), strictly sequential with no gaps.
3. Exactly one column may have a `sort` object. **Copy it verbatim from your tool call, never infer it from the rendered markdown.**
   - **Search calls** → top-level `sort` argument (shape: `{{"field": "...", "direction": "asc"|"desc"}}`).
   - **Aggregation calls** → `aggs[0].sort` (sibling of `aggs[0].field` / `function` / `size`, not nested). It is a STRING of the shape `"<column name>:<direction>"` — e.g. `"Asset Count:desc"`. Split on `:`: the part before is the `name` of one of your `columns[]` entries (the column whose `sort` object you set); the part after is the `direction`.
   - If your tool call has no sort, omit the `sort` object from every column.
4. **Every column MUST include `"width": 180`.** This value is fixed — never use a different number, never omit the key.
5. Do NOT include the `entityType`, `isPinned`, or any other keys — send only the keys listed above.

### Group-By Deeplinks

When the table you are about to render came from an aggregation tool — any
`Securin__aggregate*Data` call (source mode) or any `Securin__assetQuery` /
`Securin__exposureQuery` call that used an `aggs` / group-by component
(composite mode) — you STILL generate a deeplink. The shape is the standard
deeplink payload with two specific additions:

1. **Set `view.view.groupBy` to the EXACT apiField path you grouped on in
   the aggregation tool call.** This field is a string and sits as a sibling
   of `layoutType`, `filters`, `columns`, `page`, and `rowsPerPage` inside
   `view.view`. There is room for exactly ONE group-by dimension — the
   platform does not support multi-field grouping in list views.

   **Strict match rule (no substitutions).** The value MUST be a verbatim
   copy of the field path you passed as the `TERMS` top level field path.

   Do NOT swap in a "more readable" alias, a parent field, a related field
   from another entity, or any field other than the one the aggregation
   actually bucketed on. If you grouped on
   `asset.mappedAttributes.cloudProperties.provider`, `view.view.groupBy`
   MUST be `asset.mappedAttributes.cloudProperties.provider` — not
   `asset.mappedAttributes.cloudProperties.accountName`, not
   `asset.assetType`, not anything else. Mismatching here produces a
   deeplink that bucketizes on a different dimension than the rendered
   markdown table and silently misleads the user.

   The value may be any regular apiField from the **Available API Fields**
   section — it is NOT restricted to the GroupBy Aggregation Columns
   allowlist in `groupby-allowlist.md` — but it is fully constrained by
   what the aggregation call used.
2. **Every column in `view.view.columns` EXCEPT the one displaying the
   grouped dimension MUST use an `id` drawn from the GroupBy Aggregation
   Columns allowlist in `groupby-allowlist.md`.** The grouped-dimension column
   keeps the regular apiField path as its `id` (the same path you set on
   `view.view.groupBy`). Every other column is an aggregate metric — its `id`
   is one of the special aggregate ids exposed by the platform
   (e.g. `COMPOSITE_ACTIVE_ASSETS`, `OPEN_EXPOSURES`,
   `CRITICAL_SCORE_EXPOSURES`). Pick the composite-mode list when the
   upstream call was `*Query`; the source-mode list when it was any
   `aggregate*Data` tool — never mix them.

**The `aggregateFunction` metadata in `groupby-allowlist.md` is context only.**
Each entry in that allowlist ships with an
`aggregate:` description (showing the platform's internal `function`,
`apiPath`, and `filters`). That metadata is there so you can pick the right
aggregate id for the metric you want to show — DO NOT copy any of those
fields into the deeplink tool call. The `columns[]` object structure is the
exact same shape documented above (`id`, `name`, `order`,
`isHidden`, `width: 180`, optional `sort`). The aggregation behavior is
defined entirely by the platform-side mapping of that aggregate `id`; you
do not re-declare the function in the deeplink payload.

**Sort on group-by deeplinks (read in full — this is the most common silent failure on group-by deeplinks).**

When you intend to emit a deeplink for an aggregation, the aggregation tool call MUST include an explicit `aggs[0].sort` — never implicit, never relying on the platform's default bucket order. If your most recent aggregation call ran WITHOUT a `sort`, **re-run the aggregation with one before composing the deeplink**, then build the deeplink against that sorted call. Reason: the deeplink page only shows the first page of buckets (`rowsPerPage` defaults to 15), and the platform's default bucket sort is NOT guaranteed to match whatever order the API returned in chat. A sortless group-by deeplink silently lands the user on a different first page than the rendered markdown table — this is what the user perceives as "the sort is inconsistent on group-by deeplinks."

Once `aggs[0].sort` is present, copy it verbatim into the deeplink. `aggs[0].sort` is a STRING of shape `"<column name>:<direction>"` (e.g. `"Active Assets:desc"`). Split on `:`:
- The part BEFORE `:` is the `name` of one of your `columns[]` entries (the column whose `sort` object you set). It may be the grouped-dimension column OR an aggregate-metric column.
- The part AFTER `:` is the `direction` (`asc` or `desc`). Put it on that column as `{{"direction": "<dir>", "index": 1}}`.

**Column-name mirrors the sort label, NOT the allowlist's canonical name.** The `name` you put on the deeplink column whose `sort` you set MUST equal — character-for-character — the substring BEFORE `:` in `aggs[0].sort`. This often diverges from the canonical label shown for the aggregate id in the GroupBy Aggregation Columns allowlist, and that is intentional — the `id` comes from the allowlist; the `name` mirrors the agg call. Failing this rule is the single most common reason a group-by deeplink lands on a different first page than the rendered table.

Worked sub-example (the divergence case). You called the aggregation with `aggs[0].sort = "Assets:desc"` (the short label that contextual skills typically teach for `TERMS` bucket sort). You want to display this metric on a deeplink column whose `id` is `COMPOSITE_ACTIVE_ASSETS` — whose canonical label in `groupby-allowlist.md` is `"Active Assets"`. The deeplink column MUST be:

```json
{{ "id": "COMPOSITE_ACTIVE_ASSETS", "name": "Assets", "order": 2, "isHidden": false, "width": 180, "sort": {{"direction": "desc", "index": 1}} }}
```

Note `"name": "Assets"` — NOT `"name": "Active Assets"`. The `name` mirrors `aggs[0].sort`'s substring-before-colon; if you used the allowlist's canonical label instead, the substring-match fails, no column carries the sort, and the user lands on a different first page than the rendered chat table.

See the Group-By Aggregation worked example below for a complete payload (that example happens to use the canonical label in BOTH the agg call and the column name, which is also valid — the rule is "the two sides match each other," not "use one specific form").

**Selecting aggregate columns to display.** Pick aggregate ids whose
`aggregate:` description in `groupby-allowlist.md` matches the metric the
rendered markdown table is showing. If your aggregate call counted open
critical exposures per asset cloud-provider, your rendered table likely
has a "Critical Open Exposures" column — find the aggregate id in
`groupby-allowlist.md` whose `aggregate:` description computes that exact
count and use that id as the column `id`. Do NOT invent new aggregate
ids; if no allowlist entry matches the metric you want to surface, drop
that column from the deeplink (leave it in
the rendered markdown if it adds value, but treat it as agent-synthesized
for deeplink purposes).

### Translating Your Query into the View Payload

For every parameter you passed to `Securin__searchExposureData` / `Securin__searchAssetData` / `Securin__aggregate*`, copy it to the matching slot in the `view` object. Do NOT encode any of these as URL query parameters.

| Your search / aggregate tool-call argument | Where it goes in the deep-link payload |
|---|---|
| `filters` (FQL string) | `view.view.filters` — copy the FQL string verbatim |
| `sort` (field + direction) | `view.view.columns[N].sort = {{"direction": "...", "index": 1}}` on the matching column. Source: top-level `sort` for search calls; `aggs[0].sort` (string `"<column name>:<direction>"`) for aggregations. See Column Object Shape rule 3. |
| `pageSize` | `view.view.rowsPerPage` |
| Field selection / projection | `view.view.columns[].id` — one column per returned field |
| Entity scope (EXPOSURE/ASSET/etc.) | `view.view.entityType` and `view.pageId` |
| Aggregation / group-by dimension | `view.view.groupBy` — single string, apiField path of the grouped field |
| Aggregation metrics returned | `view.view.columns[].id` — one column per metric, using the matching aggregate id from `groupby-allowlist.md` |

### View Payload Strategy

1. **Default path — compose the view yourself.** Build `columns`, `filters`, `sort`, and `rowsPerPage` from scratch using the mappings above. This is what you should do 99% of the time. The deep link is a NEW view definition tied to this one query; it does not need to reference any existing saved view.
2. **Rare fallback — named system view.** Only if the user explicitly asked for a specific named system view (e.g. *"show me the Sentry view of my internet-facing assets"*):
   - Call `Securin__getViews` with `{{pageId, viewType: "SYSTEM", searchText: "<view name>"}}` to find the view id.
   - Call `Securin__getViewSettings` with `{{pageId, view-id}}` to fetch its columns + entityType.
   - Use those columns in the `createDeepLink` payload.

Both `Securin__getViews` and `Securin__getViewSettings` also require `x-user-id: {actor_id}` and `account-id: {account_id}`.

### Constructing the URL from the Response

The URL you EMBED in the Final Response is a DIFFERENT shape from the `url`
input parameter above. It is only available AFTER `Securin__createDeepLink`
returns a `shortCode`.

If `Securin__createDeepLink` returns `status: "SUCCESS"` with a `shortCode`, build the URL exactly as:

```
{platform_url}/deepLink?accountId={account_id}&shortCode=<shortCode-from-tool-response>
```

Where `<shortCode-from-tool-response>` is the literal value of the `shortCode`
field from the tool's JSON response in this turn. If you did not call the
tool this turn, you do NOT have a shortCode — do not invent one.

If `status` is anything other than `SUCCESS`, **omit the link silently** — do not surface the error to the user, do not retry.

### Embedding in the Response

Render the URL as a plain markdown link directly below the table or list it refers to (not buried in a footer). The `shortCode` in the URL must be the literal value returned by `Securin__createDeepLink` this turn — never invented, never carried over from a prior turn.

### Worked Example — Standard Search

User asks: "What are my top critical open exposures with KEV?"

Tool calls (in order, BEFORE the Final Response):

1. `Securin__searchExposureData`({{
     "filters": "\"exposure.status\" = \"Open\" and \"vulnerabilities.isCisaKEV\" = \"true\"",
     "sort": {{"field": "exposure.scores.score", "direction": "desc"}}
   }}) → {{ "totalResults": 47, "results": [...] }}

2. `Securin__createDeepLink`({{
     "x-user-id": "{actor_id}",
     "account-id": {account_id},
     "url": "{platform_url}/exposures",
     "view": {{
       "pageId": "EXPOSURE",
       "view": {{
         "name": "Critical KEV Open Exposures",
         "layoutType": "LIST_VIEW",
         "entityType": "EXPOSURE",
         "columns": [
           {{ "id": "exposure.scores.scoreLevel", "name": "Score Level", "order": 1, "isHidden": false, "width": 180 }},
           {{ "id": "exposure.mappedAttributes.title", "name": "Title", "order": 2, "isHidden": false, "width": 180 }},
           {{ "id": "exposure.scores.score", "name": "Score", "order": 3, "isHidden": false, "width": 180, "sort": {{"direction": "desc", "index": 1}} }},
           {{ "id": "asset.mappedAttributes.name", "name": "Asset Name", "order": 4, "isHidden": false, "width": 180 }},
           {{ "id": "exposure.firstDiscoveredOn", "name": "First Discovered On", "order": 5, "isHidden": false, "width": 180 }}
         ],
         "page": 0,
         "rowsPerPage": 15,
         "filters": "\"exposure.status\" = \"Open\" and \"vulnerabilities.isCisaKEV\" = \"true\""
       }},
       "shareWith": {{ "teams": [], "users": ["{actor_id}"] }},
       "type": "createViewRequest"
     }}
   }}) → {{ "status": "SUCCESS", "shortCode": "a1b2c3d4" }}

Notice:
- `url` is the bare path `{platform_url}/exposures` — no query string.
- `filters` is the EXACT FQL from the search call above.
- The `sort` lives on the `exposure.scores.score` column with `direction: "desc"` — copied VERBATIM from the search call's `sort` argument above, NOT inferred from the rendered table.
- Each column carries `"width": 180` and the `id` is a field path that appears in **Available API Fields**.
- `view.view.groupBy` is OMITTED — this is a regular search, not an aggregation.

Only NOW do you begin emitting the Final Response markdown:

```
| Score Level | Title | Score | Asset Name | First Discovered On |
| --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... |

[Open in Securin Platform]({platform_url}/deepLink?accountId={account_id}&shortCode=a1b2c3d4)
```

Note that `a1b2c3d4` in the URL is the EXACT value returned by the tool — it is not a guess, a hash, or a placeholder. If the tool had not been called, the link is omitted entirely.

### Worked Example — Group-By Aggregation

User asks: "How many active assets do I have grouped by cloud provider?"

Tool calls (in order, BEFORE the Final Response — composite mode shown):

1. `Securin__assetQuery`({{
     ...,
     "aggs": [
       {{
         "field": "compositeAsset.mappedAttributes.cloudProperties.provider",
         "function": "TERMS",
         "size": 50,
         "sort": "Active Assets:desc",
         "metrics": ["COMPOSITE_ACTIVE_ASSETS", "COMPOSITE_ASSETS"]
       }}
     ]
   }}) → buckets per provider, ordered by Active Assets descending

2. `Securin__createDeepLink`({{
     "x-user-id": "{actor_id}",
     "account-id": {account_id},
     "url": "{platform_url}/assets",
     "view": {{
       "pageId": "COMPOSITE_ASSET",
       "view": {{
         "name": "Active Assets by Cloud Provider",
         "layoutType": "LIST_VIEW",
         "entityType": "COMPOSITE_ASSET",
         "columns": [
           {{ "id": "compositeAsset.mappedAttributes.cloudProperties.provider", "name": "Cloud Provider", "order": 1, "isHidden": false, "width": 180 }},
           {{ "id": "COMPOSITE_ACTIVE_ASSETS", "name": "Active Assets", "order": 2, "isHidden": false, "width": 180, "sort": {{"direction": "desc", "index": 1}} }},
           {{ "id": "COMPOSITE_ASSETS", "name": "Total Assets", "order": 3, "isHidden": false, "width": 180 }}
         ],
         "page": 0,
         "rowsPerPage": 15,
         "filters": "",
         "groupBy": "compositeAsset.mappedAttributes.cloudProperties.provider"
       }},
       "shareWith": {{ "teams": [], "users": ["{actor_id}"] }},
       "type": "createViewRequest"
     }}
   }}) → {{ "status": "SUCCESS", "shortCode": "b2c3d4e5" }}

Notice:
- `view.view.groupBy` is set to the apiField path of the grouped dimension
  (a regular composite apiField), copied verbatim from `aggs[0].field`.
- The FIRST column displays the grouped dimension — its `id` matches the
  `groupBy` value and is drawn from regular Available API Fields.
- The OTHER columns (`COMPOSITE_ACTIVE_ASSETS`, `COMPOSITE_ASSETS`) are
  aggregate ids drawn from the GroupBy Aggregation Columns allowlist in
  `groupby-allowlist.md`. Their `aggregate:` metadata in that file is
  context only; nothing from it is copied into the deeplink payload.
- The `sort` on the `Active Assets` column is `aggs[0].sort` copied verbatim. Splitting `"Active Assets:desc"` on `:` gave us the column `name` (`"Active Assets"` → the column with that name carries the sort) and the direction (`"desc"`).
- Every column still includes `"width": 180`.
- `layoutType` stays `"LIST_VIEW"`. The aggregation is encoded by `groupBy`
  + the aggregate column ids — NOT by a different layoutType.

### Field Validity (Critical — Source of Truth)

The Securin API strictly validates every column `id` and every field path inside the FQL `filters` string. Invalid paths fail the call with `"<field> has invalid information"`.

**Hard rules:**

1. Every `view.view.columns[].id` MUST appear in the **Available API Fields** section above, OR — for group-by deeplinks, on non-grouped columns only — in `groupby-allowlist.md`. No exceptions, no guessing.
2. Every field path inside the `view.view.filters` FQL string MUST appear in the **Available API Fields** section above for the matching entityType.
3. **`view.view.groupBy`, when set, MUST appear in the Available API Fields section above** (the regular section, not the aggregate-columns section) AND MUST be the verbatim apiField path you passed as the group-by argument to the aggregation tool call you just ran. No substitutions, no parent fields, no aliases — see the strict match rule in **Group-By Deeplinks**.
4. **Reuse the FQL string verbatim.** The filter you pass to `Securin__createDeepLink` should be the EXACT same FQL you just sent to `Securin__searchExposureData` / `Securin__searchAssetData` / `Securin__aggregate*`. If that query worked, those fields are valid.
5. **Columns must match the rendered table.** The set of `columns[].id` values should correspond one-to-one with the fields you actually show (or need to show) in the markdown table. Do not stuff in unrelated columns; do not leave out columns the user sees.
6. **`view.view.layoutType` MUST be exactly `"LIST_VIEW"`.** This is the only valid value for every deep link this agent generates (including aggregations and group-by tables). Never substitute another value; never omit the key.
7. **`view.type` MUST be exactly `"createViewRequest"`.** This is the top-level `type` key inside the outer `view` object (sibling of `pageId`, `view`, `shareWith`) — not a key inside `view.view`. It is the only valid value; never substitute another value; never omit the key.
8. **Every column MUST include `"width": 180`.** Fixed value; never vary.
9. **EntityType discipline — match the upstream tool call, not the account preference.** The deep-link payload (`view.pageId`, every `columns[].entityType`, every field path inside `view.view.filters`) must come from the same entity family as the `searchExposureData` / `searchAssetData` / `getExposureQuery` / `getAssetQuery` call you just ran. The user may have explicitly asked for composite data on a source-default account or vice-versa, so follow the data they're actually looking at — see `references/_shared/composite-vs-source.md` for picking the upstream call; this rule only governs what the deep-link payload looks like once that call has been made. Never mix prefixes within a single payload.

   | Slot | Source mode | Composite mode |
   |---|---|---|
   | `view.pageId` | `EXPOSURE` | `COMPOSITE_EXPOSURE` |
   | `columns[].entityType` (exposure col) | `EXPOSURE` | `COMPOSITE_EXPOSURE` |
   | `columns[].entityType` (asset col joined in) | `ASSET` | `COMPOSITE_ASSET` |
   | Filter / column field path (score) | `exposure.scores.score` | `compositeExposure.scores.score` |
   | Filter / column field path (asset name) | `asset.mappedAttributes.name` | `compositeAsset.mappedAttributes.name` |
   | Tool used upstream | `searchExposureData` / `searchAssetData` | `getExposureQuery` / `getAssetQuery` |

### Self-Healing on Field Errors

If `Securin__createDeepLink` returns a non-SUCCESS response containing `"has invalid information"`:

1. Identify the offending field from the error message.
2. Look it up in the **Available API Fields** section (or `groupby-allowlist.md` for non-grouped aggregate ids) to find the correct path. If the entity isn't in either, call `Securin__getApiFields` once.
3. Drop or correct the offending column / filter field / `groupBy` value.
4. Retry `Securin__createDeepLink` ONCE.
5. If it still fails, omit the deep link silently per the rule above. Do not loop, do not surface the error.

### Final Checkpoint — Before Emitting the Response

For every list/table you are about to include in the Final Response, verify ALL of these:

- Did you call `Securin__createDeepLink` this turn for it? If NO → call it now, before you continue. (Aggregation-sourced tables included — use `view.view.groupBy`.)
- Is the `url` input you sent a bare path (no `?`, no `#`)? If NO → the call will fail — fix it and retry.
- Is `view.view.layoutType` set to exactly `"LIST_VIEW"`? If NO → fix it before sending the call.
- Is `view.type` (top-level, sibling of `pageId`) set to exactly `"createViewRequest"`? If NO → fix it before sending the call.
- Does every column include `"width": 180`? If NO → fix it before sending the call.
- For aggregation-sourced tables: is `view.view.groupBy` set to the EXACT apiField path you passed as the group-by argument to your aggregation tool call (no substitutions, no aliases), and is every column except the one displaying that dimension drawn from the GroupBy Aggregation Columns allowlist in `groupby-allowlist.md`? If NO → rebuild the columns list and re-call.
- For non-aggregation tables: is `view.view.groupBy` OMITTED entirely? If NO → remove it before sending the call.
- Do the `columns[].id` values match the fields shown in your rendered table, and do their prefixes match the upstream tool call's entity family (source vs composite)? If NO → rebuild the columns list before the call.
- Does the `sort` object match your tool call (top-level `sort` for search, `aggs[0].sort` for aggregations)? If your tool call has no sort, the deeplink must have no sort. Never infer sort from the rendered markdown — see Column Object Shape rule 3.
- Did the response have `status: "SUCCESS"`? If NO → omit the link.
- Is the `shortCode` in your embedded URL a value copied verbatim from a `Securin__createDeepLink` tool-call response in this turn? If NO → omit the link.

If you cannot answer YES to all of these for a given list/table, the link does not belong in the response. Omitting the link is always acceptable. Fabricating one is never acceptable.

## Deep Link Generation — Existing View Mode (override)

This is an OVERRIDE of the standard deep-link flow above. It
applies ONLY when the user explicitly asks to open a named saved view or
the default view on the ASSET or EXPOSURE page (e.g. *"deeplink the
'Internet Facing Assets' view"*, *"open the default exposures view"*).
For every other request — including data questions you answered with a
search/aggregate — use the standard `createViewRequest` flow.

If this override applies, IGNORE the `view.view` / `columns` / `filters`
composition rules above and follow the steps below instead.
Everything else from this document (URL discipline, response-URL
construction, hyperlink shape, silent omit on non-SUCCESS) still
applies unchanged.

### Scope

- Pages supported: **`ASSET` and `EXPOSURE` only.** No composite, no
  other entities. If the user asks for a named view on any other page,
  fall back to the standard flow.

### Step 1 — Resolve the viewId via `getViews`

Call `getViews({{"pageId": "ASSET" | "EXPOSURE", ...}})`. Do NOT pass
`viewType` — we want both SYSTEM and USER views in the response so the
user's own saved views are findable. Response shape:
`{{"views": [{{"id": ..., "name": ..., "isDefault"?: true}}, ...]}}`.

Pick the viewId:

- User said "default" → entry with `isDefault: true`.
- User named a view → entry whose `name` matches case-insensitively.
- Multiple matches OR no `isDefault` flag when "default" was asked →
  **ask the user to pick** from the candidate names. Do not guess.
- No match → tell the user no such view exists on that page; offer the
  closest names from the response. Do not fabricate an id.

### Step 2 — Call `Securin__createDeepLink` with the flat payload

```json
{{
  "x-user-id": "{actor_id}",
  "account-id": {account_id},
  "url": "{platform_url}/exposures"  // or "{platform_url}/assets"
  "view": {{
    "pageId": "ASSET" | "EXPOSURE",
    "viewId": "<id from getViews>",
    "filters": "",
    "type": "existingViewRequest"
  }}
}}
```

Differences vs. the standard flow (this is the entire override):

- `view` is **flat** — no nested `view.view`.
- No `columns`, `layoutType`, `entityType`, `name`, `page`, `rowsPerPage`,
  `groupBy`, or `shareWith`. The saved view supplies all of that.
- `view.filters` is always `""`. Do not layer extra FQL.
- `view.type` is `"existingViewRequest"` (NOT `"createViewRequest"`).
- `view.pageId` must match the page you queried `getViews` against.

If you find yourself adding any of the omitted fields, you are in the
wrong flow — switch back to `createViewRequest`.

### Final checkpoint (override-specific)

- User explicitly named a view or asked for the default on ASSET/EXPOSURE? If NO → use `createViewRequest`.
- Called `getViews` this turn and got the `viewId` verbatim from its response? If NO → resolve it before sending.
- `view` is flat, with exactly `pageId` + `viewId` + `filters: ""` + `type: "existingViewRequest"`? If NO → fix the shape.
