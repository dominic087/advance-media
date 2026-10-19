import sys, numpy as np, cv2
from PIL import Image, ImageOps
D = sys.argv[1]; sys.path.insert(0, D)
import photopost as P
# Family Plus
o = ImageOps.exif_transpose(Image.open(D + '/fotos/fp1.jpg')).convert('RGB')
P.make(o, D + '/out/family-plus-fondo.jpg', 'FAMILY PLUS', 'TRICICLO ELÉCTRICO PARA TODA LA FAMILIA',
       [('800 W', 'MOTOR'), ('40 km/h', 'VEL. MÁXIMA'), ('45 km', 'AUTONOMÍA'), ('1 AÑO', 'GARANTÍA ELÉCTRICA')], cy=0.36)
# Family Plus Q
o = Image.open(D + '/fotos/fpq1.jpg').convert('RGB')
P.make(o, D + '/out/family-plus-q-fondo.jpg', 'FAMILY PLUS Q', 'TRICICLO ELÉCTRICO CON BATERÍA DE 72 V',
       [('1000 W', 'MOTOR'), ('45 km/h', 'VEL. MÁXIMA'), ('50 km', 'AUTONOMÍA'), ('72 V', 'BATERÍA')], cy=0.95)
# Family Q (foto aclarada; placas originales sin tocar)
rgb = np.array(Image.open(D + '/fotos/fq2.jpg').convert('RGB'))
rgb = (255 * ((rgb / 255.0) ** 0.8) * 1.04).clip(0, 255).astype(np.uint8)
hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV); blu = (hsv[..., 0] > 95) & (hsv[..., 0] < 130)
hsv[..., 1] = np.where(blu, (hsv[..., 1] * 0.35).astype(np.uint8), hsv[..., 1]); rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
P.make(Image.fromarray(rgb), D + '/out/family-q-fondo.jpg', 'FAMILY Q', 'TRICICLO ELÉCTRICO DE 1000 W',
       [('1000 W', 'MOTOR'), ('45 km/h', 'VEL. MÁXIMA'), ('50 km', 'AUTONOMÍA'), ('1 AÑO', 'GARANTÍA ELÉCTRICA')], cy=0.5, zoom=0.9)
