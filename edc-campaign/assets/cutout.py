"""Cut the character poses out of assets/karan-character-sheet.webp into
public/karan/*.png (transparent). Background = bright pixels connected to
the crop border; edges are feathered by 1px."""
import os
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sheet = Image.open(os.path.join(ROOT, "assets", "karan-character-sheet.webp")).convert("RGB")
BOXES = {  # x0, y0, x1, y1 on the 1536x1024 sheet
    "front": (200, 28, 560, 612),
    "three-quarter": (620, 28, 970, 612),
    "side": (1080, 28, 1330, 612),
    "neutral": (90, 640, 345, 958),
    "thinking": (440, 640, 725, 958),
    "explaining": (790, 640, 1150, 958),
    "happy": (1180, 640, 1490, 958),
}
for name, box in BOXES.items():
    im = sheet.crop(box)
    a = np.asarray(im.convert("L")).astype(int)
    def border_bg(mask):
        lab, _ = ndimage.label(mask)
        ids = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
        return np.isin(lab, list(ids))

    # Seed the background from eroded bright pixels so thin white details
    # (sleeve stripes, sneakers) touching the edge are not flooded.
    bright = a > 246
    seed = border_bg(ndimage.binary_erosion(bright, iterations=3, border_value=1))
    bg = ndimage.binary_dilation(seed, iterations=3) & bright
    if name in ("front", "three-quarter", "side"):
        # soft floor shadow: very light pixels below the sneakers, connected to bg
        h = a.shape[0]
        band = np.zeros_like(bright)
        band[int(h * 0.93):] = True
        shadow = band & (a > 226)
        lab, _ = ndimage.label(shadow | bg)
        ids = set(np.unique(lab[bg])) - {0}
        bg |= np.isin(lab, list(ids)) & shadow & ~ndimage.binary_dilation(a < 190, iterations=2)
    fg = ndimage.binary_fill_holes(~bg)
    lab2, n2 = ndimage.label(fg)
    if n2 > 1:  # keep the figure only (drops stray sheet text)
        sizes = ndimage.sum(fg, lab2, range(1, n2 + 1))
        fg = lab2 == (1 + int(np.argmax(sizes)))
    alpha = Image.fromarray((fg * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.8))
    # tighten: remove halo by eroding alpha slightly
    al = np.asarray(alpha).astype(float)
    al = np.clip((al - 60) * 255 / 195, 0, 255).astype("uint8")
    rgba = im.convert("RGBA")
    rgba.putalpha(Image.fromarray(al))
    bb = rgba.getbbox()
    rgba = rgba.crop(bb)
    rgba.save(os.path.join(ROOT, "public", "karan", f"{name}.png"))
    print(name, rgba.size)
