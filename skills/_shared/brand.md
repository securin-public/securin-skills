# Securin Brand Guidelines (CC-4)

Every visual artifact a skill produces — reports, tables, charts, dashboards, infographics, slide-deck exports, PDFs — MUST follow Securin brand by default. The user can opt out or customize, but **you must apply Securin brand unless they do**.

## The hard rule

**Default to Securin brand on every visual output.** Before rendering, confirm theme/palette only when the user has *already* expressed a preference; otherwise ship Securin-branded and offer customization as a follow-up.

## Brand purple scale

Every purple used anywhere in Securin visuals comes from this one scale. Never introduce a purple that isn't on it.

| Token | Hex | Anchor |
|---|---|---|
| `purple-900` | `#4D268D` | |
| `purple-800` | `#5F29B7` | |
| `purple-700` | `#6F2DDA` | |
| `purple-600` | `#7F30FF` | **brand primary** — light-mode accent, light-mode logo mark |
| `purple-500` | `#9C66FF` | dark-mode logo mark |
| `purple-400` | `#B083FD` | |
| `purple-300` | `#CEB6FC` | light-mode background accent, dark-mode primary accent |
| `purple-200` | `#E3D6FC` | |
| `purple-100` | `#F0E8FD` | |
| `purple-50` | `#F7F4FD` | |

## Core UI colors

| Token | Hex | Role |
|---|---|---|
| **primary** | `#7F30FF` | Brand purple — accents, highlights, key data callouts, links |
| **secondary** | `#E96001` | Buttons, CTAs, labels |
| **accent** | `#9C66FF` | Secondary highlights, hover states |
| **accent-soft** | `#CEB6FC` | Callout-card backgrounds, subtle fills |
| **text-primary** | `#241D30` | Titles, subtitles, body text |
| **text-secondary** | `#3C364A` | Muted text, axes, ticks, legends |
| **bg** | `#F3F3F3` | Page background |
| **surface** | `#FDFCFD` | Card / panel background |

Headings are `#241D30` (ink), not purple. Purple is an **accent**, not a heading color — use it for emphasis, data marks, rules, and callouts.

## Multi-series chart palette (primary sequence)

Assign in order, starting at position 1. **Max 10 distinct series. Never skip or shuffle.**

| Position | Hex |
|---|---|
| 1 | `#9C66FF` |
| 2 | `#7F30FF` |
| 3 | `#E96001` |
| 4 | `#4D268D` |
| 5 | `#DD639C` |
| 6 | `#6F2DDA` |
| 7 | `#F7C22B` |
| 8 | `#FC4839` |
| 9 | `#169AE6` |
| 10 | `#90CC63` |

Group any tail beyond 10 series into **"Other"** (`#F7F8F9`).

### Single-value charts

Use the brand primary: `#7F30FF`. Alternatives, all from the purple scale: `#9C66FF`, `#6F2DDA`, `#4D268D`.

### Dual-value combos

| Combo | Color 1 | Color 2 |
|---|---|---|
| 1 | `#9C66FF` | `#7F30FF` |
| 2 | `#4D268D` | `#DD639C` |
| 3 | `#7F30FF` | `#E96001` |
| 4 | `#6F2DDA` | `#CEB6FC` |

## Severity & criticality — CHML (semantic & fixed)

CHML colors are **semantic and fixed — never reorder them, and never use them for non-severity data.** They intentionally use a red → amber → gray scale because severity carries meaning the viewer reads at a glance. This is the **one** place Securin visuals use traffic-light semantics; everywhere else stays on the purple/multi-series palette.

**Severity:**

| Severity | Hex |
|---|---|
| Critical | `#A60D08` |
| High | `#FD766B` |
| Medium | `#F99930` |
| Low | `#F7C22B` |
| Info | `#C5CBD6` |

**Asset criticality** (same scale; Minor replaces Info):

| Criticality | Hex |
|---|---|
| Critical | `#A60D08` |
| High | `#FD766B` |
| Medium | `#F99930` |
| Low | `#F7C22B` |
| Minor | `#90CC63` |

**CHML + Other** (severity with an overflow bucket):

| Bucket | Hex |
|---|---|
| Critical | `#A60D08` |
| High | `#FD766B` |
| Medium | `#F99930` |
| Low | `#F7C22B` |
| Info | `#C5CBD6` |
| Other | `#9C66FF` |

## Ordinal ramps

### Prioritization funnel (5-stop purple, top = darkest = most urgent)

| Stop | Hex |
|---|---|
| 1 (top / most urgent) | `#4D268D` |
| 2 | `#6F2DDA` |
| 3 | `#9C66FF` |
| 4 | `#CEB6FC` |
| 5 (bottom / least urgent) | `#F0E8FD` |

Do **not** reverse this order.

### Threat-actor map (5-stop red, darkest = least)

| Stop | Hex |
|---|---|
| 1 (darkest) | `#A60D08` |
| 2 | `#FD766B` |
| 3 | `#FBBAB8` |
| 4 | `#F3D1D1` |
| 5 (lightest) | `#FFEBEB` |

### Sequential ramps (heatmaps, tree maps, scales)

**Purple, 10-stop** — this is the brand purple scale, darkest → lightest:

`#4D268D → #5F29B7 → #6F2DDA → #7F30FF → #9C66FF → #B083FD → #CEB6FC → #E3D6FC → #F0E8FD → #F7F4FD`

**Red, 10-stop** (`#A60D08` darkest = most severe → `#FFF7F7` lightest):

`#A60D08 → #E35D52 → #FD766B → #FF8F86 → #FFA59D → #FFBAB4 → #FFCDC8 → #FFDDDA → #FFEEED → #FFF7F7`

Use the purple ramp as the default colormap for heatmaps and sequential scales.

## Gradients — backgrounds only

**Gradients are background decoration only. Never apply a gradient to chart bars, lines, or pie/donut slices** — chart marks use flat fills at 100% opacity.

```css
/* Direction: 90° — hero panels, report covers, KPI card backgrounds */
background: linear-gradient(90deg, #7F30FF 0%, #CEB6FC 100%);
```

## Usage rules

| Rule | Detail |
|---|---|
| Series order | Series 1 = `#9C66FF`, then follow the fixed sequence above. Never skip or shuffle. |
| Severity | CHML colors are semantic and fixed. Must not be used for non-severity data. |
| Funnel | Use only the 5-stop purple ramp. Top = darkest, bottom = lightest. Do not reverse. |
| Gradient | Background decoration only. Never on chart bars, lines, or slices. |
| Gray (`#F7F8F9`) | Reserved for "Other", "Unknown", or unavailable data categories. Not a series color. |
| Opacity | 100% on all chart fills. Use 40% opacity only for hover / active highlight states. |

## Typography

**Font stack (preferred order):**
1. `Poppins` — headings and titles
2. `DM Sans` — body text, labels, axis and legend text
3. `Lato` — fallback
4. system sans-serif fallback (`-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`)

CSS:
```css
--font-heading: "Poppins", "DM Sans", "Lato", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
--font-body:    "DM Sans", "Lato", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
```

**Weights:**
- Body: 400 (DM Sans)
- Labels / emphasis: 500 (DM Sans)
- Headings: 600 (Poppins SemiBold)

Do not use 700 — Poppins SemiBold at 600 is the heaviest weight in the system.

## Theme

**Default theme is LIGHT.** Only switch to dark on explicit user request.

### Light (default)

| Surface | Value |
|---|---|
| Page background | `#F3F3F3` |
| Card / panel background | `#FDFCFD`, 1px border in `#E3D6FC` |
| Title / heading text | `#241D30` |
| Body text | `#241D30` |
| Muted text, axes, ticks | `#3C364A` |
| Accent / highlight | `#7F30FF` |
| Chart plot area | `#FDFCFD` |
| Chart gridlines | `rgba(127, 48, 255, 0.15)` |

### Dark (on request)

| Surface | Value |
|---|---|
| Page background | `#241D30` |
| Card / panel background | `#3C364A` |
| Title / heading text | `#FDFCFD` |
| Body text | `#FDFCFD` |
| Muted text, axes, ticks | `rgba(253, 252, 253, 0.72)` |
| Accent / highlight | `#CEB6FC` |
| Secondary / CTA | `#FD9825` |
| Background accent | `#7F30FF` |
| Chart gridlines | `rgba(206, 182, 252, 0.18)` |

> Note: the brand deck lists `#3C364A` for *both* dark card background and dark body text, which would render body copy invisible against its own card. Muted dark text therefore uses `#FDFCFD` at 72% opacity until the deck is corrected.

## Logos

Logo assets live in `_shared/securin_logos/`. Always use the SVG for print, slide decks, or anywhere it may be scaled; use the PNG for inline HTML where SVG is awkward.

| Asset | Use when |
|---|---|
| `securin-wordmark-on-light.svg` / `.png` | Full wordmark on light backgrounds (default) |
| `securin-wordmark-on-dark.svg` / `.png` | Full wordmark on dark / gradient backgrounds |
| `securin-icon-on-light.svg` / `.png` | "S" mark alone on light backgrounds — favicons, avatars, tight spaces |
| `securin-icon-on-dark.svg` / `.png` | "S" mark alone on dark backgrounds |

The wordmark's mark renders `#7F30FF` on light and `#9C66FF` on dark; letterforms are `#191717` on light and `#F8F8F8` on dark.

Placement rules:
- Top-left of every exported report/deck/dashboard.
- Minimum clear space around the logo = height of the "S" character on all sides.
- Never recolor, distort, rotate, or add effects.
- Minimum width: 96px for the wordmark, 24px for the icon.

If a logo file is missing from `_shared/securin_logos/`, fall back to a text header *"Securin"* in `#7F30FF` at weight 600 and inform the user the image asset is unavailable.

## Chart & graph conventions

- For a single series, fill with the single-value color `#7F30FF` (flat — not a gradient).
- For multi-series, assign from the primary sequence in order (`#9C66FF → #7F30FF → #E96001 → …`). Stop at 10 series; group the tail into "Other" (`#F7F8F9`).
- For severity / criticality, use the fixed CHML colors — never the series palette.
- Use the 10-stop purple ramp as the colormap for heatmaps / sequential scales.
- Chart fills at 100% opacity; use 40% only for hover / active states.
- Legend text and axis labels in `#3C364A` at weight 400.
- Title in `#241D30` at weight 600.
- Always label the data — a chart without numbers is half an insight.

### Plotly example

```python
import plotly.graph_objects as go
SECURIN_PALETTE = [
    "#9C66FF", "#7F30FF", "#E96001", "#4D268D", "#DD639C",
    "#6F2DDA", "#F7C22B", "#FC4839", "#169AE6", "#90CC63",
]
fig = go.Figure(...)
fig.update_layout(
    font=dict(family="DM Sans, Lato, sans-serif", size=13, color="#241D30"),
    title=dict(font=dict(family="Poppins, DM Sans, sans-serif", size=20, color="#241D30")),
    plot_bgcolor="#FDFCFD",
    paper_bgcolor="#FDFCFD",
    colorway=SECURIN_PALETTE,
    xaxis=dict(gridcolor="rgba(127,48,255,0.15)", linecolor="#3C364A", tickcolor="#3C364A"),
    yaxis=dict(gridcolor="rgba(127,48,255,0.15)", linecolor="#3C364A", tickcolor="#3C364A"),
)
```

### Matplotlib example

```python
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

SECURIN_PALETTE = [
    "#9C66FF", "#7F30FF", "#E96001", "#4D268D", "#DD639C",
    "#6F2DDA", "#F7C22B", "#FC4839", "#169AE6", "#90CC63",
]
# Sequential colormap for heatmaps / scales — brand purple scale, light → dark (darkest = highest value)
securin_cmap = LinearSegmentedColormap.from_list(
    "securin",
    ["#F7F4FD", "#F0E8FD", "#E3D6FC", "#CEB6FC", "#B083FD",
     "#9C66FF", "#7F30FF", "#6F2DDA", "#5F29B7", "#4D268D"],
)
plt.rcParams.update({
    "font.family": "DM Sans",
    "axes.prop_cycle": plt.cycler(color=SECURIN_PALETTE),
    "figure.facecolor": "#FDFCFD",
    "axes.facecolor":   "#FDFCFD",
    "axes.edgecolor":   "#3C364A",
    "axes.labelcolor":  "#3C364A",
    "xtick.color":      "#3C364A",
    "ytick.color":      "#3C364A",
    "axes.titlecolor":  "#241D30",
    "grid.color":       "#7F30FF",
    "grid.alpha":       0.15,
})
```

### HTML / CSS snippet

```html
<style>
  :root {
    /* Core UI */
    --securin-primary: #7F30FF;
    --securin-secondary: #E96001;
    --securin-accent: #9C66FF;
    --securin-accent-soft: #CEB6FC;
    --securin-text-primary: #241D30;
    --securin-text-secondary: #3C364A;
    --securin-bg: #F3F3F3;
    --securin-surface: #FDFCFD;

    /* Brand purple scale */
    --purple-900: #4D268D;
    --purple-800: #5F29B7;
    --purple-700: #6F2DDA;
    --purple-600: #7F30FF;
    --purple-500: #9C66FF;
    --purple-400: #B083FD;
    --purple-300: #CEB6FC;
    --purple-200: #E3D6FC;
    --purple-100: #F0E8FD;
    --purple-50:  #F7F4FD;

    /* Multi-series palette */
    --s-color-1: #9C66FF;
    --s-color-2: #7F30FF;
    --s-color-3: #E96001;
    --s-color-4: #4D268D;
    --s-color-5: #DD639C;
    --s-color-6: #6F2DDA;
    --s-color-7: #F7C22B;
    --s-color-8: #FC4839;
    --s-color-9: #169AE6;
    --s-color-10: #90CC63;

    /* Severity (CHML) */
    --severity-critical: #A60D08;
    --severity-high: #FD766B;
    --severity-medium: #F99930;
    --severity-low: #F7C22B;
    --severity-info: #C5CBD6;

    /* Type */
    --font-heading: "Poppins", "DM Sans", "Lato", -apple-system, sans-serif;
    --font-body: "DM Sans", "Lato", -apple-system, sans-serif;
  }
  body {
    font-family: var(--font-body);
    background: var(--securin-bg);
    color: var(--securin-text-primary);
  }
  h1, h2, h3 { font-family: var(--font-heading); color: var(--securin-text-primary); font-weight: 600; }
  .card { background: var(--securin-surface); border: 1px solid var(--purple-200); border-radius: 8px; }
  /* Gradient = background decoration only, never on chart marks */
  .hero { background: linear-gradient(90deg, #7F30FF 0%, #CEB6FC 100%); color: #FDFCFD; }
</style>
```

## Customization — offer it, don't force it

After delivering a Securin-branded output, offer one line of customization options:

> *"This report uses Securin brand (purple / multi-series palette, light theme). Want to customize — e.g., dark theme, your company colors, swap the logo?"*

Respect any preference expressed in the same conversation or in CLAUDE.md / project instructions.

## Don't

- Don't reorder or recolor the CHML severity scale, and don't use those semantic red/amber colors for non-severity data.
- Don't apply gradients to chart bars, lines, or pie/donut slices — gradients are background-only.
- Don't skip or shuffle the multi-series sequence; assign in order starting at `#9C66FF`.
- Don't introduce a purple that isn't on the brand purple scale.
- Don't mix fonts — stick to the Poppins → DM Sans → Lato stack.
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
| Time series | **Line** (flat fill — no gradient on the line or area) |
| Distribution | **Histogram** or **box plot** |
| Part-to-whole | **Donut** (never pie — donuts read better) |
| Heatmap (e.g., severity × workspace) | **Heatmap** with `securin_cmap` (10-stop purple ramp) |
| KPI single-number | **Big-number card** with gradient background |

### Rendering path

- In Claude Code and other MCP clients that support file artifacts: render PNG/SVG/HTML and attach it.
- In text-only channels: emit an ASCII/block-character bar chart (`▇▇▇▆▅▃`) plus the underlying table and note that a graphical version is available on request.

### Infographics

For CVE-enrichment and zero-day reports, build a single-page infographic: hero panel (gradient background) with the CVE title + verdict, KPI row (CVSS / EPSS / SVRS / KEV), affected-products grid, and threat-actor chips — all using the palette + logo.

### Don't

- Don't produce a pure-markdown response when a chart/infographic would communicate the same data faster.
- Don't render a chart without labels.
- Don't skip the brand palette and fonts.

See also: [_shared/account-preflight.md](account-preflight.md) · [_shared/deep-links.md](deep-links.md) · [_shared/fql-grammar.md](fql-grammar.md) · [_shared/sorting-rules.md](sorting-rules.md)
