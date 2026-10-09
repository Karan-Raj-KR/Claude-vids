import React from "react";
import { Composition } from "remotion";
import timeline from "../timeline.json";
import { Film } from "./Film";
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
  </>
);
