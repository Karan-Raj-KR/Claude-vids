import React from "react";
import { useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN_OUT, OUT, rand, tw } from "../lib/anim";
import { useLayout } from "../lib/layout";
import { display, Fill, Kicker, mono, Rise } from "../components/ui";

const PAN = 120; // 19.0 s // camera drops from the events to the crowd

/** 0:17–0:21 · Proof he brings people together. */
export const People: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx, H } = useLayout();
  const T = TEXT.people;

  const pan = tw(f, PAN, 22, 0, 1, IN_OUT);

  // Crowd: 120 squares, filled in a shuffled order while the counter rolls.
  const cols = pick(12, 10);
  const rows = Math.ceil(T.crowdCount / cols);
  const cell = pick(40, 60);
  const gap = pick(12, 14);
  const fillStart = PAN + 8;
  const fillDur = 52; // count lands on 20.0 s
  const order = Array.from({ length: T.crowdCount }, (_, i) => i).sort(
    (a, b) => rand(a + 0.5) - rand(b + 0.5),
  );
  const rank = new Array(T.crowdCount);
  order.forEach((idx, k) => (rank[idx] = k));
  const count = Math.round(
    tw(f, fillStart, fillDur, 0, T.crowdCount, (t) => t),
  );
  const plus = tw(f, fillStart + fillDur, 10);

  return (
    <Fill color={COLORS.paper}>
      {/* Part A: events */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          translate: `0 ${-pan * H}px`,
          scale: `${tw(f, 0, PAN, 1, 1.025, (t) => t)}`,
          transformOrigin: `${pick(140, 88)}px 50%`,
        }}
      >
        <div
          style={{
            position: "absolute",
            left: mx,
            top: pick(226, 400),
            right: mx,
          }}
        >
          <Kicker text={T.kicker} size={30} p={tw(f, 0, 18)} />
          <div
            style={{
              marginTop: pick(30, 30),
              display: "flex",
              flexWrap: "wrap",
              columnGap: pick(112, 128) * 0.26,
            }}
          >
            {T.headline.split(" ").map((w, i) => (
              <Rise key={w + i} p={tw(f, 4 + i * 5, 16)} inline>
                <span
                  style={{
                    ...display(pick(112, 128), { wdth: 118 }),
                    color: COLORS.ink,
                  }}
                >
                  {w}
                </span>
              </Rise>
            ))}
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            left: mx,
            right: mx,
            top: pick(500, 830),
            display: "grid",
            gridTemplateColumns: pick("repeat(4, 1fr)", "repeat(2, 1fr)"),
            gap: pick(24, 24),
          }}
        >
          {T.events.map((e, i) => {
            const st = 15 + i * 15; // on 8th notes
            const p = tw(f, st, 14, 0, 1, OUT);
            return (
              <div
                key={e}
                style={{
                  height: pick(300, 320),
                  background: COLORS.ink,
                  padding: pick(30, 32),
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "space-between",
                  opacity: tw(f, st, 4),
                  translate: `0 ${(1 - p) * 60}px`,
                  scale: `${0.9 + 0.1 * p}`,
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                  <div
                    style={{ width: 22, height: 22, background: COLORS.accent }}
                  />
                  <div
                    style={{ ...mono(28, { wght: 700 }), color: COLORS.accent }}
                  >
                    {String(i + 1).padStart(2, "0")}
                  </div>
                </div>
                <div
                  style={{
                    ...display(pick(52, 56), {
                      wdth: 100,
                      wght: 850,
                      lh: 1.02,
                    }),
                    whiteSpace: "pre-line",
                    color: COLORS.paper,
                  }}
                >
                  {e}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Part B: the crowd */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          translate: `0 ${(1 - pan) * H}px`,
          scale: `${tw(f, PAN + 22, 240 - PAN - 22, 1, 1.03, (t) => t)}`,
          transformOrigin: "50% 50%",
        }}
      >
        <div
          style={{
            position: "absolute",
            left: mx,
            top: pick((1080 - (rows * cell + (rows - 1) * gap)) / 2 - 10, 250),
          }}
        >
          <div style={{ display: "flex", alignItems: "flex-start" }}>
            <div
              style={{
                ...display(pick(300, 280), { wdth: 112, lh: 0.86 }),
                color: COLORS.accent,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {count}
            </div>
            <div
              style={{
                ...display(pick(300, 280), { wdth: 112, lh: 0.86 }),
                color: COLORS.accent,
                opacity: plus,
                translate: `${(1 - plus) * -20}px 0`,
              }}
            >
              {T.crowdSuffix}
            </div>
          </div>
        </div>
        <div
          style={{
            position: "absolute",
            left: mx,
            bottom: pick(
              (1080 - (rows * cell + (rows - 1) * gap)) / 2 - 12,
              250,
            ),
            width: pick(900, 904),
          }}
        >
          <Rise p={tw(f, fillStart + 20, 18)}>
            <div
              style={{
                ...display(pick(58, 60), { wdth: 100, wght: 850, lh: 1.05 }),
                color: COLORS.ink,
              }}
            >
              {T.crowdLine1}
            </div>
          </Rise>
          <Rise p={tw(f, fillStart + 30, 18)}>
            <div
              style={{
                ...display(pick(44, 46), {
                  wdth: 100,
                  wght: 500,
                  lh: 1.2,
                  track: 0,
                }),
                color: COLORS.ink,
                whiteSpace: "normal",
                marginTop: 10,
              }}
            >
              {T.crowdLine2}
            </div>
          </Rise>
        </div>

        <div
          style={{
            position: "absolute",
            left: pick(
              1780 - (cols * cell + (cols - 1) * gap),
              (1080 - (cols * cell + (cols - 1) * gap)) / 2,
            ),
            top: pick((1080 - (rows * cell + (rows - 1) * gap)) / 2, 580),
            display: "grid",
            gridTemplateColumns: `repeat(${cols}, ${cell}px)`,
            gap,
          }}
        >
          {Array.from({ length: T.crowdCount }).map((_, i) => {
            const st = fillStart + (rank[i] / T.crowdCount) * fillDur;
            const p = tw(f, st, 8, 0, 1, OUT);
            return (
              <div
                key={i}
                style={{
                  width: cell,
                  height: cell,
                  background: rand(i * 4.3) > 0.86 ? COLORS.accent : COLORS.ink,
                  scale: `${p}`,
                }}
              />
            );
          })}
        </div>
      </div>
    </Fill>
  );
};
