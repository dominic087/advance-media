# Piezas semana 16-21 nov: último día Buen Fin, Beta y Family (foto con fondo + datos)
# Uso: python3 semana6.py <carpeta con photopost.py, cutpost.py y logo-white.png>
import sys
from PIL import Image, ImageOps, ImageEnhance
sys.path.insert(0, sys.argv[1]); from photopost import make
B = "/mnt/project-files/fotos/"; O = sys.argv[1] + "/out/"
def load(p): return ImageOps.exif_transpose(Image.open(p)).convert("RGB")
G = ("1 AÑO", "GARANTÍA ELÉCTRICA")
make(load(B + "semana3/toldo/181032.jpg"), O + "buenfin-ultimo-dia.jpg", "¡ÚLTIMO DÍA!", "BUEN FIN: LLÉVATE UN REGALO CON TU COMPRA",
     [("CASCO", "DE PROTECCIÓN"), ("O", "TÚ ELIGES"), ("FUNDA", "PARA LLUVIA Y SOL")], cy=0.6, cx=0.5)
b = ImageEnhance.Brightness(load(B + "semana6/beta2.jpg")).enhance(1.35)
make(b, O + "beta.jpg", "BETA", "LIGERA, ÁGIL Y CON CANASTILLA",
     [("500 W", "MOTOR"), ("30 km/h", "VEL. MÁXIMA"), ("35 km", "AUTONOMÍA"), G], cy=0.72, cx=0.55, zoom=1.3)
make(load(B + "semana6/tf1.jpg"), O + "family.jpg", "FAMILY", "EL CLÁSICO PARA TODA LA FAMILIA",
     [("600 W", "MOTOR"), ("35 km/h", "VEL. MÁXIMA"), ("40 km", "AUTONOMÍA"), G], cy=0.75, cx=0.55)
# Rayo y Magic (sin ficha técnica confirmada: solo garantía, refacciones y asistencia, que incluyen todos los modelos)
X = [("1 AÑO", "GARANTÍA ELÉCTRICA"), ("REFACCIONES", "DISPONIBLES"), ("ASISTENCIA", "TELEFÓNICA")]
make(load(B + "semana6/rayo3-limpia.jpg"), O + "rayo.jpg", "RAYO", "BICIMOTO ELÉCTRICA", X, cy=0.0, cx=0.35, zoom=0.9)
make(load(B + "semana6/magic1.jpg"), O + "magic.jpg", "MAGIC", "TRICICLO ELÉCTRICO", X, cy=0.6, cx=0.5)
# Family Plus Toldo (vel. 45 km/h confirmada por Valente el 12 nov; motor y autonomía como en la pieza del 31 oct)
make(load(B + "semana3/toldo/181034.jpg"), O + "family-plus-toldo.jpg", "FAMILY PLUS TOLDO", "PROTEGIDO DEL SOL Y LA LLUVIA",
     [("800 W", "MOTOR"), ("45 km/h", "VEL. MÁXIMA"), ("45 km", "AUTONOMÍA"), G], cy=0.75, cx=0.55)
