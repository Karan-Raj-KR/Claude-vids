import React from "react";
import {
  AbsoluteFill,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Audio } from "@remotion/media";
import timeline from "../../timeline-v2.json";
import { COLORS } from "../config";
import { rand, tw } from "../lib/anim";
import * as S from "./shots";

const SHOTS: Record<string, React.FC> = {
  everyone: S.Everyone,
  startup: S.Startup,
  idea: S.Idea,
  whos: S.Whos,
  building: S.Building,
  karan: S.KaranShot,
  rajkr: S.RajKr,
  lockup: S.Lockup,
  products: S.Products,
  revenue: S.Revenue,
  erp: S.Erp,
  clinic: S.Clinic,
  eligent: S.Eligent,
  formpilot: S.FormPilot,
  prs: S.Prs,
  grid: S.Grid,
  first: S.First,
  score: S.Score,
  awards: S.Awards,
  events: S.Events,
  crowd: S.Crowd,
  promises: S.Promises,
  pledge1: S.Pledge1,
  pledge2: S.Pledge2,
  pledge3: S.Pledge3,
  vote: S.Vote,
  ballot: S.Ballot,
};

/** Every cut lands with a short directional smear; heavy hits add camera shake. */
const Cut: React.FC<{
  index: number;
  hit: string;
  children: React.ReactNode;
}> = ({ index, hit, children }) => {
  const f = useCurrentFrame();
  const dir = index % 2 ? 1 : -1;
  const heavy = hit === "impact" || hit === "drop";
  const amp = heavy ? 18 * (1 - tw(f, 0, 12, 0, 1, (t) => t)) : 0;
  const sx = amp * (rand(f * 1.7 + index) - 0.5) * 2;
  const sy = amp * (rand(f * 2.3 + index * 7) - 0.5) * 2;
  const smear = tw(f, 0, 5, 1, 0);
  return (
    <AbsoluteFill
      style={{
        translate: `${dir * 70 * smear * smear + sx}px ${sy}px`,
        filter: smear > 0.02 ? `blur(${smear * 10}px)` : undefined,
        scale: `${1 + (heavy ? 0.04 : 0.02) * smear}`,
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export const Reel: React.FC<{ withAudio?: boolean }> = ({
  withAudio = true,
}) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: COLORS.ink, overflow: "hidden" }}>
      {timeline.shots.map((s, i) => {
        const Shot = SHOTS[s.id];
        return (
          <Sequence
            key={s.id}
            name={s.id}
            from={s.from}
            durationInFrames={s.dur}
            premountFor={fps}
          >
            <Cut index={i} hit={s.hit}>
              <Shot />
            </Cut>
          </Sequence>
        );
      })}
      {withAudio ? <Audio src={staticFile("soundtrack-v2.wav")} /> : null}
    </AbsoluteFill>
  );
};
