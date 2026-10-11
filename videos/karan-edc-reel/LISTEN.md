# Listen check: karan-showreel (sound layer v1)

Sounds are real CC0 recordings from the opus-sound-layer kit (see audio/kit/CREDITS.md),
placed on the picture's own timing. Music is the synthesized bed from audio-src/score_v2.py.
A human ear check is the final call. These are not a verdict that the sound is good.

Timecodes to check by ear:
1. 0:03.75: name slam (hero hit + boom)
2. 0:11.25: "6 FIGURES+" slam (hero)
3. 0:13.13: "1ST" hit
4. 0:19.10: first impact stat
5. 0:26.25: closing slam (hero)

QA result (sound-layer qa.py, last run): 18 FAIL, 33 warnings. Not fixed:
- Picture: name and 6-figures slams land while the picture is still moving (picture timing, not sound).
- Hero body: the 6-figures hits are short on low end.
- Audible: small cues (intro dot, event 3-4, plan 4, whip, card 10/13, impact 2) sit under the music.
- True peak -0.97 dBTP, limit -1.0.
