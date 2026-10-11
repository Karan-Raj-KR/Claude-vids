"""52.5 s score for the Karan EDC showreel: score_v2's instruments re-arranged to 28 bars.

128 BPM, F minor, Fm - Db - Ab - Eb. 112 beats = 52.5 s. Section starts follow the
picture's time-warp (index.html window.W), so every hero hit sits on a beat:

  beats  0-11  (0.00-5.63)   intro: pads, rising arp, riser, reverse cymbal
  beats 12-35  (5.63-16.88)  drop 1: name slam on 12, four-on-floor, hook
  beats 36-51  (16.88-24.38) drop 2: "6 FIGURES+" slam on 36 (the big one),
                             hook up an octave; "1ST" hit on 46
  beats 52-53                drop-out + whoosh as the camera flies to the cards
  beats 54-63  (25.31-30.00) drop 2 continues under the proof cards
  beats 64-71  (30.00-33.75) breakdown under "creator & leader": no kick, pads, piano
  beats 72-87  (33.75-41.25) THE PLAN: the groove comes back warm and wide, one plan
                             card lands on each of beats 75, 78, 81, 84 (pluck + lift)
  beats 88-99  (41.25-46.88) build under the quote: filtered kick, snare roll, riser
  beats 100-111 (46.88-52.50) final drop on 100, last chord on 108 rings out

Usage: python score_52.py <out_dir>  -> score-52-raw.wav, music-52-raw.wav
"""

import sys
import numpy as np
import soundfile as sf
import synth as S

S.LENGTH = 52.5
S.N = int(S.SR * S.LENGTH)
import score_v2 as V  # noqa: E402  (binds N from the 45 s length above)

SR, BEAT, BAR, N = S.SR, S.BEAT, S.BAR, S.N
b, place, hz, adsr = S.b, S.place, S.hz, S.adsr
S16 = BEAT / 4
CH, PROG, BASS, chord_at = V.CHORDS, V.PROG, V.BASS, V.chord_at


def groove(drums, bass, i, rolling):
    place(drums, S.kick(1.0), b(i))
    if i % 4 in (1, 3):
        place(drums, S.clap(0.48 if rolling else 0.45), b(i))
    root = BASS[chord_at(i)]
    if rolling:
        for k in range(4):
            place(drums, S.hat(level=0.26 if k == 2 else 0.12), b(i) + k * S16, pan=0.3 if k % 2 else -0.15)
        place(drums, V.shaker(0.08), b(i) + S16 * 3, pan=0.5)
        for k in (1, 2, 3):
            place(bass, S.bass_note(root + (12 if k == 2 else 0), S16 * 0.9, 0.42, cutoff=700), b(i) + k * S16)
    else:
        place(drums, S.hat(level=0.24), b(i) + BEAT / 2, pan=0.25)
        if i % 4 == 3:
            place(drums, S.hat(open_=True, level=0.14), b(i) + BEAT / 2, pan=-0.25)
        place(bass, S.bass_note(root, BEAT * 0.42, 0.55, cutoff=650), b(i) + BEAT / 2)


def hook(bus, phrase, start, up=0, level=0.3, bright=1.0, pan=0.1, until=99):
    for step, note, ln in phrase:
        if step < until:
            place(bus, V.lead(note + up, ln * S16, level, bright), b(start) + step * S16, pan=pan)


def build():
    drums, bass, lead_bus, keys, pads, fx = (S.buf() for _ in range(6))
    kicks = []

    # ---- intro (0-11)
    for k, c in enumerate(("Fm", "Db", "Ab")):
        place(pads, V.pad_chord(c, BAR * 1.1, 0.2 + 0.02 * k, 900 + 400 * k), b(4 * k))
    for s in range(48):
        tones = CH[chord_at(s // 4)]
        note = tones[s % 4] + 12 + (12 if s % 8 >= 4 else 0)
        place(keys, V.arp_note(note, 350 + 3800 * (s / 47) ** 1.6, 0.16 + 0.12 * s / 47), s * S16, pan=-0.5 + (s % 4) / 3)
    place(fx, S.riser(BAR * 1.5, 0.45, 150, 5000), b(6))
    place(fx, V.reverse_cymbal(BEAT * 2, 0.5), b(10))
    place(bass, np.sin(2 * np.pi * hz(29) * np.arange(int(BAR * 3 * SR)) / SR) * adsr(int(BAR * 3 * SR), 2.0, 0.2) * 0.1, 0)

    # ---- drop 1 (12-35): name slam
    place(fx, S.impact(1.0, 2.4), b(12))
    place(fx, V.downlifter(1.4, 0.4), b(12) + 0.05)
    for i in range(12, 36):
        kicks.append(i)
        groove(drums, bass, i, rolling=False)
    for i in (34, 35):
        for k in range(4):
            place(drums, V.snare(0.18 + 0.05 * k, 200 + 10 * k), b(i) + k * S16)
    for bar in range(3, 9):
        place(pads, V.pad_chord(PROG[bar % 4], BAR, 0.16, 2200), b(bar * 4))
    for phrase, start in ((V.HOOK_A, 12), (V.HOOK_B, 20), (V.HOOK_A, 28)):
        hook(lead_bus, phrase, start, level=0.32)

    # ---- drop 2 (36-63): "6 FIGURES+" is the biggest moment of the film
    place(fx, V.reverse_cymbal(BEAT * 2, 0.55), b(34))
    place(fx, S.impact(1.0, 3.2), b(36))
    place(fx, V.downlifter(2.0, 0.45), b(36) + 0.05)
    place(keys, V.big_chord("Fm", BAR * 1.2, 0.4), b(36))
    place(fx, S.impact(0.55, 1.4), b(46))                       # "1ST"
    place(fx, S.whoosh(1.0, 0.6), b(52) - 0.3)                  # fly to the cards
    place(fx, V.reverse_cymbal(BEAT * 2, 0.45), b(52))
    place(pads, V.pad_chord("Fm", BEAT * 2.2, 0.3, 3000), b(52))
    for i in range(36, 64):
        if i in (52, 53):
            continue
        kicks.append(i)
        groove(drums, bass, i, rolling=True)
    for bar in range(9, 16):
        if bar != 13:
            place(pads, V.pad_chord(PROG[bar % 4], BAR, 0.15, 2600), b(bar * 4))
    hook(lead_bus, V.HOOK_A, 36, up=12, level=0.26, bright=1.2, pan=-0.1)
    hook(lead_bus, V.HOOK_B, 44, level=0.24, bright=1.2, pan=-0.1, until=24)
    hook(lead_bus, V.HOOK_B, 56, up=12, level=0.24, bright=1.2, pan=-0.1)
    for s in range(112):
        beat = 36 + s // 4
        if beat in (52, 53):
            continue
        place(keys, V.arp_note(CH[chord_at(beat)][(s * 3) % 4] + 24, 3200, 0.07), b(36) + s * S16, pan=0.6 if s % 2 else -0.6)

    # ---- breakdown (64-71)
    place(fx, V.downlifter(1.6, 0.35), b(64))
    place(pads, V.pad_chord("Ab", BAR, 0.32, 1400), b(64))
    place(pads, V.pad_chord("Eb", BAR, 0.32, 1500), b(68))
    for step, note, ln in V.HOOK_A:
        place(keys, V.piano(note - 12, 0.32), b(64) + step * S16, pan=0.15)
    for i in (64, 66, 68, 70):
        n = int(BEAT * 1.8 * SR)
        place(bass, np.sin(2 * np.pi * hz(BASS[chord_at(i)] - 12) * np.arange(n) / SR) * adsr(n, 0.02, 0.3) * 0.22, b(i))
    place(drums, S.clap(0.22), b(67)); place(drums, S.clap(0.22), b(71))

    # ---- the plan (72-87): main part, groove back with a warm hook
    place(fx, S.impact(0.6, 1.6), b(72))
    for i in range(72, 88):
        kicks.append(i)
        groove(drums, bass, i, rolling=False)
    for bar in range(18, 22):
        place(pads, V.pad_chord(PROG[bar % 4], BAR, 0.2, 2600), b(bar * 4))
    hook(lead_bus, V.HOOK_A, 72, level=0.24, bright=0.9, pan=0.15)
    hook(lead_bus, V.HOOK_B, 80, level=0.26, bright=1.1, pan=0.15)
    for k, i in enumerate((75, 78, 81, 84)):                  # one per plan card
        place(keys, V.piano(CH[chord_at(i)][k % 4] + 12, 0.34), b(i), pan=-0.45 + 0.3 * k)
    for i in (86, 87):
        for k in range(4):
            place(drums, V.snare(0.16 + 0.04 * k, 200 + 10 * k), b(i) + k * S16)

    # ---- build (88-99)
    build_bus = S.buf()
    for i in range(88, 100):
        place(build_bus, S.kick(0.85), b(i))
        kicks.append(i)
        place(build_bus, S.bass_note(BASS[chord_at(i)], BEAT * 0.42, 0.45, cutoff=500), b(i) + BEAT / 2)
    roll = []
    for i in range(92, 96):
        roll += [b(i), b(i) + BEAT / 2]
    for i in (96, 97):
        roll += [b(i) + k * S16 for k in range(4)]
    for i in (98, 99):
        roll += [b(i) + k * S16 / 2 for k in range(8)]
    for k, t in enumerate(roll):
        if t < b(100) - 0.12:
            place(drums, V.snare(0.12 + 0.4 * (k / len(roll)) ** 1.5, 180 + 140 * k / len(roll)), t)
    for k, c in enumerate(("Db", "Eb", "Fm")):
        place(pads, V.pad_chord(c, BAR, 0.22 + 0.02 * k, 1600 + 600 * k), b(88 + 4 * k))
    place(fx, S.riser(BAR * 2 - 0.1, 0.6, 200, 9000), b(92))
    s0, s1 = int(b(88) * SR), int(b(100) * SR)
    k = np.clip((np.arange(N) - s0) / (s1 - s0), 0, 1)
    drums += V.sweep_lp(build_bus, 300 * (40 ** k))

    # ---- final drop (100-111)
    place(fx, S.impact(1.0, 3.0), b(100))
    place(fx, V.reverse_cymbal(0.3, 0.0), b(100))
    for i in range(100, 108):
        kicks.append(i)
        place(drums, S.kick(1.0), b(i))
        if i % 4 in (1, 3):
            place(drums, S.clap(0.5), b(i))
        for k in range(4):
            place(drums, S.hat(level=0.24 if k == 2 else 0.1), b(i) + k * S16, pan=0.3 if k % 2 else -0.15)
    place(bass, V.reese(41, BAR * 0.98, 0.55), b(100))
    place(bass, V.reese(37, BAR * 0.98, 0.5), b(104))
    place(keys, V.big_chord("Fm", BAR, 0.42), b(100))
    place(keys, V.big_chord("Db", BAR, 0.4), b(104))
    hook(lead_bus, V.HOOK_A, 100, up=12, level=0.28, bright=1.4, pan=0.0)
    place(drums, S.kick(1.0), b(108))
    place(fx, S.impact(0.7, 2.0), b(108))
    place(keys, V.big_chord("Ab", BAR * 1.6, 0.46), b(108))
    place(pads, V.pad_chord("Ab", BAR * 1.0, 0.3, 3200), b(108))
    place(bass, V.reese(44, BAR * 0.95, 0.42), b(108))

    # ---- mix (same chain as score_v2)
    duck = np.ones(N)
    dn = int(0.2 * SR)
    shape = 1 - 0.7 * np.exp(-np.arange(dn) / (0.07 * SR))
    for i in kicks:
        s = int(b(i) * SR)
        duck[s:s + dn] = np.minimum(duck[s:s + dn], shape[:max(0, min(dn, N - s))])
    duck = duck[:, None]
    lead_bus = V.delay(lead_bus, BEAT * 0.75, fb=0.35, mix=0.28)
    keys = V.delay(keys, BEAT * 0.75, fb=0.3, mix=0.18)
    music = drums * 0.92 + (bass * 0.9 + lead_bus * 0.85 + keys * 0.8 + pads) * duck
    music = S.reverb(music, seconds=1.8, wet=0.14)
    fx = S.reverb(fx, seconds=2.6, wet=0.24, tone=6500)
    music /= np.max(np.abs(music)) + 1e-9
    fx /= np.max(np.abs(fx)) + 1e-9
    tail = np.ones(N)
    fs = int(51.5 * SR)
    tail[fs:] = np.linspace(1, 0, N - fs) ** 1.5
    mix = (music * 0.8 + fx * 0.42) * tail[:, None]
    stem = music * tail[:, None]
    return mix / (np.max(np.abs(mix)) + 1e-9), stem / (np.max(np.abs(stem)) + 1e-9)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    mix, stem = build()
    sf.write(f"{out}/score-52-raw.wav", (mix * 0.89).astype(np.float32), SR, subtype="PCM_24")
    sf.write(f"{out}/music-52-raw.wav", (stem * 0.89).astype(np.float32), SR, subtype="PCM_24")
    print("wrote", out)
