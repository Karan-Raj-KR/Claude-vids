"""
Original soundtrack for the EDC campaign film. Every sound is synthesized
here, so the track is royalty-free.

    python3 audio/make_soundtrack.py   ->  public/soundtrack.wav

120 BPM, A minor (Am-F-C-G), one beat = 0.5 s = 30 video frames.
Cue times below are in seconds and mirror the animation constants in
src/scenes/*.tsx (scene starts come from timeline.json).
"""

import json
import os
import wave

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TL = json.load(open(os.path.join(ROOT, "timeline.json")))
FPS = TL["fps"]
DUR = TL["durationInFrames"] / FPS
BEAT = 60 / TL["bpm"]
BAR = 4 * BEAT
S = {k: v["from"] / FPS for k, v in TL["scenes"].items()}  # scene starts (s)

N = int(DUR * SR)
rng = np.random.default_rng(7)


def bus():
    return np.zeros((2, N))


drums, music, sfx, verb_send = bus(), bus(), bus(), bus()
kick_times = []


def place(dst, sig, t, gain=1.0, pan=0.0):
    """Mix a mono or stereo signal into a bus at time t (s)."""
    i = int(round(t * SR))
    if i >= N:
        return
    if sig.ndim == 1:
        left = sig * np.sqrt(0.5 * (1 - pan))
        right = sig * np.sqrt(0.5 * (1 + pan))
        sig = np.vstack([left, right]) * np.sqrt(2)
    n = min(sig.shape[1], N - i)
    dst[:, i : i + n] += gain * sig[:, :n]


def env(n, attack=0.002, decay=0.2, curve=1.0):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay * curve)


def filt(x, kind, freq, order=2):
    sos = butter(order, freq, btype=kind, fs=SR, output="sos")
    return sosfilt(sos, x)


def noise(sec):
    return rng.standard_normal(int(sec * SR))


def saw(freq, sec, detune_cents=0.0, phase=0.0):
    t = np.arange(int(sec * SR)) / SR
    f = freq * 2 ** (detune_cents / 1200)
    return 2 * ((t * f + phase) % 1.0) - 1


def note(name):
    names = {"C": -9, "C#": -8, "D": -7, "Eb": -6, "E": -5, "F": -4, "F#": -3,
             "G": -2, "Ab": -1, "A": 0, "Bb": 1, "B": 2}
    pitch, octave = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[pitch] + 12 * (octave - 4)) / 12)


CHORDS = {  # voicings around middle C
    "Am": ["A3", "C4", "E4", "A4"],
    "F": ["F3", "A3", "C4", "F4"],
    "C": ["G3", "C4", "E4", "G4"],
    "G": ["G3", "B3", "D4", "G4"],
}
BASS = {"Am": "A1", "F": "F1", "C": "C2", "G": "G1"}
PROG = ["Am", "F", "C", "G"]


def chord_at(t):
    if t >= 28.0:
        return "C"
    if 26.0 <= t < 28.0:
        return "G"
    return PROG[int(t // BAR) % 4]


# ---------------------------------------------------------------- instruments

def kick(t, gain=1.0):
    n = int(0.45 * SR)
    tt = np.arange(n) / SR
    freq = 46 + 110 * np.exp(-tt * 38)
    body = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tt * 7.5)
    click = filt(noise(0.006), "highpass", 2500) * 0.35
    body[: click.size] += click
    place(drums, np.tanh(body * 1.6), t, 0.95 * gain)
    kick_times.append(t)


def clap(t, gain=1.0):
    n = int(0.3 * SR)
    out = np.zeros(n)
    for k, off in enumerate([0, 0.009, 0.019]):
        i = int(off * SR)
        burst = filt(rng.standard_normal(n - i), "bandpass", [900, 2600]) * env(n - i, 0.0005, 0.012 if k < 2 else 0.11)
        out[i:] += burst
    place(drums, out, t, 0.42 * gain, pan=-0.05)
    place(verb_send, out, t, 0.25 * gain)


def hat(t, open_=False, gain=1.0, pan=0.25):
    dur = 0.18 if open_ else 0.045
    x = filt(noise(dur), "highpass", 7500) * env(int(dur * SR), 0.0005, dur / 3)
    place(drums, x, t, 0.16 * gain, pan=pan)


def bass_note(t, freq, length, gain=1.0):
    x = saw(freq, length) + 0.5 * saw(freq * 0.5, length)
    x = filt(x, "lowpass", 420, order=4)
    x *= env(x.size, 0.004, length * 0.6)
    place(music, np.tanh(x * 1.4), t, 0.34 * gain)


def stab(t, chord, length=0.22, gain=1.0, cutoff=2600):
    voices = []
    for side, cents in ((-1, -9), (1, 9)):
        x = sum(saw(note(n), length, cents * side, phase=rng.random()) for n in CHORDS[chord])
        x = filt(x, "lowpass", cutoff, order=2) * env(x.size, 0.003, length * 0.45)
        voices.append(x)
    sig = np.vstack(voices) * 0.11
    place(music, sig, t, gain)
    place(verb_send, sig, t, 0.35 * gain)


def pad(t0, t1, chord, gain=1.0, cutoff=900):
    length = t1 - t0
    voices = []
    for side, cents in ((-1, -12), (1, 12)):
        x = sum(saw(note(n), length, cents * side, phase=rng.random()) for n in CHORDS[chord])
        x = filt(x, "lowpass", cutoff, order=2)
        tt = np.arange(x.size) / SR
        shape = np.clip(tt / 0.25, 0, 1) * np.clip((length - tt) / 0.3, 0, 1)
        voices.append(x * shape)
    sig = np.vstack(voices) * 0.05
    place(music, sig, t0, gain)
    place(verb_send, sig, t0, 0.4 * gain)


def pluck(t, freq, gain=1.0, pan=0.0):
    n = int(0.5 * SR)
    tt = np.arange(n) / SR
    x = (np.sin(2 * np.pi * freq * tt) + 0.3 * np.sin(2 * np.pi * 2 * freq * tt)) * np.exp(-tt * 9)
    place(music, x, t, 0.16 * gain, pan)
    place(verb_send, x, t, 0.12 * gain)


def click(t, gain=1.0):
    n = int(0.03 * SR)
    tt = np.arange(n) / SR
    x = filt(noise(0.03), "highpass", 1800) * np.exp(-tt * 400)
    x += 0.5 * np.sin(2 * np.pi * 2300 * tt) * np.exp(-tt * 160)
    place(sfx, x, t, 0.5 * gain, pan=0.2)


def tick(t, freq=2200, gain=1.0, pan=0.0):
    n = int(0.05 * SR)
    tt = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * tt) * np.exp(-tt * 90)
    place(sfx, x, t, 0.18 * gain, pan)


def sweep_noise(sec, f0, f1, shape="rise"):
    """Noise through a band-pass whose centre moves f0 -> f1 (block-wise)."""
    x = noise(sec)
    out = np.zeros_like(x)
    blocks = 48
    edges = np.linspace(0, x.size, blocks + 1).astype(int)
    for b in range(blocks):
        a, z = edges[b], edges[b + 1]
        fc = f0 * (f1 / f0) ** (b / (blocks - 1))
        lo, hi = max(40, fc * 0.6), min(SR / 2 - 100, fc * 1.6)
        seg = filt(x[max(0, a - 2000) : z], "bandpass", [lo, hi])
        out[a:z] = seg[-(z - a) :]
    tt = np.linspace(0, 1, x.size)
    if shape == "rise":
        amp = tt ** 2.2
    elif shape == "fall":
        amp = (1 - tt) ** 1.6
    else:  # bell
        amp = np.sin(np.pi * tt) ** 1.5
    return out * amp


def riser(t0, t1, gain=1.0):
    sec = t1 - t0
    x = sweep_noise(sec, 300, 6000, "rise")
    tt = np.arange(x.size) / SR
    tone = np.sin(2 * np.pi * np.cumsum(180 * (12 ** (tt / sec))) / SR) * (tt / sec) ** 2
    place(sfx, x * 0.5 + tone * 0.08, t0, 0.5 * gain)
    place(verb_send, x * 0.5, t0, 0.2 * gain)


def whoosh(t0, sec, up=True, gain=1.0, pan=0.0):
    x = sweep_noise(sec, 400 if up else 3500, 3500 if up else 300, "bell")
    place(sfx, x, t0, 0.55 * gain, pan)
    place(verb_send, x, t0, 0.2 * gain)


def impact(t, gain=1.0):
    n = int(2.2 * SR)
    tt = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 40 * np.exp(-tt * 12)) / SR) * np.exp(-tt * 2.2)
    thud = filt(noise(2.2), "lowpass", 500) * np.exp(-tt * 10) * 0.6
    crash = filt(noise(2.2), "highpass", 4500) * np.exp(-tt * 1.6) * 0.22
    place(drums, np.tanh(boom * 1.3) + thud, t, 0.8 * gain)
    place(sfx, crash, t, 0.6 * gain, pan=0.1)
    place(verb_send, crash + thud, t, 0.3 * gain)
    kick_times.append(t)


def snap(t, gain=1.0):
    clap(t, 0.9 * gain)
    tick(t, 3200, 0.8 * gain)


def counter_roll(t0, t1, count=16):
    for k in range(count):
        tt = t0 + (t1 - t0) * (k / count) ** 0.9
        tick(tt, 1400 + 1600 * k / count, 0.55, pan=0.3 * np.sin(k))


# ---------------------------------------------------------------- arrangement

# Hook 0-3 s: plucks on each word, filtered pulse, riser into the cut.
for i, tt in enumerate([0.0, 0.125, 0.25, 0.375, 0.5]):
    pluck(tt, note(["E5", "A5", "C6", "E6", "A6"][i]), 0.9, pan=(-0.3, 0.3)[i % 2])
pad(0.0, 3.0, "Am", 0.9, cutoff=700)
for k in range(12):
    hat(k * 0.25, gain=0.5 + 0.04 * k)
for tt in [1.5, 2.0, 2.5]:
    kick(tt, 0.55)
for i, tt in enumerate([1.5, 1.625, 1.75, 1.875]):  # line 2 words
    pluck(tt, note(["A4", "C5", "E5", "G5"][i]), 0.7)
stab(2.0, "Am", 0.3, 0.7, cutoff=1500)  # highlight wipe
click(2.5)
riser(1.6, 3.0, 1.0)
whoosh(2.55, 0.45, up=True, gain=0.9)

# Main groove, in sections so the energy moves with the story.
#   (start, end, kick, clap, bass, 16th hats, stab cutoff, stab gain)
SECTIONS = [
    (3.0, 7.0, True, True, True, False, 2400, 0.85),     # name
    (7.0, 12.0, True, True, True, False, 2600, 0.9),     # builds
    (12.0, 17.0, True, True, True, True, 3000, 0.95),    # wins: lift
    (17.0, 19.0, False, True, False, False, 1800, 0.7),  # people: breathe
    (19.0, 21.0, True, True, True, True, 2600, 0.9),     # crowd: back in
    (21.0, 26.5, True, True, True, True, 3800, 1.1),     # pledges: peak
]
for t0, t1, has_kick, has_clap, has_bass, hats16, cutoff, sg in SECTIONS:
    t = t0
    while t < t1 - 1e-6:
        beat_in_bar = round((t % BAR) / BEAT) % 4
        if has_kick:
            kick(t, 0.85)
        if has_clap and beat_in_bar in (1, 3):
            clap(t)
        for e in range(2):  # 8th-note hats, open on the off-beat
            hat(t + e * BEAT / 2, open_=(e == 1), gain=0.9 if e else 0.6, pan=0.25)
        if hats16:
            hat(t + BEAT * 0.25, gain=0.3, pan=-0.25)
        hat(t + BEAT * 0.75, gain=0.35, pan=-0.2)
        ch = chord_at(t)
        if has_bass:
            for e in range(2):
                bass_note(t + e * BEAT / 2, note(BASS[ch]) * (2 if e else 1), BEAT / 2 * 0.9)
        t += BEAT
    # 3-3-2 chord stabs
    t = t0 - (t0 % BAR)
    while t < t1 - 1e-6:
        for e in (0, 3, 6):
            st = t + e * BEAT / 2
            if t0 <= st < t1:
                stab(st, chord_at(st), 0.2, sg, cutoff=cutoff)
        t += BAR
pad(17.0, 19.0, "C", 1.0, cutoff=1100)
for k in range(16):  # wins: 16th-note arpeggio sparkle
    t = 12.5 + k * 0.25
    pluck(t, note(["A5", "E6", "C6", "E6"][k % 4]) if chord_at(t) == "Am" else note(["C6", "G6", "E6", "G6"][k % 4]), 0.28, pan=0.5 * np.sin(k))

# Scene hits.
impact(S["name"], 1.0)                      # 3.0 drop
snap(S["builds"])                           # 7.0 cut
for c in (30, 90, 150, 210):                # tab clicks
    click(S["builds"] + c / FPS, 1.1)
whoosh(S["builds"] + 270 / FPS, 0.5, up=False, gain=0.8)   # window collapses
impact(S["wins"], 0.75)                     # 12.0
for k in range(8):                          # grid ripple arpeggio
    pluck(S["wins"] + k * 0.0625, note(["A5", "C6", "E6", "A6"][k % 4]), 0.45, pan=0.4 * np.cos(k))
whoosh(S["wins"] + 60 / FPS, 0.5, up=False, gain=0.35)      # 120 squares dim
stab(S["wins"] + 90 / FPS, "C", 0.5, 1.2, cutoff=4000)      # 1ST PLACE
place(sfx, filt(noise(1.6), "highpass", 5000) * env(int(1.6 * SR), 0.001, 0.5), S["wins"] + 90 / FPS, 0.2)
whoosh(S["wins"] + 150 / FPS - 0.12, 0.42, up=True, gain=0.9)   # camera whip
for i in range(4):                          # award rows
    tick(S["wins"] + (160 + i * 7.5) / FPS, 1800 + i * 250, 1.0, pan=-0.2)
snap(S["people"])                           # 17.0
for i in range(4):                          # event cards on 8ths
    pluck(S["people"] + (15 + i * 15) / FPS, note(["E5", "G5", "A5", "C6"][i]), 0.8, pan=(-0.3, 0.3)[i % 2])
whoosh(S["people"] + 120 / FPS - 0.15, 0.45, up=False, gain=0.8)   # camera drops
counter_roll(S["people"] + 128 / FPS, S["people"] + 180 / FPS, 20)
pluck(S["people"] + 180 / FPS, note("A6"), 1.0)                     # "+"
riser(20.0, 21.0, 0.8)
impact(S["pledges"], 1.0)                   # 21.0
for k in (1, 2):                            # pledge 2 and 3 land
    t = S["pledges"] + k * 2.0
    stab(t, chord_at(t), 0.35, 1.2, cutoff=3500)
    place(sfx, filt(noise(1.2), "highpass", 5000) * env(int(1.2 * SR), 0.001, 0.35), t, 0.14)
whoosh(S["pledges"] + 330 / FPS, 0.4, up=True, gain=0.6)   # box travels
riser(25.8, 27.0, 0.9)

# Outro 27-30 s: drop to a held chord, then the tick lands the final hit.
impact(S["vote"], 0.7)
pad(27.0, 28.1, "G", 1.3, cutoff=1200)
click(S["vote"] + 60 / FPS, 1.4)
impact(S["vote"] + 60 / FPS, 1.0)
stab(S["vote"] + 60 / FPS, "C", 1.6, 1.3, cutoff=3500)
pad(28.0, 30.0, "C", 1.4, cutoff=1400)
pluck(28.0, note("C6"), 0.9, pan=-0.2)
pluck(28.125, note("E6"), 0.7, pan=0.2)
pluck(28.25, note("G6"), 0.6, pan=-0.2)

# ---------------------------------------------------------------- mix

# Sidechain: duck the music under every kick.
duck = np.ones(N)
for kt in kick_times:
    i = int(kt * SR)
    n = min(int(0.28 * SR), N - i)
    if n > 0:
        tt = np.arange(n) / SR
        duck[i : i + n] = np.minimum(duck[i : i + n], 1 - 0.55 * np.exp(-tt * 14))
music *= duck

# Reverb: decaying stereo noise impulse.
ir_len = int(1.6 * SR)
tt = np.arange(ir_len) / SR
ir = np.vstack([rng.standard_normal(ir_len), rng.standard_normal(ir_len)]) * np.exp(-tt * 3.2)
ir = np.vstack([filt(ir[0], "lowpass", 6000), filt(ir[1], "lowpass", 6000)]) * 0.012
wet = np.vstack([fftconvolve(verb_send[c], ir[c])[:N] for c in range(2)])

mix = drums * 1.0 + music * 1.0 + sfx * 0.9 + wet * 1.0
mix = np.vstack([filt(mix[c], "highpass", 28) for c in range(2)])

# Gentle bus saturation, fade the tail, normalise to -1 dBFS.
mix = np.tanh(mix * 1.05) / np.tanh(1.05)
fade = np.clip((DUR - np.arange(N) / SR) / 0.6, 0, 1)
mix *= fade
mix *= 10 ** (-1 / 20) / np.max(np.abs(mix))

out = os.path.join(ROOT, "public", "soundtrack.wav")
pcm = (mix.T * 32767).astype("<i2")
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
rms = 20 * np.log10(np.sqrt(np.mean(mix ** 2)))
print(f"wrote {out}: {DUR:.1f}s, RMS {rms:.1f} dBFS")
