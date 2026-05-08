# Account-ID Preflight (CC-1)

Every skill in this plugin MUST run this preflight as **Step 0** before any data-returning tool call. Skipping leaks cross-account data risk and produces unauthorized or empty results.

## The rule

Before you call any `search*Data`, `aggregate*Data`, or account-scoped `get*` tool, you MUST:

1. Know the account-id to scope the request to.
2. Trust that the caller's token has access once you have the account-id — no tool call needed to verify this.

## Step-by-step (revised per schema)

### 1. Determine account-id

In priority order:

1. **From the user's message.** If the user said "in account 42" or "use `acc-123`", use it.
2. **From earlier in this turn.** Reuse the resolved account-id. Re-prompt only if the user pivots.
3. **Ask the user directly.** If the account-id was not provided and is not cached, stop and ask: "Which account ID should I use?" Do **not** call any tool to discover accounts — large deployments return thousands of entries and block the workflow.

### 2. Validate access — the right way

✅ **For account access:** once the user provides an account-id, trust it — no tool call is needed to validate access. `getUserProfileByAccountId` is available only if you need to fetch the user's display name or role for the response.

✅ **For per-resource permissions** (e.g., "can the caller *edit* this saved view?"), use:
- `getEffectiveAccess` — full permission snapshot.
- `getEffectiveAccessPermissions` — permissions list.
- `getEffectiveAccessWorkspaces` — which workspaces the caller can see within the account.

### 3. Workspace scoping (when the question implies a subset)

If the user said "in prod", "the cloud BU", "the EU workspace", resolve workspace-ids with:

- `getEffectiveAccessWorkspaces(account-id=<>)` — workspaces the caller sees.
- `getWorkspacesByAccountId(account-id=<>)` — all workspaces in the account (may be broader than what the caller sees — intersect with effective-access result).

Include the workspace-ids as additional FQL constraints: e.g. `asset.workspaceId in ['ws-1','ws-2']` (confirm field path via `getApiFields` 🧪).

### 4. Cache for the turn

Resolved account-id and workspace-ids are stable for the rest of the turn. Re-prompt only on pivot.

## Detect the active model

Call `getAccountSettings` for the resolved account-id (from the CC-1 preflight) using the following payload:

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

**Cache the result for the turn. You MUST do this before making any calls to retrieve asset or exposure data.** The flag rarely changes within a conversation.

## Tools used

| Tool | Purpose |
|---|---|
| `getUserProfileByAccountId` | Validate access for a known account-id. |
| `getUserProfileByDefaultAccount` | Use only when a single default account is expected. |
| `getAccountDetails` | Enrich an account-id with display name for pickers. |
| `listAccounts` | List sub-accounts of a parent (partner/management use only). |
| `getEffectiveAccess` / `getEffectiveAccessPermissions` | Full permission snapshot. |
| `getEffectiveAccessWorkspaces` / `getWorkspacesByAccountId` | Workspace-level scoping. |
| `getAccountSettings` | Checks account-level feature flags (e.g., composite vs. source models). |

## Boilerplate the user sees

> "To proceed I need an account ID — please share it (e.g. `42` or `acc-123`)."

> "Using account `42` (Acme Corp) — confirmed via `getUserProfileByAccountId`. Proceeding."

## Don't

- Don't hardcode an account-id.
- Don't guess from prior conversations that may have been in a different scope.
- Don't batch cross-account queries silently. If the user wants multiple accounts, loop explicitly and label results per account-id.
