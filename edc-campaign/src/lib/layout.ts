import { useVideoConfig } from "remotion";

/** Landscape (1920×1080) vs vertical (1080×1920) layout switch. */
export const useLayout = () => {
  const { width, height } = useVideoConfig();
  const V = height > width;
  return {
    W: width,
    H: height,
    V,
    /** Pick a value for landscape or vertical. */
    pick: <T>(landscape: T, vertical: T): T => (V ? vertical : landscape),
    /** Safe margins. */
    mx: V ? 88 : 140,
    my: V ? 150 : 110,
  };
};
