"""BOP-Hub figure palette.

The single Python source for BOP-Hub colours. The palette is Maastricht University
house style: measured against the ORIGINAL artwork, the mark's three non-green
colours each resolve to a UM colour rendered slightly off (navy dE 4.2, blue
dE 4.3, orange dE 4.1). The values below are the official UM ones, not the
samples. The green is the one colour with no UM equivalent.

Do not re-sample assets/img/bop-hub-logo-master.png: its 64-colour palette
reduction merged the orange to #BA5726, 13.3 dE off the artwork. Reasoning in
BRAND.md; the CSS copies are in assets/main.scss.

    from tools.bophub_palette import SERIES, use_style
    use_style()

Rules this module exists to enforce, restated because they are easy to lose in a
notebook:

* SERIES is assigned in order and never cycled. A sixth category folds into
  OTHER, or the chart becomes small multiples.
* Colour follows the entity, not its rank. Filtering a chart must not repaint
  the series that survive.
* DIVERGING has no green pole. Green means "beneficial outcome" on this site,
  and a scale running into green would claim the high end of any measure is good.
* Confidence and weight of evidence are NEVER a red-amber-green scale. Use
  SEQUENTIAL, or a bar glyph, or a bar chart.
"""

from __future__ import annotations

import os

__all__ = [
    "NAVY", "BLUE", "ORANGE", "GREEN", "RUST",
    "BLUE_INK", "ORANGE_INK", "GREEN_INK", "LINK", "LINK_HOVER", "INK", "MUTED",
    "PAPER", "WASH", "RULE", "RULE_STRONG", "DARK_GROUND",
    "SERIES", "SERIES_DARK", "OTHER", "SEQUENTIAL", "DIVERGING",
    "ROLE", "STYLE_PATH", "use_style", "contrast", "check_contrast",
]

# -- house style: fills and rules, never text ---------------------------------
NAVY   = "#001C3D"   # UM Blue, style guide
BLUE   = "#00A2DB"   # UM light blue, style guide
ORANGE = "#EB5B25"   # UM secondary orange, brand_colours.csv
GREEN  = "#4AA718"   # the mark's green; no UM equivalent
RUST   = ORANGE      # alias kept for 2026-11 code; prefer ORANGE

# -- darkened variants: the only ones allowed to carry text -------------------
# Ratios are white / wash. UM's own #007FAD reaches 4.53 on white but only 4.22
# on the wash, so BLUE_INK is a derived half-step darker.
BLUE_INK   = "#1478A1"   # derived            4.96 / 4.63
ORANGE_INK = "#AE0B12"   # UM institutional   7.35 / 6.86
GREEN_INK  = "#377F11"   # derived            4.99 / 4.66
LINK       = "#1E5A96"   # UM link default    7.10 / 6.62
LINK_HOVER = "#D2460F"   # UM link hover, library implementation. 4.54 / 4.24
INK        = "#333333"   # UM body text      12.63 / 11.79
MUTED      = "#565C66"   # derived            6.73 / 6.28

# -- surfaces -----------------------------------------------------------------
PAPER       = "#FFFFFF"   # UM white
WASH        = "#F6F7F9"   # derived
RULE        = "#E3E3E3"   # UM light grey
RULE_STRONG = "#C9CED6"   # derived
DARK_GROUND = NAVY        # UM Blue, the slide ground

# -- categorical --------------------------------------------------------------
# Slots 1-3 are the UM hues; 4-5 extend away from them. Validated across ALL
# pairs (not just adjacent) for deutan/protan/tritan separation, lightness band,
# chroma floor and 3:1 contrast on white. Worst pair: delta-E 9.6 (deutan).
# Re-validate if you change a value.
SERIES = [BLUE_INK, ORANGE_INK, GREEN, "#B972F1", "#81168C"]
OTHER  = "#6B7785"

# Re-stepped for the UM Blue ground, not inverted from the light set. Its worst
# pair sits at delta-E 7.8, acceptable only because direct labels are mandatory.
SERIES_DARK = ["#20A9E6", "#CF5C16", "#7EB023", "#826CE1", "#DF6EBF"]

# -- magnitude: one hue, light to dark ----------------------------------------
SEQUENTIAL = ["#DDF2FE", "#A6D4EE", "#7BB5D4", "#4E96BA",
              "#1477A0", "#0C5877", "#053B51"]

# -- polarity: rust to blue through a neutral grey, deliberately no green -----
DIVERGING = ["#B14420", "#CA775D", "#E0A795", "#F1F1EF",
             "#86BFDE", "#3A9BC9", "#13759D"]

# -- the role encoding: colour AND shape, always together ---------------------
ROLE = {
    "initiating": {"color": ORANGE,      "marker": "o", "label": "Initiating event"},
    "key":        {"color": RULE_STRONG, "marker": "D", "label": "Key event"},
    "outcome":    {"color": GREEN,       "marker": "s", "label": "Beneficial outcome"},
}

STYLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "bop-hub.mplstyle")


def use_style(dark: bool = False) -> None:
    """Apply the BOP-Hub matplotlib style and colour cycle."""
    import matplotlib.pyplot as plt
    from cycler import cycler

    plt.style.use(STYLE_PATH)
    if dark:
        plt.rcParams.update({
            "axes.prop_cycle": cycler(color=SERIES_DARK),
            "figure.facecolor": DARK_GROUND,
            "axes.facecolor": DARK_GROUND,
            "savefig.facecolor": DARK_GROUND,
            "text.color": "#E8EEF4",
            "axes.labelcolor": "#E8EEF4",
            "axes.edgecolor": "#3C546F",
            "xtick.color": "#AFC0D0",
            "ytick.color": "#AFC0D0",
            "grid.color": "#163353",
        })


# -- contrast arithmetic, so a value can be checked without leaving Python ----
def _lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    """WCAG 2.x contrast ratio between two hex colours."""
    la, lb = _luminance(a), _luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast(surface: str = PAPER) -> None:
    """Print every text-bearing token against a surface, flagging AA failures."""
    for name in ("BLUE_INK", "ORANGE_INK", "GREEN_INK", "LINK",
                 "LINK_HOVER", "INK", "MUTED", "NAVY"):
        ratio = contrast(globals()[name], surface)
        flag = "ok " if ratio >= 4.5 else "FAIL"
        print(f"  {flag} {name:<10} {globals()[name]}  {ratio:5.2f}:1")


if __name__ == "__main__":
    print(f"text tokens on PAPER {PAPER}:")
    check_contrast(PAPER)
    print(f"\ntext tokens on WASH {WASH}:")
    check_contrast(WASH)
    print("\nseries on white (fills need >= 3:1):")
    for i, c in enumerate(SERIES, 1):
        print(f"  series-{i}   {c}  {contrast(c, PAPER):5.2f}:1")
