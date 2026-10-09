# MOTION.md — Builder Set No. 2026

Brand and motion system for the showreel (format after the brand-intake skill).

## Colour
| Role | Hex | Use |
|---|---|---|
| Manual blue (bg) | `#DCE5EB` | every page background |
| Page white | `#F7F8F5` | step panels, callouts |
| Ink | `#141414` | type, outlines |
| Brick red | `#FF4A1C` | the hero brick, step badges, key numbers |
| Stud yellow | `#FFC629` | secondary bricks, highlights |
Dark and neutral tones lean slightly blue toward the manual paper. No gradients beyond the soft
radial vignette on the page.

## Type
- Archivo, expanded black (wdth 125, wght 900): step titles, names, numbers.
- Archivo regular width (wdth 100, wght 600–800): supporting lines.
- JetBrains Mono 600: part counts ("1x", "18x"), page numbers, labels.
Minimum on-screen sizes are a 90px headline, 40px body and 28px labels.

## Motion
- **Bricks snap:** each part enters from above with `back.out(1.6)` in 0.35s and lands on a beat.
  The landing gets a 2–3px settle and a click sound.
- **Text:** a mask rise using `power4.out` in 0.45s. Nothing scales from 0; entries start at
  scale 0.85 or above.
- **Camera:** slow pushes between 1.00 and 1.04 across each page, plus a whip of y 110% between
  steps.
- **Easing:** never use ease-in on an entrance. Exits are quick (0.25s, `power2.in`) so they
  clear before the next beat.
- **Beat grid:** 120 BPM. Pages turn on bar lines (every 2s) and parts land on beats (every 0.5s).
