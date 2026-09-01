# Securin Logos

Securin logo assets. Skills read them from here when rendering branded outputs (reports, dashboards, decks, infographics).

## Files

| Filename | Use |
|---|---|
| `securin-wordmark-on-light.svg` | Full wordmark on light backgrounds (default) |
| `securin-wordmark-on-light.png` | PNG fallback for the light-background wordmark |
| `securin-wordmark-on-dark.svg` | Full wordmark on dark / gradient backgrounds |
| `securin-wordmark-on-dark.png` | PNG fallback for the dark-background wordmark |
| `securin-icon-on-light.svg` | "S" mark alone on light backgrounds — favicons, avatars, tight spaces |
| `securin-icon-on-light.png` | PNG fallback for the light-background icon |
| `securin-icon-on-dark.svg` | "S" mark alone on dark backgrounds |
| `securin-icon-on-dark.png` | PNG fallback for the dark-background icon |

Prefer the SVG anywhere the asset may be scaled (print, slide decks, high-DPI). Use the PNG for inline HTML where SVG is awkward.

## Colors

| Element | On light | On dark |
|---|---|---|
| "S" mark | `#7F30FF` | `#9C66FF` |
| Wordmark letterforms | `#191717` | `#F8F8F8` |

## Contributing

When adding a new logo variant, update this README and [_shared/brand.md](../brand.md) → *Logos* section so every skill picks it up. Keep filenames lowercase and hyphenated — no spaces, so references don't need URL-encoding.

## Fallback behavior

If a skill needs a logo and the file isn't present here, it falls back to a text header *"Securin"* rendered in `#7F30FF` at weight 600 (per [_shared/brand.md](../brand.md)) and informs the user the image asset is unavailable.
