import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";

const NAVY = "#011A5D", DEEP = "#000B2E", BURGUNDY = "#8A2C45", ROSE = "#E8A9BA", CREAM = "#F3E9D2", WA = "#25D366";
const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const n = (f: number, a: number, d: number, from: number, to: number, e: (t: number) => number = ease) =>
  interpolate(f, [a, a + d], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
const lin = Easing.linear;

const Bg: React.FC<{ children: React.ReactNode; fade?: boolean }> = ({ children, fade = true }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: `linear-gradient(160deg, ${NAVY} 0%, ${DEEP} 100%)`, fontFamily: FONT, fontWeight: 900, alignItems: "center", justifyContent: "center", opacity: fade ? n(f, 0, 10, 0, 1, lin) : 1 }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: 24, height: "100%", background: BURGUNDY }} />
      <Img src={staticFile("logo-white.png")} style={{ position: "absolute", top: 80, left: 80, width: 300 }} />
      {children}
    </AbsoluteFill>
  );
};

const Intro: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Bg>
      <div style={{ color: CREAM, fontSize: 150, lineHeight: 1, translate: `0px ${n(f, 0, 30, 70, 0)}px`, opacity: n(f, 0, 18, 0, 1, lin) }}>GARANTÍA</div>
      <div style={{ marginTop: 50, background: BURGUNDY, color: CREAM, fontSize: 56, padding: "20px 56px", borderRadius: 60, opacity: n(f, 14, 16, 0, 1, lin), translate: `0px ${n(f, 14, 26, 40, 0)}px` }}>EN TODO LO ELÉCTRICO</div>
      <div style={{ marginTop: 120, color: CREAM, fontSize: 300, lineHeight: 1, opacity: n(f, 30, 20, 0, 1, lin), scale: String(n(f, 30, 30, 0.8, 1)) }}>1 AÑO</div>
    </Bg>
  );
};

const Cards: React.FC = () => {
  const f = useCurrentFrame();
  const items = [
    ["REFACCIONES", "de todo tipo"],
    ["ASISTENCIA", "telefónica"],
    ["REPARACIÓN", "de tu unidad con nosotros"],
  ];
  return (
    <Bg>
      <div style={{ color: ROSE, fontSize: 52, marginBottom: 60, opacity: n(f, 0, 12, 0, 1, lin) }}>ADEMÁS TE ACOMPAÑAMOS CON</div>
      {items.map(([a, b], i) => (
        <div key={i} style={{ width: 880, marginBottom: 44, padding: "44px 40px", borderRadius: 32, background: i === 2 ? BURGUNDY : "rgba(243,233,210,0.1)", opacity: n(f, 12 + i * 22, 14, 0, 1, lin), translate: `${n(f, 12 + i * 22, 24, -120, 0)}px 0px` }}>
          <div style={{ color: CREAM, fontSize: 100, lineHeight: 1 }}>{a}</div>
          <div style={{ color: ROSE, fontSize: 48, fontWeight: 700, marginTop: 14 }}>{b}</div>
        </div>
      ))}
    </Bg>
  );
};

const Repair: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <Bg>
      <div style={{ color: ROSE, fontSize: 60, textAlign: "center", opacity: n(f, 0, 14, 0, 1, lin) }}>¿TU UNIDAD NECESITA</div>
      <div style={{ color: CREAM, fontSize: 118, textAlign: "center", lineHeight: 1, marginTop: 10, opacity: n(f, 6, 14, 0, 1, lin), translate: `0px ${n(f, 6, 26, 50, 0)}px` }}>REPARACIÓN?</div>
      <div style={{ marginTop: 100, color: CREAM, fontSize: 84, textAlign: "center", lineHeight: 1.1, opacity: n(f, 40, 16, 0, 1, lin), translate: `0px ${n(f, 40, 26, 50, 0)}px` }}>Tráela con<br />nosotros</div>
    </Bg>
  );
};

const Cta: React.FC = () => {
  const f = useCurrentFrame();
  const pulse = 1 + 0.03 * Math.sin(f / 5);
  return (
    <Bg>
      <Img src={staticFile("logo-white.png")} style={{ position: "absolute", top: 80, left: 80, width: 300, opacity: 0 }} />
      <div style={{ color: CREAM, fontSize: 130, lineHeight: 1, textAlign: "center", opacity: n(f, 0, 16, 0, 1, lin) }}>ESCRÍBENOS</div>
      <div style={{ marginTop: 70, background: WA, color: DEEP, fontSize: 52, padding: "34px 66px", borderRadius: 80, scale: String(pulse), opacity: n(f, 10, 14, 0, 1, lin) }}>POR WHATSAPP</div>
      <div style={{ color: CREAM, fontSize: 40, fontWeight: 600, marginTop: 80, opacity: n(f, 20, 14, 0, 1, lin) }}>facebook.com/advancemobilityvg</div>
      <div style={{ color: CREAM, fontSize: 36, fontWeight: 500, marginTop: 14, opacity: n(f, 26, 14, 0, 1, lin) }}>Guadalajara, Jalisco</div>
    </Bg>
  );
};

export const GarantiaVideo: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: DEEP }}>
      <Sequence from={0} durationInFrames={110}><Intro /></Sequence>
      <Sequence from={100} durationInFrames={150}><Cards /></Sequence>
      <Sequence from={240} durationInFrames={120}><Repair /></Sequence>
      <Sequence from={350} durationInFrames={115}><Cta /></Sequence>
      <AbsoluteFill style={{ backgroundColor: DEEP, opacity: n(f, 452, 12, 0, 1, lin), pointerEvents: "none" }} />
    </AbsoluteFill>
  );
};
