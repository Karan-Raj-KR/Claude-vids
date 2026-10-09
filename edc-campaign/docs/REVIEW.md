# Still review

Stills are in `docs/stills/`. `v1` is the first pass, `v2` the revision. Each beat was checked for hierarchy, spacing, clipping, contrast, colour and typography in both 16:9 and 9:16.

## Pass 1 — problems found

### Global
- **G1 · Clipping.** The mask-reveal container cuts off descenders. You can see it on *g* and *y* in "building" and "actually" (hook), *p* in "products" (builds) and *y* in "year" (pledge 1). The mask needs about 0.2em of padding below the baseline.
- **G2 · Vertical composition.** Most 9:16 frames are the 16:9 layout stacked from the top, so the lower 35–50% of the frame is empty. This affects Pledges, Builds, Vote, People (events) and Wins (awards). Each vertical scene needs its own vertical centring.
- **G3 · Phone legibility.** Some mono labels are 26–28px: score labels, "Yenepoya, Mangaluru" and the participants line. That is too small at phone size. The minimum for any label becomes 30px, and 32px for vertical.

### 1 · Hook
- H1. Descender clipping (G1).
- H2. The highlight block bleeds 19px left of the text margin. That is acceptable as a highlighter convention, so I'm keeping it, but it shouldn't bleed more.
- Hierarchy and contrast pass. Line 1 recedes to stone (4.0:1 on paper, and it's secondary text). Line 2 is ink on paper (16:1), and ink on vermilion for "building" (5.6:1).

### 2 · Name
- N1. During the 4-second hold, the right ~30% of the 16:9 frame is dead. The name should be set larger so it owns the frame. It can go up to about 300px and still keep the 140px margin.
- N2. 9:16: the name can grow from 168px to about 180px. The block is already centred well enough.

### 3 · Builds
- B1. **Clipping:** the period in "Real products." is cut off by the 660px column (16:9).
- B2. **Redundant copy:** the ERP subline ("Live. 41 tables, ~45 routes.") repeats the chips directly underneath it. It should show the live URL instead.
- B3. The window has 130px (16:9) or 210px (9:16) of dead space under the table. Either shorten the window or let the content fill it.
- B4. The left column has a 190px hole between the headline and the stats. The second stat only arrives at 9.0s, so for 2 seconds the column looks unfinished. Both stats should come in earlier and the spacing should be tighter.
- B5. The cursor tip sits on the tab label ("SCHOOL ERP") and covers letters. The click point should move to the lower part of the tab.
- B6. 9:16: the bottom 380px is empty (see G2).

### 4 · Wins
- W1. Nothing tells you how to read the 11×11 grid. Without a key, the vermilion square doesn't connect to "1ST PLACE". It needs a caption: "1 square = 1 team".
- W2. Mono labels at 26–28px are too small (G3).
- W3. The awards list sits high, leaving 300px empty at the bottom in 16:9. It should be centred vertically.
- W4. 9:16 Open Loop is dense but it reads, and the hierarchy holds: title → grid → 1ST PLACE → bars.

### 5 · People
- P1. **Typography bug:** the headline renders as "Co-led4+events" with no word spaces, because the gap is set in em on a container with the default font size.
- P2. The event cards are 360px tall with the titles pushed to the bottom, which leaves big black voids. They should be shorter, with larger titles, and centred as a block.
- P3. Crowd: the caption ends 110px above the bottom of the grid. The number and caption should be centred against the grid.

### 6 · Pledges
- PL1. **Clipping (9:16):** "HACKATHONS" runs past the right margin at 118px.
- PL2. 9:16: all the content is in the top half and the bottom 1000px is empty (G2).
- PL3. 16:9: the content sits high and the lower third is empty. It should be centred on the frame and the title enlarged.

### 7 · Vote
- V1. 16:9 passes: strong hierarchy, the tick reads instantly, and the name keeps a 145px margin on the right.
- V2. 9:16: the lockup is too small for the frame. The box and name should grow (box 200px, name 150px).

### Colour / brand
- All five palette colours are used consistently, with no gradients and no glow. Vermilion is reserved for the box, the kickers and the key numbers. Pass.
- KĀRYO renders with the macron (Archivo latin-ext subset). ₹ renders correctly. Pass.

## Pass 2: fixes applied (stills in `v2`, `v3`, `tr2`)

| Issue | Fix |
|---|---|
| G1 descenders clipped | The mask got real pixel padding below the baseline. The old `em` padding resolved against a 16px parent, which is why it was too small. The hidden state now offsets by that padding too. |
| G2 vertical frames top-heavy | Every 9:16 scene was re-centred on its own grid: Builds (block 270–1650), Name, People, Pledges (adding the rail fills the lower third), Wins awards (starts at 470), Vote (bigger lockup). |
| G3 small labels | All mono labels are now ≥30px (16:9) and ≥32px for the most important ones in 9:16. |
| N1 empty right side | The name went from 252 to 306px and now spans 140→1625px. |
| B1 clipped headline | The headline is now 80px at wdth 104 in a 700px column. |
| B2 redundant ERP copy | The subline is now "Live at erpdemo.karanrajkr.com". |
| B3 dead space in window | The window is now 700px tall (was 780), and its top and bottom align with the left column. |
| B4 left-column hole | The stats are bottom-aligned to the window, and both arrive by 8.3s instead of 9.0s. |
| B5 cursor over label | The click point moved to the lower-right of each tab. |
| W1 grid had no key | Added the legend "1 square = 1 team" under the grid. |
| W3 awards sat high | The list now starts at 262px with 40px row padding, so it is centred. |
| P1 "Co-led4+events" | The word gap is now in px from the headline size. |
| P2 empty cards | Cards are now 300px tall with deliberate 2-line titles (pre-line). |
| P3 crowd alignment | The number aligns to the top of the grid and the caption to its bottom. |
| PL1 "HACKATHONS" clipped (9:16) | The 9:16 title is now 104px at wdth 100. |
| PL2/PL3 static, top-heavy pledges | Added a progress rail that fills over each 2-second pledge. It recaps all three promises and anchors the lower third. |
| V2 small 9:16 lockup | The box is now 190px, the name 144px, and VOTE 140px. |

### Found while scrubbing transitions (`tr`, `tr2`)
- **Muddy colour blends:** interpolating vermilion → ink (window morph) and vermilion → paper (ballot box) produced brown and salmon mid-tones. Both were replaced with hard-edged mask wipes. Inside the window, an ink panel wipes over the vermilion box. The ballot box hollows out from its centre. The box now stays vermilion for the whole film.
- **Stray kicker square:** when a scene exited, its kicker square scaled *up* instead of out. Fixed in `Kicker`.
- **Window overlapping the headline:** the morphing window crossed "Real products." as the headline rose. The left column now enters after the morph.
- **Beat sync:** every event was moved onto the 120 BPM grid. Hook words land on 16ths. Clicks, cuts, the 1ST PLACE flip, the camera whip, the camera pan, the counter landing, the pledges and the final tick all land on beats. The soundtrack reads the same numbers from `timeline.json`.

## Pass 3: full-length watch-back (`docs/qa/*-sheet.jpg`)

I checked both renders at 1× using a 4 fps contact sheet (120 frames per film), plus ffmpeg `freezedetect`, `blackdetect` and scene-cut detection.

| Found | Fix |
|---|---|
| The outgoing and incoming pledge titles overlapped for 8 frames at 23.0 s and 25.0 s, so glyphs collided. | The outgoing pledge now clears in 10 frames and is gone exactly on the beat the next one enters. |
| Fully static holds of 0.8–1.8 s at 0.6, 15.3, 18.1, 20.1, 21.5, 23.4, 25.4 and 28.1 s. | Added a slow camera drift (2–3% over the hold) to the hook, awards, events, crowd and final lockup, and tracking that opens on each pledge title. Every hold still gives at least 1.5 s to read. |
| The encode came out as `yuvj420p` (full-range JPEG intermediate), which some phones and WhatsApp render with crushed or washed-out colour. | Frames are now PNG and encoded as BT.709 `yuv420p` in TV range. |
| The final push-in pushed the name to an 86px right margin. | The push was reduced to 2%, giving a margin of about 114px. |

**Final checks, both versions:** H.264 High · `yuv420p` BT.709 · 60 fps · 1800 frames = 30.000 s · AAC 48 kHz stereo, −11.9 LUFS integrated, −1 dBFS peak · no black frames. Hard cuts were detected at 7, 12, 17, 21 and 27 s. 3.0 s is a same-colour continuity cut, so the detector doesn't flag it. Each cut has an audio transient within 10 ms (one analysis hop).
