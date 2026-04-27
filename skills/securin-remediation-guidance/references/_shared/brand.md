<!-- Mirrored from skills/_shared/brand.md. Do not edit here — edit the source and run scripts/sync-shared.sh. -->

# Securin Brand Guidelines (CC-4)

Every visual artifact a skill produces — reports, tables, charts, dashboards, infographics, slide-deck exports, PDFs — MUST follow Securin brand by default. The user can opt out or customize, but **you must apply Securin brand unless they do**.

## The hard rule

**Default to Securin brand on every visual output.** Before rendering, confirm theme/palette only when the user has *already* expressed a preference; otherwise ship Securin-branded and offer customization as a follow-up.

## Color palette

| Token | Hex | Role |
|---|---|---|
| **primary** | `#712880` | Securin primary purple — headings, brand strip, primary chart color |
| **primary-dark** | `#453983` | Secondary indigo — axes, dark UI text, emphasis |
| **accent-1** | `#542ade` | Vivid purple — key data callouts, primary action highlights |
| **accent-2** | `#987bf7` | Light purple — secondary series, hover states |
| **accent-3** | `#d7cbfb` | Lavender — backgrounds of callout cards, lightest bucket in scales |

### Monotone usage (default)

All five colors sit on a **single hue family** (purple/indigo). When a visual needs multiple series or severity bands, pick ordered slices from this palette in the order listed above. Do **not** pull in external colors (red/green/yellow) unless the user asks for traffic-light semantics — Securin's visual identity is monotone purple.

### Gradients (use liberally)

The palette is built for smooth gradients. Prefer a gradient fill over a flat color in:
- Hero panels / report covers
- Chart area fills (under line charts, inside bar fills)
- KPI cards
- Progress bars

Recommended gradient stops:
- **Primary gradient:** `#712880 → #542ade` (deep → vivid)
- **Soft gradient:** `#542ade → #d7cbfb` (vivid → lavender)
- **Background wash:** `#ffffff → #d7cbfb` (white → lavender, 0% → 100%)

CSS:
```css
background: linear-gradient(135deg, #712880 0%, #542ade 100%);
background: linear-gradient(135deg, #542ade 0%, #d7cbfb 100%);
```

Matplotlib / Plotly colormap:
```python
from matplotlib.colors import LinearSegmentedColormap
securin_cmap = LinearSegmentedColormap.from_list(
    "securin",
    ["#712880", "#453983", "#542ade", "#987bf7", "#d7cbfb"],
)
```

## Severity / ordinal mapping

When encoding severity (`Critical → Info`) or any ordinal bucket, map **darkest = worst**:

| Severity | Color |
|---|---|
| Critical | `#712880` |
| High | `#453983` |
| Medium | `#542ade` |
| Low | `#987bf7` |
| Info | `#d7cbfb` |

This keeps the visual monotone while preserving severity ordering at a glance.

## Typography

**Font stack (preferred order):**
1. `Lato`
2. `Google Sans`
3. `Roboto`
4. system sans-serif fallback (`-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`)

CSS:
```css
font-family: "Lato", "Google Sans", "Roboto", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

**Weights:**
- Body: 400
- Emphasis: 600
- Headings: 700

## Theme

**Default theme is LIGHT.**

- Page background: `#ffffff`
- Card / panel background: `#ffffff` with 1px border in `#d7cbfb` or subtle shadow
- Text: `#111111` (body), `#712880` (headings)
- Chart plot area: `#ffffff`
- Chart gridlines: `#d7cbfb` at 40% opacity
- Chart axes / ticks: `#453983`

Only switch to dark theme on explicit user request.

## Logos

Logo assets live in `_shared/securin_logos/`. Always use the vector/high-resolution asset for print or slide decks; use the PNG for inline HTML.

| Asset | Use when |
|---|---|
| `Securin_logo_purple.svg` / `.png` | Wordmark on light backgrounds (default) |
| `Securin_logo_white.svg` / `.png` | Wordmark on dark / gradient backgrounds |

Placement rules:
- Top-left of every exported report/deck/dashboard.
- Minimum clear space around the logo = height of the "S" character on all sides.
- Never recolor, distort, rotate, or add effects.
- Minimum width: 96px.

If a logo file is missing from `_shared/securin_logos/`, fall back to a text header *"Securin"* in primary (`#712880`) at weight 700 and inform the user the image asset is unavailable.

## Chart & graph conventions

- Use the monotone gradient colormap for heatmaps / sequential scales.
- For bar / column charts of a single series, fill with the primary gradient.
- For multi-series, pick from the palette in order (primary → primary-dark → accent-1 → accent-2 → accent-3). Stop at 5 series; if more, group the tail into "Other".
- Legend text and axis labels in `#453983` at weight 400.
- Title in `#712880` at weight 700.
- Always label the data — chart-without-numbers is half an insight.

### Plotly example

```python
import plotly.graph_objects as go
SECURIN_PALETTE = ["#712880", "#453983", "#542ade", "#987bf7", "#d7cbfb"]
fig = go.Figure(...)
fig.update_layout(
    font=dict(family="Lato, Google Sans, Roboto", size=13, color="#111"),
    title=dict(font=dict(family="Lato", size=20, color="#712880")),
    plot_bgcolor="#ffffff",
    paper_bgcolor="#ffffff",
    colorway=SECURIN_PALETTE,
    xaxis=dict(gridcolor="rgba(215,203,251,0.4)", linecolor="#453983"),
    yaxis=dict(gridcolor="rgba(215,203,251,0.4)", linecolor="#453983"),
)
```

### Matplotlib example

```python
import matplotlib.pyplot as plt
SECURIN_PALETTE = ["#712880", "#453983", "#542ade", "#987bf7", "#d7cbfb"]
plt.rcParams.update({
    "font.family": "Lato",
    "axes.prop_cycle": plt.cycler(color=SECURIN_PALETTE),
    "figure.facecolor": "#ffffff",
    "axes.facecolor":   "#ffffff",
    "axes.edgecolor":   "#453983",
    "axes.labelcolor":  "#453983",
    "xtick.color":      "#453983",
    "ytick.color":      "#453983",
    "axes.titlecolor":  "#712880",
    "grid.color":       "#d7cbfb",
    "grid.alpha":       0.4,
})
```

### HTML / CSS snippet

```html
<style>
  :root {
    --securin-primary: #712880;
    --securin-primary-dark: #453983;
    --securin-accent-1: #542ade;
    --securin-accent-2: #987bf7;
    --securin-accent-3: #d7cbfb;
    --securin-bg: #ffffff;
    --securin-body: #111111;
  }
  body {
    font-family: "Lato", "Google Sans", "Roboto", -apple-system, sans-serif;
    background: var(--securin-bg);
    color: var(--securin-body);
  }
  h1, h2, h3 { color: var(--securin-primary); font-weight: 700; }
  .card { background: #fff; border: 1px solid var(--securin-accent-3); border-radius: 8px; }
  .hero { background: linear-gradient(135deg, #712880 0%, #542ade 100%); color: #fff; }
</style>
```

## Customization — offer it, don't force it

After delivering a Securin-branded output, offer one line of customization options:

> *"This report uses Securin brand (purple monotone, light theme). Want to customize — e.g., dark theme, your company colors, swap the logo?"*

Respect any preference expressed in the same conversation or in CLAUDE.md / project instructions.

## Don't

- Don't substitute red/green/yellow for severity unless the user explicitly asks for a traffic-light scheme.
- Don't mix fonts — stick to the Lato → Google Sans → Roboto stack.
- Don't use a dark background by default.
- Don't drop the logo on exported reports/decks.
- Don't ship a plain markdown table when a bar chart would tell the story better — visual communication is mandatory (see CC-4 below).

---

## CC-4 — Visual communication is mandatory

**Every skill response that returns aggregated or multi-row data MUST produce a visual artifact when the delivery channel supports it.** Markdown alone is not enough for:

- Any aggregation result (counts by severity, workspace, scanner, etc.)
- Time series (exposure trend, remediation velocity, new-vs-closed over time)
- Distribution (asset criticality histogram, component version distribution)
- Comparison (prod vs non-prod, KEV vs non-KEV, quarter-over-quarter)
- Executive summaries / single-CVE reports

### Pick the right chart

| Data shape | Chart |
|---|---|
| Single-series categorical count | **Bar** (horizontal if labels are long) |
| Multi-series categorical | **Grouped / stacked bar** |
| Time series | **Line** (area fill with the soft gradient) |
| Distribution | **Histogram** or **box plot** |
| Part-to-whole | **Donut** (never pie — donuts read better) |
| Heatmap (e.g., severity × workspace) | **Heatmap** with `securin_cmap` |
| KPI single-number | **Big-number card** with gradient background |

### Rendering path

- In Claude Code and other MCP clients that support file artifacts: render PNG/SVG/HTML and attach it.
- In text-only channels: emit an ASCII/block-character bar chart (`▇▇▇▆▅▃`) plus the underlying table and note that a graphical version is available on request.

### Infographics

For CVE-enrichment and zero-day reports, build a single-page infographic: hero panel (gradient) with the CVE title + verdict, KPI row (CVSS / EPSS / SVRS / KEV), affected-products grid, and threat-actor chips — all using the palette + logo.

### Don't

- Don't produce a pure-markdown response when a chart/infographic would communicate the same data faster.
- Don't render a chart without labels.
- Don't skip the brand palette and fonts.

See also: [_shared/account-preflight.md](account-preflight.md) · [_shared/deep-links.md](deep-links.md) · [_shared/fql-grammar.md](fql-grammar.md) · [_shared/sorting-rules.md](sorting-rules.md)
