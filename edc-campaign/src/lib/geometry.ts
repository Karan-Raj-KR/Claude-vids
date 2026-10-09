import type { Rect } from "./anim";

/**
 * Shared positions for "the box" as it carries across cuts.
 * Each scene ends with the box where the next scene picks it up.
 */

/** Founder tag in the name scene (start of the product window morph). */
export const tagRect = (V: boolean): Rect =>
  V ? { x: 88, y: 960, w: 600, h: 104 } : { x: 140, y: 740, w: 660, h: 118 };

/** Product window in the builds scene. */
export const windowRect = (V: boolean): Rect =>
  V ? { x: 88, y: 590, w: 904, h: 760 } : { x: 860, y: 190, w: 920, h: 700 };

/** 11×11 grid of Open Loop teams in the wins scene. */
export const grid = (V: boolean) => {
  const cell = V ? 62 : 46;
  const gap = V ? 14 : 12;
  const n = 11;
  const size = n * cell + (n - 1) * gap;
  const x0 = V ? (1080 - size) / 2 : 1780 - size;
  const y0 = V ? 440 : (1080 - size - 60) / 2;
  const cellRect = (r: number, c: number): Rect => ({
    x: x0 + c * (cell + gap),
    y: y0 + r * (cell + gap),
    w: cell,
    h: cell,
  });
  return { cell, gap, n, size, x0, y0, cellRect, winner: cellRect(5, 5) };
};

/** Pledge number box. */
export const pledgeBox = (V: boolean): Rect =>
  V ? { x: 88, y: 560, w: 180, h: 180 } : { x: 140, y: 290, w: 170, h: 170 };

/** Ballot checkbox in the vote scene. */
export const ballotBox = (V: boolean): Rect =>
  V ? { x: 88, y: 790, w: 190, h: 190 } : { x: 140, y: 404, w: 190, h: 190 };
