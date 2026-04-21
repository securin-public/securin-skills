# Account-ID Preflight (CC-1)

Every skill in this plugin MUST run this preflight as **Step 0** before any data-returning tool call. Skipping leaks cross-account data risk and produces unauthorized or empty results.

## The rule

Before you call any `search*Data`, `aggregate*Data`, `hybrid*Data`, or account-scoped `get*` tool, you MUST:

1. Know the account-id to scope the request to.
2. Trust that the caller's token has access (verified indirectly through `getUserProfile`).

## Step-by-step (revised per schema)

### 1. Determine account-id

In priority order:

1. **From the user's message.** If the user said "in account 42" or "use `acc-123`", use it.
2. **From earlier in this turn.** Reuse the resolved account-id. Re-prompt only if the user pivots.
3. **From `getUserProfile`.** The authoritative source. This is how we discover the accounts the caller's bearer token can see.
   - Parse the returned profile for the `accounts[]` (or equivalent) field.
   - If exactly **one** account → use it silently.
   - If **more than one** → list them by name + id and call `AskUserQuestion` to pick one (or multiple, if the workflow supports multi-account). Use `getAccountDetails` if you need display names for the picker.
   - If **zero** → surface the auth error and stop. Do not guess.
4. **Fallback: `listAccount(account-id=<parent>)`** — only relevant when the caller is a management / partner account wanting to operate on a sub-account. Requires the parent `account-id` already.

### 2. Validate access — the right way

❌ **`hasActorAccessToResource` does NOT validate account access.** Its `resource-type` enum is `[Views, Dashboards, Tags, Widgets]`. Use it for those resource types, not for accounts.

✅ **For account access, trust `getUserProfile`**: the accounts it returns are, by definition, accessible to the caller's token. No separate access check is required.

✅ **For per-resource permissions** (e.g., "can the caller *edit* this saved view?"), use:
- `getEffectiveAccess` — full permission snapshot.
- `getEffectiveAccessPermissions` — permissions list.
- `getEffectiveAccessWorkspaces` — which workspaces the caller can see within the account.
- `hasActorAccessToResource` — last step; only valid for the four resource types listed above.

### 3. Workspace scoping (when the question implies a subset)

If the user said "in prod", "the cloud BU", "the EU workspace", resolve workspace-ids with:

- `getEffectiveAccessWorkspaces(account-id=<>)` — workspaces the caller sees.
- `getWorkspacesByAccountId(account-id=<>)` — all workspaces in the account (may be broader than what the caller sees — intersect with effective-access result).

Include the workspace-ids as additional FQL constraints: e.g. `asset.workspaceId in ['ws-1','ws-2']` (confirm field path via `getApiFields` 🧪).

### 4. Cache for the turn

Resolved account-id and workspace-ids are stable for the rest of the turn. Re-prompt only on pivot.

## Tools used

| Tool | Purpose |
|---|---|
| `getUserProfile` | **Primary.** Returns the caller's profile + accessible accounts. |
| `getUserProfileByAccountId` / `getUserProfileByDefaultAccount` / `getUserProfileByWorkspaceId` | Alternate profile views by specific scope. |
| `getAccountDetails` | Enrich an account-id with display name for pickers. |
| `listAccount` | List sub-accounts of a parent (partner/management use only). |
| `getEffectiveAccess` / `getEffectiveAccessPermissions` | Full permission snapshot. |
| `getEffectiveAccessWorkspaces` / `getWorkspacesByAccountId` | Workspace-level scoping. |
| `hasActorAccessToResource` | **Only for** `Views, Dashboards, Tags, Widgets`. Not for accounts. |

## Boilerplate the user sees

> "I have access to 3 accounts on this token: **Acme Corp** (`42`), **Acme EU** (`43`), **Lab** (`99`). Which should I use?"

> "Using account `42` (Acme Corp) — confirmed via `getUserProfile`. Proceeding."

## Don't

- Don't hardcode an account-id.
- Don't guess from prior conversations that may have been in a different scope.
- Don't call `hasActorAccessToResource` with `resource-type: Account` — it will reject the request.
- Don't batch cross-account queries silently. If the user wants multiple accounts, loop explicitly and label results per account-id.
