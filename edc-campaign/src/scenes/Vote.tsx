import React from "react";
import { useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN_OUT, OUT, tw } from "../lib/anim";
import { ballotBox } from "../lib/geometry";
import { useLayout } from "../lib/layout";
import {
  ClickRing,
  Cursor,
  display,
  Fill,
  mono,
  Rise,
  Tick,
} from "../components/ui";

const CLICK = 60; // 28.0 s, on the beat

/** 0:27–0:30 · Call to action: tick the box. */
export const Vote: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const T = TEXT.vote;
  const b = ballotBox(V);

  // The filled number box hollows out (from the centre) into a ballot box.
  const hollow = tw(f, 2, 16, 0, 1, IN_OUT);
  const border = Math.round(b.w * 0.075);

  const travel = tw(f, 30, 26, 0, 1, IN_OUT);
  const target = { x: b.x + b.w * 0.55, y: b.y + b.h * 0.58 };
  const cur = {
    x: target.x + (1 - travel) * W * 0.45,
    y: target.y + (1 - travel) * H * 0.35,
  };
  const press = tw(f, CLICK - 3, 3) - tw(f, CLICK, 8);

  const nameSize = pick(150, 144);
  const nameLines = V
    ? T.name
        .split(" ")
        .reduce<
          string[]
        >((acc, w, i) => (i === 0 ? [w] : i === 1 ? [acc[0], w] : [acc[0], `${acc[1]} ${w}`]), [])
    : [T.name];

  return (
    <Fill color={COLORS.paper}>
      {/* slow push-in on the final lockup after the tick */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          scale: `${tw(f, CLICK + 6, 180 - CLICK - 6, 1, 1.02, (t) => t)}`,
          transformOrigin: `${b.x + b.w / 2}px ${b.y + b.h / 2}px`,
        }}
      >
        <div
          style={{ position: "absolute", left: mx, top: b.y - pick(150, 200) }}
        >
          <Rise p={tw(f, 6, 18)}>
            <div
              style={{
                ...display(pick(112, 140), { wdth: 125 }),
                color: COLORS.accent,
              }}
            >
              {T.verb}
            </div>
          </Rise>
        </div>

        <div
          style={{
            position: "absolute",
            left: b.x + b.w + pick(48, 40),
            top: b.y + pick(12, -6),
          }}
        >
          {nameLines.map((l, i) => (
            <Rise key={l} p={tw(f, 10 + i * 5, 18)}>
              <div
                style={{
                  ...display(nameSize, { wdth: 118, lh: 0.92 }),
                  color: COLORS.ink,
                }}
              >
                {l}
              </div>
            </Rise>
          ))}
          <Rise p={tw(f, 20, 18)} style={{ marginTop: pick(22, 26) }}>
            <div
              style={{
                ...display(pick(74, 70), { wdth: 100, wght: 700, lh: 1.05 }),
                color: COLORS.ink,
              }}
            >
              {T.role}
            </div>
          </Rise>
          {T.date ? (
            <Rise p={tw(f, 26, 18)} style={{ marginTop: 18 }}>
              <div
                style={{
                  ...mono(pick(36, 36), { wght: 700 }),
                  color: COLORS.accent,
                }}
              >
                {T.date}
              </div>
            </Rise>
          ) : null}
        </div>

        <div
          style={{
            position: "absolute",
            left: b.x,
            top: b.y,
            width: b.w,
            height: b.h,
            background: COLORS.accent,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <div
            style={{
              position: "absolute",
              inset: border,
              background: COLORS.paper,
              scale: `${hollow}`,
            }}
          />
          <div style={{ position: "relative", display: "flex" }}>
            <Tick
              size={b.w * 0.78}
              p={tw(f, CLICK, 14, 0, 1, OUT)}
              weight={10}
              color={COLORS.ink}
            />
          </div>
        </div>

        <div style={{ position: "absolute", left: mx, bottom: pick(110, 170) }}>
          <Rise p={tw(f, 36, 18)}>
            <div
              style={{
                ...mono(pick(38, 38), { wght: 600, track: 0.02, upper: false }),
                color: COLORS.ink,
              }}
            >
              {T.links}
            </div>
          </Rise>
        </div>

        <ClickRing
          x={target.x}
          y={target.y}
          t={tw(f, CLICK, 24)}
          r={pick(130, 120)}
          color={COLORS.accent}
        />
        <Cursor
          x={cur.x}
          y={cur.y}
          size={pick(72, 76)}
          press={press}
          opacity={tw(f, 30, 6) * tw(f, CLICK + 30, 12, 1, 0)}
        />
      </div>
    </Fill>
  );
};
