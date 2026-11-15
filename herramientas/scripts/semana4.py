# Piezas semana 3-8 nov: Luna, Family Pro y Alpha (foto con fondo + datos). Uso: python3 semana4.py <carpeta con photopost.py, cutpost.py y logo-white.png>
import sys
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter
sys.path.insert(0, sys.argv[1]); from photopost import make
B = "/mnt/project-files/fotos/semana4/"; O = sys.argv[1] + "/out/"
def load(p): return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
make(load(B + "luna/184650.jpg"), O + "luna.jpg", "LUNA", "LIGERA Y CON CANASTILLA",
     [("700 W", "MOTOR"), ("35 km/h", "VEL. MÁXIMA"), ("40 km", "AUTONOMÍA"), ("1 AÑO", "GARANTÍA ELÉCTRICA")], cy=0.6, cx=0.5, zoom=0.82)
fp = load(B + "familypro/1.jpg")  # tapar la página web del proveedor en la placa
box = (884, 711, 997, 731); a = np.array(fp)
col = tuple(int(v) for v in np.median(np.concatenate([a[713:729, 872:882], a[713:729, 998:1008]]).reshape(-1, 3), 0))
ImageDraw.Draw(fp).rectangle(box, fill=col)
m = Image.new("L", fp.size, 0); ImageDraw.Draw(m).rectangle((box[0]-2, box[1]-2, box[2]+2, box[3]+2), fill=255)
fp = Image.composite(fp.filter(ImageFilter.GaussianBlur(2)), fp, m)
make(fp, O + "family-pro.jpg", "FAMILY PRO", "PARA TODA LA FAMILIA",
     [("800 W", "MOTOR"), ("40 km/h", "VEL. MÁXIMA"), ("45 km", "AUTONOMÍA"), ("1 AÑO", "GARANTÍA ELÉCTRICA")], cy=0.6, cx=0.5)
make(load(B + "alpha/120806.jpg"), O + "alpha.jpg", "ALPHA", "ELIGE TU COLOR",
     [("500 W", "MOTOR"), ("30 km/h", "VEL. MÁXIMA"), ("35 km", "AUTONOMÍA"), ("1 AÑO", "GARANTÍA ELÉCTRICA")], cy=0.62, cx=0.5)
