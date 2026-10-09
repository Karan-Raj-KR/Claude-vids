import React from "react";
import { AbsoluteFill } from "remotion";
import { COLORS, FONTS } from "../config";
import { lerp } from "../lib/anim";

/** Archivo display style. wdth 125 = expanded, 100 = normal. */
export const display = (
  size: number,
  { wdth = 125, wght = 900, lh = 0.92, track = -0.01 } = {},
): React.CSSProperties => ({
  fontFamily: FONTS.display,
  fontSize: size,
  fontVariationSettings: `"wdth" ${wdth}, "wght" ${wght}`,
  fontWeight: wght,
  lineHeight: lh,
  letterSpacing: `${track}em`,
  whiteSpace: "nowrap",
});

/** JetBrains Mono label style (uppercase, tracked). */
export const mono = (
  size: number,
  { wght = 600, track = 0.06, upper = true } = {},
): React.CSSProperties => ({
  fontFamily: FONTS.mono,
  fontSize: size,
  fontVariationSettings: `"wght" ${wght}`,
  fontWeight: wght,
  lineHeight: 1.2,
  letterSpacing: `${track}em`,
  textTransform: upper ? "uppercase" : "none",
  whiteSpace: "nowrap",
});

/**
 * Mask reveal: content rises out of an invisible baseline.
 * p = 0 hidden below the mask, 1 resting, 2 gone above it.
 */
export const Rise: React.FC<{
  p: number;
  children: React.ReactNode;
  style?: React.CSSProperties;
  inline?: boolean;
  pad?: number; // room below the baseline for descenders, in px
}> = ({ p, children, style, inline, pad = 60 }) => {
  const y = p <= 1 ? lerp(1, 0, p) : lerp(0, -1, p - 1);
  return (
    <div
      style={{
        overflow: "hidden",
        display: inline ? "inline-block" : "block",
        paddingBottom: pad,
        marginBottom: -pad,
        ...style,
      }}
    >
      <div
        style={{ translate: `0 calc(${y * 108}% + ${Math.max(0, y) * pad}px)` }}
      >
        {children}
      </div>
    </div>
  );
};

/** Kicker: small vermilion square + mono label. */
export const Kicker: React.FC<{
  text: string;
  size: number;
  color?: string;
  p?: number;
}> = ({ text, size, color = COLORS.accent, p = 1 }) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      gap: size * 0.6,
      opacity: p <= 1 ? Math.min(1, p * 1.5) : Math.max(0, 2 - p),
    }}
  >
    <div
      style={{
        width: size * 0.62,
        height: size * 0.62,
        background: COLORS.accent,
        scale: `${p <= 1 ? p : Math.max(0, 2 - p)}`,
      }}
    />
    <Rise p={p}>
      <div style={{ ...mono(size), color }}>{text}</div>
    </Rise>
  </div>
);

/** Arrow cursor. press 0..1 squashes it on click. */
export const Cursor: React.FC<{
  x: number;
  y: number;
  size?: number;
  press?: number;
  opacity?: number;
  fill?: string;
  stroke?: string;
}> = ({
  x,
  y,
  size = 64,
  press = 0,
  opacity = 1,
  fill = COLORS.ink,
  stroke = COLORS.paper,
}) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 32 32"
    style={{
      position: "absolute",
      left: x - size * 0.16,
      top: y - size * 0.09,
      opacity,
      scale: `${1 - press * 0.16}`,
      transformOrigin: "16% 9%",
      overflow: "visible",
    }}
  >
    <path
      d="M5 3 L5 26 L11 20.5 L15 29.5 L19.2 27.6 L15.3 18.8 L23 18.8 Z"
      fill={fill}
      stroke={stroke}
      strokeWidth={2}
      strokeLinejoin="round"
    />
  </svg>
);

/** Click ring that expands from a point. */
export const ClickRing: React.FC<{
  x: number;
  y: number;
  t: number; // 0..1
  r?: number;
  color?: string;
}> = ({ x, y, t, r = 60, color = COLORS.accent }) =>
  t <= 0 || t >= 1 ? null : (
    <div
      style={{
        position: "absolute",
        left: x - r * t,
        top: y - r * t,
        width: 2 * r * t,
        height: 2 * r * t,
        borderRadius: "50%",
        border: `${Math.max(1, 6 * (1 - t))}px solid ${color}`,
        opacity: 1 - t,
      }}
    />
  );

/** Tick mark drawn by stroke-dashoffset (p 0..1). */
export const Tick: React.FC<{
  size: number;
  p: number;
  color?: string;
  weight?: number;
}> = ({ size, p, color = COLORS.accent, weight = 7 }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 40 40"
    style={{ overflow: "visible" }}
  >
    <path
      d="M7 21 L16.5 30 L34 10"
      fill="none"
      stroke={color}
      strokeWidth={weight}
      strokeLinecap="square"
      strokeLinejoin="miter"
      pathLength={1}
      strokeDasharray={1}
      strokeDashoffset={1 - p}
    />
  </svg>
);

/** Right arrow (Archivo has no → glyph). */
export const Arrow: React.FC<{ size: number; color: string }> = ({
  size,
  color,
}) => (
  <svg width={size} height={size * 0.6} viewBox="0 0 50 30">
    <path
      d="M2 15 H44 M32 3 L46 15 L32 27"
      fill="none"
      stroke={color}
      strokeWidth={5}
      strokeLinecap="square"
    />
  </svg>
);

export const Fill: React.FC<{ color: string; children?: React.ReactNode }> = ({
  color,
  children,
}) => <AbsoluteFill style={{ background: color }}>{children}</AbsoluteFill>;
