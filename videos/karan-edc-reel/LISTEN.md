# Listen check: karan-showreel v4 (45 s)

Sounds are real CC0 recordings from the opus-sound-layer kit (audio/kit/CREDITS.md),
placed from the picture's own timing (audio/cues.json). Music is the synthesized bed
audio-src/score_45.py (128 BPM, 96 beats). A human ear check is the final call.

Timecodes to check by ear:
1. 0:05.6: name slam (hero hit + boom)
2. 0:16.9: "6 FIGURES+" revenue slam (hero; the longest hold in the film, to 0:21.5)
3. 0:21.6: "1ST" Open Loop hit
4. 0:24.4: whoosh as the camera flies into the proof cards
5. 0:39.4: closing slam into KARAN FOR EDC PRESIDENT (hero)

QA (sound-layer qa.py, after 2 fix rounds): 14 FAIL, 30 warnings.
- Pass: all three hero hits now lift the 125-250 Hz band 5.6-7.0 dB (needs 3); music level steady.
- Fail, picture: at 16.9 s the frame change is a fast camera move + gold fade, not a hard cut,
  so the "cut" check does not find a clean frame change (motion spike ~12 vs ~60 at the other heroes).
- Fail, sync: the 6-figures hit's peak is 1.6 frames after its cue.
- Fail, audible: small cues (degree type, best-member pill, events 1 and 4, figures sheen,
  card 13, impact 1, plans 1 and 4) sit under the music.
- Fail, true peak: -0.28 dBTP (limit -1.0).

qa.png at the hero cues: at 5.6 s, 16.9 s and 39.4 s the waveform shows a short dip
(stop_before) then a full-band spike from the sub up past 10 kHz; picture-motion spikes are tall
at 5.6 s and 39.4 s and small at 16.9 s.
