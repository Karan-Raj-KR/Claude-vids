"""Synthesize the music bed and sound design for the Karan EDC reel.

128 BPM, 16 bars = 30.0 s. Every hit is placed on the beat grid the
storyboard uses (beat = 0.46875 s). Deterministic: a fixed RNG seed.

Usage: python synth.py <out_dir>
Writes music.wav (bed), sfx.wav (sound design) and mix.wav (both, unmastered).
"""

import sys
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
BPM = 128
BEAT = 60 / BPM            # 0.46875
BAR = BEAT * 4             # 1.875
LENGTH = 30.0
N = int(SR * LENGTH)
rng = np.random.default_rng(20261011)


def buf():
    return np.zeros((N, 2))


def place(dst, sig, t, gain=1.0, pan=0.0):
    """Add a mono or stereo signal at time t (seconds)."""
    i = int(round(t * SR))
    if i >= N:
        return
    if sig.ndim == 1:
        l = np.sqrt(0.5 * (1 - pan))
        r = np.sqrt(0.5 * (1 + pan))
        sig = np.stack([sig * l * 1.414, sig * r * 1.414], axis=1)
    sig = sig.copy()
    nf = min(len(sig), int(0.006 * SR))          # de-click every one-shot's tail
    sig[-nf:] *= np.linspace(1, 0, nf)[:, None]
    n = min(len(sig), N - i)
    dst[i:i + n] += sig[:n] * gain


def env_exp(n, decay):
    return np.exp(-np.arange(n) / (decay * SR))


def adsr(n, a, r):
    e = np.ones(n)
    na = max(1, int(a * SR))
    nr = max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na)
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


def lp(x, fc, order=2):
    sos = butter(order, min(fc, SR / 2 - 100), btype="low", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def hp(x, fc, order=2):
    sos = butter(order, fc, btype="high", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def bp(x, lo, hi, order=2):
    sos = butter(order, [lo, hi], btype="band", fs=SR, output="sos")
    return sosfilt(sos, x, axis=0)


def saw(freq, n, phase=0.0):
    t = np.arange(n) / SR
    p = (freq * t + phase) % 1.0
    return 2 * p - 1


def noise(n):
    return rng.standard_normal(n)


def hz(note):
    """MIDI note number -> Hz."""
    return 440.0 * 2 ** ((note - 69) / 12)


# ---------------------------------------------------------------- instruments

def kick(level=1.0):
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * env_exp(n, 0.16)
    click = hp(noise(n), 3000) * env_exp(n, 0.004) * 0.35
    return np.tanh((body + click) * 1.6) * level


def clap(level=1.0):
    n = int(0.35 * SR)
    x = noise(n)
    e = np.zeros(n)
    for k, off in enumerate([0, 0.011, 0.022]):
        i = int(off * SR)
        e[i:] += env_exp(n - i, 0.006 if k < 2 else 0.09)
    return bp(x * e, 900, 4200) * 1.4 * level


def hat(open_=False, level=1.0):
    n = int((0.22 if open_ else 0.06) * SR)
    x = hp(noise(n), 7500, 4)
    return x * env_exp(n, 0.07 if open_ else 0.014) * level


def supersaw(freq, n, voices=7, spread=0.012):
    out = np.zeros(n)
    for v in range(voices):
        d = (v - (voices - 1) / 2) / ((voices - 1) / 2) * spread
        out += saw(freq * (1 + d), n, phase=v / voices)
    return out / voices


def chord_notes(root):
    # minor triad + octave, voiced around the root
    return [root, root + 3, root + 7, root + 12]


def stab(root, dur=0.32, level=1.0, bright=3200):
    n = int(dur * SR)
    x = sum(supersaw(hz(m), n) for m in chord_notes(root)) / 4
    x = lp(x, bright) * env_exp(n, dur * 0.35)
    return x * level


def pad(root, dur, level=1.0, cutoff=1400, major=False):
    n = int(dur * SR)
    third = 4 if major else 3
    notes = [root, root + third, root + 7, root + 12 + (third if major else 3)]
    x = sum(supersaw(hz(m), n, voices=5, spread=0.008) for m in notes) / 4
    x = lp(x, cutoff) * adsr(n, 0.35, 0.6)
    return x * level


def bass_note(note, dur, level=1.0, cutoff=520):
    n = int(dur * SR)
    f = hz(note)
    sub = np.sin(2 * np.pi * f / 2 * np.arange(n) / SR)
    body = lp(saw(f, n), cutoff)
    return (sub * 0.7 + body * 0.6) * adsr(n, 0.004, 0.05) * level


def pluck(note, level=1.0):
    n = int(0.5 * SR)
    x = saw(hz(note), n) * 0.6 + np.sin(2 * np.pi * hz(note) * 2 * np.arange(n) / SR) * 0.3
    return lp(x, 2600) * env_exp(n, 0.12) * level


def blip(note, level=1.0):
    n = int(0.18 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * hz(note) * t) + 0.3 * np.sin(2 * np.pi * hz(note) * 2 * t)
    return x * env_exp(n, 0.05) * level


def tick(freq=2200, level=1.0):
    n = int(0.03 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t) * env_exp(n, 0.006) * level


def pop(level=1.0, freq=520):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    f = freq * (1 + 1.4 * np.exp(-t / 0.012))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.035)
    return x * level


def impact(level=1.0, length=2.2):
    n = int(length * SR)
    t = np.arange(n) / SR
    f = 30 + 55 * np.exp(-t / 0.25)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env_exp(n, 0.55)
    crack = lp(noise(n), 5000) * env_exp(n, 0.05) * 0.6
    boom = lp(noise(n), 260) * env_exp(n, 0.4) * 1.2
    fade = np.ones(n)
    k = int(n * 0.45)
    fade[-k:] = np.linspace(1, 0, k) ** 2           # always decay to silence
    return np.tanh((sub * 1.1 + crack + boom) * 1.3) * fade * level


def riser(dur, level=1.0, f0=300, f1=6000):
    n = int(dur * SR)
    x = noise(n)
    out = np.zeros(n)
    seg = int(0.02 * SR)
    for i in range(0, n, seg):
        k = i / n
        fc = f0 * (f1 / f0) ** k
        lo, hi = fc * 0.7, min(fc * 1.4, SR / 2 - 200)
        chunk = x[max(0, i - seg):i + seg]
        y = bp(chunk, lo, hi, 1)
        out[i:i + seg] = y[-min(seg, n - i):] if i else y[:min(seg, n - i)]
    t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * np.cumsum(220 * (4 ** (t / dur))) / SR) * 0.15
    e = (np.arange(n) / n) ** 2.2
    return (out + tone) * e * level


def whoosh(dur=0.45, level=1.0, up=True):
    n = int(dur * SR)
    x = noise(n)
    seg = int(0.015 * SR)
    out = np.zeros(n)
    for i in range(0, n, seg):
        k = i / n
        k = k if up else 1 - k
        fc = 400 * (12 ** k)
        y = bp(x[i:i + seg * 2], fc * 0.6, min(fc * 1.6, SR / 2 - 200), 1)
        out[i:i + seg] = y[:min(seg, n - i)]
    e = np.sin(np.pi * np.arange(n) / n) ** 1.5
    return out * e * level


def reverb(x, seconds=2.2, wet=0.25, tone=5000):
    n = int(seconds * SR)
    irs = []
    for _ in range(2):
        ir = noise(n) * env_exp(n, seconds / 6.5)
        irs.append(lp(ir, tone))
    y = np.stack([fftconvolve(x[:, c], irs[c])[:N] for c in range(2)], axis=1)
    y /= (np.max(np.abs(y)) + 1e-9)
    y *= np.max(np.abs(x)) + 1e-9
    return x * (1 - wet) + y * wet


# ---------------------------------------------------------------- arrangement

def b(i):
    """Time of beat i."""
    return i * BEAT


# F minor world: bar roots (MIDI) i - VI - VII - i style
ROOTS = [41, 41, 37, 39]          # F2, F2, Db2, Eb2 for bass
CHORD = [53, 53, 49, 51]          # F3, F3, Db3, Eb3 for stabs/pads


def build_music():
    drums, bass, keys, pads = buf(), buf(), buf(), buf()

    # kick map: beats where the kick plays
    full = set(range(4, 36)) | set(range(42, 52)) | {58, 59, 60, 61}
    half = {36, 38, 40}                       # builds: half-time
    for i in sorted(full | half):
        place(drums, kick(0.95), b(i))
    # claps on 2 and 4 of each bar in full groove; one per bar in half-time
    for i in range(4, 52):
        if i % 4 in (1, 3) and i in full:
            place(drums, clap(0.42), b(i))
    place(drums, clap(0.42), b(38) + BEAT)
    # hats: offbeat 8ths in groove, 16ths shimmer in builds
    for i in range(4, 52):
        if i in full:
            place(drums, hat(level=0.25), b(i) + BEAT / 2, pan=0.25)
            if i % 4 == 3:
                place(drums, hat(open_=True, level=0.16), b(i) + BEAT / 2, pan=-0.2)
        elif 36 <= i < 42:
            for k in range(4):
                place(drums, hat(level=0.10 + 0.04 * (k == 2)), b(i) + k * BEAT / 4, pan=0.35)
    for i in (58, 59, 60, 61):
        place(drums, hat(level=0.22), b(i) + BEAT / 2, pan=0.25)

    # bass: offbeat pump in the groove, long notes in half-time
    for i in range(4, 52):
        bar = i // 4
        root = ROOTS[bar % 4]
        if i in full:
            place(bass, bass_note(root, BEAT * 0.45, 0.5), b(i) + BEAT / 2)
            if i % 2 == 0:
                place(bass, bass_note(root - 12, BEAT * 0.3, 0.35), b(i))
        elif i in half:
            place(bass, bass_note(root, BEAT * 1.8, 0.42, cutoff=380), b(i))
    for i in (58, 59, 60, 61):
        place(bass, bass_note(41, BEAT * 0.45, 0.5), b(i) + BEAT / 2)
    place(bass, bass_note(29, BEAT * 3.5, 0.5, cutoff=200), b(58))

    # stabs: proof section (bars 5-8) and EDC (bars 2-3), syncopated
    for bar in range(2, 9):
        root = CHORD[bar % 4]
        level = 0.30 if bar >= 5 else 0.22
        for off in (0, 1.5, 2.5):
            place(keys, stab(root, level=level, bright=2600 if bar < 5 else 3800), b(bar * 4) + off * BEAT, pan=-0.15)
    # vision: brighter stabs, filter open
    for i in range(46, 52):
        root = CHORD[(i // 4) % 4]
        place(keys, stab(root + 12, dur=0.22, level=0.18, bright=5200), b(i) + BEAT / 2, pan=0.2)

    # pads: intro (dark), builds/impact (airy), quote breakdown, lockup (major lift)
    place(pads, pad(41, BAR * 1.05, 0.30, cutoff=700), 0)
    place(pads, pad(49, BEAT * 6.2, 0.26, cutoff=1800), b(36))
    place(pads, pad(51, BEAT * 4.2, 0.24, cutoff=1800), b(42))
    place(pads, pad(53, BEAT * 3.2, 0.30, cutoff=1200), b(52))
    place(pads, pad(49, BEAT * 3.2, 0.30, cutoff=1500), b(55))
    place(pads, pad(44, BEAT * 6.5, 0.34, cutoff=2600, major=True), b(58))

    # sidechain: duck bass + pads + keys under each kick
    duck = np.ones(N)
    dn = int(0.18 * SR)
    shape = 1 - 0.65 * np.exp(-np.arange(dn) / (0.06 * SR))
    for i in sorted(full | half):
        s = int(b(i) * SR)
        duck[s:s + dn] = np.minimum(duck[s:s + dn], shape[:max(0, min(dn, N - s))])
    duck = duck[:, None]

    music = drums * 0.9 + (bass * 0.85 + keys + pads) * duck
    music = reverb(music, seconds=1.6, wet=0.12)
    # intro filter sweep on bar 0 is baked into the pad; fade the last beat
    tail = np.ones(N)
    fs = int(b(62) * SR)
    tail[fs:] = np.linspace(1, 0.0, N - fs) ** 1.3
    return music * tail[:, None]


def build_sfx():
    fx = buf()
    # F01: breathing ticks, swell into the name slam
    for i in range(4):
        place(fx, tick(1800, 0.25), b(i))
    place(fx, riser(BAR, 0.55, 120, 2400), 0)
    place(fx, impact(1.0), b(4))
    place(fx, tick(2600, 0.3), b(6))
    place(fx, tick(2600, 0.3), b(7))
    # F01 -> F02 iris
    place(fx, whoosh(0.4, 0.5), b(8) - 0.32)
    place(fx, pop(0.55, 480), b(10))                     # Best Member pill
    # F03 event nodes: ascending blips
    for k, note in enumerate([72, 75, 79, 84]):
        place(fx, blip(note, 0.32), b(12 + k), pan=-0.4 + 0.27 * k)
    place(fx, whoosh(0.35, 0.55, up=False), b(16) - 0.25)  # whip left
    # F04: count-up tick run, accelerating, lands at beat 19
    t, step = b(16) + 0.05, 0.09
    while t < b(19):
        place(fx, tick(2400 + 600 * (t - b(16)), 0.18), t)
        step = max(0.035, step * 0.9)
        t += step
    place(fx, pop(0.4, 700), b(19))
    place(fx, riser(BEAT * 2, 0.35, 400, 7000), b(18))
    # F05: cobalt hit, IIT card arrival
    place(fx, impact(0.75, 1.6), b(20))
    place(fx, whoosh(0.4, 0.4), b(23) - 0.3)
    place(fx, pop(0.35, 900), b(23))
    # F06: 1ST hit, stat ticks, score bar swell
    place(fx, impact(0.95, 1.8), b(26))
    t = b(26) + 0.25
    for k in range(14):
        place(fx, tick(3000, 0.12), t + k * 0.07)
    place(fx, riser(BEAT * 2, 0.25, 600, 5000), b(28))
    # F07: proof wall, one stab per eighth
    for k in range(6):
        place(fx, hat(open_=False, level=0.35), b(32) + k * BEAT / 2, pan=-0.5 + 0.2 * k)
        place(fx, blip(84 + (k % 3) * 2, 0.12), b(32) + k * BEAT / 2)
    # F08: builds glide
    place(fx, whoosh(1.4, 0.25), b(36))
    for k in range(3):
        place(fx, tick(1500, 0.15), b(37) + k * BEAT * 1.4)
    place(fx, whoosh(0.4, 0.45), b(42) - 0.3)            # push-in
    # F09: impact plucks
    for k, note in enumerate([65, 68, 72]):
        place(fx, pluck(note, 0.35), b(42 + k))
    # F10: wipe + card pops
    place(fx, whoosh(0.38, 0.45, up=False), b(46) - 0.3)
    for k in range(4):
        place(fx, pop(0.32, 560 + 80 * k), b(47 + k))
    # F11: collapse to dot, quote hits
    place(fx, whoosh(0.35, 0.4, up=False), b(52) - 0.3)
    place(fx, pluck(60, 0.3), b(52))
    place(fx, pluck(63, 0.3), b(53))
    place(fx, impact(0.6, 1.4), b(54))                   # "Now…"
    place(fx, riser(BEAT * 3.5, 0.5, 200, 8000), b(58) - BEAT * 3.5)
    # F12: network burst, name slam, tagline pop, Monday tick
    place(fx, impact(1.0, 2.6), b(58))
    for k in range(8):
        place(fx, tick(2000 + 200 * k, 0.12), b(58) + 0.08 + k * 0.06, pan=-0.6 + 0.17 * k)
    place(fx, impact(0.55, 1.6), b(60))
    place(fx, pop(0.4, 640), b(61))
    place(fx, tick(2400, 0.22), b(62))
    fx = reverb(fx, seconds=2.4, wet=0.22, tone=6000)
    return fx


def main(out):
    music = build_music()
    fx = build_sfx()
    music /= np.max(np.abs(music)) + 1e-9
    fx /= np.max(np.abs(fx)) + 1e-9
    mix = music * 0.72 + fx * 0.55
    mix /= np.max(np.abs(mix)) + 1e-9
    sf.write(f"{out}/music.wav", (music * 0.89).astype(np.float32), SR, subtype="PCM_24")
    sf.write(f"{out}/sfx.wav", (fx * 0.89).astype(np.float32), SR, subtype="PCM_24")
    sf.write(f"{out}/mix-raw.wav", (mix * 0.89).astype(np.float32), SR, subtype="PCM_24")
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
