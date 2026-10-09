# Karan Raj KR: 20 s showreel (fast cut)

**Finished files:** `renders/Karan-Raj-KR-Showreel-20s-16x9.mp4` and `renders/Karan-Raj-KR-Showreel-20s-9x16.mp4`. Both are 60 fps H.264 with AAC audio, encoded to the reel-export upload spec.

## Structure

The reel runs at 150 BPM (1 beat = 0.4 s) with about 40 cuts.

| Time | Section | What happens |
|---|---|---|
| 0–2.4 s | Hook | DON'T · JUST · TALK. (struck out) · BUILD. Karan drops in with a stud burst. |
| 2.4–6.4 s | Builds | I ship products. Then School ERP, ClinicDesk, Eligent and FormPilot, one per beat. Then 6-figure revenue and 18 merged PRs. |
| 6.4–12 s | Wins | 121 teams: the camera pulls out and the losers drop away, leaving 1ST. Then 80 vs 60 and ₹20,000, then five awards on five beats, then a marquee recap wall. |
| 12–14.8 s | People | Co-led 4+ events (cards dealt in), then 120+ as the crowd explodes into a grid. |
| 14.8–20 s | Finale | NEXT BUILD: EDC, then the three promises, then a zoom-through into the name, a burst, and the links. |

## Editing

- **Scenes:** `tools/build.py` writes `compositions/*.html`. After any change, run `python3 tools/make_vertical.py` to refresh the 9:16 copies.
- **Motion helpers:** `assets/reel.js` holds the slam, whip, punch, flash, shake, marquee, burst and text-fit helpers. Big type is fitted to the canvas width once, at setup.
- **Score:** `python3 audio/score.py` regenerates `assets/score.wav` (150 BPM, synthesized, with a hit on every cut).
- **Commands:**
  - Check: `npx hyperframes check` (run it from `vertical/` for 9:16)
  - Render: `npx hyperframes render -f 60 -q delivery`
