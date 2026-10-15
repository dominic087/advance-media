import { AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";

const NAVY = "#011A5D", DEEP = "#000B2E", BURGUNDY = "#8A2C45", CREAM = "#F3E9D2", ROSE = "#E8A9BA", WA = "#25D366", AMBER = "#F5A623";
const FONT = "Inter, 'Helvetica Neue', Arial, sans-serif";
const ease = Easing.bezier(0.16, 1, 0.3, 1);
const n = (f: number, a: number, d: number, from: number, to: number, e: (t: number) => number = ease) =>
  interpolate(f, [a, a + d], [from, to], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: e });
const lin = Easing.linear;
const BG = `radial-gradient(ellipse at 50% 35%, #0a2f8a 0%, ${NAVY} 45%, ${DEEP} 100%)`;

// Fades a scene in and out over its own duration
const Scene: React.FC<{ dur: number; children: React.ReactNode; bg?: string }> = ({ dur, children, bg }) => {
  const f = useCurrentFrame();
  const o = Math.min(n(f, 0, 12, 0, 1, lin), n(f, dur - 12, 12, 1, 0, lin));
  return <AbsoluteFill style={{ opacity: o, background: bg ?? DEEP, fontFamily: FONT, overflow: "hidden" }}>{children}</AbsoluteFill>;
};

const Bolt: React.FC<{ size: number; color: string }> = ({ size, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24"><path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z" fill={color} /></svg>
);
const Fuel: React.FC<{ size: number; color: string }> = ({ size, color }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color} strokeWidth={2} strokeLinejoin="round" strokeLinecap="round">
    <rect x="3" y="3" width="11" height="18" rx="2" /><path d="M3 21h11" /><rect x="5.5" y="6" width="6" height="4" rx="0.5" fill={color} />
    <path d="M14 9h2a2 2 0 0 1 2 2v6a1.5 1.5 0 0 0 3 0V8l-3-3" />
  </svg>
);

// 1. Intro
const Intro: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const tx = n(f, 0, dur, 0, -820, lin);
  const sc = 1 + n(f, 0, dur, 0, 0.04, lin);
  return (
    <Scene dur={dur}>
      <Img src={staticFile("c180_hero.jpg")} style={{ position: "absolute", left: 0, top: 560, height: 1360, translate: `${tx}px 0px`, scale: String(sc), transformOrigin: "left bottom" }} />
      <AbsoluteFill style={{ background: `linear-gradient(to bottom, ${DEEP} 0%, ${DEEP} 30%, rgba(0,11,46,0.0) 48%, rgba(0,11,46,0) 82%, rgba(0,11,46,0.75) 100%)` }} />
      <Img src={staticFile("logo-white.png")} style={{ position: "absolute", top: 80, left: 70, width: 300, opacity: n(f, 0, 15, 0, 1, lin) }} />
      <div style={{ position: "absolute", top: 210, left: 70, right: 70 }}>
        <div style={{ display: "inline-block", background: AMBER, color: DEEP, fontWeight: 900, fontSize: 38, padding: "10px 28px", borderRadius: 30, letterSpacing: 2, opacity: n(f, 6, 12, 0, 1, lin), translate: `${n(f, 6, 20, -60, 0)}px 0px` }}>¡NUEVO!</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 190, lineHeight: 1, marginTop: 18, letterSpacing: -4, opacity: n(f, 10, 14, 0, 1, lin), translate: `0px ${n(f, 10, 24, 60, 0)}px` }}>CARGO 180</div>
        <div style={{ color: CREAM, fontWeight: 800, fontSize: 50, marginTop: 14, opacity: n(f, 20, 14, 0, 1, lin), translate: `0px ${n(f, 20, 24, 40, 0)}px` }}>Híbrida: gasolina + eléctrica</div>
      </div>
    </Scene>
  );
};

// 2. Hybrid explainer
const Hybrid: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const card = (i: number, icon: React.ReactNode, title: string, sub: string, color: string) => (
    <div style={{ display: "flex", alignItems: "center", gap: 34, width: 900, padding: "34px 40px", borderRadius: 34, background: "rgba(255,255,255,0.08)", border: `3px solid ${color}`,
      opacity: n(f, 14 + i * 16, 14, 0, 1, lin), translate: `${n(f, 14 + i * 16, 26, i ? 120 : -120, 0)}px 0px` }}>
      <div style={{ width: 130, height: 130, borderRadius: 65, background: color, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>{icon}</div>
      <div><div style={{ color: "white", fontWeight: 900, fontSize: 56, lineHeight: 1.05 }}>{title}</div><div style={{ color: CREAM, fontWeight: 600, fontSize: 36, marginTop: 8 }}>{sub}</div></div>
    </div>
  );
  const arrowO = n(f, 40, 14, 0, 1, lin);
  return (
    <Scene dur={dur} bg={BG}>
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 150 }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 40, letterSpacing: 6, opacity: n(f, 0, 14, 0, 1, lin) }}>LA VENTAJA</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 150, lineHeight: 1, marginTop: 10, opacity: n(f, 4, 14, 0, 1, lin), scale: String(n(f, 4, 24, 1.2, 1)) }}>HÍBRIDA</div>
        <div style={{ height: 60 }} />
        {card(0, <Bolt size={80} color={DEEP} />, "Motor eléctrico", "1800 W · batería 60V-45Ah", WA)}
        <div style={{ color: AMBER, fontSize: 70, fontWeight: 900, margin: "14px 0", opacity: arrowO, translate: `0px ${Math.sin(f / 6) * 6}px` }}>⇅</div>
        {card(1, <Fuel size={80} color={DEEP} />, "Generador a gasolina", "Recarga la batería en el camino", AMBER)}
        <div style={{ marginTop: 60, color: CREAM, fontWeight: 800, fontSize: 52, textAlign: "center", lineHeight: 1.2, opacity: n(f, 60, 16, 0, 1, lin), translate: `0px ${n(f, 60, 24, 30, 0)}px` }}>
          ¿Se acaba la batería?<br /><span style={{ color: "white", fontWeight: 900 }}>Tú sigues trabajando.</span>
        </div>
      </AbsoluteFill>
      <Img src={staticFile("c180_cut.png")} style={{ position: "absolute", bottom: 50, left: 60 + n(f, 0, dur, 30, -30, lin), width: 960, opacity: n(f, 70, 16, 0, 1, lin), translate: `${n(f, 70, 30, 300, 0)}px 0px`, filter: "drop-shadow(0 30px 30px rgba(0,0,0,0.5))" }} />
    </Scene>
  );
};

// Full photo scene with headline
const PhotoScene: React.FC<{ dur: number; src: string; h: number; top: number; x0: number; x1: number; zoom: number; kicker: string; big: string; sub: string; size?: number }> = (p) => {
  const f = useCurrentFrame();
  const tx = n(f, 0, p.dur, p.x0, p.x1, lin);
  const sc = 1 + n(f, 0, p.dur, 0, p.zoom, lin);
  return (
    <Scene dur={p.dur}>
      <Img src={staticFile(p.src)} style={{ position: "absolute", left: 0, top: p.top, height: p.h, translate: `${tx}px 0px`, scale: String(sc) }} />
      <AbsoluteFill style={{ background: `linear-gradient(to bottom, rgba(0,11,46,0.85) 0%, rgba(0,11,46,0) 22%, rgba(0,11,46,0) 55%, ${DEEP} 80%)` }} />
      <div style={{ position: "absolute", left: 70, right: 70, bottom: 170 }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 40, letterSpacing: 5, opacity: n(f, 8, 12, 0, 1, lin) }}>{p.kicker}</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: p.size ?? 140, whiteSpace: "pre-line", lineHeight: 1, marginTop: 10, opacity: n(f, 12, 12, 0, 1, lin), translate: `0px ${n(f, 12, 24, 50, 0)}px` }}>{p.big}</div>
        <div style={{ display: "inline-block", marginTop: 26, background: BURGUNDY, color: CREAM, fontWeight: 800, fontSize: 44, padding: "14px 32px", borderRadius: 40, opacity: n(f, 22, 12, 0, 1, lin), translate: `0px ${n(f, 22, 24, 30, 0)}px` }}>{p.sub}</div>
      </div>
    </Scene>
  );
};

// 5. Specs
const Specs: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const items = [["1800 W", "MOTOR"], ["55 km/h", "VELOCIDAD MÁX."], ["70 km", "AUTONOMÍA ELÉCTRICA"], ["1 TON", "CAPACIDAD DE CARGA"], ["12\"", "RODADA"], ["30°", "VOLTEO HIDRÁULICO"]];
  return (
    <Scene dur={dur} bg={BG}>
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 190 }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 40, letterSpacing: 6, opacity: n(f, 0, 12, 0, 1, lin) }}>FICHA TÉCNICA</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 120, lineHeight: 1, marginTop: 10, marginBottom: 70, opacity: n(f, 4, 12, 0, 1, lin) }}>CARGO 180</div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 30, width: 940 }}>
          {items.map(([b, l], i) => (
            <div key={i} style={{ padding: "40px 10px", borderRadius: 30, textAlign: "center", background: i === 3 ? BURGUNDY : "rgba(243,233,210,0.1)", border: "2px solid rgba(243,233,210,0.25)",
              opacity: n(f, 10 + i * 6, 12, 0, 1, lin), translate: `0px ${n(f, 10 + i * 6, 22, 50, 0)}px` }}>
              <div style={{ color: CREAM, fontWeight: 900, fontSize: 92, lineHeight: 1 }}>{b}</div>
              <div style={{ color: ROSE, fontWeight: 700, fontSize: 28, marginTop: 14, letterSpacing: 1 }}>{l}</div>
            </div>
          ))}
        </div>
        <div style={{ marginTop: 50, color: CREAM, fontWeight: 600, fontSize: 34, opacity: n(f, 50, 12, 0, 1, lin) }}>+ generador a gasolina para recargar en el camino</div>
        <Img src={staticFile("c180_cut.png")} style={{ width: 720, marginTop: 40, opacity: n(f, 46, 14, 0, 1, lin), translate: `0px ${n(f, 46, 26, 60, 0)}px` }} />
      </AbsoluteFill>
    </Scene>
  );
};

// 6. Colours
const Colors: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const cols: [string, string, string][] = [["c180_azul.png", "AZUL", "#1F5FD6"], ["c180_gris.png", "GRIS", "#5B5F66"], ["c180_rojo.png", "ROJO", "#C8102E"]];
  return (
    <Scene dur={dur} bg={BG}>
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 140 }}>
        <div style={{ color: ROSE, fontWeight: 800, fontSize: 40, letterSpacing: 6, opacity: n(f, 0, 12, 0, 1, lin) }}>ELIGE TU COLOR</div>
        <div style={{ color: "white", fontWeight: 900, fontStyle: "italic", fontSize: 110, lineHeight: 1, marginTop: 10, opacity: n(f, 4, 12, 0, 1, lin) }}>3 COLORES</div>
      </AbsoluteFill>
      {cols.map(([src, name, c], i) => {
        const d = 12 + i * 14;
        const left = i % 2 === 0;
        return (
          <div key={i} style={{ position: "absolute", top: 440 + i * 470, left: 0, right: 0, height: 440, opacity: n(f, d, 12, 0, 1, lin), translate: `${n(f, d, 26, left ? -400 : 400, 0)}px 0px` }}>
            <Img src={staticFile(src)} style={{ position: "absolute", top: 0, [left ? "left" : "right"]: 30, height: 400 } as React.CSSProperties} />
            <div style={{ position: "absolute", bottom: 40, [left ? "right" : "left"]: 70, background: c, color: "white", fontWeight: 900, fontSize: 54, padding: "14px 44px", borderRadius: 40, border: "3px solid rgba(255,255,255,0.8)" } as React.CSSProperties}>{name}</div>
          </div>
        );
      })}
    </Scene>
  );
};

// 7. CTA
const Cta: React.FC<{ dur: number }> = ({ dur }) => {
  const f = useCurrentFrame();
  const pulse = 1 + 0.035 * Math.sin(f / 5);
  return (
    <Scene dur={dur} bg={BG}>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", fontWeight: 900 }}>
        <Img src={staticFile("logo-white.png")} style={{ width: 600, opacity: n(f, 0, 16, 0, 1, lin), translate: `0px ${n(f, 0, 24, 40, 0)}px` }} />
        <Img src={staticFile("c180_cut.png")} style={{ width: 860, marginTop: 50, opacity: n(f, 6, 16, 0, 1, lin), scale: String(n(f, 6, 30, 0.9, 1)) }} />
        <div style={{ color: "white", fontStyle: "italic", fontSize: 120, lineHeight: 1, marginTop: 30, opacity: n(f, 12, 14, 0, 1, lin) }}>CARGO 180</div>
        <div style={{ color: CREAM, fontSize: 42, fontWeight: 700, marginTop: 14, opacity: n(f, 16, 14, 0, 1, lin) }}>Fuerza que trabaja contigo</div>
        <div style={{ marginTop: 60, background: WA, color: DEEP, fontSize: 46, fontWeight: 900, padding: "30px 60px", borderRadius: 70, scale: String(pulse), opacity: n(f, 22, 12, 0, 1, lin) }}>ESCRÍBENOS POR WHATSAPP</div>
        <div style={{ color: CREAM, fontSize: 34, fontWeight: 600, marginTop: 44, opacity: n(f, 28, 12, 0, 1, lin) }}>Garantía y refacciones · Guadalajara, Jalisco</div>
      </AbsoluteFill>
    </Scene>
  );
};

// timeline (30 fps)
const T = { intro: [0, 120], hybrid: [108, 180], ton: [276, 120], hyd: [384, 130], specs: [502, 135], colors: [625, 135], cta: [748, 130] } as const;
export const CARGO180_FRAMES = 878;

export const Cargo180Video: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ backgroundColor: DEEP }}>
      <Sequence from={T.intro[0]} durationInFrames={T.intro[1]}><Intro dur={T.intro[1]} /></Sequence>
      <Sequence from={T.hybrid[0]} durationInFrames={T.hybrid[1]}><Hybrid dur={T.hybrid[1]} /></Sequence>
      <Sequence from={T.ton[0]} durationInFrames={T.ton[1]}>
        <PhotoScene dur={T.ton[1]} src="c180_hero.jpg" h={1650} top={60} x0={-640} x1={-760} zoom={0.06} kicker="CAPACIDAD DE CARGA" big="1 TONELADA" sub="Para el trabajo pesado" />
      </Sequence>
      <Sequence from={T.hyd[0]} durationInFrames={T.hyd[1]}>
        <PhotoScene dur={T.hyd[1]} src="c180_tilt.jpg" h={1500} top={80} x0={-560} x1={-1040} zoom={0.03} kicker="DESCARGA SIN ESFUERZO" big={"CAJA\nHIDRÁULICA"} size={128} sub="Volteo de 30°" />
      </Sequence>
      <Sequence from={T.specs[0]} durationInFrames={T.specs[1]}><Specs dur={T.specs[1]} /></Sequence>
      <Sequence from={T.colors[0]} durationInFrames={T.colors[1]}><Colors dur={T.colors[1]} /></Sequence>
      <Sequence from={T.cta[0]} durationInFrames={T.cta[1]}><Cta dur={T.cta[1] + 10} /></Sequence>
      {f > 150 && f < 740 ? <Img src={staticFile("logo-white.png")} style={{ position: "absolute", top: 70, right: 60, width: 230, opacity: 0.9 }} /> : null}
    </AbsoluteFill>
  );
};
