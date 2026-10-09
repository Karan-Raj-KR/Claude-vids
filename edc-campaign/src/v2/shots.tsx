import React from "react";
import { interpolateColors, useCurrentFrame } from "remotion";
import { COLORS, TEXT } from "../config";
import { IN, OUT, rand, tw } from "../lib/anim";
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
import { VISUALS } from "../scenes/Builds";
import { BACK, Big, Karan, Label, pop, slam } from "./kit";

const C = COLORS;
const abs = (s: React.CSSProperties): React.CSSProperties => ({
  position: "absolute",
  ...s,
});

/* ------------------------------------------------------------- HOOK 0–3 s */

export const Everyone: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  return (
    <Fill color={C.paper}>
      <div style={abs({ left: mx, top: pick(120, 160) })}>
        <Label size={30} color={C.ink}>
          {TEXT.hook.kicker}
        </Label>
      </div>
      <div
        style={abs({
          left: mx,
          top: pick(330, 560),
          ...slam(f, 0, 9),
          transformOrigin: "0 50%",
        })}
      >
        {V ? (
          <>
            <Big size={232} color={C.ink}>
              EVERY
            </Big>
            <Big size={232} color={C.ink}>
              ONE
            </Big>
          </>
        ) : (
          <Big size={236} color={C.ink} wdth={112}>
            EVERYONE
          </Big>
        )}
      </div>
      <Karan
        pose="thinking"
        x={pick(W - 330, W / 2 + 180)}
        y={H + 6}
        h={pick(430, 560)}
        style={{ translate: pop(f, 8, 14, 460) }}
      />
    </Fill>
  );
};

export const Startup: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx } = useLayout();
  return (
    <Fill color={C.ink}>
      <div style={abs({ left: mx, top: pick(330, 700) })}>
        <Rise p={tw(f, 0, 8)}>
          <Big size={pick(120, 110)} color={C.stone}>
            has a
          </Big>
        </Rise>
        <div
          style={{ ...slam(f, 4, 9), transformOrigin: "0 50%", marginTop: 16 }}
        >
          <Big size={pick(260, 152)} color={C.paper} wdth={110}>
            startup
          </Big>
        </div>
      </div>
    </Fill>
  );
};

export const Idea: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx, W, H } = useLayout();
  return (
    <Fill color={C.accent}>
      <div
        style={abs({
          left: mx,
          top: pick(330, 380),
          ...slam(f, 0, 8, 1.6),
          transformOrigin: "0 50%",
        })}
      >
        <Big size={pick(320, 220)} color={C.ink} wdth={112}>
          idea.
        </Big>
      </div>
      <Karan
        pose="thinking"
        x={pick(W - 340, W / 2)}
        y={H + 10}
        h={pick(760, 900)}
        style={{
          translate: pop(f, 2, 14, 600),
          rotate: `${tw(f, 0, 30, -4, 2)}deg`,
          scale: `${tw(f, 0, 30, 1, 1.06)}`,
        }}
      />
    </Fill>
  );
};

export const Whos: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx, W, H } = useLayout();
  return (
    <Fill color={C.paper}>
      <div style={abs({ left: mx, top: pick(300, 300) })}>
        <Rise p={tw(f, 0, 10)}>
          <Big size={pick(190, 170)} color={C.ink}>
            Who’s
          </Big>
        </Rise>
        <Rise p={tw(f, 5, 10)}>
          <Big size={pick(190, 150)} color={C.ink} wdth={110}>
            actually
          </Big>
        </Rise>
      </div>
      {/* side view faces left: he walks into frame */}
      <Karan
        pose="side"
        x={pick(W - 300, W / 2 + 160)}
        y={pick(H - 70, H - 90)}
        h={pick(760, 900)}
        style={{
          translate: `${tw(f, 0, 22, W * 0.5, 0, OUT)}px ${Math.abs(Math.sin(f * 0.45)) * -14 * (1 - tw(f, 18, 8))}px`,
        }}
      />
    </Fill>
  );
};

export const Building: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const grow = tw(f, 30, 15, 1, 30, IN);
  return (
    <Fill color={C.ink}>
      <Karan
        pose="explaining"
        x={pick(W - 330, W / 2 + 120)}
        y={H + 6}
        h={pick(560, 700)}
        style={{ translate: pop(f, 4, 14, 500), opacity: tw(f, 30, 5, 1, 0) }}
      />
      <div
        style={abs({
          left: mx,
          top: pick(330, 520),
          display: "flex",
          alignItems: "baseline",
          flexWrap: "wrap",
          gap: 20,
        })}
      >
        <div
          style={{
            position: "relative",
            ...slam(f, 0, 9),
            transformOrigin: "0 50%",
          }}
        >
          <div
            style={abs({
              inset: "-2% -4% -10% -4%",
              background: C.accent,
              scale: `${tw(f, 2, 10, 0, 1, OUT) * grow} ${grow}`,
              transformOrigin: grow > 1.001 ? "50% 50%" : "0 50%",
              zIndex: 3,
            })}
          />
          <Big
            size={pick(230, 150)}
            color={C.ink}
            wdth={110}
            style={{
              position: "relative",
              zIndex: 4,
              opacity: tw(f, 30, 5, 1, 0),
            }}
          >
            building
          </Big>
        </div>
        <Big
          size={pick(230, 150)}
          color={C.paper}
          wdth={110}
          style={{ opacity: tw(f, 8, 4) * tw(f, 30, 5, 1, 0) }}
        >
          {V ? "?" : "one?"}
        </Big>
      </div>
    </Fill>
  );
};

/* ------------------------------------------------------------- NAME 3–6.5 s */

const NameBehind: React.FC<{
  word: string;
  bg: string;
  fg: string;
  pose: "front" | "three-quarter";
  fromSide?: boolean;
}> = ({ word, bg, fg, pose, fromSide }) => {
  const f = useCurrentFrame();
  const { pick, W, H } = useLayout();
  const drop = fromSide
    ? `${tw(f, 0, 16, W * 0.6, 0, BACK)}px 0`
    : `0 ${tw(f, 2, 18, -H, 0, BACK)}px`;
  return (
    <Fill color={bg}>
      <div
        style={abs({
          left: 0,
          right: 0,
          top: pick(70, 330),
          display: "flex",
          justifyContent: "center",
          ...slam(f, 0, 10, 1.25),
        })}
      >
        <Big
          size={pick(word.length > 5 ? 300 : 370, word.length > 5 ? 170 : 200)}
          color={fg}
        >
          {word}
        </Big>
      </div>
      <Karan
        pose={pose}
        x={W / 2}
        y={pick(H - 30, H - 120)}
        h={pick(720, 1180)}
        style={{ translate: drop, scale: `${tw(f, 0, 60, 1, 1.04)}` }}
      />
    </Fill>
  );
};

export const KaranShot: React.FC = () => (
  <NameBehind word={TEXT.name.first} bg={C.accent} fg={C.paper} pose="front" />
);
export const RajKr: React.FC = () => (
  <NameBehind
    word={TEXT.name.last}
    bg={C.ink}
    fg={C.paper}
    pose="three-quarter"
    fromSide
  />
);

export const Lockup: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const T = TEXT.name;
  return (
    <Fill color={C.paper}>
      <Karan
        pose="front"
        x={pick(W - 380, W / 2 + 200)}
        y={pick(H - 50, H - 60)}
        h={pick(860, 820)}
        style={{
          translate: `${tw(f, 0, 12, 120, 0, OUT)}px 0`,
          scale: `${tw(f, 0, 90, 1, 1.03)}`,
        }}
      />
      <div style={abs({ left: mx, top: pick(190, 230) })}>
        <Rise p={tw(f, 0, 10)}>
          <Big size={pick(196, 180)} color={C.ink}>
            {T.first}
          </Big>
        </Rise>
        <Rise p={tw(f, 4, 10)}>
          <Big size={pick(196, 180)} color={C.ink}>
            {T.last}
          </Big>
        </Rise>
        <div
          style={{
            marginTop: pick(36, 36),
            display: "inline-block",
            background: C.accent,
            padding: pick("16px 30px", "14px 26px"),
            clipPath: `inset(0 ${(1 - tw(f, 10, 12, 0, 1, OUT)) * 100}% 0 0)`,
          }}
        >
          <div
            style={{
              ...display(pick(64, 56), { wdth: 100, wght: 800 }),
              color: C.ink,
            }}
          >
            {T.tag}
          </div>
        </div>
        <div
          style={{
            marginTop: 26,
            display: "flex",
            flexDirection: "column",
            gap: 6,
          }}
        >
          {(V ? T.detail.split(" · ") : [T.detail]).map((d, i) => (
            <Rise key={d} p={tw(f, 18 + i * 4, 12)}>
              <div
                style={{
                  ...mono(pick(32, 30), { wght: 500 }),
                  color: C.ink,
                  opacity: 0.7,
                  whiteSpace: "normal",
                  maxWidth: pick(980, 560),
                }}
              >
                {d}
              </div>
            </Rise>
          ))}
        </div>
      </div>
    </Fill>
  );
};

/* ------------------------------------------------------------- BUILDS 6.5–11 s */

export const Products: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx, W, H } = useLayout();
  return (
    <Fill color={C.ink}>
      <div style={abs({ left: mx, top: pick(120, 170) })}>
        <Label size={30}>{TEXT.builds.kicker}</Label>
      </div>
      <div
        style={abs({
          left: mx,
          top: pick(330, 330),
          ...slam(f, 0, 9),
          transformOrigin: "0 50%",
        })}
      >
        <Big size={pick(170, 124)} color={C.paper} wdth={110}>
          Real
        </Big>
        <Big size={pick(170, 124)} color={C.paper} wdth={110}>
          products.
        </Big>
      </div>
      <Karan
        pose="three-quarter"
        x={pick(W - 330, W / 2 + 180)}
        y={pick(H - 40, H - 60)}
        h={pick(780, 900)}
        style={{ translate: pop(f, 3, 14, 700) }}
      />
    </Fill>
  );
};

export const Revenue: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx, W, H } = useLayout();
  const st = TEXT.builds.stats[0];
  return (
    <Fill color={C.accent}>
      <div
        style={abs({
          left: mx,
          top: pick(250, 330),
          ...slam(f, 0, 9),
          transformOrigin: "0 50%",
        })}
      >
        <Big size={pick(220, 150)} color={C.ink} wdth={108}>
          6-figure
        </Big>
        <Big size={pick(220, 150)} color={C.ink} wdth={108}>
          revenue
        </Big>
        <div
          style={{
            ...mono(pick(36, 34), { wght: 700 }),
            color: C.ink,
            marginTop: 24,
          }}
        >
          {st.label}
        </div>
      </div>
      <Karan
        pose="happy"
        x={pick(W - 290, W / 2 + 200)}
        y={H + 6}
        h={pick(560, 660)}
        style={{ translate: pop(f, 4, 14, 600) }}
      />
    </Fill>
  );
};

const ProductShot: React.FC<{ i: number; bg: string }> = ({ i, bg }) => {
  const f = useCurrentFrame();
  const { V, pick, mx } = useLayout();
  const P = TEXT.builds.products[i];
  const Visual = VISUALS[i];
  const win = V
    ? { x: 88, y: 800, w: 904, h: 760 }
    : { x: 940, y: 150, w: 840, h: 780 };
  const onAccent = bg === C.accent;
  return (
    <Fill color={bg}>
      <div style={abs({ left: mx, top: pick(150, 170) })}>
        <Label
          size={30}
          color={onAccent ? C.ink : C.accent}
        >{`${TEXT.builds.kicker} · ${i + 1}/4`}</Label>
      </div>
      <div
        style={abs({ left: mx, top: pick(330, 300), width: pick(740, 904) })}
      >
        <div style={{ ...slam(f, 0, 8), transformOrigin: "0 50%" }}>
          <div
            style={{
              ...display(pick(108, 132), { wdth: 104, lh: 0.95 }),
              color: C.ink,
            }}
          >
            {P.title}
          </div>
        </div>
        <Rise p={tw(f, 4, 10)}>
          <div
            style={{
              ...display(pick(46, 44), {
                wdth: 100,
                wght: 600,
                lh: 1.2,
                track: 0,
              }),
              whiteSpace: "normal",
              color: C.ink,
              marginTop: 20,
            }}
          >
            {P.line}
          </div>
        </Rise>
      </div>
      <div
        style={abs({
          left: win.x,
          top: win.y,
          width: win.w,
          height: win.h,
          background: C.ink,
          borderRadius: 18,
          overflow: "hidden",
          translate: `0 ${tw(f, 0, 12, 200, 0, BACK)}px`,
        })}
      >
        <div
          style={abs({
            left: 36,
            right: 36,
            top: 36,
            display: "flex",
            gap: 10,
          })}
        >
          {[0, 1, 2].map((k) => (
            <div
              key={k}
              style={{
                width: 16,
                height: 16,
                background: k === 0 ? C.accent : C.graphite,
              }}
            />
          ))}
        </div>
        <div style={abs({ left: 36, right: 36, top: 80 })}>
          <Visual t={f + 6} s={pick(1.05, 1.05)} />
        </div>
      </div>
      <ClickRing
        x={win.x + win.w * 0.7}
        y={win.y + 60}
        t={tw(f, 2, 18)}
        r={70}
        color={C.paper}
      />
      <Cursor
        x={win.x + win.w * 0.7}
        y={win.y + 60}
        size={64}
        press={tw(f, 0, 2) - tw(f, 2, 6)}
        fill={C.paper}
        stroke={C.ink}
      />
    </Fill>
  );
};
export const Erp: React.FC = () => <ProductShot i={0} bg={C.paper} />;
export const Clinic: React.FC = () => <ProductShot i={1} bg={C.accent} />;
export const Eligent: React.FC = () => <ProductShot i={2} bg={C.paper} />;
export const FormPilot: React.FC = () => <ProductShot i={3} bg={C.accent} />;

export const Prs: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx, W, H } = useLayout();
  const st = TEXT.builds.stats[1];
  const n = Math.round(tw(f, 0, 26, 0, 18, OUT));
  return (
    <Fill color={C.ink}>
      <div style={abs({ left: mx, top: pick(150, 300) })}>
        <div
          style={{
            ...display(pick(460, 380), { wdth: 112, lh: 0.86 }),
            color: C.accent,
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {n}
        </div>
        <Rise p={tw(f, 6, 12)}>
          <Big
            size={pick(120, 104)}
            color={C.paper}
            wdth={108}
            style={{ marginTop: 20 }}
          >
            merged PRs
          </Big>
        </Rise>
        <Rise p={tw(f, 12, 12)}>
          <div
            style={{
              ...mono(pick(38, 36), { wght: 700 }),
              color: C.accent,
              marginTop: 20,
            }}
          >
            {st.label} · open source
          </div>
        </Rise>
      </div>
      <Karan
        pose="explaining"
        x={pick(W - 330, W / 2 + 200)}
        y={H + 6}
        h={pick(560, 660)}
        style={{ translate: pop(f, 6, 14, 600) }}
      />
    </Fill>
  );
};

/* ------------------------------------------------------------- WINS 12–17.5 s */

export const Grid: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const T = TEXT.wins;
  const cell = pick(50, 66);
  const gap = pick(12, 12);
  const size = 11 * cell + 10 * gap;
  const x0 = pick(W - 140 - size, (W - size) / 2);
  const y0 = pick((H - size) / 2, 640);
  const fill = tw(f, 74, 16, 1, 60, IN); // winner cell fills the frame into the next shot
  const cells = [];
  for (let r = 0; r < 11; r++)
    for (let c = 0; c < 11; c++) {
      const win = r === 5 && c === 5;
      const d = Math.hypot(r - 5, c - 5);
      const appear = tw(f, d * 2.2, 8);
      const dim = win ? 0 : tw(f, 36 + d * 1.6, 8);
      cells.push(
        <div
          key={`${r}-${c}`}
          style={abs({
            left: x0 + c * (cell + gap),
            top: y0 + r * (cell + gap),
            width: cell,
            height: cell,
            background: win
              ? C.accent
              : interpolateColors(dim, [0, 1], [C.stone, C.graphite]),
            scale: `${win ? fill * (1 + 0.3 * tw(f, 50, 6) - 0.3 * tw(f, 56, 10)) : appear}`,
            zIndex: win ? 5 : 1,
          })}
        />,
      );
    }
  return (
    <Fill color={C.ink}>
      {cells}
      <div style={abs({ left: mx, top: pick(150, 170) })}>
        <Label size={30}>{TEXT.wins.kicker}</Label>
        <div
          style={{ ...slam(f, 0, 9), transformOrigin: "0 50%", marginTop: 26 }}
        >
          <Big size={pick(110, 104)} color={C.paper} wdth={108}>
            Open Loop
          </Big>
          <Big size={pick(110, 104)} color={C.paper} wdth={108}>
            2026
          </Big>
        </div>
        <div
          style={{
            ...mono(pick(30, 30), { wght: 500 }),
            color: C.stone,
            marginTop: 18,
          }}
        >
          {T.eventPlace}
        </div>
      </div>
      <div
        style={abs({ left: mx, top: pick(620, 1530), opacity: tw(f, 10, 6) })}
      >
        <div
          style={{
            ...display(pick(150, 140), { wdth: 112, lh: 0.9 }),
            color: C.paper,
          }}
        >
          {Math.round(tw(f, 10, 26, 0, 121, OUT))}
        </div>
        <div
          style={{
            ...mono(pick(34, 34), { wght: 700 }),
            color: C.accent,
            marginTop: 10,
          }}
        >
          teams · 1 square = 1 team
        </div>
      </div>
      {!V ? null : null}
    </Fill>
  );
};

export const First: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx, W, H } = useLayout();
  const T = TEXT.wins;
  return (
    <Fill color={C.accent}>
      <div
        style={abs({
          left: mx,
          top: pick(120, 200),
          ...slam(f, 0, 9, 1.7),
          transformOrigin: "0 30%",
        })}
      >
        <div
          style={{
            ...display(pick(560, 400), { wdth: 112, lh: 0.82 }),
            color: C.ink,
          }}
        >
          1ST
        </div>
        <Big size={pick(170, 150)} color={C.ink} style={{ marginTop: 10 }}>
          place
        </Big>
        <div
          style={{
            ...mono(pick(36, 34), { wght: 700 }),
            color: C.ink,
            marginTop: 26,
          }}
        >
          {T.event} · {T.product}
        </div>
      </div>
      <Karan
        pose="happy"
        x={pick(W - 340, W / 2 + 160)}
        y={H + 6}
        h={pick(640, 760)}
        style={{
          translate: pop(f, 4, 16, 700),
          rotate: `${Math.sin(f * 0.35) * 3 * tw(f, 10, 20)}deg`,
        }}
      />
    </Fill>
  );
};

export const Score: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx } = useLayout();
  const T = TEXT.wins;
  const bar = (label: string, v: number, start: number, accent: boolean) => {
    const p = tw(f, start, 20, 0, 1, OUT);
    return (
      <div style={{ marginTop: 26 }}>
        <div
          style={{
            ...mono(pick(32, 32), { wght: 700 }),
            color: accent ? C.accent : C.stone,
          }}
        >
          {label}
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 24,
            marginTop: 10,
          }}
        >
          <div
            style={{
              width: pick(1200, 700) * (v / 100) * p,
              height: pick(80, 70),
              background: accent ? C.accent : C.stone,
            }}
          />
          <div
            style={{
              ...display(pick(110, 96), { wdth: 108 }),
              color: accent ? C.accent : C.stone,
            }}
          >
            {Math.round(v * p)}
          </div>
        </div>
      </div>
    );
  };
  return (
    <Fill color={C.ink}>
      <div style={abs({ left: mx, top: pick(130, 360) })}>
        <Label size={30}>{`${T.event} · score / 100`}</Label>
        {bar(T.scoreUs.label, T.scoreUs.value, 0, true)}
        {bar(T.scoreThem.label, T.scoreThem.value, 4, false)}
        <div
          style={{
            display: "flex",
            flexWrap: "wrap",
            gap: 24,
            alignItems: "baseline",
            marginTop: 44,
            ...slam(f, 14, 9),
            transformOrigin: "0 50%",
          }}
        >
          <div
            style={{
              ...display(pick(96, 86), { wdth: 104, wght: 900 }),
              color: C.paper,
            }}
          >
            {T.prize}
          </div>
        </div>
        <Rise p={tw(f, 18, 12)} style={{ marginTop: 20 }}>
          <div
            style={{
              ...mono(pick(30, 28), { wght: 500 }),
              color: C.stone,
              whiteSpace: "normal",
              maxWidth: pick(1600, 904),
            }}
          >
            {T.facts}
          </div>
        </Rise>
      </div>
    </Fill>
  );
};

export const Awards: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx } = useLayout();
  const T = TEXT.wins;
  return (
    <Fill color={C.paper}>
      <div style={abs({ left: mx, top: pick(120, 200) })}>
        <Label size={30}>{T.kicker}</Label>
      </div>
      <div
        style={abs({
          left: mx,
          right: mx,
          top: pick(220, 420),
          scale: `${tw(f, 50, 70, 1, 1.03, (t) => t)}`,
          transformOrigin: "0 50%",
        })}
      >
        {T.awards.map((a, i) => {
          const st = i * 15;
          return (
            <div
              key={a.name}
              style={{
                display: "flex",
                flexDirection: V ? "column" : "row",
                justifyContent: "space-between",
                alignItems: V ? "flex-start" : "center",
                gap: 12,
                padding: `${pick(30, 34)}px 0`,
                borderTop: `4px solid ${C.ink}`,

                ...slam(f, st, 8, 1.15),
                transformOrigin: "0 50%",
              }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 26 }}>
                <div
                  style={{
                    width: 34,
                    height: 34,
                    background: C.accent,
                    flexShrink: 0,
                  }}
                />
                <div
                  style={{
                    ...display(pick(62, 66), { wdth: 102, lh: 1 }),
                    color: C.ink,
                    textTransform: "uppercase",
                    whiteSpace: V ? "normal" : "nowrap",
                  }}
                >
                  {a.name}
                </div>
              </div>
              <div
                style={{
                  ...mono(pick(32, 32), { wght: 700 }),
                  color: C.accent,
                  marginLeft: V ? 60 : 0,
                }}
              >
                {a.detail}
              </div>
            </div>
          );
        })}
      </div>
    </Fill>
  );
};

/* ------------------------------------------------------------- PEOPLE 17.5–21 s */

export const Events: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx } = useLayout();
  const T = TEXT.people;
  return (
    <Fill color={C.ink}>
      <div style={abs({ left: mx, top: pick(120, 200) })}>
        <Label size={30}>{T.kicker}</Label>
        <div
          style={{ ...slam(f, 0, 9), transformOrigin: "0 50%", marginTop: 24 }}
        >
          <Big
            size={pick(150, 124)}
            color={C.paper}
            wdth={110}
            style={{ whiteSpace: "normal" }}
          >
            {T.headline}
          </Big>
        </div>
      </div>
      <div
        style={abs({
          left: mx,
          right: mx,
          top: pick(500, 760),
          display: "grid",
          gridTemplateColumns: pick("repeat(4, 1fr)", "repeat(2, 1fr)"),
          gap: 22,
        })}
      >
        {T.events.map((e, i) => {
          const st = 6 + i * 15;
          return (
            <div
              key={e}
              style={{
                height: pick(330, 340),
                background: i % 2 ? C.paper : C.accent,
                padding: 30,
                display: "flex",
                flexDirection: "column",
                justifyContent: "space-between",
                opacity: tw(f, st, 3),
                translate: `0 ${tw(f, st, 12, 140, 0, BACK)}px`,
                rotate: `${tw(f, st, 12, (rand(i) - 0.5) * 16, 0, OUT)}deg`,
              }}
            >
              <div style={{ ...mono(30, { wght: 700 }), color: C.ink }}>
                {String(i + 1).padStart(2, "0")}
              </div>
              <div
                style={{
                  ...display(pick(54, 56), { wdth: 100, wght: 850, lh: 1.02 }),
                  whiteSpace: "pre-line",
                  color: C.ink,
                }}
              >
                {e}
              </div>
            </div>
          );
        })}
      </div>
    </Fill>
  );
};

export const Crowd: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const T = TEXT.people;
  const cols = pick(12, 10);
  const rows = Math.ceil(T.crowdCount / cols);
  const cell = pick(40, 56);
  const gap = pick(12, 12);
  const gw = cols * cell + (cols - 1) * gap;
  const gh = rows * cell + (rows - 1) * gap;
  const order = Array.from({ length: T.crowdCount }, (_, i) => i).sort(
    (a, b) => rand(a + 0.5) - rand(b + 0.5),
  );
  const rank: number[] = [];
  order.forEach((idx, k) => (rank[idx] = k));
  const FILL = 50;
  const count = Math.round(tw(f, 4, FILL, 0, T.crowdCount, (t) => t));
  const plus = tw(f, 4 + FILL, 8);
  return (
    <Fill color={C.paper}>
      <div
        style={abs({
          left: pick(W - 140 - gw, (W - gw) / 2),
          top: pick((H - gh) / 2, 560),
          display: "grid",
          gridTemplateColumns: `repeat(${cols}, ${cell}px)`,
          gap,
        })}
      >
        {Array.from({ length: T.crowdCount }).map((_, i) => {
          const st = 4 + (rank[i] / T.crowdCount) * FILL;
          return (
            <div
              key={i}
              style={{
                width: cell,
                height: cell,
                background: rand(i * 4.3) > 0.86 ? C.accent : C.ink,
                scale: `${tw(f, st, 8, 0, 1, BACK)}`,
              }}
            />
          );
        })}
      </div>
      <div style={abs({ left: mx, top: pick(250, 220) })}>
        <div style={{ display: "flex" }}>
          <div
            style={{
              ...display(pick(300, 260), { wdth: 112, lh: 0.86 }),
              color: C.accent,
              fontVariantNumeric: "tabular-nums",
            }}
          >
            {count}
          </div>
          <div
            style={{
              ...display(pick(300, 260), { wdth: 112, lh: 0.86 }),
              color: C.accent,
              opacity: plus,
              scale: `${tw(f, 4 + FILL, 10, 1.6, 1, OUT)}`,
            }}
          >
            {T.crowdSuffix}
          </div>
        </div>
      </div>
      <div
        style={abs({ left: mx, top: pick(600, 1480), width: pick(860, 904) })}
      >
        <Rise p={tw(f, 20, 12)}>
          <div
            style={{
              ...display(pick(64, 62), { wdth: 100, wght: 850 }),
              color: C.ink,
            }}
          >
            {T.crowdLine1}
          </div>
        </Rise>
        <Rise p={tw(f, 28, 12)}>
          <div
            style={{
              ...display(pick(46, 46), {
                wdth: 100,
                wght: 500,
                lh: 1.2,
                track: 0,
              }),
              color: C.ink,
              whiteSpace: "normal",
              marginTop: 10,
            }}
          >
            {T.crowdLine2}
          </div>
        </Rise>
      </div>
      {V ? null : (
        <Karan
          pose="explaining"
          x={mx + 250}
          y={H + 6}
          h={300}
          style={{ translate: pop(f, 40, 14, 320) }}
        />
      )}
    </Fill>
  );
};

/* ------------------------------------------------------------- PLEDGES 21–26.75 s */

export const Promises: React.FC = () => {
  const f = useCurrentFrame();
  const { pick, mx } = useLayout();
  return (
    <Fill color={C.accent}>
      <div
        style={abs({
          left: mx,
          top: pick(240, 560),
          ...slam(f, 0, 7, 1.8),
          transformOrigin: "0 50%",
        })}
      >
        <Big size={pick(250, 190)} color={C.ink}>
          My 3
        </Big>
        <Big size={pick(250, 150)} color={C.ink} wdth={112}>
          promises
        </Big>
        <div
          style={{
            ...mono(pick(40, 40), { wght: 700 }),
            color: C.ink,
            marginTop: 24,
          }}
        >
          for EDC
        </div>
      </div>
    </Fill>
  );
};

const Pledge: React.FC<{
  i: number;
  bg: string;
  fg: string;
  box: string;
  pose: "explaining" | "happy" | "front";
}> = ({ i, bg, fg, box, pose }) => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const it = TEXT.pledges.items[i];
  const full = pose === "front";
  return (
    <Fill color={bg}>
      <div
        style={abs({
          left: mx,
          top: pick(150, 200),
          width: pick(180, 180),
          height: pick(180, 180),
          background: box,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          ...slam(f, 0, 8, 2),
        })}
      >
        <div style={{ ...display(150, { wdth: 100, lh: 1 }), color: bg }}>
          {i + 1}
        </div>
      </div>
      <div
        style={abs({ left: mx, top: pick(400, 460), width: pick(1320, 904) })}
      >
        <div style={{ display: "flex", flexWrap: "wrap", columnGap: 36 }}>
          {it.title.split(" ").map((w, k) => (
            <Rise key={w + k} p={tw(f, 3 + k * 3, 9)} inline>
              <Big
                size={pick(136, 108)}
                color={fg}
                wdth={pick(110, 100)}
                style={{
                  letterSpacing: `${tw(f, 0, 105, -0.015, 0.012, (t) => t)}em`,
                }}
              >
                {w}
              </Big>
            </Rise>
          ))}
        </div>
        <Rise p={tw(f, 12, 12)} style={{ marginTop: 30 }}>
          <div
            style={{
              ...display(pick(56, 52), {
                wdth: 100,
                wght: 650,
                lh: 1.2,
                track: 0,
              }),
              color: fg,
              whiteSpace: "normal",
            }}
          >
            {it.line}
          </div>
        </Rise>
      </div>
      {/* progress rail */}
      <div
        style={abs({
          left: mx,
          right: mx,
          bottom: pick(70, 90),
          display: "flex",
          gap: 16,
        })}
      >
        {[0, 1, 2].map((k) => (
          <div
            key={k}
            style={{
              flex: 1,
              height: 10,
              background: fg,
              opacity: k <= i ? 1 : 0.2,
              scale: k === i ? `${tw(f, 0, 105, 0, 1, (t) => t)} 1` : "1 1",
              transformOrigin: "0 50%",
            }}
          />
        ))}
      </div>
      <Karan
        pose={pose}
        x={pick(W - 300, W / 2 + 220)}
        y={full ? pick(H - 110, H - 130) : pick(H - 100, H - 120)}
        h={full ? pick(640, 700) : pick(520, 560)}
        style={{ translate: pop(f, 6, 14, 500), opacity: V && i === 2 ? 1 : 1 }}
      />
    </Fill>
  );
};
export const Pledge1: React.FC = () => (
  <Pledge i={0} bg={C.ink} fg={C.paper} box={C.accent} pose="explaining" />
);
export const Pledge2: React.FC = () => (
  <Pledge i={1} bg={C.paper} fg={C.ink} box={C.accent} pose="happy" />
);
export const Pledge3: React.FC = () => (
  <Pledge i={2} bg={C.accent} fg={C.ink} box={C.ink} pose="front" />
);

/* ------------------------------------------------------------- VOTE 26.75–30 s */

export const Vote: React.FC = () => {
  const f = useCurrentFrame();
  const { pick } = useLayout();
  return (
    <Fill color={C.ink}>
      <div
        style={abs({
          inset: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          ...slam(f, 0, 8, 2.2),
        })}
      >
        <Big size={pick(400, 236)} color={C.accent} wdth={125}>
          {TEXT.vote.verb}
        </Big>
      </div>
    </Fill>
  );
};

export const Ballot: React.FC = () => {
  const f = useCurrentFrame();
  const { V, pick, mx, W, H } = useLayout();
  const T = TEXT.vote;
  const CLICK = 30; // 28.0 s
  const b = V ? { x: 88, y: 330, w: 170 } : { x: 140, y: 250, w: 190 };
  const target = { x: b.x + b.w * 0.55, y: b.y + b.w * 0.58 };
  const travel = tw(f, 4, 24, 0, 1, OUT);
  const ticked = f >= CLICK;
  return (
    <Fill color={C.paper}>
      <div
        style={abs({
          inset: 0,
          scale: `${tw(f, CLICK, 120, 1, 1.03, (t) => t)}`,
          transformOrigin: `${target.x}px ${target.y}px`,
        })}
      >
        <div
          style={abs({
            left: b.x,
            top: b.y,
            width: b.w,
            height: b.w,
            border: `${Math.round(b.w * 0.08)}px solid ${C.accent}`,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            ...slam(f, 0, 8, 1.6),
          })}
        >
          <Tick
            size={b.w * 0.74}
            p={tw(f, CLICK, 10, 0, 1, OUT)}
            weight={10}
            color={C.ink}
          />
        </div>
        <div
          style={abs({
            left: b.x + b.w + pick(44, 36),
            top: b.y + pick(4, -4),
          })}
        >
          {(V
            ? [TEXT.name.first, TEXT.name.last]
            : [TEXT.name.first, TEXT.name.last]
          ).map((l, i) => (
            <Rise key={l} p={tw(f, 2 + i * 4, 10)}>
              <Big size={pick(160, 124)} color={C.ink}>
                {l}
              </Big>
            </Rise>
          ))}
          <Rise p={tw(f, 10, 10)} style={{ marginTop: 22 }}>
            <div
              style={{
                ...display(pick(76, 64), { wdth: 100, wght: 750 }),
                color: C.ink,
              }}
            >
              {T.role}
            </div>
          </Rise>
          {T.date ? (
            <Rise p={tw(f, 14, 10)} style={{ marginTop: 14 }}>
              <div style={{ ...mono(36, { wght: 700 }), color: C.accent }}>
                {T.date}
              </div>
            </Rise>
          ) : null}
        </div>
        <div style={abs({ left: mx, bottom: pick(90, 130) })}>
          <Rise p={tw(f, 16, 12)}>
            <div
              style={{
                ...mono(pick(36, 36), { wght: 600, track: 0.02, upper: false }),
                color: C.ink,
              }}
            >
              {T.links}
            </div>
          </Rise>
        </div>
        {ticked ? (
          <Karan
            pose="happy"
            x={pick(W - 330, W / 2 + 160)}
            y={pick(H - 170, H - 230)}
            h={pick(560, 640)}
            style={{ scale: `${tw(f, CLICK, 12, 0.6, 1, BACK)}` }}
          />
        ) : (
          <Karan
            pose="front"
            x={pick(W - 330, W / 2 + 160)}
            y={pick(H - 170, H - 230)}
            h={pick(640, 700)}
            style={{ translate: pop(f, 0, 14, 400) }}
          />
        )}
        <ClickRing
          x={target.x}
          y={target.y}
          t={tw(f, CLICK, 22)}
          r={130}
          color={C.accent}
        />
        <Cursor
          x={target.x + (1 - travel) * W * 0.5}
          y={target.y + (1 - travel) * H * 0.4}
          size={72}
          press={tw(f, CLICK - 3, 3) - tw(f, CLICK, 8)}
          opacity={tw(f, 4, 4) * tw(f, CLICK + 24, 10, 1, 0)}
        />
      </div>
    </Fill>
  );
};
