---
name: karan-edc-reel
canvas: 1920x1080
colors:
  ink: "#0E0D0C"        # background, warm black (never pure #000)
  paper: "#F3EFE7"      # foreground text on ink and cobalt; vision-scene canvas
  card: "#FBF9F5"       # UI cards on the paper canvas
  signal: "#FF4B1F"     # the dot, the EDC colour field, focal accents
  cobalt: "#2B3DF5"     # proof colour field
  acid: "#D9FF3A"       # rare punctuation only: "1ST", score bar, tagline pill
  muted: "#8C857C"      # secondary mono on ink
  hairline: "rgba(243,239,231,0.18)"
typography:
  display: { family: "Archivo Black", weight: 400, tracking: "-0.04em", case: upper }
  serif:   { family: "Instrument Serif", style: italic, weight: 400, tracking: "-0.02em" }
  mono:    { family: "JetBrains Mono", weight: 400/700, tracking: "0.14em", case: upper, min: 20px }
motion:
  bpm: 128
  beat: 0.46875s
  bar: 1.875s
  eases: { slam: "expo.out", settle: "power3.out", spring: "back.out(1.6)", exit: "power2.in", travel: "power4.inOut" }
radii: { card: 28px, pill: 999px, tile: 0px }
---

## Overview

Campaign showreel for an EDC presidential candidate. Dark editorial base with hard
colour-block scene swaps (signal red for the club, cobalt for proof, paper for the
plan), heavy uppercase display type against an italic serif, and mono HUD chrome.

## The spine

One signal-red dot. Idea -> Execution -> Opportunities: it starts alone, becomes
the full stop after the name, draws the event line, multiplies into the 140-person
crowd, marks the score bar, and finally connects into a network behind the lockup.

## Type voices

- Display (Archivo Black): claims and numbers. Uppercase, tight.
- Serif italic (Instrument Serif): the human aside under each claim.
- Mono (JetBrains Mono): metadata, labels, HUD. Uppercase, tracked 0.14em.

## Chrome (every scene)

Corner brackets 28px in hairline; top-left "KARAN RAJ KR · EDC 2026"; top-right
section index ("01 — IDENTITY"); bottom-left timecode; bottom-right "128 BPM" and a
16-cell bar counter with the current bar filled. Chrome is 20px mono, never louder
than content.

## Composition rules

- Edge-anchored layouts, 140px side margins; nothing centred-and-floating except
  the final lockup (deliberate).
- Cuts land on bar or beat lines of the 128 BPM grid.
- Colour fields are flat fills; glows are radial and only behind the dot.

## Do / Don't

- Do keep every claim verbatim from BRIEF.md.
- Don't show "win" next to Hack BLR (Top 40 only); don't say "3x winner";
  don't say "Co-founder".
- Don't draw fake app screenshots: build cards are typographic name cards.
- Don't use gradients on text, neon glows, or pure #000 / #fff.
