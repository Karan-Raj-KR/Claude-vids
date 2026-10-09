import { Easing, interpolate } from "remotion";

// One motion language for the whole film.
export const OUT = Easing.bezier(0.16, 1, 0.3, 1); // fast start, soft land
export const IN_OUT = Easing.bezier(0.65, 0, 0.35, 1); // camera moves, morphs
export const IN = Easing.bezier(0.7, 0, 0.84, 0); // exits

/** Clamped tween from `a` to `b` over [start, start + dur] frames. */
export const tw = (
  frame: number,
  start: number,
  dur: number,
  a = 0,
  b = 1,
  easing: (t: number) => number = OUT,
) =>
  interpolate(frame, [start, start + Math.max(1, dur)], [a, b], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export type Rect = { x: number; y: number; w: number; h: number };

export const lerpRect = (a: Rect, b: Rect, t: number): Rect => ({
  x: lerp(a.x, b.x, t),
  y: lerp(a.y, b.y, t),
  w: lerp(a.w, b.w, t),
  h: lerp(a.h, b.h, t),
});

/** Deterministic pseudo-random in [0, 1) — same value every render. */
export const rand = (i: number) => {
  const s = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return s - Math.floor(s);
};
