import React from "react";
import { interpolateColors, useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN, IN_OUT, OUT, tw } from "../lib/anim";
import { useLayout } from "../lib/layout";
import {
  ClickRing,
  Cursor,
  display,
  Fill,
  Kicker,
  Rise,
} from "../components/ui";

/** 0:00–0:03 · Hook. Ends with the "building" block filling the frame. */
export const Hook: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, my, W, H } = useLayout();
  const T = TEXT.hook;

  const s1 = pick(96, 88);
  const s2 = pick(156, 128);

  // Line 1 recedes when line 2 lands; the stack re-centres (camera settle).
  const recede = tw(f, 82, 18, 0, 1, IN_OUT);
  const shift = pick(170, 250) * (1 - recede);
  const line1Color = interpolateColors(
    recede,
    [0, 1],
    [COLORS.ink, COLORS.stone],
  );

  const hl = tw(f, 120, 14, 0, 1, OUT); // highlight wipe (beat 4)
  const grow = tw(f, 154, 26, 1, 34, IN); // block fills the frame by the cut
  const wordFade = tw(f, 154, 8, 1, 0);

  // Cursor travels in from off-frame to the highlight block (relative coords).
  const travel = tw(f, 120, 28, 0, 1, OUT);
  const press = tw(f, 147, 3) - tw(f, 150, 6); // click on beat 5
  const curOpacity = tw(f, 118, 4) * tw(f, 154, 6, 1, 0);

  const word = (w: string, i: number) => (
    <Rise key={w + i} p={tw(f, i * 7.5, 14)} inline>
      <span
        style={{ ...display(s1, { wdth: 100, wght: 760 }), color: line1Color }}
      >
        {w}
      </span>
    </Rise>
  );

  const big = (txt: string, start: number) => (
    <Rise p={tw(f, start, 16)} inline>
      <span style={{ ...display(s2), color: COLORS.ink }}>{txt}</span>
    </Rise>
  );

  return (
    <Fill color={COLORS.paper}>
      <div style={{ position: "absolute", left: mx, top: my }}>
        <Kicker
          text={T.kicker}
          size={pick(30, 30)}
          color={COLORS.ink}
          p={tw(f, 0, 18)}
        />
      </div>

      <div
        style={{
          position: "absolute",
          left: mx,
          right: mx,
          top: 0,
          bottom: 0,
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          gap: pick(44, 56),
          translate: `0 ${shift}px`,
          scale: `${tw(f, 0, 150, 1, 1.03, (t) => t)}`, // camera drift
          transformOrigin: "0% 50%",
        }}
      >
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            columnGap: s1 * 0.26,
            rowGap: s1 * 0.06,
          }}
        >
          {T.line1.map(word)}
        </div>

        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            columnGap: s2 * 0.28,
            rowGap: s2 * 0.02,
          }}
        >
          {V ? (
            <>
              {big(T.line2Before.split(" ")[0], 90)}
              {big(T.line2Before.split(" ").slice(1).join(" "), 97.5)}
            </>
          ) : (
            big(T.line2Before, 90)
          )}
          <span style={{ position: "relative", zIndex: 5 }}>
            {/* The box, first appearance: highlight block that becomes the next scene. */}
            <div
              style={{
                position: "absolute",
                left: -s2 * 0.12,
                right: -s2 * 0.12,
                top: s2 * 0.02,
                bottom: -s2 * 0.06,
                background: COLORS.accent,
                scale: `${hl * grow} ${grow}`,
                transformOrigin: grow > 1.001 ? "50% 50%" : "0% 50%",
              }}
            />
            <div style={{ position: "relative", opacity: wordFade }}>
              {big(T.line2Highlight, 105)}
            </div>
            <div
              style={{
                position: "absolute",
                left: "50%",
                top: "52%",
                translate: `${(1 - travel) * W * 0.45}px ${(1 - travel) * H * 0.4}px`,
              }}
            >
              <ClickRing
                x={0}
                y={0}
                t={tw(f, 150, 22)}
                r={pick(90, 80)}
                color={COLORS.ink}
              />
              <Cursor
                x={0}
                y={0}
                size={pick(72, 76)}
                press={press}
                opacity={curOpacity}
              />
            </div>
          </span>
          {big(T.line2After, 112.5)}
        </div>
      </div>
    </Fill>
  );
};
