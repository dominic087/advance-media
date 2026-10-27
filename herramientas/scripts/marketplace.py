# Imagen cuadrada para Marketplace (2160x2160 HD + 1080x1080): vehículo, características y 3 colores
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

NAVY, DEEP, CREAM, BURG, ROSE, WA, AMBER = (1, 26, 93), (0, 11, 46), (243, 233, 210), (138, 44, 69), (232, 169, 186), (37, 211, 102), (245, 166, 35)
K = 2; W = H = 1080 * K
FONTS = "/usr/share/fonts/opentype/inter/"
font = lambda name, size: ImageFont.truetype(FONTS + name, size * K)

def background():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((x - W * 0.62) / W) ** 2 + ((y - H * 0.38) / H) ** 2) / 0.75
    c0, c1, c2 = np.array((10, 47, 138)), np.array(NAVY), np.array(DEEP)
    t = np.clip(r, 0, 1)[..., None]
    rgb = np.where(t < 0.45, c0 + (c1 - c0) * (t / 0.45), c1 + (c2 - c1) * ((t - 0.45) / 0.55))
    return Image.fromarray(rgb.astype(np.uint8)).convert("RGBA")

def cutout(path, box_w, box_h):
    """Recorte sin fondo, con alfa reforzado (el fondo original ya era azul marino)."""
    im = Image.open(path).convert("RGBA")
    a = np.asarray(im.getchannel("A"), np.float32)
    im.putalpha(Image.fromarray(np.clip(a * 2.5, 0, 255).astype(np.uint8)))
    r = min(box_w * K / im.width, box_h * K / im.height)
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)

def shadow(im, blur=18):
    s = Image.new("RGBA", im.size, (0, 0, 0, 0)); s.putalpha(im.getchannel("A").point(lambda v: v * 0.55))
    pad = blur * 3 * K; out = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    out.alpha_composite(s, (pad, pad + 12 * K)); return out.filter(ImageFilter.GaussianBlur(blur * K)), pad

def paste(base, im, x, y):
    sh, pad = shadow(im); base.alpha_composite(sh, (x - pad, y - pad)); base.alpha_composite(im, (x, y))

def make(cfg, out):
    im = background(); d = ImageDraw.Draw(im)
    lg = Image.open(cfg["logo"]).convert("RGBA"); lw = 250 * K
    lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    im.alpha_composite(lg, (W - 50 * K - lw, 46 * K))
    # título
    fp = font("Inter-Black.otf", 26); tw = d.textlength("¡NUEVO!", font=fp)
    d.rounded_rectangle((50 * K, 50 * K, 50 * K + tw + 40 * K, 96 * K), 23 * K, fill=AMBER)
    d.text((70 * K, 73 * K), "¡NUEVO!", font=fp, fill=DEEP, anchor="lm")
    d.text((44 * K, 218 * K), cfg["title"], font=font("Inter-BlackItalic.otf", cfg.get("title_size", 128)), fill="white", anchor="ls")
    d.text((52 * K, 266 * K), cfg["sub"], font=font("Inter-Bold.otf", 31), fill=CREAM, anchor="ls")
    # vehículo principal
    hx, hy, hw, hh = cfg["hero_box"]; hero = cutout(cfg["hero"], hw, hh)
    paste(im, hero, int((hx + hw / 2) * K - hero.width / 2), int((hy + hh) * K - hero.height))
    d = ImageDraw.Draw(im)
    # características
    y = 292; fb, fl = font("Inter-ExtraBold.otf", 28), font("Inter-SemiBold.otf", 20)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); do = ImageDraw.Draw(ov)
    for i in range(len(cfg["specs"])):
        do.rounded_rectangle((50 * K, (y + 56 * i) * K, 470 * K, (y + 56 * i + 48) * K), 14 * K, fill=(255, 255, 255, 24), outline=(243, 233, 210, 80), width=2 * K)
    im.alpha_composite(ov); d = ImageDraw.Draw(im)
    for big, label in cfg["specs"]:
        d.text((72 * K, (y + 24) * K), big, font=fb, fill="white", anchor="lm")
        bw = d.textlength(big, font=fb)
        d.text((72 * K + bw + 14 * K, (y + 26) * K), label, font=fl, fill=ROSE, anchor="lm")
        y += 56
    if cfg.get("note"):
        d.text((52 * K, (y + 8) * K), cfg["note"], font=font("Inter-SemiBold.otf", 21), fill=CREAM, anchor="lm")
    # colores
    cy = 728
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).line((50 * K, cy * K, W - 50 * K, cy * K), fill=(243, 233, 210, 70), width=2 * K)
    im.alpha_composite(ov); d = ImageDraw.Draw(im)
    d.text((W // 2, (cy + 26) * K), "3 COLORES DISPONIBLES", font=font("Inter-Black.otf", 26), fill=CREAM, anchor="mm")
    slot = (W - 100 * K) // 3
    for i, (src, name, col) in enumerate(cfg["colors"]):
        v = cutout(src, 290, 132)
        cx = 50 * K + slot * i + slot // 2
        paste(im, v, cx - v.width // 2, (cy + 180) * K - v.height)
        d = ImageDraw.Draw(im); f = font("Inter-Black.otf", 22); nw = d.textlength(name, font=f) + 44 * K
        d.rounded_rectangle((cx - nw / 2, (cy + 168) * K, cx + nw / 2, (cy + 202) * K), 18 * K, fill=col, outline=(255, 255, 255, 220), width=2 * K)
        d.text((cx, (cy + 185) * K), name, font=f, fill="white", anchor="mm")
    # pie
    fy = 1012
    btn = "ESCRÍBENOS POR WHATSAPP"; fb = font("Inter-ExtraBold.otf", 25); bw = d.textlength(btn, font=fb) + 56 * K
    d.rounded_rectangle((50 * K, (fy - 30) * K, 50 * K + bw, (fy + 30) * K), 30 * K, fill=WA)
    d.text((50 * K + bw / 2, fy * K), btn, font=fb, fill=DEEP, anchor="mm")
    d.text((W - 50 * K, (fy - 12) * K), "Guadalajara, Jalisco", font=font("Inter-Bold.otf", 24), fill=CREAM, anchor="rm")
    d.text((W - 50 * K, (fy + 16) * K), "Garantía 1 año en todo lo eléctrico", font=font("Inter-Medium.otf", 18), fill=ROSE, anchor="rm")
    im = im.convert("RGB"); im.save(out.replace(".jpg", "-hd.jpg"), quality=93)
    im.resize((1080, 1080), Image.LANCZOS).save(out, quality=92)

if __name__ == "__main__":
    C, LOGO, OUT = sys.argv[1], sys.argv[2], sys.argv[3]  # carpeta de recortes, logo blanco, carpeta de salida
    make(dict(logo=LOGO, title="FAMILY", sub="Triciclo eléctrico de pasajeros", hero=f"{C}/f_hero.png", hero_box=(530, 125, 520, 590),
              specs=[("45 km/h", "velocidad máxima"), ("60 km", "de autonomía"), ("850 W", "motor"), ("48V-20Ah", "batería"),
                     ("200 kg", "peso soportado"), ('8"', "rodada"), ("Bluetooth", "bocina")],
              colors=[(f"{C}/f_rojo.png", "ROJO", (200, 16, 46)), (f"{C}/f_verde.png", "VERDE", (92, 150, 105)), (f"{C}/f_negro.png", "NEGRO", (30, 30, 34))]),
         f"{OUT}/marketplace-family.jpg")
    make(dict(logo=LOGO, title="CARGO 180", sub="Híbrida: gasolina + eléctrica", hero=f"{C}/c_hero.png", hero_box=(490, 300, 570, 400),
              specs=[("1 TON", "capacidad de carga"), ("1800 W", "motor eléctrico"), ("55 km/h", "velocidad máxima"), ("70 km", "autonomía eléctrica"),
                     ("60V-45Ah", "batería"), ("30°", "volteo hidráulico"), ('12"', "rodada")],
              note="+ generador a gasolina que recarga la batería",
              colors=[(f"{C}/c_azul.png", "AZUL", (31, 95, 214)), (f"{C}/c_gris.png", "GRIS", (91, 95, 102)), (f"{C}/c_rojo.png", "ROJO", (200, 16, 46))]),
         f"{OUT}/marketplace-cargo180.jpg")
