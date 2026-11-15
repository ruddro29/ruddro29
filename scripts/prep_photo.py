"""
Prepare portrait photo for clean ASCII conversion:
  1. Remove solid cream background
  2. Normalize skin vs dark features (hair, eyes, eyebrows, mustache, clothes)
  3. Keep face skin bright/clean while emphasizing facial contours
"""
import os
import sys
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
INP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "source-photo.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "source-prepped.png")

img = cv2.imread(INP)
if img is None:
    raise FileNotFoundError(f"Cannot read image: {INP}")

h, w = img.shape[:2]

# Detect outer cream background
corners = np.vstack([img[0:15, 0:15], img[0:15, -15:], img[-15:, 0:15], img[-15:, -15:]])
bg_color = np.median(corners.reshape(-1, 3), axis=0).astype(np.float32)

diff = np.linalg.norm(img.astype(np.float32) - bg_color, axis=2)
flood = (diff < 26).astype(np.uint8) * 255

cv2.floodFill(flood, None, (0, 0), 128)
cv2.floodFill(flood, None, (w - 1, 0), 128)
cv2.floodFill(flood, None, (0, h - 1), 128)
cv2.floodFill(flood, None, (w - 1, h - 1), 128)

outer_bg = (flood == 128)
alpha = (~outer_bg).astype(np.uint8) * 255

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Bilateral filtering to smooth skin textures while keeping eyes, brows, nose lines intact
smooth = cv2.bilateralFilter(gray, 9, 45, 9)
smooth = cv2.bilateralFilter(smooth, 9, 45, 9)

# We want the skin (around gray ~115) to land comfortably in the lighter zone (~210-230)
# and darker areas (hair, eyes, facial hair, shirt) to remain crisp and dark (<100).
# Piecewise tone curve:
tone = np.zeros_like(smooth, dtype=np.float32)

# Linear stretch targeting hair vs skin separation
# Values < 40 remain dark (< 30)
# Values 40..130 stretch up into 30..220
# Values > 130 stretch up into 220..255
for y in range(h):
    for x in range(w):
        v = smooth[y, x]
        if v < 45:
            tone[y, x] = v * (35.0 / 45.0)
        elif v < 125:
            tone[y, x] = 35.0 + (v - 45.0) * ((225.0 - 35.0) / 80.0)
        else:
            tone[y, x] = 225.0 + (v - 125.0) * ((255.0 - 225.0) / 130.0)

# Extract edge lines (DoG)
fine = cv2.GaussianBlur(smooth, (0, 0), 1.2).astype(np.float32)
coarse = cv2.GaussianBlur(smooth, (0, 0), 5.0).astype(np.float32)
lines = np.clip((coarse - fine) / 30.0, 0, 1)

# Subtract edge lines to enhance eyebrows, eyelids, lips, chin
out = np.clip(tone - 65.0 * lines, 0, 255.0)

# Composite onto pure white background
mask = cv2.GaussianBlur(alpha.astype(np.float32) / 255.0, (0, 0), 1.0)
out = out * mask + 255.0 * (1.0 - mask)

# Bounding box crop
ys, xs = np.where(alpha > 20)
min_y, max_y = ys.min(), ys.max()
min_x, max_x = xs.min(), xs.max()
subject_h = max_y - min_y
subject_w = max_x - min_x

side = int(min(max(subject_w * 1.05, subject_h * 0.90), min(h, w)))
cx = (min_x + max_x) // 2
cy = int(min_y + subject_h * 0.44)

x0 = max(0, min(w - side, cx - side // 2))
y0 = max(0, min(h - side, cy - side // 2))
cropped = out[y0 : y0 + side, x0 : x0 + side]

Image.fromarray(cropped.astype(np.uint8), mode="L").save(OUT)
print(f"wrote {OUT} {cropped.shape}")
