---
workflow: general-video
flow: automation
storyboard: no
message: "Don't just talk. Build. Karan ships, wins, and brings people with him."
aspect: 1920x1080
length: 20s
angle: fast-cut hype reel
---

## Intent

A faster, much more dynamic 20-second cut of the Karan Raj KR showreel. This was asked for after the 40 s "Builder Set" version felt too basic. It runs at 150 BPM, cuts roughly every 0.4 s, and fills the frame with kinetic type.

## Assets

- assets/karan/*.png: the LEGO Karan poses cut from the character sheet.

## Customizations

- Registry: camera-shake (vendored into assets/vendor/camera-shake.js, translation only, capped overscan). whip-pan-cut, confetti and perspective-marquee were installed for reference; their techniques (directional blur whips, seeded bursts, marquee rows) are re-implemented in assets/reel.js.
- Native 9:16 from the same scenes.

## Notes

- Verified facts only (see edc-campaign/src/config.ts). Always write KĀRYO with the macron.
