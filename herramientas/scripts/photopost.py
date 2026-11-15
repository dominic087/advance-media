# Plantilla de post con la foto original de fondo (2160x2700): título arriba, datos abajo
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, sys.path[0]); from cutpost import NAVY, DEEP, CREAM, BURG, ROSE, WA, K, W, H, font, LOGO

def grad(h, top_a, bot_a):
    a = np.linspace(top_a, bot_a, h)[:, None].repeat(W, 1)
    g = np.zeros((h, W, 4), np.uint8); g[..., :3] = DEEP; g[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(g)

def make(photo, out, title, sub, items, cy=0.5, cx=0.5, zoom=1.0):
    """photo: RGB image already cleaned. cy/cx: where the crop window sits (0..1). zoom>1 crops tighter."""
    im = Image.new("RGBA", (W, H), NAVY + (255,))
    PH = H - 134 * K
    r = max(W / photo.width, PH / photo.height) * zoom
    ph = photo.resize((int(photo.width * r), int(photo.height * r)), Image.LANCZOS)
    if ph.width < W:  # foto más angosta: relleno lateral con la misma foto desenfocada
        rb = max(W / photo.width, PH / photo.height)
        bg = photo.resize((int(photo.width * rb), int(photo.height * rb)), Image.LANCZOS).filter(ImageFilter.GaussianBlur(30 * K))
        bt = int((bg.height - PH) * cy); bl = (bg.width - W) // 2
        im.paste(bg.crop((bl, bt, bl + W, bt + PH)), (0, 0))
    left = int((ph.width - W) * cx); top = int((ph.height - PH) * cy)
    if ph.width < W: im.paste(ph.crop((0, top, ph.width, top + PH)), ((W - ph.width) // 2, 0))
    else: im.paste(ph.crop((left, top, left + W, top + PH)), (0, 0))
    im.alpha_composite(grad(380 * K, 0.92, 0.0), (0, 0))
    y0 = H - 134 * K - 150 * K
    im.alpha_composite(grad(120 * K, 0.0, 0.8), (0, y0 - 120 * K))
    im.alpha_composite(Image.new("RGBA", (W, 150 * K), DEEP + (205,)), (0, y0))
    d = ImageDraw.Draw(im)
    lg = Image.open(LOGO); lw = 250 * K; lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
    im.alpha_composite(lg, (W - 60 * K - lw, 44 * K))
    ts = 150
    while d.textlength(title, font=font("Inter-BlackItalic.otf", ts)) > W - 130 * K or ts > 128: ts -= 4
    d.text((56 * K, 232 * K), title, font=font("Inter-BlackItalic.otf", ts), fill=CREAM, anchor="ls")
    f = font("Inter-Bold.otf", 30); tw = d.textlength(sub, font=f)
    d.rounded_rectangle((60 * K, 258 * K, 60 * K + tw + 50 * K, 314 * K), 28 * K, fill=BURG)
    d.text((85 * K, 286 * K), sub, font=f, fill=CREAM, anchor="lm")
    cw = W // len(items)
    for i, (b, l) in enumerate(items):
        x = i * cw + cw // 2
        d.text((x, y0 + 58 * K), b, font=font("Inter-ExtraBold.otf", 44), fill=CREAM, anchor="mm")
        d.text((x, y0 + 108 * K), l, font=font("Inter-Bold.otf", 19), fill=ROSE, anchor="mm")
        if i: d.line((i * cw, y0 + 30 * K, i * cw, y0 + 120 * K), fill=BURG, width=3 * K)
    d.rectangle((0, H - 134 * K, W, H - 130 * K), fill=BURG); d.rectangle((0, H - 130 * K, W, H), fill=DEEP)
    d.text((60 * K, H - 73 * K), "Guadalajara, Jalisco", font=font("Inter-SemiBold.otf", 30), fill=CREAM, anchor="lm")
    btn = "ESCRÍBENOS POR WHATSAPP"; fb = font("Inter-Bold.otf", 28); bw = d.textlength(btn, font=fb) + 60 * K
    d.rounded_rectangle((W - 60 * K - bw, H - 108 * K, W - 60 * K, H - 38 * K), 35 * K, fill=WA)
    d.text((W - 60 * K - bw / 2, H - 73 * K), btn, font=fb, fill=DEEP, anchor="mm")
    im = im.convert("RGB"); im.save(out, quality=93)
    im.resize((1080, 1350), Image.LANCZOS).save(out.replace(".jpg", "_prev.jpg"), quality=90)

def over_original(clean_png, orig):
    """Pegar el recorte limpio (sin logos) sobre la foto original para conservar el fondo."""
    base = orig.convert("RGBA"); c = Image.open(clean_png).convert("RGBA")
    base.alpha_composite(c); return base.convert("RGB")
