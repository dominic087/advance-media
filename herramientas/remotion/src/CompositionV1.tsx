import {
  AbsoluteFill,
  Easing,
  Img,
  Interactive,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const NAVY = "#011A5D";
const NAVY_DARK = "#000F38";
const BURGUNDY = "#8A2C45";
const CREAM = "#F3E9D2";
const FONT =
  "Inter, 'Arial Black', 'Helvetica Neue', Arial, sans-serif";

const ease = Easing.bezier(0.16, 1, 0.3, 1);

/* ---------- Escena 1: logo ---------- */
const LogoScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill name="Logo" style={{ backgroundColor: NAVY }}>
      <Interactive.Div
        name="Barra vino"
        style={{
          position: "absolute",
          left: 0,
          top: 1180,
          height: 14,
          backgroundColor: BURGUNDY,
          width: interpolate(frame, [0.6 * fps, 1.6 * fps], [0, 1080], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
          }),
        }}
      />
      <Img
        src={staticFile("logo.jpg")}
        style={{
          position: "absolute",
          left: 0,
          top: 460,
          width: 1080,
          height: 1080,
          opacity: interpolate(frame, [0, 0.8 * fps], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
          }),
          scale: interpolate(frame, [0, 1.2 * fps], [0.85, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
            output: "perceptual-scale",
          }),
        }}
      />
      <Interactive.Div
        name="Lema"
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1250,
          textAlign: "center",
          fontFamily: FONT,
          fontStyle: "italic",
          fontSize: 54,
          letterSpacing: 8,
          color: CREAM,
          opacity: interpolate(frame, [1.2 * fps, 2 * fps], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
          }),
          translate: interpolate(
            frame,
            [1.2 * fps, 2 * fps],
            ["0px 30px", "0px 0px"],
            {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: ease,
            },
          ),
        }}
      >
        MOVILIDAD ELÉCTRICA
      </Interactive.Div>
    </AbsoluteFill>
  );
};

/* ---------- Escena 2: triciclo ---------- */
const TricicloScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const line = (start: number) => ({
    opacity: interpolate(frame, [start * fps, (start + 0.7) * fps], [0, 1], {
      extrapolateLeft: "clamp" as const,
      extrapolateRight: "clamp" as const,
      easing: ease,
    }),
    translate: interpolate(
      frame,
      [start * fps, (start + 0.7) * fps],
      ["-60px 0px", "0px 0px"],
      {
        extrapolateLeft: "clamp" as const,
        extrapolateRight: "clamp" as const,
        easing: ease,
      },
    ),
  });

  return (
    <AbsoluteFill
      name="Triciclo"
      style={{
        background: `linear-gradient(180deg, ${NAVY} 0%, ${NAVY_DARK} 100%)`,
      }}
    >
      {/* foto con zoom lento */}
      <Interactive.Div
        name="Marco foto"
        style={{
          position: "absolute",
          left: 60,
          top: 150,
          width: 960,
          height: 1080,
          borderRadius: 48,
          overflow: "hidden",
          border: `10px solid ${CREAM}`,
          boxShadow: `24px 24px 0 ${BURGUNDY}`,
          opacity: interpolate(frame, [0, 0.6 * fps], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
          translate: interpolate(frame, [0, 0.9 * fps], ["0px 120px", "0px 0px"], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
          }),
        }}
      >
        <Img
          src={staticFile("triciclo.jpg")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "50% 55%",
            scale: interpolate(frame, [0, 7 * fps], [1, 1.12], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.linear,
              output: "perceptual-scale",
            }),
          }}
        />
      </Interactive.Div>

      {/* textos */}
      <Interactive.Div
        name="Titulo"
        style={{
          position: "absolute",
          left: 80,
          top: 1320,
          fontFamily: FONT,
          fontStyle: "italic",
          fontSize: 104,
          lineHeight: 1,
          color: CREAM,
          ...line(0.6),
        }}
      >
        TRICICLO
        <br />
        <span style={{ color: "#E0A3B3" }}>ELÉCTRICO</span>
      </Interactive.Div>

      <Interactive.Div
        name="Beneficio 1"
        style={{
          position: "absolute",
          left: 80,
          top: 1580,
          fontFamily: FONT,
          fontSize: 48,
          color: CREAM,
          ...line(1.4),
        }}
      >
        ✔ Ahorra en gasolina
      </Interactive.Div>
      <Interactive.Div
        name="Beneficio 2"
        style={{
          position: "absolute",
          left: 80,
          top: 1660,
          fontFamily: FONT,
          fontSize: 48,
          color: CREAM,
          ...line(2.0),
        }}
      >
        ✔ Ideal para tu negocio
      </Interactive.Div>
      <Interactive.Div
        name="Beneficio 3"
        style={{
          position: "absolute",
          left: 80,
          top: 1740,
          fontFamily: FONT,
          fontSize: 48,
          color: CREAM,
          ...line(2.6),
        }}
      >
        ✔ Silencioso y sin humo
      </Interactive.Div>
    </AbsoluteFill>
  );
};

/* ---------- Escena 3: cierre ---------- */
const CierreScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fade = (start: number) =>
    interpolate(frame, [start * fps, (start + 0.7) * fps], [0, 1], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: ease,
    });

  return (
    <AbsoluteFill name="Cierre" style={{ backgroundColor: NAVY }}>
      <Img
        src={staticFile("logo.jpg")}
        style={{
          position: "absolute",
          left: 0,
          top: 250,
          width: 1080,
          height: 1080,
          opacity: fade(0),
        }}
      />
      <Interactive.Div
        name="Llamado"
        style={{
          position: "absolute",
          left: 90,
          right: 90,
          top: 1230,
          padding: "46px 0",
          borderRadius: 40,
          backgroundColor: BURGUNDY,
          color: CREAM,
          textAlign: "center",
          fontFamily: FONT,
          fontStyle: "italic",
          fontSize: 76,
          opacity: fade(0.5),
          scale: interpolate(frame, [0.5 * fps, 1.2 * fps], [0.8, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
            output: "perceptual-scale",
          }),
        }}
      >
        ¡COTIZA HOY!
      </Interactive.Div>
      <Interactive.Div
        name="Ubicacion"
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1480,
          textAlign: "center",
          fontFamily: FONT,
          fontSize: 50,
          color: CREAM,
          opacity: fade(1.3),
        }}
      >
        Guadalajara, Jalisco
      </Interactive.Div>
      <Interactive.Div
        name="Contacto"
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1570,
          textAlign: "center",
          fontFamily: FONT,
          fontSize: 44,
          color: "#E0A3B3",
          opacity: fade(1.8),
        }}
      >
        Escríbenos por WhatsApp
      </Interactive.Div>
    </AbsoluteFill>
  );
};

/* ---------- Video completo ---------- */
export const AdvanceVideoV1: React.FC = () => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: NAVY, fontWeight: 900 }}>
      <Sequence name="Logo" from={0} durationInFrames={4 * fps} layout="absolute-fill">
        <LogoScene />
      </Sequence>
      <Sequence name="Triciclo" from={4 * fps} durationInFrames={7 * fps} layout="absolute-fill">
        <TricicloScene />
      </Sequence>
      <Sequence name="Cierre" from={11 * fps} durationInFrames={4 * fps} layout="absolute-fill">
        <CierreScene />
      </Sequence>
      {/* destello crema en los cortes */}
      {[4 * fps, 11 * fps].map((cut) => (
        <AbsoluteFill
          key={cut}
          style={{
            backgroundColor: CREAM,
            opacity: interpolate(frame, [cut - 1, cut, cut + 8], [0, 0.9, 0], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
            }),
            pointerEvents: "none",
          }}
        />
      ))}
    </AbsoluteFill>
  );
};
