#!/usr/bin/env python3
"""Trace the BOP-Hub logo from its raster original into a clean, flat SVG.

The artwork is a generated PNG: four flat inks on white, with antialiased edges.
That is the ideal case for a per-colour trace -- the geometry is recoverable
exactly, and the result is a real vector file with the brand hexes in it rather
than an approximation of them.

How it works, and why not a one-shot autotrace:

1. SUPERSAMPLE. The image is scaled up (default 3x, Lanczos) before anything
   else, so an antialiased edge resolves to within a third of an original pixel
   instead of snapping to the nearest whole one.
2. UNMIX, don't match. Nearest-colour matching is wrong at an antialiased edge:
   a half-covered navy pixel is a mid slate blue, which in any colour space sits
   closer to the artwork's cyan than to navy, and every navy edge grows a cyan
   halo. Instead each pixel is modelled as one ink composited over white --
   solve for the coverage alpha that best explains it, take the ink with the
   smallest residual, and keep the pixel where alpha >= 0.5. That is how the
   image was made, so it inverts cleanly. A generic autotrace guesses the
   palette from the pixels and reproduces the file's colour drift with its
   shapes.
3. TRACE EACH INK SEPARATELY with potrace, then stack them. Masks are dilated by
   one supersampled pixel first: adjacent inks share a boundary, and tracing them
   independently otherwise leaves hairline slivers of background between them.
4. FILL WITH NAMED COLOURS, not sampled ones. The geometry comes from the
   artwork; the colours come from the palette below. That is what makes this a
   fix for the corrupt master rather than a re-encoding of it.

White is not traced. It becomes transparent, so the counters of the letters and
the centres of the nodes knock out properly and the mark can sit on any ground.
Pass --white-ground for a version with the white painted in.

Variants, from the same trace rather than from separate artwork:

    --reversed        navy becomes white, for a dark ground. Without this the
                      wordmark disappears on anything near UM Blue.
    --mono COLOUR     every ink in one colour, for single-colour print.
    --crop x0,y0,x1,y1   cut a region out, in SOURCE pixel coordinates -- used
                      to take the B mark out of the lockup. The paths are
                      clipped, not redrawn, so the mark can never drift from
                      the lockup it came from.
    --square          pad the viewBox out to a square around the crop. Needed
                      because the gap between the B and the arrow after it is
                      only ~100 px, so a square viewBox alone would pull the
                      arrow back in; the clip is what keeps it out.

    python3 tools/vectorise_logo.py <source.png> --out assets/img/bop-hub-logo.svg

Needs Pillow, numpy and `potracer` (pure-Python potrace: pip install potracer).
"""

from __future__ import annotations

import argparse
import sys

import numpy as np
from PIL import Image

try:
    import potrace
except ImportError:  # pragma: no cover
    sys.exit("needs potracer:  pip install potracer")

# The ink the artwork is drawn in, and the house-style value it resolves to.
# Order is z-order, back to front: largest area first.
PALETTE = [
    # name      as drawn    UM house style   source
    ("navy",   "#02264C",  "#001C3D"),   # UM Blue, style guide
    ("blue",   "#00B1DC",  "#00A2DB"),   # UM light blue, style guide
    ("orange", "#FE6107",  "#EB5B25"),   # UM secondary orange, brand_colours.csv
    ("green",  "#4AA718",  "#4AA718"),   # BOP-Hub's own; no UM equivalent
]
GROUND = "#FFFFFF"


def _srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    """sRGB 0-255 -> CIELAB. Shape (..., 3) in, (..., 3) out."""
    c = rgb.astype(np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ m.T / np.array([0.95047, 1.0, 1.08883])
    eps, kappa = 216 / 24389, 24389 / 27
    f = np.where(xyz > eps, np.cbrt(xyz), (kappa * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16,
                     500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _dilate(mask: np.ndarray) -> np.ndarray:
    """Grow a boolean mask by one pixel in the four directions."""
    out = mask.copy()
    out[1:, :] |= mask[:-1, :]
    out[:-1, :] |= mask[1:, :]
    out[:, 1:] |= mask[:, :-1]
    out[:, :-1] |= mask[:, 1:]
    return out


def _path_data(path, scale: float, ox: float, oy: float, places: int) -> str:
    """potrace path -> SVG 'd', scaled back down and shifted to the ink box."""
    def pt(p):
        return (f"{round(p.x / scale - ox, places):g},"
                f"{round(p.y / scale - oy, places):g}")

    out = []
    for curve in path:
        out.append("M" + pt(curve.start_point))
        for seg in curve:
            if seg.is_corner:
                out.append("L" + pt(seg.c) + "L" + pt(seg.end_point))
            else:
                out.append("C" + pt(seg.c1) + " " + pt(seg.c2) + " " + pt(seg.end_point))
        out.append("Z")
    return "".join(out)


def vectorise(src: str, out: str, *, house_style: bool = True, supersample: int = 3,
              turdsize: int = 2, alphamax: float = 1.0, opttolerance: float = 0.2,
              places: int = 2, white_ground: bool = False, title: str = "BOP-Hub",
              reversed_: bool = False, mono: str | None = None,
              crop: tuple[float, float, float, float] | None = None,
              square: bool = False) -> None:
    img = Image.open(src).convert("RGB")
    w0, h0 = img.size
    if supersample > 1:
        img = img.resize((w0 * supersample, h0 * supersample), Image.LANCZOS)
    arr = np.asarray(img)

    # 2. unmix: model each pixel as one ink composited over the ground
    px = arr.astype(np.float64)
    ground = np.array(_hex_to_rgb(GROUND), dtype=np.float64)
    alphas, residuals = [], []
    for _, drawn, _ in PALETTE:
        ink = np.array(_hex_to_rgb(drawn), dtype=np.float64)
        v = ground - ink                       # ground -> ink direction
        a = ((ground - px) @ v) / (v @ v)       # least-squares coverage
        a = np.clip(a, 0.0, 1.0)
        model = ground - a[..., None] * v
        alphas.append(a)
        residuals.append(np.linalg.norm(px - model, axis=-1))
    alpha = np.stack(alphas)                    # (ink, h, w)
    resid = np.stack(residuals)
    best = resid.argmin(0)                      # which ink explains the pixel

    masks = []
    for i in range(len(PALETTE)):
        masks.append((best == i) & (alpha[i] >= 0.5))
    counts = [int(m.sum()) for m in masks]
    if min(counts) == 0:
        missing = [n for (n, *_), c in zip(PALETTE, counts) if c == 0]
        sys.exit(f"palette entry not found in the source: {', '.join(missing)}")

    # ink bounding box, so the SVG carries no dead margin
    ink = np.any(np.stack(masks), axis=0)
    ys, xs = np.where(ink)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    ox, oy = x0 / supersample, y0 / supersample
    clip = None
    if crop:
        cx0, cy0, cx1, cy1 = crop
        clip = (round(cx0 - ox, places), round(cy0 - oy, places),
                round(cx1 - cx0, places), round(cy1 - cy0, places))
        vb_x, vb_y, vb_w, vb_h = clip
        if square:
            side = max(vb_w, vb_h)
            vb_x = round(vb_x - (side - vb_w) / 2, places)
            vb_y = round(vb_y - (side - vb_h) / 2, places)
            vb_w = vb_h = side
    else:
        vb_x = vb_y = 0.0
        vb_w = round((x1 - x0) / supersample, places)
        vb_h = round((y1 - y0) / supersample, places)

    layers = []
    for (name, drawn, official), mask, n in zip(PALETTE, masks, counts):
        # 3. one supersampled pixel of overlap, so no background shows between inks.
        # potracer inverts whatever it is given, so hand it the complement.
        bmp = potrace.Bitmap(~_dilate(mask))
        path = bmp.trace(turdsize=turdsize * supersample * supersample,
                         turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                         alphamax=alphamax, opticurve=True, opttolerance=opttolerance)
        fill = official if house_style else drawn
        if mono:
            fill = mono
        elif reversed_ and name == "navy":
            fill = GROUND
        layers.append((name, fill, drawn, official, n,
                       _path_data(path, supersample, ox, oy, places)))

    note = (f"all {mono}" if mono else
            "house-style values, navy reversed out" if reversed_ else
            "house-style values" if house_style else "the artwork's own values")
    head = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_x:g} {vb_y:g} {vb_w:g} {vb_h:g}"',
        f'     width="{vb_w:g}" height="{vb_h:g}" role="img" aria-label="{title}">',
        f'  <title>{title}</title>',
        f'  <!-- Traced from {src.split("/")[-1]} at {supersample}x by',
        '       tools/vectorise_logo.py. Geometry is the artwork; colours are',
        f'       {note}. See BRAND.md. -->',
    ]
    if white_ground:
        head.append(f'  <rect x="{vb_x:g}" y="{vb_y:g}" width="{vb_w:g}" '
                    f'height="{vb_h:g}" fill="{GROUND}"/>')
    body = [f'  <path fill="{fill}" fill-rule="evenodd" d="{d}"/>'
            f'<!-- {name}: {n:,} px, drawn {drawn} -->'
            for name, fill, drawn, official, n, d in layers]
    if clip:
        kx, ky, kw, kh = clip
        body = ([f'  <clipPath id="crop"><rect x="{kx:g}" y="{ky:g}" '
                 f'width="{kw:g}" height="{kh:g}"/></clipPath>',
                 '  <g clip-path="url(#crop)">']
                + ["  " + b for b in body] + ["  </g>"])
    svg = "\n".join(head + body + ["</svg>", ""])

    with open(out, "w") as fh:
        fh.write(svg)

    print(f"{out}  {vb_w:g} x {vb_h:g}  {len(svg) / 1024:.1f} KB")
    for name, fill, drawn, official, n, d in layers:
        print(f"   {name:<7} {fill}  {n // supersample ** 2:>8,} px  {len(d) / 1024:5.1f} KB path")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source", help="the ORIGINAL artwork PNG, not a derivative")
    ap.add_argument("--out", default="bop-hub-logo.svg")
    ap.add_argument("--as-drawn", action="store_true",
                    help="keep the artwork's sampled hexes instead of the house-style ones")
    ap.add_argument("--white-ground", action="store_true",
                    help="paint the white background in instead of leaving it transparent")
    ap.add_argument("--supersample", type=int, default=3)
    ap.add_argument("--turdsize", type=int, default=2, help="drop specks below this area")
    ap.add_argument("--alphamax", type=float, default=1.0, help="corner threshold, 0=all corners")
    ap.add_argument("--opttolerance", type=float, default=0.2, help="curve-merging tolerance")
    ap.add_argument("--places", type=int, default=2, help="decimal places in path data")
    ap.add_argument("--title", default="BOP-Hub")
    ap.add_argument("--reversed", dest="reversed_", action="store_true",
                    help="navy becomes white, for a dark ground")
    ap.add_argument("--mono", metavar="COLOUR", help="every ink in one colour")
    ap.add_argument("--crop", metavar="X0,Y0,X1,Y1",
                    help="clip to this region, in source pixel coordinates")
    ap.add_argument("--square", action="store_true",
                    help="pad the viewBox out to a square around --crop")
    a = ap.parse_args()
    crop = tuple(float(v) for v in a.crop.split(",")) if a.crop else None
    if crop is not None and len(crop) != 4:
        ap.error("--crop takes four comma-separated numbers")
    vectorise(a.source, a.out, house_style=not a.as_drawn, supersample=a.supersample,
              turdsize=a.turdsize, alphamax=a.alphamax, opttolerance=a.opttolerance,
              places=a.places, white_ground=a.white_ground, title=a.title,
              reversed_=a.reversed_, mono=a.mono, crop=crop, square=a.square)


if __name__ == "__main__":
    main()
