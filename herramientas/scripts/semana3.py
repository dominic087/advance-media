# Piezas semana 27-31 oct: Cargo 110 y Family Plus Toldo (foto con fondo + datos). Uso: python3 semana3.py <carpeta con photopost.py, cutpost.py y logo-white.png>
import sys
from PIL import Image, ImageOps
sys.path.insert(0, sys.argv[1]); from photopost import make
B = "/mnt/project-files/fotos/semana3/"; O = sys.argv[1] + "/out/"
def load(p): return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
c = load(B + "cargo110/142328.jpg")
from PIL import ImageFilter
make(c, O + "cargo-110.jpg", "CARGO 110", "PARA TU NEGOCIO",
     [("1 AÑO", "GARANTÍA ELÉCTRICA"), ("REFACCIONES", "DE TODO TIPO"), ("ASISTENCIA", "TELEFÓNICA")], cy=0.55, cx=1.0, zoom=1.16)  # recorte a la derecha: fuera letrero y camioneta de otro negocio
make(load(B + "toldo/181159.jpg"), O + "family-plus-toldo.jpg", "FAMILY PLUS TOLDO", "CON TECHO Y PARABRISAS",
     [("800 W", "MOTOR"), ("40 km/h", "VEL. MÁXIMA"), ("45 km", "AUTONOMÍA"), ("1 AÑO", "GARANTÍA ELÉCTRICA")], cy=0.6, cx=0.5)
