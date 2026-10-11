"""Score v2 for the Karan EDC showreel: an arranged track, not a loop.

128 BPM, F minor, i-VI-III-VII (Fm - Db - Ab - Eb). 16 bars = 30.0 s.

  bars 1-2   (0.00-3.75)   intro: pads, rising arp, riser, reverse cymbal
  bars 3-6   (3.75-11.25)  drop 1: four-on-floor, pumping bass, lead hook
  bars 7-10  (11.25-18.75) drop 2: 16th hats, rolling bass, hook up an octave,
                           counter-arp; drop-out + whoosh on beat 32 (15.0 s)
  bars 11-12 (18.75-22.5)  breakdown: no kick, pads, piano hook
  bars 13-14 (22.5-26.25)  build: kick returns filtered, snare roll 8th->32nd,
                           riser, a breath of silence before the drop
  bars 15-16 (26.25-30.0)  final drop: reese bass, big chords, lead; last chord
                           on beat 60 (28.125 s) rings out to the end

Big hits at 3.75, 11.25 ("6 FIGURES+") and 26.25, plus a small one at 13.125 for "1ST".
Deterministic (fixed seed). Usage: python score_v2.py <out_dir>
"""

import sys
import numpy as np
import soundfile as sf
import synth as S

SR, BEAT, BAR, N = S.SR, S.BEAT, S.BAR, S.N
b = S.b
place, lp, hp, bp, noise, hz, saw = S.place, S.lp, S.hp, S.bp, S.noise, S.hz, S.saw
env_exp, adsr = S.env_exp, S.adsr
S16 = BEAT / 4

CHORDS = {  # pad voicings
    "Fm": [53, 56, 60, 65], "Db": [49, 53, 56, 61], "Ab": [56, 60, 63, 68], "Eb": [51, 55, 58, 63],
}
PROG = ["Fm", "Db", "Ab", "Eb"]
BASS = {"Fm": 41, "Db": 37, "Ab": 44, "Eb": 39}

HOOK_A = [(0, 77, 3), (3, 80, 3), (6, 84, 2), (8, 82, 2), (10, 80, 2), (12, 79, 4),
          (16, 77, 3), (19, 80, 3), (22, 75, 2), (24, 77, 6), (30, 72, 2)]
HOOK_B = [(0, 75, 3), (3, 79, 3), (6, 82, 2), (8, 84, 2), (10, 82, 2), (12, 80, 4),
          (16, 79, 3), (19, 82, 3), (22, 84, 2), (24, 87, 6), (30, 84, 2)]


def chord_at(beat):
    return PROG[(beat // 4) % 4]


def sweep_lp(x, cutoff):
    """Click-free time-varying low-pass: crossfade between pre-filtered copies."""
    bands = np.geomspace(200, 12000, 9)
    lc = np.log(np.clip(cutoff, bands[0], bands[-1]))
    lb = np.log(bands)
    pos = np.interp(lc, lb, np.arange(len(bands)))
    lo = np.floor(pos).astype(int)
    hi = np.minimum(lo + 1, len(bands) - 1)
    w = pos - lo
    filt = [lp(x, f) for f in bands]
    stack = np.stack(filt, axis=0)
    idx = np.arange(len(x))
    a = stack[lo, idx]
    c = stack[hi, idx]
    if x.ndim == 2:
        w = w[:, None]
    return a * (1 - w) + c * w


# ------------------------------------------------------------- instruments

def lead(note, dur, level=1.0, bright=1.0):
    n = int((dur + 0.25) * SR)
    f = hz(note)
    x = S.supersaw(f, n, voices=5, spread=0.009) * 0.7 + saw(f * 2, n) * 0.12
    t = np.arange(n) / SR
    cutoff = 900 + 4200 * bright * np.exp(-t / 0.18)
    y = sweep_lp(x, cutoff)
    e = adsr(n, 0.006, 0.22)
    e[int(dur * SR):] *= np.exp(-np.arange(n - int(dur * SR)) / (0.08 * SR))
    return y * e * level


def piano(note, level=1.0):
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    f = hz(note)
    x = (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t / 0.4)
         + 0.25 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t / 0.2))
    return x * np.exp(-t / 0.55) * adsr(n, 0.003, 0.05) * level


def arp_note(note, cutoff, level=1.0):
    n = int(S16 * 1.6 * SR)
    x = saw(hz(note), n) * 0.6 + np.sign(np.sin(2 * np.pi * hz(note) * np.arange(n) / SR)) * 0.25
    return lp(x, cutoff) * env_exp(n, 0.07) * adsr(n, 0.002, 0.02) * level


def snare(level=1.0, tone=190):
    n = int(0.28 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * tone * t) * np.exp(-t / 0.05)
    nz = bp(noise(n), 1500, 7000) * np.exp(-t / 0.09)
    return (body * 0.5 + nz) * level


def shaker(level=1.0):
    n = int(0.05 * SR)
    return hp(noise(n), 6000, 4) * np.sin(np.pi * np.arange(n) / n) ** 2 * level


def reverse_cymbal(dur, level=1.0):
    n = int(dur * SR)
    x = hp(noise(n), 4000, 2)
    e = (np.arange(n) / n) ** 3
    return x * e * level


def downlifter(dur=1.2, level=1.0):
    n = int(dur * SR)
    return S.whoosh(dur, 1.0, up=False)[:n] * np.exp(-np.arange(n) / (0.5 * SR)) * level


def reese(note, dur, level=1.0):
    n = int(dur * SR)
    f = hz(note)
    x = saw(f * 0.995, n) + saw(f * 1.005, n, 0.3)
    sub = np.sin(2 * np.pi * f / 2 * np.arange(n) / SR)
    return (lp(x, 520) * 0.45 + sub * 0.7) * adsr(n, 0.01, 0.06) * level


def pad_chord(name, dur, level=1.0, cutoff=1800):
    n = int(dur * SR)
    x = sum(S.supersaw(hz(m), n, voices=5, spread=0.008) for m in CHORDS[name]) / 4
    return lp(x, cutoff) * adsr(n, 0.25, 0.5) * level


def big_chord(name, dur, level=1.0):
    n = int(dur * SR)
    notes = CHORDS[name] + [m + 12 for m in CHORDS[name][:3]]
    x = sum(S.supersaw(hz(m), n, voices=7, spread=0.014) for m in notes) / len(notes)
    t = np.arange(n) / SR
    return lp(x, 5200) * np.exp(-t / (dur * 0.45)) * adsr(n, 0.004, 0.3) * level


def delay(x, time, fb=0.38, taps=6, mix=0.32):
    """Ping-pong feedback delay on a stereo buffer."""
    out = x.copy()
    d = int(time * SR)
    for k in range(1, taps + 1):
        g = mix * fb ** (k - 1)
        src = x[:-d * k] if d * k < len(x) else None
        if src is None:
            break
        side = (k % 2)
        tap = np.zeros_like(x)
        tap[d * k:, side] = (src[:, 0] + src[:, 1]) * 0.5 * g
        out += lp(tap, 4500)
    return out


# ------------------------------------------------------------- arrangement

def build():
    drums, bass, lead_bus, keys, pads, fx = (S.buf() for _ in range(6))
    kicks = []

    # ---- intro (beats 0-7)
    place(pads, pad_chord("Fm", BAR * 1.1, 0.2, 900), b(0))
    place(pads, pad_chord("Db", BAR * 1.1, 0.22, 1300), b(4))
    for s in range(32):
        beat = s // 4
        tones = CHORDS[chord_at(beat)]
        note = tones[s % 4] + 12 + (12 if s % 8 >= 4 else 0)
        cutoff = 350 + 3800 * (s / 31) ** 1.6
        place(keys, arp_note(note, cutoff, 0.16 + 0.12 * s / 31), s * S16, pan=-0.5 + (s % 4) / 3)
    place(fx, S.riser(BAR * 1.0, 0.45, 150, 5000), b(4))
    place(fx, reverse_cymbal(BEAT * 2, 0.5), b(6))
    place(bass, np.sin(2 * np.pi * hz(29) * np.arange(int(BAR * 2 * SR)) / SR) * adsr(int(BAR * 2 * SR), 1.5, 0.2) * 0.1, 0)

    # ---- drop 1 (beats 8-23)
    place(fx, S.impact(1.0, 2.4), b(8))
    place(fx, downlifter(1.4, 0.4), b(8) + 0.05)
    for i in range(8, 24):
        kicks.append(i)
        place(drums, S.kick(1.0), b(i))
        if i % 4 in (1, 3):
            place(drums, S.clap(0.45), b(i))
        place(drums, S.hat(level=0.24), b(i) + BEAT / 2, pan=0.25)
        if i % 4 == 3:
            place(drums, S.hat(open_=True, level=0.14), b(i) + BEAT / 2, pan=-0.25)
        root = BASS[chord_at(i)]
        place(bass, S.bass_note(root, BEAT * 0.42, 0.55, cutoff=650), b(i) + BEAT / 2)
    for i in (22, 23):  # fill
        for k in range(4):
            place(drums, snare(0.18 + 0.05 * k, 200 + 10 * k), b(i) + k * S16)
    for bar in range(2, 6):
        place(pads, pad_chord(PROG[bar % 4], BAR, 0.16, 2200), b(bar * 4))
    for phrase, start in ((HOOK_A, 8), (HOOK_B, 16)):
        for step, note, ln in phrase:
            place(lead_bus, lead(note, ln * S16, 0.32), b(start) + step * S16, pan=0.1)

    # ---- drop 2 (beats 24-39), drop-out on 32-33
    for i in range(24, 40):
        if i in (32, 33):
            continue
        kicks.append(i)
        place(drums, S.kick(1.0), b(i))
        if i % 4 in (1, 3):
            place(drums, S.clap(0.48), b(i))
        for k in range(4):
            acc = 0.26 if k == 2 else 0.12
            place(drums, S.hat(level=acc), b(i) + k * S16, pan=0.3 if k % 2 else -0.15)
        place(drums, shaker(0.08), b(i) + S16 * 3, pan=0.5)
        root = BASS[chord_at(i)]
        for k in (1, 2, 3):  # rolling bass
            place(bass, S.bass_note(root + (12 if k == 2 else 0), S16 * 0.9, 0.42, cutoff=700), b(i) + k * S16)
    place(fx, reverse_cymbal(BEAT * 2, 0.5), b(22))             # into "6 FIGURES+"
    place(fx, S.impact(1.0, 2.6), b(24))                       # "6" slam
    place(fx, S.impact(0.6, 1.4), b(28))                       # "1ST"
    place(fx, S.whoosh(1.0, 0.6), b(32) - 0.3)                  # zoom-out
    place(fx, reverse_cymbal(BEAT * 2, 0.45), b(32))
    place(pads, pad_chord("Fm", BEAT * 2.2, 0.3, 3000), b(32))
    for bar in range(6, 10):
        if bar != 8:
            place(pads, pad_chord(PROG[bar % 4], BAR, 0.15, 2600), b(bar * 4))
    for phrase, start in ((HOOK_A, 24), (HOOK_B, 34)):
        for step, note, ln in phrase:
            t = b(start) + step * S16
            if start == 34 and step >= 24:
                continue
            place(lead_bus, lead(note + 12 if start == 24 else note, ln * S16, 0.26, 1.2), t, pan=-0.1)
    for s in range(64):  # counter arp in bars 7-8 and 9-10 (skipping the drop-out)
        beat = 24 + s // 4
        if beat in (32, 33):
            continue
        tones = CHORDS[chord_at(beat)]
        place(keys, arp_note(tones[(s * 3) % 4] + 24, 3200, 0.07), b(24) + s * S16, pan=0.6 if s % 2 else -0.6)

    # ---- breakdown (beats 40-47)
    place(fx, downlifter(1.6, 0.35), b(40))
    place(pads, pad_chord("Ab", BAR, 0.32, 1400), b(40))
    place(pads, pad_chord("Eb", BAR, 0.32, 1500), b(44))
    for step, note, ln in HOOK_A:
        place(keys, piano(note - 12, 0.32), b(40) + step * S16, pan=0.15)
    for i in (40, 42, 44, 46):
        place(bass, np.sin(2 * np.pi * hz(BASS[chord_at(i)] - 12) * np.arange(int(BEAT * 1.8 * SR)) / SR)
              * adsr(int(BEAT * 1.8 * SR), 0.02, 0.3) * 0.22, b(i))
    place(drums, S.clap(0.22), b(43)); place(drums, S.clap(0.22), b(47))

    # ---- build (beats 48-55)
    build_bus = S.buf()
    for i in range(48, 56):
        place(build_bus, S.kick(0.85), b(i))
        kicks.append(i)
        root = BASS[chord_at(i)]
        place(build_bus, S.bass_note(root, BEAT * 0.42, 0.45, cutoff=500), b(i) + BEAT / 2)
    roll = []
    for i in range(48, 52):
        roll += [b(i), b(i) + BEAT / 2]
    for i in (52, 53):
        roll += [b(i) + k * S16 for k in range(4)]
    for i in (54, 55):
        roll += [b(i) + k * S16 / 2 for k in range(8)]
    for k, t in enumerate(roll):
        if t < b(56) - 0.12:
            place(drums, snare(0.12 + 0.4 * (k / len(roll)) ** 1.5, 180 + 140 * k / len(roll)), t)
    place(pads, pad_chord("Db", BAR, 0.24, 1800), b(48))
    place(pads, pad_chord("Eb", BAR, 0.26, 2600), b(52))
    place(fx, S.riser(BAR * 2 - 0.1, 0.6, 200, 9000), b(48))
    # sweep the build bus open: low-pass from 400 Hz to full over two bars
    s0, s1 = int(b(48) * SR), int(b(56) * SR)
    k = np.clip((np.arange(N) - s0) / (s1 - s0), 0, 1)
    build_bus = sweep_lp(build_bus, 300 * (40 ** k))
    drums += build_bus

    # ---- final drop (beats 56-63)
    place(fx, S.impact(1.0, 3.0), b(56))
    place(fx, reverse_cymbal(0.3, 0.0), b(56))
    for i in range(56, 60):
        kicks.append(i)
        place(drums, S.kick(1.0), b(i))
        if i % 4 in (1, 3):
            place(drums, S.clap(0.5), b(i))
        for k in range(4):
            place(drums, S.hat(level=0.24 if k == 2 else 0.1), b(i) + k * S16, pan=0.3 if k % 2 else -0.15)
    place(bass, reese(41, BAR * 0.98, 0.55), b(56))
    place(keys, big_chord("Fm", BAR, 0.42), b(56))
    for step, note, ln in HOOK_A[:6]:
        place(lead_bus, lead(note + 12, ln * S16, 0.28, 1.4), b(56) + step * S16)
    # last chord rings out under the held lockup
    place(drums, S.kick(1.0), b(60))
    place(fx, S.impact(0.7, 2.0), b(60))
    place(keys, big_chord("Db", BAR * 2.2, 0.48), b(60))
    place(pads, pad_chord("Db", BAR * 1.0, 0.3, 3200), b(60))
    place(bass, reese(37, BAR * 0.95, 0.45), b(60))

    # ---- mix
    duck = np.ones(N)
    dn = int(0.2 * SR)
    shape = 1 - 0.7 * np.exp(-np.arange(dn) / (0.07 * SR))
    for i in kicks:
        s = int(b(i) * SR)
        duck[s:s + dn] = np.minimum(duck[s:s + dn], shape[:max(0, min(dn, N - s))])
    duck = duck[:, None]
    lead_bus = delay(lead_bus, BEAT * 0.75, fb=0.35, mix=0.28)
    keys = delay(keys, BEAT * 0.75, fb=0.3, mix=0.18)
    music = drums * 0.92 + (bass * 0.9 + lead_bus * 0.85 + keys * 0.8 + pads) * duck
    music = S.reverb(music, seconds=1.8, wet=0.14)
    fx = S.reverb(fx, seconds=2.6, wet=0.24, tone=6500)
    music /= np.max(np.abs(music)) + 1e-9
    fx /= np.max(np.abs(fx)) + 1e-9
    mix = music * 0.8 + fx * 0.42
    tail = np.ones(N)
    fs = int(29.2 * SR)
    tail[fs:] = np.linspace(1, 0, N - fs) ** 1.5
    mix *= tail[:, None]
    stem = music * tail[:, None]
    return mix / (np.max(np.abs(mix)) + 1e-9), stem / (np.max(np.abs(stem)) + 1e-9)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    mix, stem = build()
    sf.write(f"{out}/score-v2-raw.wav", (mix * 0.89).astype(np.float32), SR, subtype="PCM_24")
    sf.write(f"{out}/music-raw.wav", (stem * 0.89).astype(np.float32), SR, subtype="PCM_24")
    print("wrote", out)
