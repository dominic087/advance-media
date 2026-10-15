import {
  AbsoluteFill,
  Easing,
  Img,
  Interactive,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";

const NAVY = "#011A5D";
const DEEP = "#000B2E";
const BURGUNDY = "#8A2C45";
const ROSE = "#E8A9BA";
const CREAM = "#F3E9D2";
const WA = "#25D366";
const FONT = "Inter, 'Arial Black', 'Helvetica Neue', Arial, sans-serif";

const ease = Easing.bezier(0.16, 1, 0.3, 1);

const n = (
  frame: number,
  start: number,
  dur: number,
  from: number,
  to: number,
  easing: (t: number) => number = ease,
) =>
  interpolate(frame, [start, start + dur], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });

const s = (
  frame: number,
  start: number,
  dur: number,
  from: string,
  to: string,
  easing: (t: number) => number = ease,
) =>
  interpolate(frame, [start, start + dur], [from, to], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing,
  });

/* ---------- Fondo con degradado y líneas de velocidad ---------- */
const Backdrop: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      name="Fondo"
      style={{
        background: `radial-gradient(circle at 50% 30%, #0B3399 0%, ${NAVY} 45%, ${DEEP} 100%)`,
      }}
    >
      {[0, 1, 2, 3].map((i) => (
        <div
          key={i}
          style={{
            position: "absolute",
            left: -300,
            top: 260 + i * 470,
            width: 1700,
            height: 4,
            backgroundColor: "rgba(255,255,255,0.07)",
            rotate: "-14deg",
            translate: `${((frame * (0.6 + i * 0.25)) % 120) - 60}px 0px`,
          }}
        />
      ))}
    </AbsoluteFill>
  );
};

/* ---------- Barras de velocidad (como las del logo) ---------- */
const SpeedBars: React.FC<{ y: number; start: number }> = ({ y, start }) => {
  const frame = useCurrentFrame();
  const widths = [620, 440, 280];
  return (
    <>
      {widths.map((w, i) => (
        <Interactive.Div
          key={i}
          name={`Barra ${i + 1}`}
          style={{
            position: "absolute",
            left: 0,
            top: y + i * 34,
            width: w,
            height: 18,
            backgroundColor: i === 0 ? CREAM : i === 1 ? ROSE : BURGUNDY,
            transform: "skewX(-30deg)",
            translate: s(
              frame,
              start + i * 4,
              22,
              `${-w - 200}px 0px`,
              "0px 0px",
            ),
          }}
        />
      ))}
    </>
  );
};

/* ---------- Escena 1: gancho ---------- */
const HookScene: React.FC = () => {
  const frame = useCurrentFrame();
  const lines = ["EL FUTURO", "DE LA", "MOVILIDAD", "ESTÁ AQUÍ"];

  return (
    <AbsoluteFill name="Gancho">
      <Backdrop />
      {/* destello de luz */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.18) 50%, transparent 60%)",
          translate: s(frame, 10, 40, "-1200px 0px", "1200px 0px", Easing.linear),
        }}
      />
      <div style={{ position: "absolute", left: 80, top: 330 }}>
        {lines.map((t, i) => (
          <div
            key={t}
            style={{ overflow: "hidden", height: 150, marginBottom: 6 }}
          >
            <Interactive.Div
              name={`Línea ${i + 1}`}
              style={{
                fontFamily: FONT,
                fontStyle: "italic",
                fontSize: 124,
                lineHeight: "150px",
                color: i === 2 ? NAVY : CREAM,
                backgroundColor: i === 2 ? CREAM : "transparent",
                display: "inline-block",
                padding: i === 2 ? "0 24px" : 0,
                translate: s(frame, 4 + i * 7, 20, "0px 170px", "0px 0px"),
              }}
            >
              {t}
            </Interactive.Div>
          </div>
        ))}
      </div>

      <SpeedBars y={1040} start={40} />

      <Img
        src={staticFile("logo-white.png")}
        style={{
          position: "absolute",
          left: 100,
          top: 1160,
          width: 880,
          opacity: n(frame, 50, 18, 0, 1),
          scale: interpolate(frame, [50, 76], [0.8, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
            output: "perceptual-scale",
          }),
        }}
      />
    </AbsoluteFill>
  );
};

/* ---------- Escena 2: producto ---------- */
const features = [
  "Ahorra en gasolina",
  "Silencioso y sin humo",
  "Ideal para tu negocio",
];

const ProductScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill name="Producto" style={{ opacity: n(frame, 0, 15, 0, 1, Easing.linear) }}>
      {/* fondo: la misma foto ya desenfocada (imagen fija, sin filtros pesados) */}
      <Img
        src={staticFile("bg-blur.jpg")}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, rgba(1,26,93,0.55) 0%, rgba(0,11,46,0.85) 100%)`,
        }}
      />

      {/* marca arriba */}
      <Img
        src={staticFile("logo-white.png")}
        style={{
          position: "absolute",
          left: 70,
          top: 70,
          width: 360,
          opacity: n(frame, 10, 20, 0, 1),
        }}
      />

      {/* tarjeta con la foto */}
      <Interactive.Div
        name="Tarjeta foto"
        style={{
          position: "absolute",
          left: 90,
          top: 190,
          width: 900,
          height: 1050,
          borderRadius: 56,
          overflow: "hidden",
          border: `8px solid ${CREAM}`,
          boxShadow: `22px 22px 0 ${BURGUNDY}`,
          translate: s(frame, 6, 28, "0px 260px", "0px 0px"),
          rotate: s(frame, 6, 28, "-4deg", "0deg"),
          opacity: n(frame, 6, 16, 0, 1),
        }}
      >
        <Img
          src={staticFile("triciclo.jpg")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "50% 38%",
            scale: interpolate(frame, [0, 195], [1.02, 1.16], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.linear,
              output: "perceptual-scale",
            }),
          }}
        />
      </Interactive.Div>

      {/* banda con el nombre del producto */}
      <Interactive.Div
        name="Banda título"
        style={{
          position: "absolute",
          left: 40,
          top: 1160,
          width: 1000,
          height: 130,
          backgroundColor: BURGUNDY,
          transform: "skewX(-8deg)",
          translate: s(frame, 24, 22, "-1100px 0px", "0px 0px"),
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            transform: "skewX(8deg)",
            fontFamily: FONT,
            fontStyle: "italic",
            fontSize: 88,
            color: CREAM,
            letterSpacing: 2,
          }}
        >
          TRICICLO ELÉCTRICO
        </div>
      </Interactive.Div>

      {/* beneficios */}
      {features.map((t, i) => (
        <Interactive.Div
          key={t}
          name={`Beneficio ${i + 1}`}
          style={{
            position: "absolute",
            left: 90,
            top: 1345 + i * 92,
            display: "flex",
            alignItems: "center",
            gap: 20,
            padding: "0 40px 0 14px",
            height: 74,
            borderRadius: 37,
            backgroundColor: CREAM,
            color: NAVY,
            fontFamily: FONT,
            fontSize: 40,
            translate: s(frame, 46 + i * 12, 20, "1200px 0px", "0px 0px"),
          }}
        >
          <div
            style={{
              width: 48,
              height: 48,
              borderRadius: 24,
              backgroundColor: BURGUNDY,
              color: CREAM,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 30,
            }}
          >
            ✓
          </div>
          {t}
        </Interactive.Div>
      ))}
    </AbsoluteFill>
  );
};

/* ---------- Escena: ficha técnica ---------- */
const specs = [
  { big: "900 W", label: "MOTOR", dark: false },
  { big: "40 km/h", label: "VELOCIDAD MÁXIMA", dark: false },
  { big: "45 km", label: "AUTONOMÍA", dark: false },
  { big: "1 AÑO", label: "GARANTÍA EN TODO LO ELÉCTRICO", dark: true },
  { big: "CÁMARA", label: "DE REVERSA TRASERA", dark: true },
  { big: "TOLDO", label: "ESTRUCTURADO", dark: true },
];

const SpecsScene: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill name="Ficha técnica" style={{ opacity: n(frame, 0, 15, 0, 1, Easing.linear) }}>
      <Img
        src={staticFile("bg-blur.jpg")}
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, rgba(1,26,93,0.6) 0%, rgba(0,11,46,0.9) 100%)`,
        }}
      />

      <Img
        src={staticFile("logo-white.png")}
        style={{ position: "absolute", left: 70, top: 60, width: 360, opacity: n(frame, 6, 18, 0, 1) }}
      />

      <Interactive.Div
        name="Título ficha"
        style={{
          position: "absolute",
          left: 90,
          top: 175,
          fontFamily: FONT,
          fontStyle: "italic",
          fontSize: 100,
          color: CREAM,
          opacity: n(frame, 4, 16, 0, 1),
          translate: s(frame, 4, 20, "-80px 0px", "0px 0px"),
        }}
      >
        FICHA TÉCNICA
      </Interactive.Div>
      <Interactive.Div
        name="Línea título"
        style={{
          position: "absolute",
          left: 90,
          top: 296,
          height: 12,
          backgroundColor: BURGUNDY,
          width: n(frame, 14, 24, 0, 520),
        }}
      />

      <Interactive.Div
        name="Foto triciclo"
        style={{
          position: "absolute",
          left: 90,
          top: 340,
          width: 900,
          height: 500,
          borderRadius: 48,
          overflow: "hidden",
          border: `8px solid ${CREAM}`,
          boxShadow: `18px 18px 0 ${BURGUNDY}`,
          opacity: n(frame, 10, 16, 0, 1),
          translate: s(frame, 10, 24, "0px 120px", "0px 0px"),
        }}
      >
        <Img
          src={staticFile("triciclo.jpg")}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: "50% 38%",
            scale: interpolate(frame, [0, 210], [1.05, 1.15], {
              extrapolateLeft: "clamp",
              extrapolateRight: "clamp",
              easing: Easing.linear,
              output: "perceptual-scale",
            }),
          }}
        />
      </Interactive.Div>

      {specs.map((sp, i) => {
        const col = i % 2;
        const row = Math.floor(i / 2);
        const start = 28 + i * 10;
        return (
          <Interactive.Div
            key={sp.big}
            name={`Dato ${i + 1}`}
            style={{
              position: "absolute",
              left: 90 + col * 460,
              top: 900 + row * 220,
              width: 440,
              height: 200,
              borderRadius: 32,
              backgroundColor: sp.dark ? BURGUNDY : CREAM,
              color: sp.dark ? CREAM : NAVY,
              boxSizing: "border-box",
              padding: "0 30px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              opacity: n(frame, start, 14, 0, 1),
              scale: interpolate(frame, [start, start + 18], [0.82, 1], {
                extrapolateLeft: "clamp",
                extrapolateRight: "clamp",
                easing: ease,
                output: "perceptual-scale",
              }),
            }}
          >
            <div style={{ fontFamily: FONT, fontStyle: "italic", fontSize: 76, lineHeight: 1.05 }}>
              {sp.big}
            </div>
            <div
              style={{
                fontFamily: FONT,
                fontSize: 26,
                lineHeight: 1.2,
                marginTop: 8,
                color: sp.dark ? ROSE : BURGUNDY,
                letterSpacing: 1,
              }}
            >
              {sp.label}
            </div>
          </Interactive.Div>
        );
      })}
    </AbsoluteFill>
  );
};

/* ---------- Escena 3: llamado a la acción ---------- */
const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const pulse = 1 + 0.045 * Math.sin(frame / 5);

  return (
    <AbsoluteFill name="Cierre" style={{ opacity: n(frame, 0, 15, 0, 1, Easing.linear) }}>
      <Backdrop />

      <Img
        src={staticFile("logo-white.png")}
        style={{
          position: "absolute",
          left: 100,
          top: 190,
          width: 880,
          opacity: n(frame, 6, 20, 0, 1),
          scale: interpolate(frame, [6, 30], [0.85, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: ease,
            output: "perceptual-scale",
          }),
        }}
      />

      <SpeedBars y={470} start={14} />

      <div style={{ position: "absolute", left: 80, top: 600 }}>
        <div style={{ overflow: "hidden", height: 190 }}>
          <Interactive.Div
            name="Cotiza"
            style={{
              fontFamily: FONT,
              fontStyle: "italic",
              fontSize: 170,
              lineHeight: "190px",
              color: CREAM,
              translate: s(frame, 22, 20, "0px 210px", "0px 0px"),
            }}
          >
            COTIZA
          </Interactive.Div>
        </div>
        <div style={{ overflow: "hidden", height: 190 }}>
          <Interactive.Div
            name="Hoy"
            style={{
              fontFamily: FONT,
              fontStyle: "italic",
              fontSize: 170,
              lineHeight: "190px",
              color: CREAM,
              backgroundColor: BURGUNDY,
              display: "inline-block",
              padding: "0 36px",
              translate: s(frame, 30, 20, "0px 210px", "0px 0px"),
            }}
          >
            HOY
          </Interactive.Div>
        </div>
      </div>

      <Interactive.Div
        name="Qué vendemos"
        style={{
          position: "absolute",
          left: 80,
          top: 1010,
          fontFamily: FONT,
          fontSize: 50,
          color: CREAM,
          opacity: n(frame, 44, 18, 0, 1),
          translate: s(frame, 44, 18, "0px 30px", "0px 0px"),
        }}
      >
        Triciclos y bicimotos eléctricas
        <div style={{ color: ROSE, fontSize: 42, marginTop: 10 }}>
          Mejor relación calidad-precio
        </div>
      </Interactive.Div>

      {/* botón WhatsApp */}
      <Interactive.Div
        name="Botón WhatsApp"
        style={{
          position: "absolute",
          left: 100,
          top: 1230,
          width: 880,
          height: 140,
          borderRadius: 70,
          backgroundColor: WA,
          color: DEEP,
          fontFamily: FONT,
          fontSize: 44,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          boxShadow: `0 0 0 ${18 * (pulse - 0.955) * 10}px rgba(37,211,102,0.25)`,
          scale: pulse,
          opacity: n(frame, 58, 16, 0, 1),
        }}
      >
        ESCRÍBENOS POR WHATSAPP
      </Interactive.Div>

      <Interactive.Div
        name="Contacto"
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          top: 1420,
          textAlign: "center",
          fontFamily: FONT,
          fontSize: 38,
          color: CREAM,
          opacity: n(frame, 74, 18, 0, 1),
        }}
      >
        facebook.com/advancemobilityvg
        <div style={{ color: ROSE, fontSize: 34, marginTop: 10 }}>
          Guadalajara, Jalisco
        </div>
      </Interactive.Div>
    </AbsoluteFill>
  );
};

/* ---------- Video completo (15 s a 30 fps) ---------- */
export const AdvanceVideo: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill style={{ backgroundColor: DEEP, fontWeight: 900 }}>
      <Sequence name="Gancho" from={0} durationInFrames={120} layout="absolute-fill">
        <HookScene />
      </Sequence>
      <Sequence name="Producto" from={105} durationInFrames={180} layout="absolute-fill">
        <ProductScene />
      </Sequence>
      <Sequence name="Ficha técnica" from={270} durationInFrames={210} layout="absolute-fill">
        <SpecsScene />
      </Sequence>
      <Sequence name="Cierre" from={465} durationInFrames={165} layout="absolute-fill">
        <CtaScene />
      </Sequence>
      <AbsoluteFill
        style={{
          backgroundColor: DEEP,
          opacity: n(frame, 616, 14, 0, 1, Easing.linear),
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
