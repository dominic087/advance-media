# Herramientas de contenido – Advance Mobility

- `remotion/` – código de los videos (Reels 1080×1920). Composiciones: FamilyVideo, GarantiaVideo, Cargo180Video. Las imágenes que usan van en `remotion/public/` (ver carpetas de medios del repo).
- `scripts/mk.py` – plantilla de post 1080×1350 (foto + specs + botón WhatsApp).
- `scripts/fam2.py` – diseño Family en alta resolución (2160×2700).
- `scripts/esr.py`, `esr180.py` – reescalado con Real-ESRGAN (ncnn, CPU).
- `scripts/assets180.py`, `mask3.py` – recortes sin fondo (rembg) y limpieza.
- `catalogo.md` – especificaciones por modelo.
- `scripts/historia_entregas.py` – historia semanal "Entregas Advance" (1080×1920, 15 s) con fotos de clientes, recortadas para que no salgan caras; editar `SHOTS` (incluye el recorte) cada semana. Usa `logo-white.png`.
