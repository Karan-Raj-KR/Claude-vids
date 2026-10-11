---
format: 1920x1080
duration: 30s
message: "From organising events to building an ecosystem."
arc: Identity → EDC record → Proof → Builds → Impact → Proposals → Close
audience: NIAT-S-VYASA students and Instagram followers
mode: collaborative
version: 2
---

# Karan for EDC President — storyboard v2 (built)

## Build notes

- Built as one continuous composition (index.html) so the signal dot travels unbroken
  across every scene; scenes are `<section class="clip">` blocks s01–s12.
- Skills used: motion-design (energetic personality, expo.out signature ease),
  gsap-plugins (SplitText masks, CustomEase), hyperframes-keyframes (camera moves,
  squash/stretch landings), hyperframes-registry (grain-overlay, whip-pan-cut and
  number-wheel recipes), threejs-postprocessing (bloom on the 3D network finale).
- GSAP and Three.js are vendored under assets/vendor (CDN is blocked in this sandbox
  and local files keep renders reproducible).
- Teaser lives in ../karan-edc-teaser (10s, same grid, its own score).

**This video tells NIAT-S-VYASA students that Karan has gone from organising events
to building things, and will build an ecosystem as EDC President.**

- **Format:** 1920x1080, 30.0s = 16 bars at 128 BPM (beat 0.46875s, bar 1.875s).
  No voiceover; synthesized music bed + sound design. No captions.
- **Spine:** one signal-red dot (idea → execution → opportunities). Callbacks:
  F01 dot → F01 full stop → F03 event line → F04 crowd → F06 score marker → F12 network.
- **Brand:** frame.md (ink / paper / signal / cobalt / acid; Archivo Black,
  Instrument Serif italic, JetBrains Mono).
- **Bans:** no slideshow (every scene hands its motion to the next), no
  screensaver motion, no fake app screenshots, no "win" beside Hack BLR, no
  "3x winner", no "Co-founder", no gradients on text.
- **Held frame:** F12 lockup holds still for its last ~1s.
- **Truthfulness:** every claim is verbatim from the candidate's brief. Build
  cards are typographic name cards, not screenshots.
- **Seam direction:** leftward travel; colour-field swaps cut on downbeats.

Total: 8+4+4+4+6+6+4+6+4+6+6+6 = 64 beats = 30.0s.

## Frame 1 — Identity

- scene: Red dot alone, then KARAN RAJ KR slams in with the dot as its full stop
- duration: 3.75s
- start: 0
- poster: 3.4
- transition_in: cut
- status: animated
- src: index.html#s01 (was compositions/f01-identity.html)
- voiceover: onscreen
- blueprint: kinetic-type-beats (adapt) + rules kinetic-beat-slam, ambient-glow-bloom
- audio: sub swell 0–1.875, impact + snare on 1.875, ticks on beats 6 and 7

Bar 1: the dot breathes inside a hairline ring on each beat (an idea, waiting).
Bar 2 downbeat: "KARAN RAJ KR" slams left-anchored, dot flies into place as the
full stop. "Founder, KĀRYO" (serif italic) rises on beat 6, "B.TECH CSE (AI/ML) ·
NIAT-S-VYASA, BENGALURU" (mono) types on beat 7. Seam out: the dot scales up to
fill the frame with signal red.

## Frame 2 — EDC role

- scene: Red field, "Finance Head" in serif, Best Member badge pops
- duration: 1.875s
- start: 3.75
- poster: 1.5
- transition_in: dot-iris (from F01)
- status: animated
- src: index.html#s02 (was compositions/f02-edc-role.html)
- voiceover: onscreen
- rules: waterfall-entry, spring-pop-entrance
- audio: whoosh into downbeat, pop on beat 3

On screen: "02 — EDC LEADERSHIP · LAST TERM" (mono), "Finance Head" (serif italic,
huge), "ENTREPRENEURSHIP CLUB" (display), pill "★ BEST MEMBER AWARD". Ghost
outline "EDC" at right. Seam out: the ink baseline extends into F03's event line.

## Frame 3 — EDC events

- scene: An ink line draws through 4 event nodes, one per beat
- duration: 1.875s
- start: 5.625
- poster: 1.7
- transition_in: cut (line continuity)
- status: animated
- src: index.html#s03 (was compositions/f03-edc-events.html)
- voiceover: onscreen
- rules: svg-path-draw, spring-pop-entrance
- audio: four pitched blips on the beats

On screen: "CO-ORGANISED 4+ EVENTS" (mono), nodes labelled "BUILD A PRODUCT IN
30 MIN" / "pitch", "ALL TEAMS SPONSORED", "ENTREPRENEURSHIP DEBATE", "IPL AUCTION".
Seam out: whip left onto ink.

## Frame 4 — 140+

- scene: The dot multiplies into a 140-dot crowd while 140+ counts up
- duration: 1.875s
- start: 7.5
- poster: 1.7
- transition_in: whip-left
- status: animated
- src: index.html#s04 (was compositions/f04-attendees.html)
- voiceover: onscreen
- rules: counting-dynamic-scale, center-outward-expansion
- audio: rising tick run under the count, hit on the landing

On screen: "140+" (display, huge), "attendees at the biggest one" (serif italic),
"AND THE TEAMS KEPT BUILDING AFTERWARDS →" (mono). Seam out: cobalt panel cuts in
from the bottom on the downbeat.

## Frame 5 — Six figures + incubator

- scene: 6 FIGURES+ lands, then the IIT incubation card slides in
- duration: 2.8125s
- start: 9.375
- poster: 2.5
- transition_in: wipe-up (cobalt)
- status: animated
- src: index.html#s05 (was compositions/f05-proof-money.html)
- voiceover: onscreen
- blueprint: dataviz-countup (adapt) + rules kinetic-beat-slam, nudge-curve
- audio: impact on downbeat, whoosh + click as the card lands

On screen: "03 — PROOF" (mono), "6 FIGURES+" (display), "earned through products
& agencies" (serif italic); card: "SELECTED" / "IIT ALUMNI INCUBATION CENTRE" /
"cohort". Seam out: hard cut on beat.

## Frame 6 — Open Loop 2026

- scene: 1ST in acid, four stats count up, 80 vs 60 score bar fills
- duration: 2.8125s
- start: 12.1875
- poster: 2.6
- transition_in: cut
- status: animated
- src: index.html#s06 (was compositions/f06-open-loop.html)
- voiceover: onscreen
- blueprint: dataviz-countup + rules counting-dynamic-scale, stat-bars-and-fills
- audio: big hit on "1ST", ticks under the counts

On screen: "OPEN LOOP 2026" (mono), "1ST" (display, acid), "place · FormPilot"
(serif italic); stats "309 PARTICIPANTS", "121 TEAMS", "109 COLLEGES", "14 STATES";
score bars "FORMPILOT 80" (acid) vs "NEXT BEST 60". Seam out: tiles flip.

## Frame 7 — Proof wall

- scene: Six proof tiles cascade in on eighth notes, then hold
- duration: 1.875s
- start: 15.0
- poster: 1.7
- transition_in: cut
- status: animated
- src: index.html#s07 (was compositions/f07-proof-wall.html)
- voiceover: onscreen
- blueprint: grid-card-assemble
- audio: six hi-hat stabs, one per tile

Tiles: "IDEATHON — winner", "HACK BLR 2026 — Top 40 of 2,500+ teams · solo",
"GRIT AWARDS 2026 — Content + Hackathons", "TECHNOLOGY INNOVATORS AWARD",
"20+ — merged open-source PRs", "ECSOC — Project Admin · crewai-recipes".
Seam out: the grid tilts back into the F08 card wall.

## Frame 8 — Builds

- scene: A tilted wall of seven typographic build cards drifts past
- duration: 2.8125s
- start: 16.875
- poster: 2.0
- transition_in: tilt (3D)
- status: animated
- src: index.html#s08 (was compositions/f08-builds.html)
- voiceover: onscreen
- rules: 3d-camera-flight, depth-of-field-blur
- audio: airy riser, soft clicks as cards pass focus

On screen: "04 — BUILDS" (mono), "SHIPPED." (display). Cards: "ELIGENT ·
app.karanrajkr.com", "FORMPILOT · Chrome extension", "KĀRYO CLIENT ONBOARDING
MANAGER · built in 24 hours", "SCHOOL ERP", "VC PITCHES", "OSS MENTOR",
"PERSONAL COMPANION". Seam out: camera pushes into the dot on the last card.

## Frame 9 — Impact

- scene: Three statements stack in, one per beat, red dots as bullets
- duration: 1.875s
- start: 19.6875
- poster: 1.7
- transition_in: push-in
- status: animated
- src: index.html#s09 (was compositions/f09-impact.html)
- voiceover: onscreen
- rules: waterfall-entry
- audio: three soft plucks

On screen: "05 — IMPACT" (mono), "Mentored batchmates — who now earn.", "Built a
docs-automation app — used by 3 batchmates.", "Took the stage — juniors'
orientation." Seam out: paper wipes in from the right.

## Frame 10 — Proposals

- scene: Four clean proposal cards spring onto a paper canvas
- duration: 2.8125s
- start: 21.5625
- poster: 2.4
- transition_in: wipe-left (paper)
- status: animated
- src: index.html#s10 (was compositions/f10-vision.html)
- voiceover: onscreen
- blueprint: grid-card-assemble (adapt) + rules spring-pop-entrance
- audio: bright pops per card, music filter opens

On screen: "06 — PROPOSALS, NOT PROMISES" (mono), "THE PLAN." (display). Cards:
"01 FOUNDER SESSIONS · on campus", "02 BUILD NIGHTS & HACKATHONS · campus +
national", "03 DEMO DAY · for student products", "04 OPPORTUNITIES BOARD ·
internships · programmes · competitions". Seam out: cards collapse into the dot.

## Frame 11 — The line

- scene: Three lines of the closing statement land on beats
- duration: 2.8125s
- start: 24.375
- poster: 2.6
- transition_in: scale-swap (cards → dot)
- status: animated
- src: index.html#s11 (was compositions/f11-quote.html)
- voiceover: onscreen
- rules: kinetic-beat-slam
- audio: music drops to pads, one hit on "Now"

On screen: "We've attended events." (serif italic, muted), "We've built projects."
(serif italic, muted), "NOW LET'S BUILD A CAMPUS WHERE IDEAS TURN INTO COMPANIES."
(display), red dot as the full stop. Seam out: text clears, the dot stays.

## Frame 12 — Lockup

- scene: The dot spawns a network; KARAN FOR EDC PRESIDENT locks up and holds
- duration: 2.8125s
- start: 27.1875
- poster: 2.6
- transition_in: cut (dot continuity)
- status: animated
- src: index.html#s12 (was compositions/f12-lockup.html)
- voiceover: onscreen
- blueprint: constellation-hub (scatter end card adapt) + logo-assemble-lockup
- audio: final impact on the downbeat, tail rings out to 30.0

On screen: "KARAN" (display), "FOR EDC PRESIDENT" (display, signal), pill "DON'T
JUST ATTEND. BUILD." (acid), "VOTING STARTS MONDAY · NIAT-S-VYASA" (mono).
Held: everything still from ~29.0s.
