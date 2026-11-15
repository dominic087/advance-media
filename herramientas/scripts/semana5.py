# Piezas semana 9-14 nov: New Victoria, Carga 160 y Audi (foto con fondo + datos)
import sys
from PIL import Image, ImageOps
sys.path.insert(0, sys.argv[1]); from photopost import make
B = sys.argv[2]; O = sys.argv[1] + "/out/"
def load(p): return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
G = ("1 AÑO", "GARANTÍA ELÉCTRICA")
make(load(B + "nv1.jpg"), O + "new-victoria.jpg", "NEW VICTORIA", "CÓMODA Y CON CAJUELA",
     [("700 W", "MOTOR"), ("35 km/h", "VEL. MÁXIMA"), ("40 km", "AUTONOMÍA"), G], cy=0.55, cx=0.5)
make(load(B + "c1.jpg"), O + "carga-160.jpg", "CARGA 160", "CON CABINA PARA TU NEGOCIO",
     [("1100 W", "MOTOR"), ("45 km/h", "VEL. MÁXIMA"), ("50 km", "AUTONOMÍA"), G], cy=0.6, cx=0.4)
make(load(B + "au2.jpg"), O + "audi.jpg", "AUDI", "POTENCIA PARA LA CIUDAD",
     [("850 W", "MOTOR"), ("40 km/h", "VEL. MÁXIMA"), ("45 km", "AUTONOMÍA"), G], cy=0.6, cx=0.4)
