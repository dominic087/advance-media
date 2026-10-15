import { Composition } from "remotion";
import { AdvanceVideo } from "./Composition";
import { FamilyVideo } from "./FamilyVideo";
import { GarantiaVideo } from "./GarantiaVideo";
import { Cargo180Video, CARGO180_FRAMES } from "./Cargo180Video";

export const RemotionRoot: React.FC = () => {
  return (
    <>
    <Composition id="Cargo180Video" component={Cargo180Video} durationInFrames={CARGO180_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="GarantiaVideo" component={GarantiaVideo} durationInFrames={465} fps={30} width={1080} height={1920} />
    <Composition id="FamilyVideo" component={FamilyVideo} durationInFrames={555} fps={30} width={1080} height={1920} />
    <Composition
      id="AdvanceVideo"
      component={AdvanceVideo}
      durationInFrames={630}
      fps={30}
      width={1080}
      height={1920}
    />
    </>
  );
};
