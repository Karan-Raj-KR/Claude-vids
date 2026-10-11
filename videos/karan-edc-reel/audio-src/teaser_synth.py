"""10 s teaser cut of the campaign score, built from the same instruments.

Same 128 BPM grid: intro (beats 0-3), name hit (4), four proof hits on
beats 8/10/12/14, lockup hit on 16, tail to 10.0 s.

Usage: python teaser_synth.py <out_dir>   -> teaser-raw.wav
"""

import sys
import numpy as np
import soundfile as sf
import synth as S

S.LENGTH = 10.0
S.N = int(S.SR * S.LENGTH)
b = S.b


def build():
    drums, bass, keys, pads, fx = S.buf(), S.buf(), S.buf(), S.buf(), S.buf()
    groove = range(4, 16)
    for i in groove:
        S.place(drums, S.kick(0.95), b(i))
        if i % 4 in (1, 3):
            S.place(drums, S.clap(0.42), b(i))
        S.place(drums, S.hat(level=0.25), b(i) + S.BEAT / 2, pan=0.25)
        root = S.ROOTS[(i // 4) % 4]
        S.place(bass, S.bass_note(root, S.BEAT * 0.45, 0.5), b(i) + S.BEAT / 2)
        if i % 2 == 0:
            S.place(bass, S.bass_note(root - 12, S.BEAT * 0.3, 0.35), b(i))
    for i in (16, 17, 18, 19):
        S.place(drums, S.kick(0.9), b(i))
    for bar in range(1, 4):
        for off in (0, 1.5, 2.5):
            S.place(keys, S.stab(S.CHORD[bar % 4], level=0.26, bright=3400), b(bar * 4) + off * S.BEAT, pan=-0.15)
    S.place(pads, S.pad(41, S.BAR * 1.05, 0.3, cutoff=700), 0)
    S.place(pads, S.pad(44, S.BEAT * 5.6, 0.34, cutoff=2600, major=True), b(16))
    S.place(bass, S.bass_note(29, S.BEAT * 4, 0.5, cutoff=200), b(16))

    for i in range(4):
        S.place(fx, S.tick(1800, 0.25), b(i))
    S.place(fx, S.riser(S.BAR, 0.55, 120, 2400), 0)
    S.place(fx, S.impact(1.0), b(4))
    S.place(fx, S.tick(2600, 0.3), b(6))
    for k, i in enumerate((8, 10, 12, 14)):
        S.place(fx, S.whoosh(0.3, 0.45, up=k % 2 == 0), b(i) - 0.24)
        S.place(fx, S.impact(0.55, 1.0), b(i))
    S.place(fx, S.riser(S.BEAT * 3, 0.45, 300, 8000), b(16) - S.BEAT * 3)
    S.place(fx, S.impact(1.0, 2.2), b(16))
    S.place(fx, S.pop(0.4, 640), b(17))
    S.place(fx, S.tick(2400, 0.22), b(18))

    duck = np.ones(S.N)
    dn = int(0.18 * S.SR)
    shape = 1 - 0.65 * np.exp(-np.arange(dn) / (0.06 * S.SR))
    for i in list(groove) + [16, 17, 18, 19]:
        s = int(b(i) * S.SR)
        duck[s:s + dn] = np.minimum(duck[s:s + dn], shape[:max(0, min(dn, S.N - s))])
    music = drums * 0.9 + (bass * 0.85 + keys + pads) * duck[:, None]
    music = S.reverb(music, seconds=1.6, wet=0.12)
    fx = S.reverb(fx, seconds=2.4, wet=0.22, tone=6000)
    music /= np.max(np.abs(music)) + 1e-9
    fx /= np.max(np.abs(fx)) + 1e-9
    mix = music * 0.72 + fx * 0.55
    tail = np.ones(S.N)
    fs = int(9.2 * S.SR)
    tail[fs:] = np.linspace(1, 0, S.N - fs) ** 1.3
    mix *= tail[:, None]
    return mix / (np.max(np.abs(mix)) + 1e-9)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    sf.write(f"{out}/teaser-raw.wav", (build() * 0.89).astype(np.float32), S.SR, subtype="PCM_24")
    print("wrote", out)
