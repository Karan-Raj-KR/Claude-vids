import React from "react";
import { useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN, IN_OUT, lerpRect, OUT, tw } from "../lib/anim";
import { tagRect } from "../lib/geometry";
import { useLayout } from "../lib/layout";
import { display, Fill, mono, Rise } from "../components/ui";

/** 0:03–0:07 · Name reveal. The full-frame box collapses into the founder tag. */
export const Name: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const T = TEXT.name;

  const tag = tagRect(V);
  const box = lerpRect(
    { x: 0, y: 0, w: W, h: H },
    tag,
    tw(f, 0, 24, 0, 1, IN_OUT),
  );

  const size = pick(306, 180);
  const top = pick(150, 600);
  const exit = tw(f, 222, 18, 0, 1, IN); // whip out on the cut
  const push = tw(f, 0, 240, 1, 1.035, IN_OUT); // slow camera push

  const detail = V ? T.detail.split(" · ") : [T.detail];

  return (
    <Fill color={COLORS.ink}>
      <div
        style={{
          position: "absolute",
          inset: 0,
          scale: `${push}`,
          transformOrigin: `${mx}px ${top + size}px`,
          translate: `${-exit * W * 0.3}px 0`,
          opacity: 1 - exit,
        }}
      >
        <div style={{ position: "absolute", left: mx - size * 0.04, top }}>
          <Rise p={tw(f, 10, 22)}>
            <div style={{ ...display(size, { lh: 0.9 }), color: COLORS.paper }}>
              {T.first}
            </div>
          </Rise>
          <Rise p={tw(f, 16, 22)}>
            <div style={{ ...display(size, { lh: 0.9 }), color: COLORS.paper }}>
              {T.last}
            </div>
          </Rise>
        </div>

        <div
          style={{
            position: "absolute",
            left: mx,
            top: tag.y + tag.h + pick(40, 44),
            display: "flex",
            flexDirection: "column",
            gap: 8,
          }}
        >
          {detail.map((d, i) => (
            <Rise key={d} p={tw(f, 34 + i * 4, 18)}>
              <div
                style={{
                  ...mono(pick(36, 34), { wght: 500 }),
                  color: COLORS.stone,
                }}
              >
                {d}
              </div>
            </Rise>
          ))}
        </div>
      </div>

      {/* The box: full frame → founder tag. */}
      <div
        style={{
          position: "absolute",
          left: box.x,
          top: box.y,
          width: box.w,
          height: box.h,
          background: COLORS.accent,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
        }}
      >
        <Rise p={tw(f, 18, 18, 0, 1, OUT)}>
          <div
            style={{
              ...display(pick(64, 58), { wdth: 100, wght: 800, track: -0.005 }),
              color: COLORS.ink,
            }}
          >
            {T.tag}
          </div>
        </Rise>
      </div>
    </Fill>
  );
};
