# Quita el texto "MODELO RAYO" del anuncio del proveedor (Rayo/3.jpg): cubre el recuadro con textura de pared limpia
import sys, numpy as np, cv2
im = cv2.imread(sys.argv[1]).astype(np.float32); h, w = im.shape[:2]
x0, y0, x1, y1 = 560, 0, w, 315
src = im[0:190, 0:560]                      # pared limpia arriba a la izquierda
tile = np.concatenate([src, src[::-1]], 0)  # 380 filas
tile = np.concatenate([tile, tile[:, ::-1]], 1)[:y1 - y0, :x1 - x0]
# igualar brillo al promedio de la pared alrededor del recuadro
ref = np.concatenate([im[0:315, 540:560].reshape(-1, 3), im[315:330, 900:w].reshape(-1, 3)]).mean(0)
tile = tile - tile.reshape(-1, 3).mean(0) + ref
m = np.zeros((h, w), np.float32); m[y0:y1 - 12, x0 + 12:x1] = 1
m = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
full = im.copy(); full[y0:y1, x0:x1] = tile
out = im * (1 - m) + full * m
cv2.imwrite(sys.argv[2], np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])
