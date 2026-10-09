import React from "react";
import { interpolateColors, useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN_OUT, OUT, tw } from "../lib/anim";
import { grid } from "../lib/geometry";
import { useLayout } from "../lib/layout";
import { display, Fill, Kicker, mono, Rise } from "../components/ui";

const WHIP = 150; // camera whips up to the awards on beat (14.5 s)
const VERDICT = 90; // "121 teams" turns into "1st place"

/** 0:12–0:17 · Proof he wins. */
export const Wins: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, my, H } = useLayout();
  const T = TEXT.wins;
  const g = grid(V);

  const whip = tw(f, WHIP, 20, 0, 1, IN_OUT);

  // Grid ripple: cells appear by distance from the winner, then all but one dim.
  const cells = [];
  for (let r = 0; r < g.n; r++) {
    for (let c = 0; c < g.n; c++) {
      const d = Math.hypot(r - 5, c - 5);
      const isWin = r === 5 && c === 5;
      const appear = isWin ? 1 : tw(f, 2 + d * 3.2, 10);
      const dim = isWin ? 0 : tw(f, 62 + d * 2.2, 10);
      const color = isWin
        ? COLORS.accent
        : interpolateColors(dim, [0, 1], [COLORS.stone, COLORS.graphite]);
      const rc = g.cellRect(r, c);
      const pulse = isWin
        ? 1 + 0.35 * tw(f, VERDICT - 6, 6) - 0.35 * tw(f, VERDICT, 14)
        : appear;
      cells.push(
        <div
          key={`${r}-${c}`}
          style={{
            position: "absolute",
            left: rc.x,
            top: rc.y,
            width: rc.w,
            height: rc.h,
            background: color,
            scale: `${pulse}`,
            opacity: isWin ? 1 : appear,
          }}
        />,
      );
    }
  }

  const verdict = tw(f, VERDICT, 16, 0, 1, OUT);
  const bigSize = pick(132, 118);
  const barMax = pick(540, 500);

  const score = (
    label: string,
    value: number,
    start: number,
    accent: boolean,
  ) => {
    const p = tw(f, start, 26, 0, 1, OUT);
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 20,
          opacity: tw(f, start, 6),
        }}
      >
        <div
          style={{
            ...mono(pick(30, 32), { wght: 600 }),
            color: COLORS.stone,
            width: pick(230, 240),
          }}
        >
          {label}
        </div>
        <div
          style={{
            width: barMax * (value / 100) * p,
            height: pick(34, 36),
            background: accent ? COLORS.accent : COLORS.stone,
          }}
        />
        <div
          style={{
            ...display(pick(44, 46), { wdth: 100, wght: 850 }),
            color: accent ? COLORS.accent : COLORS.stone,
          }}
        >
          {Math.round(value * p)}
        </div>
      </div>
    );
  };

  return (
    <Fill color={COLORS.ink}>
      {/* Part A: Open Loop */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          translate: `0 ${-whip * H}px`,
        }}
      >
        {cells}
        <div
          style={{
            position: "absolute",
            left: g.x0,
            top: g.y0 + g.size + pick(26, 30),
            display: "flex",
            alignItems: "center",
            gap: 14,
            opacity: tw(f, 40, 12),
          }}
        >
          <div
            style={{
              width: pick(22, 24),
              height: pick(22, 24),
              background: COLORS.stone,
            }}
          />
          <div
            style={{
              ...mono(pick(30, 32), { wght: 500 }),
              color: COLORS.stone,
            }}
          >
            {T.legend}
          </div>
        </div>
        <div style={{ position: "absolute", left: mx, top: my + pick(30, 10) }}>
          <Kicker text={T.kicker} size={30} p={tw(f, 2, 18)} />
          <div style={{ marginTop: pick(30, 28) }}>
            <Rise p={tw(f, 6, 18)}>
              <div
                style={{
                  ...display(pick(76, 80), { wdth: 110, wght: 900, lh: 1 }),
                  color: COLORS.paper,
                }}
              >
                {T.event}
              </div>
            </Rise>
            <Rise p={tw(f, 12, 18)}>
              <div
                style={{
                  ...mono(pick(30, 32), { wght: 500 }),
                  color: COLORS.stone,
                  marginTop: 10,
                }}
              >
                {T.eventPlace}
              </div>
            </Rise>
          </div>
        </div>

        <div
          style={{
            position: "absolute",
            left: mx,
            top: pick(420, g.y0 + g.size + 100),
          }}
        >
          {/* 121 teams → 1st place (rolling swap) */}
          <div
            style={{
              position: "relative",
              height: bigSize * 0.95,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                translate: `0 ${(1 - tw(f, 18, 18)) * 100 - verdict * 100}%`,
              }}
            >
              <div
                style={{
                  ...display(bigSize, { wdth: 112 }),
                  color: COLORS.paper,
                }}
              >
                {T.teams.toUpperCase()}
              </div>
            </div>
            <div
              style={{
                position: "absolute",
                top: 0,
                translate: `0 ${(1 - verdict) * 100}%`,
              }}
            >
              <div
                style={{
                  ...display(bigSize, { wdth: 112 }),
                  color: COLORS.accent,
                }}
              >
                {T.result}
              </div>
            </div>
          </div>
          <Rise p={tw(f, 30, 18)} style={{ marginTop: pick(18, 16) }}>
            <div
              style={{
                ...mono(pick(30, 28), { wght: 500 }),
                color: COLORS.paper,
                opacity: 0.85,
                whiteSpace: V ? "normal" : "nowrap",
              }}
            >
              {T.facts}
            </div>
          </Rise>

          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 14,
              marginTop: pick(44, 40),
            }}
          >
            {score(T.scoreUs.label, T.scoreUs.value, 96, true)}
            {score(T.scoreThem.label, T.scoreThem.value, 102, false)}
          </div>
          <div
            style={{
              display: "flex",
              gap: 28,
              alignItems: "baseline",
              marginTop: pick(34, 34),
            }}
          >
            <Rise p={tw(f, 108, 16)}>
              <div
                style={{
                  ...display(pick(48, 50), { wdth: 100, wght: 850 }),
                  color: COLORS.paper,
                }}
              >
                {T.prize}
              </div>
            </Rise>
            <Rise p={tw(f, 112, 16)}>
              <div
                style={{
                  ...mono(pick(30, 32), { wght: 600 }),
                  color: COLORS.accent,
                }}
              >
                {T.product}
              </div>
            </Rise>
          </div>
        </div>
      </div>

      {/* Part B: awards */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          translate: `0 ${(1 - whip) * H}px`,
          scale: `${tw(f, WHIP + 20, 130, 1, 1.03, (t) => t)}`, // drift while the list holds
          transformOrigin: `${pick(140, 88)}px 50%`,
        }}
      >
        <div style={{ position: "absolute", left: mx, top: my + pick(30, 10) }}>
          <Kicker text={T.kicker} size={30} />
        </div>
        <div
          style={{
            position: "absolute",
            left: mx,
            right: pick(140, 88),
            top: pick(262, 470),
            display: "flex",
            flexDirection: "column",
          }}
        >
          {T.awards.map((a, i) => {
            const st = WHIP + 10 + i * 7.5; // 16th notes
            return (
              <div
                key={a.name}
                style={{
                  display: "flex",
                  flexDirection: V ? "column" : "row",
                  alignItems: V ? "flex-start" : "center",
                  justifyContent: "space-between",
                  gap: pick(20, 16),
                  padding: `${pick(40, 44)}px 0`,
                  borderTop: `3px solid ${COLORS.graphite}`,
                  borderBottom:
                    i === T.awards.length - 1
                      ? `3px solid ${COLORS.graphite}`
                      : undefined,
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: pick(28, 24),
                  }}
                >
                  <div
                    style={{
                      width: pick(30, 30),
                      height: pick(30, 30),
                      background: COLORS.accent,
                      scale: `${tw(f, st, 10)}`,
                      flexShrink: 0,
                    }}
                  />
                  <Rise p={tw(f, st, 16)}>
                    <div
                      style={{
                        ...display(pick(60, 62), {
                          wdth: 104,
                          wght: 900,
                          lh: 1.02,
                        }),
                        color: COLORS.paper,
                        textTransform: "uppercase",
                        whiteSpace: V ? "normal" : "nowrap",
                      }}
                    >
                      {a.name}
                    </div>
                  </Rise>
                </div>
                <Rise p={tw(f, st + 4, 16)} style={{ marginLeft: V ? 54 : 0 }}>
                  <div
                    style={{
                      ...mono(pick(30, 32), { wght: 600 }),
                      color: COLORS.accent,
                    }}
                  >
                    {a.detail}
                  </div>
                </Rise>
              </div>
            );
          })}
        </div>
      </div>
    </Fill>
  );
};
