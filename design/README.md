# Smarteck — design canvas

Artboards recreated from `smarteck-website.html` (the live site source). Each
`.dc.html` file is one artboard; `canvas.json` positions them.

| File | Artboard |
| --- | --- |
| `Main.dc.html` | Homepage, desktop — 1440 frame, 1180 content, flowing |
| `Mobile.dc.html` | Homepage, 390 × 844 — header + hero, with the proposed mobile header |
| `MobileMenu.dc.html` | Mobile menu, 390 × 844 — **new**, does not exist on the site today |

`smarteck-screens.html` is the assembled canvas; it is regenerated from the
files above, so edit the artboards, not the assembled file.

## Design system

Lifted verbatim from the site's own `:root`, not re-derived.

Type: Space Grotesk 500/700 (display), IBM Plex Sans 400/500/600 (body),
IBM Plex Mono 500 (labels). Body 17px / 1.65. No border radius anywhere.

| Token | Value |
| --- | --- |
| `--navy` | `#112B3B` |
| `--navy-2` | `#12314A` |
| `--koper` | `#BE612E` |
| `--koper-lt` | `#E8A882` |
| `--koper-dk` | `#8E4A20` |
| `--aqua` | `#1D8F91` |
| `--aqua-lt` | `#96CCCC` |
| `--kalk` | `#F5F3EF` |
| `--kalk-2` | `#EAE6DE` |
| `--zink` | `#5F6E78` |
| `--zink-lt` | `#AEB8BE` |

Layout: `--maxw` 1180px, `--pad` 32px.

## Findings against the live site

Fixed in the recreation:

- **`ul.tight` has no CSS rule.** It is used twice in the "Voor wie" cards, and
  the global `*{margin:0;padding:0}` reset strips the list indent, so the
  markers sit outside the content box. Restored with `list-style:disc;
  padding-left:20px`.

Flagged, not changed — these are visible brand decisions:

- **No mobile navigation at all.** `@media(max-width:900px){nav.main{display:none}}`
  hides the menu and nothing replaces it. `MobileMenu.dc.html` is the proposal.
- **Header overflows on a phone.** Logo plus the "Vormen doorrekenen" button is
  wider than the 326px of content available at 390px.
- **Hero buttons break ragged on a phone.** Two inline-blocks with
  `margin-left:10px`; they want to be stacked and full-width below 900px.
- **Contrast: `.fbot` is 2.78:1.** `--zink` on `--navy` at 11px, in the footer
  bottom bar. WCAG AA wants 4.5:1. `--zink-lt` on the same ground is 7.26:1.
- **Contrast: the copper band is 3.30:1.** `#F7DECD` on `--koper` for the
  "Wat er tegen ons model pleit" body copy. Plain white on that copper is only
  4.25:1, so lightening the text is not enough — the band wants `--koper-dk`
  (`#8E4A20`), which carries white at 6.66:1.

Passing, for reference: `--zink` on `--kalk` is 4.75:1 and on white 5.27:1;
`--zink-lt` on `--navy` is 7.26:1.

## Placeholders

`KvK [nummer]` in the footer is the site's own placeholder and is carried over
as-is.
