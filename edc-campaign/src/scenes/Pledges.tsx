import React from "react";
import { useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN, IN_OUT, lerpRect, OUT, tw } from "../lib/anim";
import { ballotBox, pledgeBox } from "../lib/geometry";
import { useLayout } from "../lib/layout";
import { display, Fill, Kicker, mono, Rise } from "../components/ui";

const EACH = 120; // one pledge every 2 s, on the beat
const OUTRO = 330; // number box travels to the ballot box

/** 0:21–0:27 · Three pledges as kinetic type. */
export const Pledges: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, my } = useLayout();
  const T = TEXT.pledges;

  const box = lerpRect(
    pledgeBox(V),
    ballotBox(V),
    tw(f, OUTRO, 24, 0, 1, IN_OUT),
  );
  const digitRoll =
    tw(f, EACH - 4, 14, 0, 1, OUT) + tw(f, EACH * 2 - 4, 14, 0, 1, OUT);
  const titleSize = pick(140, 104);

  return (
    <Fill color={COLORS.ink}>
      <div style={{ position: "absolute", left: mx, top: my + pick(30, 10) }}>
        <Kicker
          text={T.kicker}
          size={pick(32, 32)}
          p={tw(f, 0, 18) * tw(f, OUTRO - 4, 14, 1, 0)}
        />
      </div>

      {T.items.map((it, i) => {
        const s = i * EACH;
        const enter = (d: number) => tw(f, s + d, 16, 0, 1, OUT);
        const leaving =
          i < 2
            ? tw(f, s + EACH - 10, 10, 0, 1, IN) // gone exactly on the next beat
            : tw(f, OUTRO - 4, 14, 0, 1, IN);
        if (f < s - 2 || leaving >= 1) return null;
        const words = it.title.split(" ");
        return (
          <div
            key={it.title}
            style={{
              position: "absolute",
              left: mx,
              right: mx,
              top: pick(530, 800),
            }}
          >
            <div
              style={{
                display: "flex",
                flexWrap: "wrap",
                columnGap: titleSize * 0.3,
                rowGap: titleSize * 0.04,
              }}
            >
              {words.map((w, k) => (
                <Rise
                  key={w + k}
                  p={leaving > 0 ? 1 + leaving : enter(k * 4)}
                  inline
                >
                  <span
                    style={{
                      ...display(titleSize, {
                        wdth: pick(118, 100),
                        // tracking slowly opens while the pledge holds
                        track: tw(f, s, EACH, -0.012, 0.014, (t) => t),
                      }),
                      color: COLORS.paper,
                    }}
                  >
                    {w}
                  </span>
                </Rise>
              ))}
            </div>
            <Rise
              p={leaving > 0 ? 1 + leaving : enter(10)}
              style={{ marginTop: pick(36, 44) }}
            >
              <div
                style={{
                  ...display(pick(54, 54), {
                    wdth: 100,
                    wght: 600,
                    lh: 1.2,
                    track: 0,
                  }),
                  whiteSpace: "normal",
                  color: COLORS.paper,
                  opacity: 0.88,
                  maxWidth: pick(1500, 904),
                }}
              >
                {it.line}
              </div>
            </Rise>
          </div>
        );
      })}

      {/* Progress rail: recaps all three promises as they land. */}
      <div
        style={{
          position: "absolute",
          left: mx,
          right: mx,
          top: pick(890, 1440),
          display: "flex",
          flexDirection: V ? "column" : "row",
          gap: pick(24, 26),
          opacity: tw(f, 6, 14) * tw(f, OUTRO - 4, 12, 1, 0),
        }}
      >
        {T.items.map((it, i) => {
          const s = i * EACH;
          const fill = tw(f, s, EACH, 0, 1, (t) => t);
          const active = f >= s && f < s + EACH;
          const done = f >= s + EACH;
          return (
            <div
              key={it.title}
              style={{
                flex: 1,
                display: "flex",
                flexDirection: V ? "row" : "column",
                alignItems: V ? "center" : "stretch",
                gap: pick(16, 22),
              }}
            >
              <div
                style={{
                  height: pick(8, 10),
                  width: V ? 150 : "auto",
                  background: COLORS.graphite,
                  flexShrink: 0,
                }}
              >
                <div
                  style={{
                    height: "100%",
                    width: `${fill * 100}%`,
                    background: COLORS.accent,
                  }}
                />
              </div>
              <div
                style={{
                  ...mono(pick(30, 32), { wght: 600 }),
                  color: active
                    ? COLORS.paper
                    : done
                      ? COLORS.paper
                      : COLORS.stone,
                  opacity: active ? 1 : done ? 0.6 : 0.8,
                }}
              >
                {String(i + 1).padStart(2, "0")} {it.title}
              </div>
            </div>
          );
        })}
      </div>

      {/* The box holds the pledge number; it rolls 1 → 2 → 3. */}
      <div
        style={{
          position: "absolute",
          left: box.x,
          top: box.y,
          width: box.w,
          height: box.h,
          background: COLORS.accent,
          overflow: "hidden",
          scale: `${tw(f, 0, 14, 0, 1, OUT)}`,
        }}
      >
        <div
          style={{
            translate: `0 ${-digitRoll * box.h}px`,
            opacity: tw(f, OUTRO, 10, 1, 0),
          }}
        >
          {[1, 2, 3].map((n) => (
            <div
              key={n}
              style={{
                height: box.h,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                ...display(box.h * 0.82, { wdth: 100, wght: 900, lh: 1 }),
                color: COLORS.ink,
              }}
            >
              {n}
            </div>
          ))}
        </div>
      </div>
    </Fill>
  );
};
