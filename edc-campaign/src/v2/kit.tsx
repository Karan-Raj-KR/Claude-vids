import React from "react";
import { Easing, Img, staticFile } from "remotion";
import { COLORS } from "../config";
import { tw } from "../lib/anim";
import { display, mono } from "../components/ui";

/** Back-out easing: overshoots then settles (pops, drops). */
export const BACK = Easing.bezier(0.34, 1.56, 0.64, 1);
export const SNAP = Easing.bezier(0.12, 1, 0.24, 1);

/** Character poses cut from assets/karan-character-sheet.webp. */
export const POSES = {
  front: { w: 357, h: 584 },
  "three-quarter": { w: 329, h: 576 },
  side: { w: 248, h: 572 },
  neutral: { w: 255, h: 309 },
  thinking: { w: 264, h: 308 },
  explaining: { w: 328, h: 305 },
  happy: { w: 281, h: 309 },
} as const;
export type Pose = keyof typeof POSES;

/** LEGO Karan, anchored by bottom-centre at (x, y), `h` px tall. */
export const Karan: React.FC<{
  pose: Pose;
  x: number;
  y: number;
  h: number;
  style?: React.CSSProperties;
}> = ({ pose, x, y, h, style }) => {
  const w = (POSES[pose].w / POSES[pose].h) * h;
  return (
    <Img
      src={staticFile(`karan/${pose}.png`)}
      style={{
        position: "absolute",
        left: x - w / 2,
        top: y - h,
        width: w,
        height: h,
        transformOrigin: "50% 100%",
        ...style,
      }}
    />
  );
};

/** Scale-down slam: big → 1 in `dur` frames. */
export const slam = (f: number, start = 0, dur = 9, from = 1.4) => ({
  scale: `${tw(f, start, dur, from, 1, SNAP)}`,
  opacity: tw(f, start, 3),
});

/** Pop from below with overshoot. */
export const pop = (f: number, start = 0, dur = 14, dist = 400) =>
  `0 ${tw(f, start, dur, dist, 0, BACK)}px`;

/** Big uppercase display line. */
export const Big: React.FC<{
  size: number;
  color: string;
  wdth?: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ size, color, wdth = 118, children, style }) => (
  <div
    style={{
      ...display(size, { wdth, lh: 0.88 }),
      color,
      textTransform: "uppercase",
      ...style,
    }}
  >
    {children}
  </div>
);

export const Label: React.FC<{
  size: number;
  color?: string;
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ size, color = COLORS.accent, children, style }) => (
  <div
    style={{ display: "flex", alignItems: "center", gap: size * 0.5, ...style }}
  >
    <div
      style={{
        width: size * 0.6,
        height: size * 0.6,
        background: COLORS.accent,
      }}
    />
    <div style={{ ...mono(size), color }}>{children}</div>
  </div>
);
