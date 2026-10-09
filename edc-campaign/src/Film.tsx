import React from "react";
import { AbsoluteFill, Sequence, staticFile, useVideoConfig } from "remotion";
import { Audio } from "@remotion/media";
import timeline from "../timeline.json";
import { COLORS } from "./config";
import { Hook } from "./scenes/Hook";
import { Name } from "./scenes/Name";
import { Builds } from "./scenes/Builds";
import { Wins } from "./scenes/Wins";
import { People } from "./scenes/People";
import { Pledges } from "./scenes/Pledges";
import { Vote } from "./scenes/Vote";

const S = timeline.scenes;

export const Film: React.FC<{ withAudio?: boolean }> = ({
  withAudio = true,
}) => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: COLORS.ink }}>
      <Sequence
        name="1 Hook"
        from={S.hook.from}
        durationInFrames={S.hook.duration}
        premountFor={fps}
      >
        <Hook />
      </Sequence>
      <Sequence
        name="2 Name"
        from={S.name.from}
        durationInFrames={S.name.duration}
        premountFor={fps}
      >
        <Name />
      </Sequence>
      <Sequence
        name="3 Builds"
        from={S.builds.from}
        durationInFrames={S.builds.duration}
        premountFor={fps}
      >
        <Builds />
      </Sequence>
      <Sequence
        name="4 Wins"
        from={S.wins.from}
        durationInFrames={S.wins.duration}
        premountFor={fps}
      >
        <Wins />
      </Sequence>
      <Sequence
        name="5 People"
        from={S.people.from}
        durationInFrames={S.people.duration}
        premountFor={fps}
      >
        <People />
      </Sequence>
      <Sequence
        name="6 Pledges"
        from={S.pledges.from}
        durationInFrames={S.pledges.duration}
        premountFor={fps}
      >
        <Pledges />
      </Sequence>
      <Sequence
        name="7 Vote"
        from={S.vote.from}
        durationInFrames={S.vote.duration}
        premountFor={fps}
      >
        <Vote />
      </Sequence>
      {withAudio ? <Audio src={staticFile("soundtrack.wav")} /> : null}
    </AbsoluteFill>
  );
};
