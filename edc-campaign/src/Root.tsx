import React from "react";
import { Composition } from "remotion";
import timeline from "../timeline.json";
import { Film } from "./Film";
import { Reel } from "./v2/Reel";
import timelineV2 from "../timeline-v2.json";
import "./lib/fonts";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Film"
      component={Film}
      width={1920}
      height={1080}
      fps={timeline.fps}
      durationInFrames={timeline.durationInFrames}
      defaultProps={{ withAudio: true }}
    />
    <Composition
      id="FilmVertical"
      component={Film}
      width={1080}
      height={1920}
      fps={timeline.fps}
      durationInFrames={timeline.durationInFrames}
      defaultProps={{ withAudio: true }}
    />
    <Composition
      id="Reel"
      component={Reel}
      width={1920}
      height={1080}
      fps={timelineV2.fps}
      durationInFrames={timelineV2.durationInFrames}
      defaultProps={{ withAudio: true }}
    />
    <Composition
      id="ReelVertical"
      component={Reel}
      width={1080}
      height={1920}
      fps={timelineV2.fps}
      durationInFrames={timelineV2.durationInFrames}
      defaultProps={{ withAudio: true }}
    />
  </>
);
