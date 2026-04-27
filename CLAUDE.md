# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **distribution package** for the Securin Platform plugin. There is no application code, no build step, and no test suite. The repo ships two things:

1. **8 agent skills** under `skills/` — `SKILL.md` files following the [Agent Skills](https://openai.com/index/agentic-ai-foundation/) open standard (YAML frontmatter + markdown). Each skill is a runtime workflow loaded by the host agent on demand.
2. **MCP wiring** — `.mcp.json` configures the host to connect to `https://mcp.securin.io/mcp` via `npx mcp-remote`. The MCP server itself lives in a separate repo (`securin-inc/securin-mcp`).

`.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` are the Claude Code plugin/marketplace manifests. They are the only Claude-Code-specific surface — everything else (skills, `.mcp.json`) is host-agnostic and works in Cursor, Copilot, Codex CLI, Gemini CLI, Windsurf, etc. Per-host install steps live in `README.md`.

## Architecture: how the skills compose

Every skill is intentionally narrow (one workflow per file) and they coordinate through four cross-cutting invariants. **`skills/_shared/` is the source of truth.** Each skill carries a generated mirror at `skills/<skill>/references/_shared/` so that an extracted skill folder is self-contained. **Edit only `skills/_shared/`; never edit a per-skill copy** — `scripts/sync-shared.sh` rewrites the mirrors and a CI check (`.github/workflows/sync-check.yml`) fails the build if they drift.

Skills link into their own bundled copy (e.g. `references/_shared/account-preflight.md`), not into `../_shared/`. This keeps a skill's references resolvable when the folder is extracted into another host's skill directory.

| Shared doc | What it enforces | When skills must apply it |
|---|---|---|
| `_shared/account-preflight.md` (CC-1) | Resolve and confirm an account-id before any data-returning call | **Step 0** of every skill, before any `search*Data` / `aggregate*Data` / `hybrid*Data` / account-scoped `get*` call |
| `_shared/deep-links.md` (CC-2) | Use `getViews` → `getViewSettings` → `createDeepLink` to give users clickable links back into the platform UI | Whenever a skill surfaces platform entities |
| `_shared/composite-vs-source.md` | Detect whether the account uses the composite or source asset data model and pick the right tools/fields | Any asset/exposure/component query — wrong model returns empty or stale results |
| `_shared/fql-grammar.md` | Canonical FQL syntax (single-quoted strings, `today() - 30` date functions, etc.) used by `filters` arguments | Any tool that accepts an FQL `filters` string |
| `_shared/sorting-rules.md` | Canonical sort keys per entity (e.g. exposures sort on `exposures.scores.score` desc — note the plural) | Any skill that returns a ranked list |
| `_shared/brand.md` (CC-4) | Default to Securin purple monotone palette + Lato + wordmark on every visual artifact unless the user opts out | Any chart, report, infographic, or deck output |

**Skill scope discipline (CC-3):** each skill's frontmatter `description` says exactly when it activates *and* which sibling skill to defer to when the ask drifts. When editing a skill, treat that boundary as load-bearing — re-route rather than absorbing scope from another skill. The seven-skill scope matrix is encoded in `README.md` ("Skills reference" table).

### Skill file layout

```
skills/<skill-name>/
  SKILL.md                    # frontmatter + workflow (must stay focused; offload depth to references/)
  references/
    <skill-specific>.md       # supplementary docs the skill links to from SKILL.md
    _shared/                  # GENERATED mirror of skills/_shared/ — do not edit
```

The agent loads `SKILL.md` first, then follows links into `references/` only when needed (progressive disclosure). A skill folder is shippable on its own: copy `skills/securin-cve-enrichment/` to any host's skills directory and it works.

### Brand assets

`skills/_shared/securin_logos/` holds the wordmark files referenced from `brand.md`. Filenames are load-bearing (`Securin_logo_purple.svg/.png`, `Securin_logo_white.svg/.png`) — branded outputs pick them up by name. The logo dir is mirrored into each skill at `references/_shared/securin_logos/` by the sync script.

## Editing skills — gotchas

- **Frontmatter `description` is the trigger surface.** The host agent decides whether to load a skill based on this field. Edit it like a search query: include the user phrasings ("enrich this CVE", "am I affected by…") that should activate it, and the negative pointers to sibling skills.
- **Tool names are tied to the upstream OpenAPI spec** served by the MCP server (`mcp.securin.io/mcp`). Don't invent tool names — the canonical list is whatever the MCP exposes at runtime. `securin-tool-search` is the fallback discovery skill when an ask doesn't match the other seven.
- **FQL string literals must use single quotes** (`exposure.status = 'Open'`). Double quotes will silently fail. See `_shared/fql-grammar.md`.
- **Sort path for exposures is `exposures.scores.score` (plural).** The singular `exposure.scores.overallScore` is filter-only. Mixing them up is the most common skill bug.

## Validating changes

The only CI gate is `shared-sync-check` (`.github/workflows/sync-check.yml`), which runs `scripts/sync-shared.sh --check` and fails if any per-skill `references/_shared/` mirror is stale. After editing anything under `skills/_shared/`, run:

```bash
bash scripts/sync-shared.sh        # rewrite all mirrors
bash scripts/sync-shared.sh --check # verify (also what CI runs)
```

Beyond that, manual checks:

- **Marketplace install** — after editing `plugin.json` / `marketplace.json`, install via `/plugin marketplace add <local-path>` then `/plugin install securin-platform@securin-skills` in Claude Code and confirm the skills and MCP both appear.
- **Skill triggering** — in a fresh session, run the example phrasing from the README's "Prompts to try" and confirm the agent loads the right skill (it announces "Using <skill> to …").
- **End-to-end smoke** — *"Enrich CVE-2024-3400."* exercises `securin-cve-enrichment` + the MCP path + brand rendering in one shot.
- **Standalone-skill smoke** — copy a single `skills/securin-*/` folder to a fresh location and confirm all `references/_shared/...` links inside `SKILL.md` resolve without `skills/_shared/` being present.

## Repo layout (quick reference)

```
.claude-plugin/        # Claude Code plugin + marketplace manifests
.mcp.json              # MCP server wiring (npx mcp-remote → mcp.securin.io)
scripts/
  sync-shared.sh       # mirrors skills/_shared/ into every skill's references/_shared/
.github/workflows/
  sync-check.yml       # CI: fails if mirrors are stale
skills/
  _shared/             # SOURCE OF TRUTH for cross-cutting invariants — edit here only
  securin-*/
    SKILL.md           # workflow entry point
    references/
      _shared/         # generated mirror — never edit
      <other>.md       # skill-specific supplementary docs
README.md              # user-facing install + per-host setup
SECURITY.md            # disclosure policy
```

## Authentication model (don't break this)

The plugin ships **no bearer tokens, no client secrets, no env vars**. Auth is delegated to `mcp-remote`, which opens a browser to `auth.securin.io` on first use and caches the credential under `~/.mcp-auth`. If you find yourself adding env-var configuration to `.mcp.json` or to skills, stop — the design promise is "no token paste, no rotation."
