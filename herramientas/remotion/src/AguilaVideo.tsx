import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";

const NAVY = "#011A5D", DEEP = "#000B2E", BURGUNDY = "#8A2C45", CREAM = "#F3E9D2", ROSE = "#E8A9BA", WA = "#25D366", ORANGE = "#F07A1A";
const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const n = (f: number, a: number, d: number, from: number, to: number, e: (t: number) => number = ease) =>
  interpolate(f, [a, a + d], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
const lin = Easing.linear;
const BG = `radial-gradient(ellipse at 50% 58%, #0a2f8a 0%, ${NAVY} 45%, ${DEEP} 100%)`;

// timeline (30 fps)
const T = { intro: [0, 110], speed: [110, 95], power: [205, 95], range: [300, 80], cta: [380, 120] } as const;
export const AGUILA_FRAMES = 500;

const BIKE_W = 1000, BIKE_H = Math.round((BIKE_W * 608) / 883);
const ROAD_Y = 1500;

// Bike position: enters fast from the right, rides in place, and leaves to the left before the CTA settles
const bikeX = (f: number) => {
  const enter = n(f, 0, 36, 1300, 0);
  const exit = n(f, 382, 22, 0, -1500, Easing.in(Easing.cubic));
  const back = n(f, 412, 40, 1300, 0);
  return f < 406 ? enter + exit : back;
};
// Speed in px/frame the background should scroll at
const speedAt = (f: number) => {
  const prev = bikeX(f - 1), cur = bikeX(f);
  return 34 + Math.max(0, (prev - cur) * 0.6);
};

// Road dashes and speed streaks that scroll to the right so the bike reads as moving left
const Road: React.FC = () => {
  const f = useCurrentFrame();
  let off = 0;
  for (let i = 0; i < f; i++) off += speedAt(i);
  const dashes = Array.from({ length: 9 }, (_, i) => ((i * 220 + off) % 1980) - 220);
  const streaks = [
    { y: 820, w: 420, s: 1.6, o: 0.35 }, { y: 930, w: 260, s: 2.2, o: 0.25 }, { y: 1040, w: 520, s: 1.3, o: 0.3 },
    { y: 1180, w: 300, s: 2.6, o: 0.2 }, { y: 1300, w: 460, s: 1.9, o: 0.3 }, { y: 1420, w: 240, s: 2.4, o: 0.22 },
    { y: 760, w: 200, s: 2.9, o: 0.18 }, { y: 1360, w: 600, s: 1.1, o: 0.18 },
  ];
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: 0, right: 0, top: ROAD_Y, height: 4, background: "rgba(243,233,210,0.25)" }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: ROAD_Y + 4, bottom: 0, background: "linear-gradient(to bottom, rgba(0,11,46,0.55), rgba(0,11,46,0.95))" }} />
      {dashes.map((x, i) => (
        <div key={i} style={{ position: "absolute", top: ROAD_Y + 60, left: x, width: 120, height: 10, borderRadius: 5, background: "rgba(243,233,210,0.35)" }} />
      ))}
      {streaks.map((s, i) => {
        const x = ((off * s.s + i * 397) % 2400) - 600;
        return <div key={i} style={{ position: "absolute", top: s.y, left: x, width: s.w, height: 5, borderRadius: 3, opacity: s.o, background: `linear-gradient(to right, rgba(255,255,255,0), ${CREAM})` }} />;
      })}
    </AbsoluteFill>
  );
};

const Bike: React.FC = () => {
  const f = useCurrentFrame();
  const x = bikeX(f);
  const bounce = Math.sin(f * 1.9) * 2 + Math.sin(f * 0.7) * 1.5;
  const tilt = (bikeX(f - 1) - x) * -0.012;
  const left = (1080 - BIKE_W) / 2 + x;
  const top = ROAD_Y - BIKE_H + 8 + bounce;
  const blur = Math.min(10, Math.abs(bikeX(f - 1) - x) * 0.12);
  const img = (dx: number, o: number, b: number) => (
    <Img src={staticFile("aguila_cut.png")} style={{ position: "absolute", left: left + dx, top, width: BIKE_W, opacity: o, filter: b ? `blur(${b}px)` : undefined, rotate: `${tilt}deg`, transformOrigin: "50% 100%" }} />
  );
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", left: left + 80, top: ROAD_Y - 18, width: BIKE_W - 160, height: 40, borderRadius: "50%", background: "rgba(0,0,0,0.55)", filter: "blur(14px)" }} />
      {img(70, 0.12, 6)}
      {img(36, 0.2, 3)}
      {img(0, 1, blur)}
    </AbsoluteFill>
  );
};

const Fade: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const f = useCurrentFrame();
  const o = Math.min(n(f, 0, 10, 0, 1, lin), n(f, dur - 10, 10, 1, 0, lin));
  return <AbsoluteFill style={{ opacity: o, fontFamily: FONT }}>{children}</AbsoluteFill>;
};

const Intro: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  return (
    <Fade dur={dur}>
      <div style={{ position: "absolute", top: 300, left: 70, right: 70 }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 42, letterSpacing: 6, opacity: n(f, 18, 12, 0, 1, lin) }}>BICIMOTO ELÉCTRICA</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 230, lineHeight: 1, letterSpacing: -6, marginTop: 24, opacity: n(f, 24, 12, 0, 1, lin), translate: `${n(f, 24, 26, -140, 0)}px 0px` }}>ÁGUILA</div>
        <div style={{ display: "inline-block", marginTop: 26, background: BURGUNDY, color: CREAM, fontWeight: 800, fontSize: 44, padding: "14px 34px", borderRadius: 40, opacity: n(f, 36, 12, 0, 1, lin), translate: `0px ${n(f, 36, 24, 30, 0)}px` }}>La más veloz de nuestra línea</div>
      </div>
    </Fade>
  );
};

const Speed: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const v = Math.round(n(f, 4, 40, 0, 45, Easing.out(Easing.cubic)));
  return (
    <Fade dur={dur}>
      <div style={{ position: "absolute", top: 260, left: 0, right: 0, textAlign: "center" }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 42, letterSpacing: 6 }}>VELOCIDAD MÁXIMA</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 300, lineHeight: 1, marginTop: 10, fontVariantNumeric: "tabular-nums" }}>
          {v}<span style={{ fontSize: 110, color: ORANGE }}> km/h</span>
        </div>
      </div>
    </Fade>
  );
};

const Card: React.FC<{ f: number; d: number; big: string; label: string; color?: string }> = ({ f, d, big, label, color }) => (
  <div style={{ flex: 1, padding: "40px 10px", borderRadius: 30, textAlign: "center", background: color ?? "rgba(243,233,210,0.1)", border: "2px solid rgba(243,233,210,0.25)", opacity: n(f, d, 12, 0, 1, lin), translate: `0px ${n(f, d, 22, 50, 0)}px` }}>
    <div style={{ color: CREAM, fontWeight: 900, fontSize: 104, lineHeight: 1 }}>{big}</div>
    <div style={{ color: ROSE, fontWeight: 700, fontSize: 30, marginTop: 14, letterSpacing: 1 }}>{label}</div>
  </div>
);

const Power: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  return (
    <Fade dur={dur}>
      <div style={{ position: "absolute", top: 260, left: 70, right: 70 }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 42, letterSpacing: 6, textAlign: "center" }}>POTENCIA</div>
        <div style={{ display: "flex", gap: 30, marginTop: 40 }}>
          <Card f={f} d={4} big="950 W" label="MOTOR" color={BURGUNDY} />
          <Card f={f} d={12} big="60 V" label="BATERÍA" />
        </div>
      </div>
    </Fade>
  );
};

const Range: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  return (
    <Fade dur={dur}>
      <div style={{ position: "absolute", top: 260, left: 0, right: 0, textAlign: "center" }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 42, letterSpacing: 6 }}>AUTONOMÍA</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 260, lineHeight: 1, marginTop: 10, scale: String(n(f, 2, 24, 1.25, 1)) }}>50 km</div>
        <div style={{ color: CREAM, fontWeight: 700, fontSize: 44, marginTop: 20, opacity: n(f, 14, 12, 0, 1, lin) }}>con una sola carga</div>
      </div>
    </Fade>
  );
};

const Cta: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const pulse = 1 + 0.035 * Math.sin(f / 5);
  return (
    <AbsoluteFill style={{ fontFamily: FONT, opacity: n(f, 0, 12, 0, 1, lin) }}>
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 230 }}>
        <Img src={staticFile("logo-white.png")} style={{ width: 560, opacity: n(f, 0, 16, 0, 1, lin), translate: `0px ${n(f, 0, 24, 40, 0)}px` }} />
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 150, lineHeight: 1, marginTop: 50, opacity: n(f, 8, 14, 0, 1, lin) }}>ÁGUILA</div>
        <div style={{ color: CREAM, fontWeight: 700, fontSize: 40, marginTop: 18, opacity: n(f, 14, 14, 0, 1, lin) }}>1 año de garantía en todo lo eléctrico</div>
      </AbsoluteFill>
      <AbsoluteFill style={{ alignItems: "center", top: ROAD_Y + 110 }}>
        <div style={{ background: WA, color: DEEP, fontSize: 46, fontWeight: 900, padding: "30px 60px", borderRadius: 70, scale: String(pulse), opacity: n(f, 40, 12, 0, 1, lin) }}>ESCRÍBENOS POR WHATSAPP</div>
        <div style={{ color: CREAM, fontSize: 34, fontWeight: 600, marginTop: 34, opacity: n(f, 46, 12, 0, 1, lin) }}>Guadalajara, Jalisco</div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const AguilaVideo: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: BG, overflow: "hidden" }}>
      <Road />
      <Bike />
      <Sequence from={T.intro[0]} durationInFrames={T.intro[1]}><Intro dur={T.intro[1]} /></Sequence>
      <Sequence from={T.speed[0]} durationInFrames={T.speed[1]}><Speed dur={T.speed[1]} /></Sequence>
      <Sequence from={T.power[0]} durationInFrames={T.power[1]}><Power dur={T.power[1]} /></Sequence>
      <Sequence from={T.range[0]} durationInFrames={T.range[1]}><Range dur={T.range[1]} /></Sequence>
      <Sequence from={T.cta[0] + 20} durationInFrames={T.cta[1] - 20}><Cta dur={T.cta[1] - 20} /></Sequence>
      {f < 395 ? <Img src={staticFile("logo-white.png")} style={{ position: "absolute", top: 80, right: 60, width: 250, opacity: 0.95, fontFamily: FONT }} /> : null}
    </AbsoluteFill>
  );
};
