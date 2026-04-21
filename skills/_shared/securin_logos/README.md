# Securin Logos

Drop Securin logo assets into this directory. Skills read them from here when rendering branded outputs (reports, dashboards, decks, infographics).

## Expected files

| Filename | Use |
|---|---|
| `Securin_logo_purple.svg` | Wordmark on light backgrounds (default) |
| `Securin_logo_purple.png` | PNG fallback for the purple wordmark |
| `Securin_logo_white.svg` | Wordmark on dark / gradient backgrounds |
| `Securin_logo_white.png` | PNG fallback for the white wordmark |

## Contributing

When adding a new logo variant, update this README and [_shared/brand.md](../brand.md) → *Logos* section so every skill picks it up.

## Fallback behavior

If a skill needs a logo and the file isn't present here, it falls back to a text header *"Securin"* rendered in `#712880` at weight 700 (per [_shared/brand.md](../brand.md)) and informs the user the image asset is unavailable.
