import React from "react";
import { useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN, IN_OUT, lerp, lerpRect, OUT, rand, tw } from "../lib/anim";
import { grid, tagRect, windowRect } from "../lib/geometry";
import { useLayout } from "../lib/layout";
import {
  ClickRing,
  Cursor,
  display,
  Fill,
  Kicker,
  mono,
  Rise,
  Tick,
} from "../components/ui";

// Local frames at which each product tab is clicked.
const CLICKS = [30, 90, 150, 210]; // on the beat
const COLLAPSE = 270; // window collapses into the winning square (beat)

const Bar: React.FC<{
  w: number | string;
  h?: number;
  c?: string;
  o?: number;
}> = ({ w, h = 14, c = COLORS.stone, o = 0.45 }) => (
  <div
    style={{ width: w, height: h, background: c, opacity: o, flexShrink: 0 }}
  />
);

/** School ERP: a data table assembling row by row. */
const Erp: React.FC<{ t: number; s: number }> = ({ t, s }) => {
  const rows = 6;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 14 * s }}>
      <div style={{ display: "flex", gap: 12 * s }}>
        {TEXT.builds.products[0].chips.map((c, i) => (
          <div
            key={c}
            style={{
              ...mono(26 * s, { wght: 700 }),
              color: i === 2 ? COLORS.ink : COLORS.accent,
              background: i === 2 ? COLORS.accent : "transparent",
              border: `3px solid ${COLORS.accent}`,
              padding: `${6 * s}px ${14 * s}px`,
              opacity: tw(t, 6 + i * 5, 8),
              translate: `0 ${tw(t, 6 + i * 5, 10, 16, 0)}px`,
            }}
          >
            {c}
          </div>
        ))}
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 10 * s,
          marginTop: 8 * s,
        }}
      >
        {Array.from({ length: rows }).map((_, r) => {
          const p = tw(t, 10 + r * 4, 12);
          return (
            <div
              key={r}
              style={{
                display: "flex",
                gap: 18 * s,
                alignItems: "center",
                padding: `${12 * s}px ${16 * s}px`,
                background: r === 0 ? "transparent" : COLORS.graphite,
                opacity: p,
                translate: `${(1 - p) * 40}px 0`,
              }}
            >
              <Bar
                w={40 * s}
                c={r === 0 ? COLORS.accent : COLORS.stone}
                o={r === 0 ? 1 : 0.6}
              />
              <Bar
                w={(160 + rand(r) * 90) * s}
                c={r === 0 ? COLORS.paper : COLORS.stone}
                o={r === 0 ? 0.7 : 0.45}
              />
              <Bar
                w={(110 + rand(r + 9) * 80) * s}
                c={r === 0 ? COLORS.paper : COLORS.stone}
                o={r === 0 ? 0.7 : 0.35}
              />
              <div style={{ flex: 1 }} />
              <Bar
                w={70 * s}
                c={r === 0 ? COLORS.paper : COLORS.accent}
                o={r === 0 ? 0.7 : 0.9}
              />
            </div>
          );
        })}
      </div>
    </div>
  );
};

/** ClinicDesk: appointment slots filling a week grid. */
const Clinic: React.FC<{ t: number; s: number }> = ({ t, s }) => {
  const cols = 5;
  const rows = 5;
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(${cols}, 1fr)`,
        gap: 10 * s,
      }}
    >
      {Array.from({ length: cols * rows }).map((_, i) => {
        const filled = rand(i * 3.1) > 0.42;
        const p = tw(t, 6 + rand(i) * 30, 10);
        const hot = rand(i * 7.7) > 0.72;
        return (
          <div
            key={i}
            style={{
              height: 62 * s,
              background: COLORS.graphite,
              position: "relative",
            }}
          >
            {filled ? (
              <div
                style={{
                  position: "absolute",
                  inset: 0,
                  background: hot ? COLORS.accent : COLORS.stone,
                  opacity: hot ? 1 : 0.55,
                  scale: `${p} 1`,
                  transformOrigin: "0 50%",
                }}
              />
            ) : null}
          </div>
        );
      })}
    </div>
  );
};

/** Eligent: opportunities checked for eligibility, then a form fills itself. */
const Eligent: React.FC<{ t: number; s: number }> = ({ t, s }) => (
  <div style={{ display: "flex", gap: 22 * s }}>
    <div
      style={{ flex: 1, display: "flex", flexDirection: "column", gap: 12 * s }}
    >
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          style={{
            background: COLORS.graphite,
            padding: 16 * s,
            display: "flex",
            alignItems: "center",
            gap: 14 * s,
            opacity: tw(t, 4 + i * 4, 8),
          }}
        >
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              gap: 10 * s,
              flex: 1,
            }}
          >
            <Bar w={`${70 - i * 12}%`} c={COLORS.paper} o={0.7} />
            <Bar w={`${45 + i * 8}%`} />
          </div>
          <div
            style={{
              width: 44 * s,
              height: 44 * s,
              border: `3px solid ${COLORS.stone}`,
            }}
          >
            <Tick size={38 * s} p={tw(t, 14 + i * 7, 8)} weight={8} />
          </div>
        </div>
      ))}
    </div>
    <div
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        gap: 14 * s,
        background: COLORS.graphite,
        padding: 18 * s,
      }}
    >
      {[0, 1, 2, 3].map((i) => (
        <div
          key={i}
          style={{ display: "flex", flexDirection: "column", gap: 8 * s }}
        >
          <Bar w={`${30 + rand(i) * 20}%`} h={10 * s} />
          <div
            style={{
              height: 30 * s,
              border: `2px solid ${COLORS.stone}`,
              padding: 6 * s,
            }}
          >
            <div
              style={{
                height: "100%",
                width: `${tw(t, 30 + i * 5, 10) * (60 + rand(i + 4) * 35)}%`,
                background: COLORS.accent,
              }}
            />
          </div>
        </div>
      ))}
    </div>
  </div>
);

/** FormPilot: a Chrome extension popup autofilling a long form. */
const FormPilot: React.FC<{ t: number; s: number }> = ({ t, s }) => (
  <div style={{ display: "flex", gap: 22 * s }}>
    <div
      style={{
        flex: 1.4,
        display: "flex",
        flexDirection: "column",
        gap: 14 * s,
      }}
    >
      {[0, 1, 2, 3, 4].map((i) => {
        const p = tw(t, 8 + i * 6, 9);
        return (
          <div
            key={i}
            style={{ display: "flex", flexDirection: "column", gap: 8 * s }}
          >
            <Bar w={`${25 + rand(i + 2) * 25}%`} h={10 * s} />
            <div
              style={{
                height: 34 * s,
                border: `2px solid ${p > 0.02 ? COLORS.accent : COLORS.stone}`,
                padding: 7 * s,
                display: "flex",
                alignItems: "center",
                gap: 4,
              }}
            >
              <div
                style={{
                  height: "100%",
                  width: `${p * (50 + rand(i + 11) * 45)}%`,
                  background: COLORS.paper,
                  opacity: 0.75,
                }}
              />
              {p > 0 && p < 1 ? (
                <div
                  style={{
                    width: 3,
                    height: "120%",
                    background: COLORS.accent,
                  }}
                />
              ) : null}
            </div>
          </div>
        );
      })}
    </div>
    <div
      style={{
        flex: 1,
        alignSelf: "flex-start",
        border: `3px solid ${COLORS.accent}`,
        padding: 18 * s,
        display: "flex",
        flexDirection: "column",
        gap: 14 * s,
        translate: `0 ${tw(t, 0, 12, 30, 0)}px`,
        opacity: tw(t, 0, 10),
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 10 * s }}>
        <div
          style={{ width: 22 * s, height: 22 * s, background: COLORS.accent }}
        />
        <div style={{ ...mono(24 * s, { wght: 700 }), color: COLORS.paper }}>
          FormPilot
        </div>
      </div>
      <Bar w="85%" />
      <Bar w="60%" />
      <div
        style={{
          height: 40 * s,
          background: COLORS.accent,
          scale: `${tw(t, 4, 14)} 1`,
          transformOrigin: "0 50%",
        }}
      />
    </div>
  </div>
);

export const VISUALS = [Erp, Clinic, Eligent, FormPilot];

/** 0:07–0:12 · Proof he builds. */
export const Builds: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W } = useLayout();
  const T = TEXT.builds;

  const win = windowRect(V);
  const morphIn = tw(f, 0, 26, 0, 1, IN_OUT);
  const morphOut = tw(f, COLLAPSE, 26, 0, 1, IN_OUT);
  const target = grid(V).winner;
  const r =
    morphOut > 0
      ? lerpRect(win, target, morphOut)
      : lerpRect(tagRect(V), win, morphIn);
  // The box stays vermilion; an ink panel wipes over it (mask) to make the
  // window, and wipes off again before the window collapses.
  const inkCover =
    tw(f, 14, 14, 0, 1, IN_OUT) * tw(f, COLLAPSE - 12, 12, 1, 0, IN_OUT);
  const contentOpacity = tw(f, 22, 8) * tw(f, COLLAPSE - 16, 6, 1, 0);

  // Which product is showing.
  let idx = 0;
  for (let i = 0; i < CLICKS.length; i++) if (f >= CLICKS[i]) idx = i;
  const local = f - CLICKS[idx];
  const swapIn = tw(local, 0, 9);
  const nextClick = CLICKS[idx + 1] ?? COLLAPSE;
  const swapOut = idx < 3 ? tw(f, nextClick - 7, 7) : 0;
  const blur = (1 - swapIn) * 14 + swapOut * 14;
  const product = T.products[idx];
  const Visual = VISUALS[idx];

  // Tabs.
  const pad = pick(28, 26);
  const tabH = pick(78, 80);
  const tabW = (win.w - pad * 2) / 4;
  const tabX = (i: number) => win.x + pad + tabW * i;
  const tabSlide = (() => {
    const prev = Math.max(0, idx - 1);
    const t = idx === 0 ? 1 : tw(local, 0, 10, 0, 1, OUT);
    return lerp(tabX(prev), tabX(idx), t);
  })();

  // Cursor.
  const tabCenter = (i: number) => ({
    x: tabX(i) + tabW * 0.62,
    y: win.y + pad + tabH * 0.8,
  });
  const cur = (() => {
    const start = { x: W + 80, y: win.y + win.h * 0.7 };
    let pos = start;
    for (let i = 0; i < CLICKS.length; i++) {
      const to = tabCenter(i);
      const t = tw(
        f,
        CLICKS[i] - (i === 0 ? 14 : 16),
        i === 0 ? 14 : 14,
        0,
        1,
        IN_OUT,
      );
      pos = { x: lerp(pos.x, to.x, t), y: lerp(pos.y, to.y, t) };
    }
    return pos;
  })();
  const press = CLICKS.reduce((a, c) => a + tw(f, c - 3, 3) - tw(f, c, 6), 0);
  const curOpacity = tw(f, 10, 6) * tw(f, COLLAPSE - 8, 8, 1, 0);

  const s = pick(1, 1.02);
  const exitL = tw(f, COLLAPSE - 6, 18, 1, 2, IN);
  const leftP = (start: number) =>
    f < COLLAPSE - 6 ? tw(f, start, 18) : exitL;

  // Stat count-up for the merged PRs.
  const prs = Math.round(tw(f, 74, 30, 0, 18, OUT));

  return (
    <Fill color={COLORS.paper}>
      {/* Left column / top block */}
      <div
        style={{
          position: "absolute",
          left: mx,
          top: pick(win.y, 270),
          width: pick(700, 904),
        }}
      >
        <Kicker text={T.kicker} size={30} p={leftP(16)} />
        <div style={{ marginTop: pick(34, 30) }}>
          {T.headline.map((h, i) => (
            <Rise key={h} p={leftP(22 + i * 6)}>
              <div
                style={{
                  ...display(pick(80, 96), { wdth: 104, wght: 900, lh: 1.0 }),
                  color: COLORS.ink,
                }}
              >
                {h}
              </div>
            </Rise>
          ))}
        </div>
      </div>

      <div
        style={{
          position: "absolute",
          left: mx,
          top: pick(win.y + win.h - 240, win.y + win.h + 60),
          display: "flex",
          flexDirection: "column",
          gap: pick(40, 28),
        }}
      >
        {T.stats.map((st, i) => (
          <div
            key={st.value}
            style={{ display: "flex", flexDirection: "column", gap: 6 }}
          >
            <Rise p={leftP(48 + i * 30)}>
              <div
                style={{
                  ...display(pick(58, 58), { wdth: 100, wght: 850, lh: 1.0 }),
                  color: COLORS.ink,
                }}
              >
                {i === 1 ? st.value.replace("18", String(prs)) : st.value}
              </div>
            </Rise>
            <Rise p={leftP(54 + i * 30)}>
              <div style={{ ...mono(30, { wght: 600 }), color: COLORS.accent }}>
                {st.label}
              </div>
            </Rise>
          </div>
        ))}
      </div>

      {/* The box → product window */}
      <div
        style={{
          position: "absolute",
          left: r.x,
          top: r.y,
          width: r.w,
          height: r.h,
          background: COLORS.accent,
          borderRadius: lerp(0, 18, morphIn) * (1 - morphOut),
          overflow: "hidden",
        }}
      >
        {/* tag text fades as the tag becomes the window */}
        {f < 10 ? (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              opacity: tw(f, 0, 8, 1, 0),
            }}
          >
            <div
              style={{
                ...display(pick(64, 58), {
                  wdth: 100,
                  wght: 800,
                  track: -0.005,
                }),
                color: COLORS.ink,
              }}
            >
              {TEXT.name.tag}
            </div>
          </div>
        ) : null}

        <div
          style={{
            position: "absolute",
            inset: 0,
            background: COLORS.ink,
            clipPath: `inset(0 0 ${(1 - inkCover) * 100}% 0)`,
          }}
        >
          <div
            style={{
              position: "absolute",
              left: 0,
              top: 0,
              width: win.w,
              height: win.h,
              opacity: contentOpacity,
            }}
          >
            {/* tab bar */}
            <div
              style={{
                position: "absolute",
                left: pad,
                top: pad,
                right: pad,
                height: tabH,
                borderBottom: `2px solid ${COLORS.graphite}`,
              }}
            />
            <div
              style={{
                position: "absolute",
                left: tabSlide - win.x,
                top: pad,
                width: tabW,
                height: tabH,
                background: COLORS.accent,
              }}
            />
            {T.products.map((p, i) => (
              <div
                key={p.tab}
                style={{
                  position: "absolute",
                  left: tabX(i) - win.x,
                  top: pad,
                  width: tabW,
                  height: tabH,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  ...mono(pick(25, 25), { wght: 700, track: 0.02 }),
                  color: i === idx ? COLORS.ink : COLORS.stone,
                }}
              >
                {p.tab}
              </div>
            ))}

            {/* product content */}
            <div
              style={{
                position: "absolute",
                left: pad + 12,
                right: pad + 12,
                top: pad + tabH + pick(40, 44),
                filter: blur > 0.1 ? `blur(${blur}px)` : undefined,
                opacity: swapIn * (1 - swapOut),
                display: "flex",
                flexDirection: "column",
                gap: pick(26, 30),
              }}
            >
              <div>
                <div
                  style={{
                    ...display(pick(70, 74), { wdth: 112, wght: 900, lh: 1 }),
                    color: COLORS.paper,
                  }}
                >
                  {product.title}
                </div>
                <div
                  style={{
                    ...display(pick(34, 36), {
                      wdth: 100,
                      wght: 500,
                      lh: 1.25,
                      track: 0,
                    }),
                    whiteSpace: "normal",
                    color: COLORS.stone,
                    marginTop: 12,
                  }}
                >
                  {product.line}
                </div>
              </div>
              <Visual t={local} s={s} />
            </div>
          </div>
        </div>
      </div>

      {CLICKS.map((c, i) => (
        <ClickRing
          key={c}
          x={tabCenter(i).x}
          y={tabCenter(i).y}
          t={tw(f, c, 20)}
          r={70}
          color={COLORS.paper}
        />
      ))}
      <Cursor
        x={cur.x}
        y={cur.y}
        size={pick(64, 70)}
        press={press}
        opacity={curOpacity}
        fill={COLORS.paper}
        stroke={COLORS.ink}
      />
    </Fill>
  );
};
