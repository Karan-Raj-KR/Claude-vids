# Listen check: karan-showreel v6 (52.5 s)

Sounds are real CC0 recordings from the opus-sound-layer kit (audio/kit/CREDITS.md),
placed from the picture's own timing (audio/cues.json). Music is the synthesized bed
audio-src/score_52.py (128 BPM, 112 beats). Final mux: loudnorm to -14 LUFS plus a
latency-compensated limiter. A human ear check is the final call.

Timecodes to check by ear:
1. 0:05.6: name slam (hero hit + boom)
2. 0:16.9: "6 FIGURES+" revenue slam (hero; held to ~0:21.5)
3. 0:35.2 to 0:39.4: the plan, one card landing on each of 35.2 / 36.6 / 38.0 / 39.4
4. 0:42.2: quote starts over the snare build
5. 0:46.9: closing slam into KARAN FOR EDC PRESIDENT (hero)

QA (sound-layer qa.py, last run): 12 FAIL, 30 warnings.
- Pass: loudness -14.5 LUFS, true peak -1.36 dBTP, audio offset 0 ms, music level steady,
  all three hero hits lift 125-250 Hz by 5.6-6.9 dB (needs 3), all four plan-card cues audible.
- Fail, picture: at 16.9 s the frame change is a fast camera move + gold fade, not a hard cut.
- Fail, sync: the 6-figures hit's peak is 1.6 frames after its cue.
- Fail, audible: small cues (degree type, best-member pill, event 1, card 1, card 13,
  leadership line, whip into the plan, closing pill) sit under the music.
