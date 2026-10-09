"""
Soundtrack for the fast-cut v2 film. Fully synthesized, so royalty-free.

    python3 audio/make_soundtrack_v2.py  ->  public/soundtrack-v2.wav

120 BPM, A minor -> lifts a whole step for the pledges. Half-time trap drums,
808 with glides, formant "vocal chops", a delayed pluck lead, a stutter into
the first drop, a filtered breakdown, a tape-stop into VOTE, and one sound per
cut chosen by the shot's "hit" in timeline-v2.json.
"""

import json
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "timeline-v2.json")))
FPS = TL["fps"]
DUR = TL["durationInFrames"] / FPS
BEAT = 60 / TL["bpm"]
BAR = 4 * BEAT
S16 = BEAT / 4
N = int(DUR * SR)
rng = np.random.default_rng(11)
SHOT = {s["id"]: s["from"] / FPS for s in TL["shots"]}

drums, bass, music, sfx, send = (np.zeros((2, N)) for _ in range(5))
kicks = []


def place(dst, sig, t, gain=1.0, pan=0.0):
    i = int(round(t * SR))
    if i >= N or i + len(sig if sig.ndim == 1 else sig[0]) < 0:
        return
    if sig.ndim == 1:
        sig = np.vstack([sig * np.sqrt(1 - pan), sig * np.sqrt(1 + pan)])
    if i < 0:
        sig, i = sig[:, -i:], 0
    n = min(sig.shape[1], N - i)
    dst[:, i : i + n] += gain * sig[:, :n]


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, btype=kind, fs=SR, output="sos"), x)


def tt(sec):
    return np.arange(int(sec * SR)) / SR


def noise(sec):
    return rng.standard_normal(int(sec * SR))


def hz(name, shift=0):
    idx = {"C": -9, "C#": -8, "D": -7, "Eb": -6, "E": -5, "F": -4, "F#": -3, "G": -2, "Ab": -1, "A": 0, "Bb": 1, "B": 2}
    return 440.0 * 2 ** ((idx[name[:-1]] + 12 * (int(name[-1]) - 4) + shift) / 12)


def saw(f, sec, ph=0.0):
    t = tt(sec)
    return 2 * ((t * f + ph) % 1) - 1


LIFT = 21.5  # key goes up a whole step for the pledges
PROG = [("A", "m"), ("F", ""), ("C", ""), ("G", "")]


def key_shift(t):
    return 2 if t >= LIFT else 0


def chord_root(t):
    if t >= 27.5:
        return "C"
    return PROG[int(t // BAR) % 4][0]


def triad(t):
    r = chord_root(t)
    table = {"A": ["A3", "C4", "E4", "A4"], "F": ["F3", "A3", "C4", "F4"], "C": ["G3", "C4", "E4", "G4"], "G": ["G3", "B3", "D4", "G4"]}
    return [hz(n, key_shift(t)) for n in table[r]]


# ------------------------------------------------------------------ voices

def kick(t, g=1.0):
    x = tt(0.42)
    body = np.sin(2 * np.pi * np.cumsum(44 + 130 * np.exp(-x * 42)) / SR) * np.exp(-x * 8)
    body[:240] += filt(noise(0.005), "highpass", 3000) * 0.4
    place(drums, np.tanh(body * 1.8), t, 0.9 * g)
    kicks.append(t)


def snare(t, g=1.0):
    x = tt(0.3)
    tone = np.sin(2 * np.pi * 190 * x) * np.exp(-x * 30)
    nz = filt(noise(0.3), "bandpass", [1200, 7000]) * np.exp(-x * 16)
    sig = tone * 0.6 + nz
    place(drums, sig, t, 0.45 * g, pan=-0.05)
    place(send, sig, t, 0.25 * g)


def clap(t, g=1.0):
    n = int(0.25 * SR)
    out = np.zeros(n)
    for k, off in enumerate([0, 0.008, 0.017]):
        i = int(off * SR)
        out[i:] += filt(rng.standard_normal(n - i), "bandpass", [900, 2800]) * np.exp(-np.arange(n - i) / SR * (70 if k < 2 else 13))
    place(drums, out, t, 0.32 * g, pan=0.05)
    place(send, out, t, 0.2 * g)


def hat(t, g=1.0, open_=False, pan=0.3):
    d = 0.16 if open_ else 0.035
    x = tt(d)
    place(drums, filt(noise(d), "highpass", 8000) * np.exp(-x / (d / 3)), t, 0.13 * g, pan)


def sub808(t, f0, f1, length, g=1.0):
    x = tt(length)
    glide = f0 + (f1 - f0) * np.clip(x / 0.09, 0, 1) if f1 != f0 else np.full_like(x, f0)
    s = np.sin(2 * np.pi * np.cumsum(glide) / SR)
    env = np.clip(x / 0.004, 0, 1) * np.exp(-x * 2.2) * np.clip((length - x) / 0.02, 0, 1)
    sig = np.tanh(s * env * 2.2)
    sig += 0.25 * filt(np.tanh(s * env * 6), "bandpass", [180, 900])  # grit so it reads on phones
    place(bass, sig, t, 0.42 * g)


FORMANTS = {"a": (800, 1150, 2900), "o": (450, 800, 2830), "e": (400, 2000, 2550), "i": (300, 2300, 3000), "u": (325, 700, 2530)}


def vox(t, f, vowel="a", length=0.18, g=1.0, pan=0.0):
    """Formant-filtered saw: a synthetic vocal chop."""
    src = saw(f, length) + 0.5 * saw(f * 1.005, length, 0.3)
    out = sum(filt(src, "bandpass", [fc * 0.85, fc * 1.15]) * w for fc, w in zip(FORMANTS[vowel], (1.0, 0.6, 0.25)))
    x = tt(length)
    out *= np.clip(x / 0.006, 0, 1) * np.clip((length - x) / 0.03, 0, 1)
    place(music, out, t, 0.9 * g, pan)
    place(send, out, t, 0.35 * g)


def pluck(t, f, g=1.0, pan=0.0, delay=True):
    x = tt(0.4)
    sig = (np.sign(np.sin(2 * np.pi * f * x)) * 0.5 + np.sin(2 * np.pi * f * x)) * np.exp(-x * 11)
    sig = filt(sig, "lowpass", 4500)
    place(music, sig, t, 0.11 * g, pan)
    if delay:  # ping-pong 3/16 delay
        for k in range(1, 4):
            place(music, sig * (0.45 ** k), t + k * 3 * S16, 0.11 * g, (-1) ** k * 0.6)


def stab(t, length=0.2, g=1.0, cutoff=2800):
    voices = []
    for side in (-1, 1):
        x = sum(saw(f * 2 ** (side * 8 / 1200), length, rng.random()) for f in triad(t))
        x = filt(x, "lowpass", cutoff) * np.exp(-tt(length) / (length * 0.45))
        voices.append(x * 0.1)
    sig = np.vstack(voices)
    place(music, sig, t, g)
    place(send, sig, t, 0.3 * g)


def pad(t0, t1, root_t=None, g=1.0, cutoff=1000):
    length = t1 - t0
    fs = triad(root_t if root_t is not None else t0)
    voices = []
    for side in (-1, 1):
        x = sum(saw(f * 2 ** (side * 12 / 1200), length, rng.random()) for f in fs)
        x = filt(x, "lowpass", cutoff)
        tx = tt(length)
        voices.append(x * np.clip(tx / 0.2, 0, 1) * np.clip((length - tx) / 0.25, 0, 1) * 0.045)
    sig = np.vstack(voices)
    place(music, sig, t0, g)
    place(send, sig, t0, 0.4 * g)


def sweep(sec, f0, f1, shape):
    x = noise(sec)
    out = np.zeros_like(x)
    edges = np.linspace(0, x.size, 41).astype(int)
    for b in range(40):
        a, z = edges[b], edges[b + 1]
        fc = f0 * (f1 / f0) ** (b / 39)
        seg = filt(x[max(0, a - 1500) : z], "bandpass", [max(40, fc * 0.6), min(SR / 2 - 200, fc * 1.6)])
        out[a:z] = seg[-(z - a) :]
    u = np.linspace(0, 1, x.size)
    amp = {"rise": u ** 2.2, "fall": (1 - u) ** 1.6, "bell": np.sin(np.pi * u) ** 1.5}[shape]
    return out * amp


def whoosh(t, sec=0.35, up=True, g=1.0):
    place(sfx, sweep(sec, 500 if up else 4000, 4000 if up else 400, "bell"), t - sec * 0.6, 0.5 * g, 0.2)


def riser(t0, t1, g=1.0):
    sec = t1 - t0
    x = tt(sec)
    tone = np.sin(2 * np.pi * np.cumsum(200 * 10 ** (x / sec)) / SR) * (x / sec) ** 2
    place(sfx, sweep(sec, 300, 7000, "rise") * 0.5 + tone * 0.07, t0, 0.5 * g)


def reverse_crash(t, sec=0.5, g=1.0):
    x = tt(sec)
    crash = filt(noise(sec), "highpass", 4000) * np.exp(-x * 3)
    place(sfx, crash[::-1], t - sec, 0.35 * g)


def impact(t, g=1.0):
    x = tt(2.0)
    boom = np.sin(2 * np.pi * np.cumsum(36 + 50 * np.exp(-x * 14)) / SR) * np.exp(-x * 2.4)
    thud = filt(noise(2.0), "lowpass", 450) * np.exp(-x * 11) * 0.6
    crash = filt(noise(2.0), "highpass", 4500) * np.exp(-x * 1.8) * 0.2
    place(drums, np.tanh(boom * 1.4) + thud, t, 0.8 * g)
    place(sfx, crash, t, 0.55 * g, 0.1)
    place(send, crash + thud, t, 0.25 * g)
    kicks.append(t)


def click(t, g=1.0):
    x = tt(0.03)
    sig = filt(noise(0.03), "highpass", 1800) * np.exp(-x * 420) + 0.5 * np.sin(2 * np.pi * 2400 * x) * np.exp(-x * 170)
    place(sfx, sig, t, 0.5 * g, 0.25)


def tick(t, f=2200, g=1.0, pan=0.0):
    x = tt(0.05)
    place(sfx, np.sin(2 * np.pi * f * x) * np.exp(-x * 90), t, 0.17 * g, pan)


# ------------------------------------------------------------------ arrangement

HOOK = ["A4", "C5", "E5", "D5", "C5", "A4", "G4", "A4"]  # vox hook, 16th grid positions below
HOOK_POS = [0, 3, 6, 8, 10, 11, 14, 15]
VOWELS = "aoeaoaea"


def groove(t0, t1, *, kick_on=True, full=True, hook=False, arp=False, roll=False):
    t = t0
    while t < t1 - 1e-6:
        bar_t = t - (t % BAR)
        pos = round((t - bar_t) / S16)  # 0..15 in the bar
        if kick_on and pos in (0, 6, 10):
            kick(t)
        if full and pos in (4, 12):
            snare(t)
            clap(t, 0.7)
        if full and pos == 8:
            snare(t, 1.2)
            clap(t)
        # hats: 8ths with 16th fills, 32nd roll at bar end
        if pos % 2 == 0:
            hat(t, 0.9 if pos % 4 == 2 else 0.6, open_=(pos == 14 and not roll))
        elif full:
            hat(t, 0.35, pan=-0.3)
        if roll and pos in (14, 15):
            for k in range(1, 3):
                hat(t + k * S16 / 3, 0.45, pan=0.1)
        # 808
        if full and pos in (0, 6, 10):
            r = hz({"A": "A1", "F": "F1", "C": "C2", "G": "G1"}[chord_root(t)], key_shift(t))
            nxt = r * (2 if pos == 10 else 1)
            sub808(t, r if pos != 10 else r * 0.75, nxt, S16 * (6 if pos == 0 else 4))
        if hook and pos in HOOK_POS:
            k = HOOK_POS.index(pos)
            vox(t, hz(HOOK[k], key_shift(t)), VOWELS[k], 0.13, 0.75, pan=0.25 * (-1) ** k)
        if arp and pos % 2 == 1:
            fs = triad(t)
            pluck(t, fs[(pos // 2) % 4] * 2, 0.8, pan=0.35 * np.sin(pos))
        if pos in (0, 7, 10) and full:
            stab(t, 0.16, 0.55)
        t += S16


# Intro 0-3 s: vox chop on each word cut, filtered pad, riser, stutter, gap.
pad(0.0, 2.875, 0.0, 1.0, cutoff=800)
for i, (t, n, v) in enumerate([(0.0, "E5", "e"), (0.5, "A4", "a"), (1.0, "C5", "i")]):
    vox(t, hz(n), v, 0.3, 1.1, pan=(-0.3, 0.3, 0)[i])
for k in range(12):
    hat(k * 0.25, 0.4 + 0.04 * k)
kick(1.5, 0.6)
kick(2.0, 0.6)
pluck(1.5, hz("A5"), 0.8)
pluck(1.75, hz("C6"), 0.7)
pluck(2.0, hz("E6"), 0.7)
for k in range(8):  # stutter: 16ths then 32nds on one vox slice
    step = S16 if k < 4 else S16 / 2
    t = 2.25 + (k * S16 if k < 4 else 4 * S16 + (k - 4) * S16 / 2)
    vox(t, hz("A4"), "a", step * 0.8, 0.8 + 0.05 * k)
riser(1.75, 2.875, 1.0)
reverse_crash(3.0, 0.6, 1.0)

groove(3.0, 6.5, hook=True)
groove(6.5, 11.0, arp=True, roll=True)
for k in range(8):  # snare roll build 11-12: 16ths, then 32nds
    snare(11.0 + k * S16, 0.3 + 0.04 * k)
for k in range(16):
    snare(11.5 + k * S16 / 2, 0.6 + 0.03 * k)
riser(11.0, 12.0, 0.9)
groove(12.0, 17.5, hook=True, arp=True, roll=True)
# breakdown 17.5-19: no kick, filtered (applied in the mix), then back in
groove(17.5, 19.0, kick_on=False, full=False)
pad(17.5, 19.0, 17.5, 1.1, cutoff=1400)
groove(19.0, 21.0, arp=True)
riser(20.5, 21.0, 0.6)
groove(21.5, 26.75, hook=True, arp=True, roll=True)

# Per-cut sounds from the timeline.
for s in TL["shots"]:
    t = s["from"] / FPS
    h = s["hit"]
    if h == "snap":
        snare(t, 0.9)
        tick(t, 3200, 0.8)
    elif h == "whoosh":
        whoosh(t, 0.35)
    elif h == "click":
        click(t, 1.2)
        tick(t + 0.03, 1700, 0.6)
    elif h == "roll":
        for k in range(18):
            tick(t + 0.42 * (k / 18) ** 0.9, 1300 + 90 * k, 0.6, pan=0.3 * np.sin(k))
    elif h == "impact":
        impact(t, 0.75)
    elif h == "drop":
        impact(t, 1.05)
        reverse_crash(t, 0.45, 0.8)
    # "vox" cuts are scored in the intro above

# Moments inside shots.
for i in range(4):  # award rows / event cards slam on 8ths
    tick(SHOT["awards"] + i * 0.25, 1800 + 200 * i, 1.0, -0.2)
    pluck(SHOT["events"] + 0.1 + i * 0.25, hz(["E5", "G5", "A5", "C6"][i]), 0.9, delay=False)
pluck(SHOT["crowd"] + 0.9, hz("A6"), 1.0)  # "+"
for k in range(12):
    tick(SHOT["crowd"] + 0.07 + 0.07 * k, 1500 + 120 * k, 0.45)
stab(SHOT["first"], 0.5, 1.3, cutoff=4500)
vox(SHOT["first"] + 0.25, hz("E5"), "o", 0.35, 1.0)

# Outro: tape-stop handled in the mix, then VOTE, ballot, tick.
pad(SHOT["ballot"], DUR, SHOT["ballot"] + 0.6, 1.3, cutoff=1400)
TICK = SHOT["ballot"] + 30 / FPS  # 28.0 s
click(TICK, 1.5)
impact(TICK, 0.9)
stab(TICK, 1.4, 1.3, cutoff=4000)
for k, (n, v) in enumerate([("C5", "a"), ("E5", "o"), ("G5", "a")]):
    vox(TICK + 0.25 + k * 0.125, hz(n), v, 0.16 if k < 2 else 0.5, 0.9)
kick(TICK + 0.5, 0.5)

# ------------------------------------------------------------------ mix

# Sidechain duck on music + bass.
duck = np.ones(N)
for kt in kicks:
    i = int(kt * SR)
    n = min(int(0.25 * SR), N - i)
    if n > 0:
        duck[i : i + n] = np.minimum(duck[i : i + n], 1 - 0.6 * np.exp(-np.arange(n) / SR * 15))
music *= duck
bass *= 0.5 + 0.5 * duck

verb_ir = np.vstack([rng.standard_normal(int(1.4 * SR)) for _ in range(2)]) * np.exp(-np.arange(int(1.4 * SR)) / SR * 3.4)
verb_ir = np.vstack([filt(c, "lowpass", 6500) for c in verb_ir]) * 0.012
wet = np.vstack([fftconvolve(send[c], verb_ir[c])[:N] for c in range(2)])

mix = drums + bass + music * 1.05 + sfx * 0.9 + wet


def segment_filter(x, t0, t1, f0, f1):
    """Low-pass sweep f0 -> f1 over [t0, t1] (block-wise)."""
    a, b = int(t0 * SR), int(t1 * SR)
    edges = np.linspace(a, b, 25).astype(int)
    for k in range(24):
        lo, hi = edges[k], edges[k + 1]
        fc = f0 * (f1 / f0) ** (k / 23)
        for c in range(2):
            seg = filt(x[c, max(0, lo - 2000) : hi], "lowpass", fc, order=4)
            x[c, lo:hi] = seg[-(hi - lo) :]
    return x


mix = segment_filter(mix, 17.5, 19.0, 500, 9000)  # breakdown opens up


def tape_stop(x, t0, t1):
    """Pitch and speed fall to zero across [t0, t1]; silence after until VOTE."""
    a, b = int(t0 * SR), int(t1 * SR)
    n = b - a
    rate = (1 - np.linspace(0, 1, n)) ** 1.4
    pos = a + np.cumsum(rate)
    for c in range(2):
        x[c, a:b] = np.interp(pos, np.arange(x.shape[1]), x[c]) * np.linspace(1, 0.2, n)
    return x


VOTE = SHOT["vote"]
mix = tape_stop(mix, VOTE - 0.5, VOTE - 0.02)
mix[:, int((VOTE - 0.02) * SR) : int(VOTE * SR)] = 0
# re-add the VOTE impact cleanly after the stop (it was rendered into the buses)
mix = np.vstack([filt(c, "highpass", 28) for c in mix])
mix = np.tanh(mix * 1.1) / np.tanh(1.1)
mix *= np.clip((DUR - np.arange(N) / SR) / 0.5, 0, 1)
mix *= 10 ** (-1 / 20) / np.max(np.abs(mix))

out = os.path.join(ROOT, "public", "soundtrack-v2.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype("<i2").tobytes())
print(f"wrote {out}")
