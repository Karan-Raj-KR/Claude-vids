---
workflow: general-video
flow: automation
storyboard: no
message: "Karan doesn't talk about building — he ships, wins, and brings people with him."
destination: social-feed
aspect: 1920x1080
language: en
length: 40s
angle: builder-set
---

## Intent

A 40-second personal showreel for Karan Raj KR, told as the instruction manual of a toy
building set: "Builder Set No. 2026". Each step of the manual adds a part (founder, products,
wins, community), the finished model is Karan, and the next build is EDC. Confident and playful,
studio-made, never a generic tech reel.

## Assets

- assets/karan/*.png — LEGO-style Karan poses cut from the user's character sheet (front,
  three-quarter, side, neutral, thinking, explaining, happy).
- assets/fonts/*.woff2 — Archivo (variable) + JetBrains Mono, same as the campaign films.

## Customizations

- Registry: grain-overlay (film grain), number-wheel (rolling counters for 18, 121, 120).
- Native 9:16 version from the same scenes (vertical.html), checked against the reel-export
  upload spec (H.264, yuv420p, tv range, bt709, AAC).
- Original synthesized soundtrack with a brick-snap sound on every part that lands.

## Notes

- Use only the verified facts from the campaign brief (edc-campaign/src/config.ts). No DOB,
  parents, partner, pre-university editing, Hive hackathon, TakeOver'26 as a win, or the word
  "president" for past roles. Always write KĀRYO with the macron.
- No toy-brand names or logos; the look is a generic building-set manual.
