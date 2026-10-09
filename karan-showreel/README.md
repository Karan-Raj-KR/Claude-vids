# Builder Set No. 2026: Karan Raj KR showreel

A 40-second personal showreel built with [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML + GSAP, rendered frame by frame). It is told as the instruction manual of a building set whose finished model is LEGO Karan.

**Finished files:** `renders/karan-builder-showreel-16x9.mp4` (1920×1080) and `renders/karan-builder-showreel-9x16.mp4` (1080×1920). Both are 60 fps H.264 with AAC audio.

| Page | Time | Step |
|---|---|---|
| Box | 0–6 s | The set box lands; the camera pushes into the instructions |
| 1 | 6–10 s | Start a company: the KĀRYO brick snaps in |
| 2 | 10–16 s | Ship products: four product bricks, then 18 merged PRs |
| 3 | 16–24 s | Compete: 121 teams down to 1st, then the trophy tower |
| 4 | 24–30 s | Bring people in: four events, then a 120+ crowd |
| Complete | 30–36 s | Build complete. Next build: EDC (the three pledges) |
| Back | 36–40 s | The back of the box: name, KĀRYO, links |

## How it was made (skills used)

- **hyperframes:** the intent layer, then the general-video workflow, with core/creative/animation for the composition contract, motion rules (spring-pop, waterfall, grid-card-assemble, dataviz-countup) and `check`/`snapshot`/animation-map gates.
- **hyperframes-registry:** the `grain-overlay` and `number-wheel` blocks.
- **brand-intake** (motion-graphics-skills): `MOTION.md` is written in its format.
- **reel-export** (motion-graphics-skills): the 9:16 file was checked against its upload spec.
- **emil-design-eng / review-animations** (emilkowalski/skills): the motion craft bar. No entrance starts from scale 0, nothing uses ease-in on an entrance, and only the toy bricks get a little overshoot.

## Editing

- **Scenes:** `tools/scenes.py` writes `compositions/step1…back.html`. `compositions/box.html` and `compositions/grain.html` are hand-written.
- **Vertical:** after editing any scene, run `python3 tools/make_vertical.py` to refresh `vertical/compositions/`.
- **Look:** shared look and brick styles are in `assets/manual.css`. Portrait overrides use `[data-width="1080"]`.
- **Score:** `python3 audio/score.py` regenerates `assets/score.wav`. It is synthesized and royalty-free, with a brick-clack timed to every part that lands.
- **Commands:**
  - Preview: `npx hyperframes preview`
  - Check: `npx hyperframes check` (run it from `vertical/` for 9:16)
  - Render: `npx hyperframes render -f 60 -q delivery`
