import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";

const NAVY = "#011A5D", DEEP = "#000B2E", BURGUNDY = "#8A2C45", CREAM = "#F3E9D2", WA = "#25D366";
const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const n = (f: number, a: number, d: number, from: number, to: number, e: (t: number) => number = ease) =>
  interpolate(f, [a, a + d], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });

const Slide: React.FC<{ src: string; caption: string; dir: 1 | -1; pos: string }> = ({ src, caption, dir, pos }) => {
  const f = useCurrentFrame();
  const scale = 1.0 + n(f, 0, 130, 0, 0.06, Easing.linear);
  const tx = dir * n(f, 0, 130, -10, 10, Easing.linear);
  const fadeIn = n(f, 0, 12, 0, 1, Easing.linear);
  return (
    <AbsoluteFill style={{ opacity: fadeIn, backgroundColor: DEEP }}>
      <Img src={staticFile(src)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "contain", objectPosition: pos, scale: String(scale), translate: `${tx * 0.4}px 0px` }} />
      <AbsoluteFill style={{ background: "linear-gradient(to bottom, rgba(0,11,46,0.55) 0%, rgba(0,11,46,0) 14%, rgba(0,11,46,0) 70%, rgba(0,11,46,0.9) 100%)" }} />
      <div style={{ position: "absolute", left: 70, right: 70, bottom: 190, translate: `0px ${n(f, 10, 25, 50, 0)}px`, opacity: n(f, 10, 20, 0, 1, Easing.linear) }}>
        <div style={{ display: "inline-block", background: BURGUNDY, color: CREAM, fontFamily: FONT, fontWeight: 800, fontSize: 44, padding: "14px 32px", borderRadius: 40, letterSpacing: 1 }}>{caption}</div>
      </div>
    </AbsoluteFill>
  );
};

const Cta: React.FC = () => {
  const f = useCurrentFrame();
  const pulse = 1 + 0.03 * Math.sin(f / 5);
  return (
    <AbsoluteFill style={{ background: `linear-gradient(160deg, ${NAVY}, ${DEEP})`, alignItems: "center", justifyContent: "center", fontFamily: FONT, fontWeight: 900, opacity: n(f, 0, 12, 0, 1, Easing.linear) }}>
      <Img src={staticFile("logo-white.png")} style={{ width: 640, translate: `0px ${n(f, 0, 25, 40, 0)}px`, opacity: n(f, 0, 20, 0, 1, Easing.linear) }} />
      <div style={{ color: CREAM, fontSize: 150, lineHeight: 1, marginTop: 70, opacity: n(f, 8, 20, 0, 1, Easing.linear), translate: `0px ${n(f, 8, 25, 40, 0)}px` }}>FAMILY</div>
      <div style={{ color: CREAM, fontSize: 44, fontWeight: 600, marginTop: 20, opacity: n(f, 14, 20, 0, 1, Easing.linear) }}>Triciclo eléctrico</div>
      <div style={{ marginTop: 90, background: WA, color: DEEP, fontSize: 46, fontWeight: 800, padding: "30px 60px", borderRadius: 70, scale: String(pulse), opacity: n(f, 20, 15, 0, 1, Easing.linear) }}>ESCRÍBENOS POR WHATSAPP</div>
      <div style={{ color: CREAM, fontSize: 36, fontWeight: 600, marginTop: 60, opacity: n(f, 28, 15, 0, 1, Easing.linear) }}>facebook.com/advancemobilityvg</div>
      <div style={{ color: CREAM, fontSize: 34, fontWeight: 500, marginTop: 14, opacity: n(f, 32, 15, 0, 1, Easing.linear) }}>Guadalajara, Jalisco</div>
    </AbsoluteFill>
  );
};


const Specs: React.FC = () => {
  const f = useCurrentFrame();
  const items = [["600 W", "MOTOR"], ["35 km/h", "VELOCIDAD MÁXIMA"], ["40 km", "AUTONOMÍA"], ["1 AÑO", "GARANTÍA EN TODO LO ELÉCTRICO"]];
  return (
    <AbsoluteFill style={{ background: `linear-gradient(160deg, ${NAVY}, ${DEEP})`, fontFamily: FONT, fontWeight: 900, opacity: n(f, 0, 12, 0, 1, Easing.linear), alignItems: "center", justifyContent: "center" }}>
      <div style={{ color: CREAM, fontSize: 70, marginBottom: 60, opacity: n(f, 0, 15, 0, 1, Easing.linear) }}>FAMILY</div>
      {items.map(([b, l], i) => (
        <div key={i} style={{ width: 860, marginBottom: 34, padding: "28px 0", borderRadius: 28, background: i === 3 ? BURGUNDY : "rgba(243,233,210,0.1)", textAlign: "center", opacity: n(f, 6 + i * 8, 14, 0, 1, Easing.linear), translate: `0px ${n(f, 6 + i * 8, 22, 50, 0)}px` }}>
          <div style={{ color: CREAM, fontSize: 110, lineHeight: 1 }}>{b}</div>
          <div style={{ color: "#E8A9BA", fontSize: 34, fontWeight: 700, marginTop: 10 }}>{l}</div>
        </div>
      ))}
    </AbsoluteFill>
  );
};

export const FamilyVideo: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: DEEP }}>
      <Sequence from={0} durationInFrames={135}><Slide src="fam1.jpg" caption="TRICICLO FAMILY" dir={1} pos="50% 50%" /></Sequence>
      <Sequence from={120} durationInFrames={135}><Slide src="fam2.jpg" caption="Asiento para pasajeros" dir={-1} pos="50% 50%" /></Sequence>
      <Sequence from={240} durationInFrames={135}><Slide src="fam3.jpg" caption="Eléctrico y silencioso" dir={1} pos="50% 50%" /></Sequence>
      <Sequence from={0} durationInFrames={375}>
        <Img src={staticFile("logo-white.png")} style={{ position: "absolute", top: 70, left: 70, width: 300, opacity: n(f, 0, 15, 0, 1, Easing.linear) * (f < 360 ? 1 : 0) }} />
      </Sequence>
      <Sequence from={360} durationInFrames={105}><Specs /></Sequence>
      <Sequence from={450} durationInFrames={105}><Cta /></Sequence>
      <AbsoluteFill style={{ backgroundColor: DEEP, opacity: n(f, 541, 14, 0, 1, Easing.linear), pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
