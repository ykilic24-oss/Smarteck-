# Smarteck — design canvas

Source for the Smarteck design canvas. Each `.dc.html` file is one artboard;
`canvas.json` positions them and picks the launch view.

| File | Artboard |
| --- | --- |
| `Main.dc.html` | Landing page, 1440 wide, flowing |
| `Dashboard.dc.html` | Web dashboard, 1440 × 900 |
| `MobileApp.dc.html` | Phone app, 390 × 844 |
| `DirectionB.dc.html` | Alternate art direction — "Warm domestic" (low-fi) |
| `DirectionC.dc.html` | Alternate art direction — "Utility brutalist" (low-fi) |

`smarteck-screens.html` is the assembled canvas; it is regenerated from the
files above, so edit the artboards, not the assembled file.

## Design system (Direction A — "Instrument panel")

Type: Archivo (display/headings), IBM Plex Sans (body), IBM Plex Mono (data,
labels, eyebrows).

| Token | Value | Use |
| --- | --- | --- |
| ink-900 | `#141310` | page ground |
| ink-800 | `#1C1A16` | cards, surfaces |
| ink-700 | `#232019` | raised / inset |
| line | `#2E2A22` | borders |
| line-strong | `#3B362C` | emphasis borders |
| text | `#F2EEE6` | primary |
| text-2 | `#A8A196` | secondary |
| text-3 | `#6F6959` | muted, mono labels |
| amber | `#E9A23B` | primary accent, CTAs, energy |
| cyan | `#35C3C6` | status "healthy", local/offline-capable |
| red | `#E0644B` | alerts only |

Amber and cyan are one accent pair at matched lightness and chroma, hue-varied.
Red is reserved for alert states and is never a series or decorative colour.

## Placeholders

Anything in `[SQUARE BRACKETS]` is a real fact that was not available — prices,
counts, customer names, company address, version numbers. Replace before this
goes anywhere public. Dashboard figures are sample data chosen to give the
chart a realistic shape.
