"""
Score for the 20 s reel (150 BPM), adapted from the v2 film engine.
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
DUR = 20.0
BEAT = 60 / 150
BAR = 4 * BEAT
S16 = BEAT / 4
N = int(DUR * SR)
rng = np.random.default_rng(11)

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


LIFT = 15.2  # key goes up a whole step for the pledges
PROG = [("A", "m"), ("F", ""), ("C", ""), ("G", "")]


def key_shift(t):
    return 2 if t >= LIFT else 0


def chord_root(t):
    if t >= 16.8:
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


HOOK = ["A4", "C5", "E5", "D5", "C5", "A4", "G4", "A4"]
HOOK_POS = [0, 3, 6, 8, 10, 11, 14, 15]
VOWELS = "aoeaoaea"

def brick(t, g=1.0, pan=0.0):
    x = tt(0.12)
    click_ = filt(noise(0.12), "bandpass", [1800, 6500]) * np.exp(-x * 160)
    body = np.sin(2 * np.pi * 760 * x) * np.exp(-x * 55) * 0.6 + np.sin(2 * np.pi * 180 * x) * np.exp(-x * 40) * 0.5
    place(sfx, click_ + body, t, 0.55 * g, pan)


def drive(t0, t1, hook=True):
    t = t0
    while t < t1 - 1e-6:
        pos = round((t % BAR) / S16)
        if pos % 4 == 0:
            kick(t, 0.9)
        if pos in (4, 12):
            clap(t, 1.0); snare(t, 0.6)
        hat(t, 0.75 if pos % 2 == 0 else 0.4, open_=(pos % 4 == 2), pan=0.3 * (-1) ** pos)
        r = hz({"A": "A1", "F": "F1", "C": "C2", "G": "G1"}[chord_root(t)], key_shift(t))
        if pos % 4 == 2:  # off-beat pumping bass
            sub808(t, r * 2, r * 2, S16 * 1.8, 0.8)
        if pos == 0:
            sub808(t, r, r, S16 * 1.6, 0.9)
        if pos in (0, 6, 10):
            stab(t, 0.14, 0.55, cutoff=3600)
        if hook and pos in HOOK_POS:
            k = HOOK_POS.index(pos)
            vox(t, hz(HOOK[k], key_shift(t)), VOWELS[k], 0.1, 0.6, pan=0.25 * (-1) ** k)
        if pos % 2 == 1:
            pluck(t, triad(t)[(pos // 2) % 4] * 2, 0.45, pan=0.35 * np.sin(pos), delay=False)
        t += S16


# hook: hits on each word, slash, then the drop on BUILD.
for i, t in enumerate((0.0, 0.4, 0.8)):
    vox(t, hz(["E5", "G5", "A5"][i]), "aoe"[i], 0.22, 1.1)
    snare(t, 0.9); kick(t, 0.8)
whoosh(1.0, 0.18, True, 0.9)
riser(0.5, 1.2, 0.7)
impact(1.2, 1.0); reverse_crash(1.2, 0.4, 0.7)
drive(1.2, 14.0)
brick(1.66, 1.3); impact(1.66, 0.45)
for k in range(8): pluck(1.7 + k * 0.03, hz("A6") * (1 + 0.05 * k), 0.35, delay=False)
whoosh(2.4, 0.2, False, 0.8)
# builds
impact(2.4, 0.5)
for i in range(4):
    t = 3.2 + i * 0.4; click(t, 1.2); whoosh(t, 0.2, i % 2 == 0, 0.6)
impact(5.0, 0.7)
for k in range(10): tick(5.6 + 0.045 * k, 1400 + 120 * k, 0.6)
whoosh(6.24 + 0.1, 0.2, False, 0.7)
# wins
riser(6.4, 7.6, 1.0)
for k in range(10): pluck(7.2 + k * 0.04, hz("E6") * (1 - 0.05 * k), 0.4, delay=False)
reverse_crash(7.6, 0.5, 1.0); impact(7.6, 1.2); stab(7.6, 0.6, 1.3, cutoff=5000)
snare(8.4, 0.8); impact(8.8, 0.5)
for i in range(5):
    t = 9.2 + i * 0.4; whoosh(t, 0.2, i % 2 == 0, 0.7); snare(t, 0.7); tick(t, 2000 + 200 * i, 0.8)
impact(11.2, 0.6)
# people
impact(12.0, 0.6)
for i in range(4): brick(12.12 + i * 0.2 + 0.25, 1.0, pan=0.2 * (-1) ** i)
whoosh(13.2, 0.2, True, 0.8)
for k in range(14): tick(13.2 + 0.05 * k, 1300 + 100 * k, 0.5)
impact(13.9, 0.7)
# stutter + gap before the finale
for k in range(8):
    step = S16 if k < 4 else S16 / 2
    t = 14.0 + (k * S16 if k < 4 else 4 * S16 + (k - 4) * S16 / 2)
    vox(t, hz("A4"), "a", step * 0.8, 0.9 + 0.05 * k); kick(t, 0.3 + 0.05 * k)
# finale
snare(14.8, 1.0); vox(14.8, hz("C5"), "o", 0.25, 1.0)
reverse_crash(15.2, 0.4, 1.0); impact(15.2, 1.2)
drive(15.2, 19.2)
for i in range(3): impact(15.6 + i * 0.4, 0.5); whoosh(15.6 + i * 0.4, 0.2, i % 2 == 0, 0.6)
reverse_crash(16.8, 0.5, 1.0); impact(16.8, 1.3); stab(16.8, 1.2, 1.4, cutoff=5000)
for k in range(12): pluck(16.9 + k * 0.035, hz("C6") * (1 + 0.04 * k), 0.4, delay=False)
pad(16.8, 20.0, 16.8, 1.3, cutoff=1600)
stab(19.2, 0.8, 1.2, cutoff=4500); kick(19.2, 1.0); impact(19.2, 0.6)

duck = np.ones(N)
for kt in kicks:
    i = int(kt * SR); n = min(int(0.2 * SR), N - i)
    if n > 0:
        duck[i : i + n] = np.minimum(duck[i : i + n], 1 - 0.6 * np.exp(-np.arange(n) / SR * 16))
music *= duck
bass *= 0.5 + 0.5 * duck
verb_ir = np.vstack([rng.standard_normal(int(1.1 * SR)) for _ in range(2)]) * np.exp(-np.arange(int(1.1 * SR)) / SR * 4)
verb_ir = np.vstack([filt(c, "lowpass", 6500) for c in verb_ir]) * 0.012
wet = np.vstack([fftconvolve(send[c], verb_ir[c])[:N] for c in range(2)])
mix = drums + bass + music * 1.05 + sfx * 0.95 + wet
mix[:, int(14.4 * SR):int(14.8 * SR)] *= np.linspace(1, 0.05, int(14.8 * SR) - int(14.4 * SR))  # the gap
mix = np.vstack([filt(c, "highpass", 28) for c in mix])
mix = np.tanh(mix * 1.0)
mix *= np.clip((DUR - np.arange(N) / SR) / 0.6, 0, 1)
mix *= 10 ** (-1.2 / 20) / np.max(np.abs(mix))
out = os.path.join(ROOT, "assets", "score.wav")
with wave.open(out, "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype("<i2").tobytes())
print("wrote", out)
