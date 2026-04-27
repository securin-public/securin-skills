---
name: securin-tool-search
description: >
  Use this skill when the user asks "is there a tool for...", "what MCP tools
  can...", "find a tool that does...", "how do I [capability not covered by
  other skills]", "list Securin tools related to [topic]", or when their
  request doesn't match any other skill's scope and you need to discover the
  right MCP tool before acting. This is the fallback skill — always prefer the
  dedicated workflow skills (triage, enrichment, correlation, remediation) when
  they fit. Requires the Securin Platform MCP server.
---

# Tool Search (Fallback Discovery)

## Purpose

The Securin MCP server exposes 300+ auto-generated tools from OpenAPI specs. Most user workflows are covered by the six dedicated skills in this plugin, but the long tail (creating tags, managing credentials, configuring connectors, admin tasks) isn't. This skill uses the server's built-in `search_tools` meta-tool to find the right MCP tool for an ad-hoc request and either run it (with preflight) or present the user a recipe.

## When to use

- "Is there a tool for managing tags?"
- "How do I create a connector?"
- "What MCP tools can I use for user management?"
- "Find a tool that exports dashboards"
- "List Securin tools related to credentials"
- Any user ask that doesn't match the other six skills' triggers.

## When NOT to use

Prefer the dedicated skill when the ask fits:

| User says something like… | Use this skill, not tool-search |
|---|---|
| "Find my critical exposures" | `securin-exposure-triage` |
| "Break down assets by type" | `securin-asset-triage` |
| "Tell me about CVE-XXXX" | `securin-cve-enrichment` |
| "Am I affected by…" | `securin-threat-correlation` |
| "How do I fix…" | `securin-remediation-guidance` |
| "List components running…" | `securin-product-triage` |

## Pre-flight

### Step 0 — Account preflight (CC-1, conditional)

See [_shared/account-preflight.md](references/_shared/account-preflight.md). Run the preflight **before** invoking a discovered tool that is account-scoped (most `search*Data`, `aggregate*Data`, `create*`, `update*`, `delete*`, `get*` tools). The `search_tools` meta-tool itself is not account-scoped and doesn't require preflight.

## Suggested tools

### Meta (always available)
- `search_tools` — BM25-ranked natural-language search over the server's tool catalog. Returns name, description, and ranking score.
- `ping` — server health check.

### After discovery
Whatever `search_tools` surfaces. Common follow-ups:
- Discovery utilities: `getApiFields`, `getSupportedActions`, `getConnectorCategories`, `getSystemCategories`.
- For write-actions: advise the user — write actions are restricted in MCP Milestone 1 per PRD.

### Deep links (CC-2)
- `createDeepLink` / `getDeepLink` — surface a deep link to the relevant platform UI section if one exists for the discovered capability.

## Workflow

### Step 1 — Formulate the query

Turn the user's ask into a short natural-language query for `search_tools`. Strip filler words; keep the intent.

| User said | Query to `search_tools` |
|---|---|
| "Is there a tool for managing tags?" | `"manage tags"` |
| "Find a tool that creates a connector" | `"create connector"` |
| "How do I export a dashboard?" | `"export dashboard"` |
| "List tools for user management" | `"user management"` |

### Step 2 — Call `search_tools`

```text
search_tools(query="<from step 1>", top_k=10)
```

Returns up to 10 tools ranked by relevance.

### Step 3 — Present candidates

Render a compact ranked list:

```markdown
Top MCP tools matching your query:

1. **`createTag`** — Create a tag in the account. *(score 0.91)*
2. **`associateTags`** — Associate tags with resources. *(score 0.87)*
3. **`getTagListDetails`** — List tags with filters. *(score 0.84)*
4. **`deleteTag`** — Delete a tag. *(score 0.79)*
5. …
```

### Step 4 — Decide the path

- **Clear winner + obvious inputs:** propose the call with concrete parameters, run Step 0 preflight if account-scoped, execute, and render result (with deep link via `createDeepLink` if applicable).
- **Multiple plausible candidates or missing inputs:** ask the user (via `AskUserQuestion` or a plain question) which tool to run and what parameters to pass.
- **Write-action tool identified:** warn the user that MCP Milestone 1 scope is read-only. Surface the tool and params so they can run it via the platform UI or a future write-enabled MCP release.

### Step 5 — Deep link (CC-2)

If the discovered tool operates on a known entity, generate a deep link:
- `createDeepLink(entityType=<entity>, filter=<matching filter>)` → filtered UI view.
- For admin / settings tools, link to the relevant settings page if the platform exposes one.

### Step 6 — Offer refinement

If `search_tools` returns low-relevance hits (top score < ~0.5) or no results, offer to:
- Re-query with different wording.
- Browse by category: `getSystemCategories`, `getConnectorCategories`, `getIntegrationCategories`.
- Fall back to a search of the full tool JSON in the plugin repo's `securin_mcp_tools.json` (if the user has it locally).

## Common recipes

### "Is there a tool for X?"
1. `search_tools(query="X")`.
2. Present top 5. Pick the top hit if score ≥ 0.7; otherwise ask user to choose.
3. Explain what each does in one line (from the description).

### "How do I do Y?"
1. `search_tools(query="Y")`.
2. Order by logical flow (e.g., `create*` → `get*` → `update*` → `delete*`).
3. Suggest a step-by-step recipe referencing the discovered tools.

### "List tools for Z"
1. `search_tools(query="Z", top_k=20)`.
2. Group by prefix / capability.
3. Return as a categorized list.

## Scope guard (CC-3)

- If during discovery you realize the ask fits a dedicated skill → hand off. Say: *"This is better handled by `securin-<skill>` — let me route you there."*
- Never duplicate a workflow that another skill owns.
- Never invent tool names — only use names returned by `search_tools`.

## Edge cases

- **`search_tools` returns zero** — try rewording the query; the index is BM25 and benefits from exact terms.
- **Tool discovered but user lacks permissions** — surface the permission error and suggest `hasActorAccessToResource` / `getEffectiveAccessPermissions` to introspect.
- **Tool exists but is deprecated / marked internal** — warn the user before invoking.
- **User wants a write action (create/update/delete) that M1 doesn't support** — tell them explicitly that MCP M1 is read-only for write operations and point to platform UI or future releases.

## Visual output (CC-4)

When this skill produces aggregated or multi-row data (counts, trends, distributions, comparisons, single-CVE reports), emit a chart/graph/infographic in the Securin brand palette (`#712880 / #453983 / #542ade / #987bf7 / #d7cbfb`), Lato font, light theme, with the Securin logo. Default colormap uses the monotone gradient defined in [_shared/brand.md](references/_shared/brand.md). Offer customization after delivery; never default to a different brand.

## References

- [Shared: Account Preflight](references/_shared/account-preflight.md)
- [Shared: Deep Links](references/_shared/deep-links.md)
- [Shared: FQL Grammar](references/_shared/fql-grammar.md)
- [Shared: Sorting Rules](references/_shared/sorting-rules.md)
- [Shared: Brand & Visual Communication](references/_shared/brand.md)
- Server's internal search index lives in `platform-mcp-server/src/securin_mcp/search.py` (BM25 over tool names + descriptions) — not directly invokable from this skill, but useful context.
