## Deep Link Generation (MANDATORY for Every List/Table/Aggregation of Customer Data)

You MUST call `Securin__createDeepLink` to mint a real `shortCode` and build the
deep-link URL from the tool's response. You MUST NOT fabricate a URL or a
shortCode. If the tool call is not made, the link is omitted entirely — there
is no third option.

**Call-order rule** — within a single turn:
1. Run all search / aggregate queries needed to answer the question.
2. For EACH list/table/aggregation you will present, call
   `Securin__createDeepLink` with the exact same FQL filter string you used
   above. Do this BEFORE you begin emitting the Final Response.
3. Only after every `createDeepLink` call has returned do you start the Final
   Response section.

The URL you embed in the response is built ONLY from the tool's returned
`shortCode` — never from pattern matching, prior turns, or guessing.

Whenever your Final Response presents a **list, table, or aggregation of customer data** (assets, exposures, vulnerabilities, weaknesses, components, threat actors, VI stats, dashboards), generate a deep link back into the Securin Platform UI so the user can open the exact same filtered view there. Render the link directly under the relevant table/list — not at the bottom of the response.

### When to Generate

- One deep link per logical list. If the response contains multiple distinct lists (e.g. critical exposures table + affected assets table), generate one link per list.
- **Skip** the deep link when the response is purely conceptual (CVE explanation, threat actor profile from VI, "what is X" answers) with no customer data list.
- **Skip** if the response is a single-record drilldown rather than a list.

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
- ✅ `"url": "{platform_url}/exposures"` — correct. Everything else (filters, sort, column selection) goes inside the `view` object.

Any filter, sort, pagination, or column-selection state you would otherwise encode as query parameters belongs in the `view.view` object instead — see the mapping in "Translating Your Query into the View Payload" below.

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
    "filters": "<the EXACT FQL filter string used in the search/aggregate query you just ran>"
  }},
  "shareWith": {{ "teams": [], "users": ["{actor_id}"] }},
  "type": "createViewRequest"
}}
```

**`layoutType` is always `"LIST_VIEW"`** for every deep link you generate — lists, tables, and aggregations (including group-by views) all use `"LIST_VIEW"`. This is the ONLY valid value for this agent's use case. Group-by behavior comes from `columns[].groupByProperties`, not from a different `layoutType`. Do not set `layoutType` to anything else, and do not omit it.

**`view.type` is always `"createViewRequest"`** — this is the top-level `type` field inside the outer `view` object (sibling of `pageId`, `view`, `shareWith`), not inside `view.view`. It is the ONLY valid value for this agent's use case. Do not set it to anything else, and do not omit it.

### Schema-Override Notice — READ THIS FIRST

The MCP tool schema for `Securin__createDeepLink` is **incomplete**. Do NOT rely on it alone — the backend HTTP API accepts more fields than the MCP schema lists, and the schema's enums are missing. When the tool schema and this document disagree, **this document wins**. Specifically:

1. **`view.view.columns` is REQUIRED even though the tool schema does not list it as a property.** The backend rejects deep-link calls that do not include a columns array. Always include it, composed per the **Column Object Shape** section below.
2. **`view.view.page` and `view.view.rowsPerPage` are REQUIRED even though the tool schema does not list them.** Always include `page: 0` and `rowsPerPage: 15` (or whatever pagination matches your query).
3. **`view.type` accepts only `"createViewRequest"`** for this agent. The tool schema declares `type` as an unconstrained string — ignore that; only `"createViewRequest"` is valid.
4. **`view.view.layoutType` accepts only `"LIST_VIEW"`** for this agent. The tool schema declares `layoutType` as an unconstrained string — ignore that; only `"LIST_VIEW"` is valid.
5. **Do NOT set `view.view.viewType`.** The tool schema lists a separate field called `viewType` with enum `["DEEP_LINK", "SAVED", "SYSTEM", "WIDGET"]`. This is a DIFFERENT field from `view.type`, and you should leave it unset. In particular, do NOT put `"DEEP_LINK"` into `view.type` — `"DEEP_LINK"` is a value that belongs to the `viewType` enum, which you are not using. The only value for `view.type` is `"createViewRequest"`.

If the LLM-visible tool schema seems to contradict any of the above, the schema is wrong and this document is right. The backend validates against its own (stricter, more complete) contract, not the MCP schema.

### Column Object Shape (Hardcoded — Source of Truth)

Every entry in `view.view.columns` is an object with these keys. Compose the
columns list fresh per call — pick field IDs from the **Available API Fields**
section above so they match the fields returned by the search/aggregate query
you just ran.

| Key | Type | Required? | Description |
|---|---|---|---|
| `id` | string | **required** | Field path from **Available API Fields** (e.g. `exposure.scores.score`, `asset.mappedAttributes.name`), OR a special aggregate id for group-by views (e.g. `GROUPBY_COLUMN`, `OPEN_EXPOSURES`, `CRITICAL_SCORE_EXPOSURES`). |
| `name` | string | **required** | Human-readable column header (e.g. `"Score"`, `"Asset Name"`). |
| `entityType` | string | **required** | One of `EXPOSURE`, `ASSET`, `VULNERABILITY`, `WEAKNESS`, `COMPONENT`, `THREATACTOR`, `VISTATS`, `DASHBOARD`. Must match the entity the field belongs to, not necessarily the top-level `entityType` of the view (e.g. an ASSET-prefixed field inside an EXPOSURE view has `entityType: "ASSET"`). |
| `isHidden` | boolean | **required** | `false` for columns that should display. Set `true` to include a field in the view data set but hide its column. |
| `sort` | object | optional | Include on the ONE column you want sorted. Shape: `{{"direction": "asc"\|"desc", "index": 1}}`. `index` is the sort priority (1 = primary). Omit on all other columns. |
| `groupByProperties` | object | optional | Only for group-by / aggregation views. Shape: `{{"function": "COUNT"\|"MAX"\|"MIN"\|"SUM"\|"AVG"\|"FIRST"\|"TERMS"\|"CARDINALITY", "field": "<field path>", "filters": "<optional FQL>", "size": <optional int>}}`. |
| `onClickViewId` | string | optional | Rare — only when the column drills into another system view on click. Leave out unless you have a specific view id to target. |

**Hard rules for the columns array:**

1. Every `id` MUST come from the **Available API Fields** section above. No guessing.
2. The column set you send MUST match (be a superset of) the fields your search/aggregate tool call actually returned for the rendered table — this is what ties the deep link to the table the user sees.
3. Exactly one column may have a `sort` object. Use the same field + direction you used in your search call's `sort` argument.
4. Do NOT include the `width`, `order`, `isPinned`, or any other keys — send only the keys listed above.

### Translating Your Query into the View Payload

For every parameter you passed to `Securin__searchExposureData` / `Securin__searchAssetData` / `Securin__aggregate*`, copy it to the matching slot in the `view` object. Do NOT encode any of these as URL query parameters.

| Your search tool-call argument | Where it goes in the deep-link payload |
|---|---|
| `filters` (FQL string) | `view.view.filters` — copy the FQL string verbatim |
| `sort` (field + direction) | `view.view.columns[N].sort = {{"direction": "...", "index": 1}}` on the matching column |
| `pageSize` | `view.view.rowsPerPage` |
| Field selection / projection | `view.view.columns[].id` — one column per returned field |
| Entity scope (EXPOSURE/ASSET/etc.) | `view.view.entityType` and `view.pageId` |

If the table you're rendering is an aggregation, set each column's `groupByProperties` to match the aggregation you ran.

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

### Worked Example

User asks: "What are my top critical open exposures with KEV?"

Tool calls (in order, BEFORE the Final Response):

1. `Securin__aggregateExposureData`({{
     "filters": "\"exposure.status\" = \"Open\" and \"vulnerabilities.isCisaKEV\" = \"true\"",
     "sort": {{"field": "exposure.scores.score", "direction": "desc"}},
     "aggs": [...]
   }}) → {{ "totalResults": 47, "buckets": [...] }}

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
           {{ "id": "exposure.scores.scoreLevel", "name": "Score Level", "entityType": "EXPOSURE", "isHidden": false }},
           {{ "id": "exposure.mappedAttributes.title", "name": "Title", "entityType": "EXPOSURE", "isHidden": false }},
           {{ "id": "exposure.scores.score", "name": "Score", "entityType": "EXPOSURE", "isHidden": false, "sort": {{"direction": "desc", "index": 1}} }},
           {{ "id": "asset.mappedAttributes.name", "name": "Asset Name", "entityType": "ASSET", "isHidden": false }},
           {{ "id": "exposure.firstDiscoveredOn", "name": "First Discovered On", "entityType": "EXPOSURE", "isHidden": false }}
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
- The `sort` lives on the `exposure.scores.score` column, matching the search `sort`.
- Each column `id` is a field path that appears in **Available API Fields**.

Only NOW do you begin emitting the Final Response markdown:

```
| CVE | Exposures | Severity |
| --- | --- | --- |
| ... | ... | ... |

[Open in Securin Platform]({platform_url}/<path>?accountId={account_id}&shortCode=a1b2c3d4)
```

Note that `a1b2c3d4` in the URL is the EXACT value returned by the tool — it is not a guess, a hash, or a placeholder. If the tool had not been called, the link is omitted entirely.

### Field Validity (Critical — Source of Truth)

The Securin API strictly validates every column `id` and every field path inside the FQL `filters` string. Invalid paths fail the call with `"<field> has invalid information"`.

**Hard rules:**

1. Every `view.view.columns[].id` MUST appear in the **Available API Fields** section above (or be one of the documented special aggregate ids for group-by views). No exceptions, no guessing.
2. Every field path inside the `view.view.filters` FQL string MUST appear in the **Available API Fields** section above for the matching entityType.
3. **Reuse the FQL string verbatim.** The filter you pass to `Securin__createDeepLink` should be the EXACT same FQL you just sent to `Securin__searchExposureData` / `Securin__searchAssetData` / `Securin__aggregate*`. If that query worked, those fields are valid.
4. **Columns must match the rendered table.** The set of `columns[].id` values should correspond one-to-one with the fields you actually show (or need to show) in the markdown table. Do not stuff in unrelated columns; do not leave out columns the user sees.
5. **`view.view.layoutType` MUST be exactly `"LIST_VIEW"`.** This is the only valid value for every deep link this agent generates (including aggregations and group-by tables). Never substitute another value; never omit the key.
6. **`view.type` MUST be exactly `"createViewRequest"`.** This is the top-level `type` key inside the outer `view` object (sibling of `pageId`, `view`, `shareWith`) — not a key inside `view.view`. It is the only valid value; never substitute another value; never omit the key.
7. **EntityType discipline — match the upstream tool call, not the account preference.** The deep-link payload (`view.pageId`, every `columns[].entityType`, every field path inside `view.view.filters`) must come from the same entity family as the `searchExposureData` / `searchAssetData` / `getExposureQuery` / `getAssetQuery` call you just ran. The user may have explicitly asked for composite data on a source-default account or vice-versa, so follow the data they're actually looking at — see `references/_shared/composite-vs-source.md` for picking the upstream call; this rule only governs what the deep-link payload looks like once that call has been made. Never mix prefixes within a single payload.

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
2. Look it up in the **Available API Fields** section to find the correct path (or call `Securin__getApiFields` once if the entity isn't in the section).
3. Drop or correct the offending column / filter field.
4. Retry `Securin__createDeepLink` ONCE.
5. If it still fails, omit the deep link silently per the rule above. Do not loop, do not surface the error.

### Final Checkpoint — Before Emitting the Response

For every list/table you are about to include in the Final Response, verify ALL of these:

- Did you call `Securin__createDeepLink` this turn for it? If NO → call it now, before you continue.
- Is the `url` input you sent a bare path (no `?`, no `#`)? If NO → the call will fail — fix it and retry.
- Is `view.view.layoutType` set to exactly `"LIST_VIEW"`? If NO → fix it before sending the call.
- Is `view.type` (top-level, sibling of `pageId`) set to exactly `"createViewRequest"`? If NO → fix it before sending the call.
- Do the `columns[].id` values match the fields shown in your rendered table, and do their prefixes match the upstream tool call's entity family (source vs composite)? If NO → rebuild the columns list before the call.
- Did the response have `status: "SUCCESS"`? If NO → omit the link.
- Is the `shortCode` in your embedded URL a value copied verbatim from a `Securin__createDeepLink` tool-call response in this turn? If NO → omit the link.

If you cannot answer YES to all of these for a given list/table, the link does not belong in the response. Omitting the link is always acceptable. Fabricating one is never acceptable.
