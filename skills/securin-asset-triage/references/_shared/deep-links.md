<!-- Mirrored from skills/_shared/deep-links.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

# Deep Links (CC-2)

Every skill response that surfaces Securin Platform entities MUST give the user a way to open those entities in the platform UI. This plugin uses a 3-tool chain: `getViews` → `getViewSettings` → `createDeepLink`.

## Final URL format (customer-facing)

`createDeepLink` returns a `shortCode`. The user-loadable URL is:

```
https://platform.securin.io/deepLink?accountId=<account-id>&shortCode=<shortCode>
```

Always render the deep link in this format. Never render the raw `shortCode` alone.

## The workflow

```
1. getViews(pageId=<entity>, viewType='SYSTEM')
   → returns system views for that entity (pick by name or isDefault: true)

2. getViewSettings(view-id=<picked id>, pageId=<entity>)
   → returns the full view payload (columns, sort, filters, layout)

3. createDeepLink(view=<settings from step 2 + overlay filter>, url, x-user-id, accessControl)
   → returns { shortCode }

4. Render URL: https://platform.securin.io/deepLink?accountId=<>&shortCode=<>
```

`createDeepLink` expects a `view` body shaped like the output of `getViewSettings`. Do not fabricate one.

## Tools used

| Tool | Purpose | Required params |
|---|---|---|
| `getViews` | List system / saved views for a page | `account-id`, `user-id`, `pageId` |
| `getViewSettings` | Fetch one view's full settings payload | `account-id`, `user-id`, `view-id`, `pageId` |
| `createDeepLink` | Create a persistent, shareable deep link | `account-id`, `x-user-id`, `url`, `view` |
| `getDeepLink` | Retrieve a deep link by `short-code` | `account-id`, `short-code` |
| `aggregateByDeepLink` | Re-run a saved deep link's filter through aggregation | `account-id`, `shortCode`, `x-user-id` |
| `getDefaultViewForGroupByField` | Get the view id the platform recommends for a group-by dimension | `account-id`, `apiPath`, `entityType` |

## Page IDs (from schema)

`ASSET, DASHBOARD, EXPOSURE, VULNERABILITY, WEAKNESS, VULNERABILITY_TIMELINE, THREATACTOR, VISTATS, TACTIC, TECHNIQUE, COMPONENT, THREAT, COMPOSITE_ASSET`

## Common system-view names per page

Pick by name via `getViews` — the exact IDs are per-account. Typical EXPOSURE system views include: *Exposures*, *CISA KEV Exposures*, *Securin KEV Exposures*, *Needs Remediation*, *RemOps - Remediation Targets*, *CVE View*, *Exposures by Asset*, *My Exposures*, *Fixes*. For ASSET, VULNERABILITY, COMPONENT pages, enumerate at request time.

## `createDeepLink` request shape

| Field | Required | Notes |
|---|---|---|
| `x-user-id` | ✅ | Caller's user id from `getUserProfile`. The deep link is owned by this user. |
| `account-id` | ✅ | From CC-1 preflight. |
| `url` | ✅ | Platform URL path the deep link resolves to. |
| `view` | ✅ | Shape derived from `getViewSettings` output — see Strategy B below. |
| `accessControl` | ✅ (practical) | Who can load the link (emails / emailDomains / workspaces / companies / seeds). Include the caller or the link is invisible to them. |
| `expiryDate` | optional | `yyyy-MM-dd`. Defaults to system preference. |
| `triggered-by` | optional | Default `UI`. Pass `MCP` for auditability. |

**Always add the caller to `accessControl.emails` with `action: ADD, roles: ['viewer']`** — without this they cannot load the link they just created.

## Two strategies

### Strategy A — platform URL from FQL (default)

For routine triage responses that don't need a persistent saved link:

1. Compose the FQL filter.
2. Call `filterToChipPost(filter=<FQL>, entityTypes=[<entity>])` to get the chip representation.
3. Render a `https://platform.securin.io/<page>?...` URL the user can open.

No write op, no sharing setup.

**Use Strategy A for:** every triage / search / correlation / zero-day response. Default.

### Strategy B — saved deep link (opt-in)

Only when the user explicitly asks to save or share a view:

#### B.1 — List views for the entity
```
getViews(account-id=<>, user-id=<caller uuid>, pageId='EXPOSURE', viewType='SYSTEM')
→ inspect .views[]; pick the default (isDefault: true) or the best name match
```

#### B.2 — Fetch the view settings
```
getViewSettings(account-id=<>, user-id=<caller uuid>, view-id=<picked>, pageId='EXPOSURE')
→ returns the full view payload (columns, sort, filters, layout)
```

#### B.3 — Confirm with the user
> "I'll create a persistent deep link based on the system view **`<name>`** with your filter overlaid. This writes a record in your platform. Proceed? (Y/n)"

#### B.4 — Call `createDeepLink`

Use the view settings from B.2 as the `view` body; add the overlay FQL filter to `view.filters`; populate `shareWith` + `accessControl`:

```json
{
  "x-user-id": "<caller uuid>",
  "account-id": <number>,
  "url": "<platform URL for the page>",
  "view": {
    "pageId": "EXPOSURE",
    "viewType": "DEEP_LINK",
    "filters": "<overlay FQL, e.g., exposure.status = 'Open' AND vulnerabilities.tags = 'Zero Day'>",
    "shareWith": {
      "users": ["<caller uuid>"],
      "teams": []
    }
  },
  "accessControl": {
    "emails": [
      {"action": "ADD", "values": ["<caller email>"], "roles": ["viewer"]}
    ]
  },
  "triggered-by": "MCP"
}
```

#### B.5 — Render the final URL

```
https://platform.securin.io/deepLink?accountId=<account-id>&shortCode=<shortCode-from-response>
```

Use `getDeepLink(account-id=<>, short-code=<>)` later to retrieve the saved record (set `includeAccessDetails=true` to audit sharing).

## Aggregation + deep link

- `aggregateByDeepLink(shortCode=<from Strategy B>)` — re-runs the saved view's filter through the aggregation pipeline. Use when the user wants both the saved view and per-bucket counts.
- For ad-hoc per-bucket counts without a saved view, use `aggregate*Data` / `hybrid*Data` and emit Strategy-A links per bucket.

## Don't

- Don't call `createDeepLink` without chaining `getViews` + `getViewSettings` first.
- Don't call `createDeepLink` without `x-user-id` + `accessControl.emails` including the caller.
- Don't hand-assemble URLs and also call `createDeepLink` in the same response — pick one strategy.
- Don't loop `createDeepLink` per row/bucket — it's a write op; one saved view per filter scope.
- Don't render just the `shortCode` — always wrap it in the `https://platform.securin.io/deepLink?accountId=<>&shortCode=<>` format.
