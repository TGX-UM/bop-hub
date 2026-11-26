# BOP-Hub style guidelines

How BOP-Hub looks, and why. This covers the website, figures, slides, posters and
anything else that goes out under the name.

**The palette is Maastricht University house style.** The mark's three non-green
colours were each checked against the UM palettes and each one is a UM colour
rendered slightly off. The values below are the **official UM ones**, not the
samples. §2 shows the measurements.

Measure against `~/Downloads/BOP_Hub_logo_Final_png.png`, the original artwork —
**not** against `assets/img/bop-hub-logo-master.png`, whose orange is corrupt (§1).

The machine-readable copies live in two places and nowhere else:

| What | Where |
|---|---|
| Web tokens | `assets/main.scss`, the `:root` block |
| Figure palette | `tools/bophub_palette.py` and `tools/bop-hub.mplstyle` |

If you need a colour, take it from one of those. Do not retype a hex code into a
slide deck from memory — export it from the palette module, or copy it from the
table below.

---

## 1. The mark

### Files

| File | Size | Use |
|---|---|---|
| `bop-hub-logo-master.png` | 1200 × 600 | Archive master. Never embed this directly. |
| `bop-hub-logo.png` | 420 × 172 | The lockup, trimmed to the ink box. Site header, slides, posters. |
| `bop-hub-mark.png` | 512 × 512 | The B alone. Avatars, favicons, anywhere under ~140 px wide. |
| `favicon-16x16.png`, `favicon-32x32.png`, `favicon.ico`, `apple-touch-icon.png` | — | Browser and device icons. |

The lockup's ink box is 1048 × 424, an aspect of **2.47 : 1**. Any rendering that
is not 2.47 : 1 has been stretched; fix it rather than nudging it.

### What it shows

Three nodes converge into the **B**, pass through a hexagonal **O**, and resolve
into a single green node on the **P**. That is the argument of the resource in one
image: several upstream events, one causal chain, one beneficial outcome. The
hexagon is the Translational Genomics module; the green node is the part that is
BOP-Hub's own and not the department's.

### Clear space and minimum size

- **Clear space** on all four sides is one quarter of the lockup's height
  (106 px at master scale). Nothing — no rule, no text, no photo edge — enters it.
- **Minimum size** for the lockup is **140 px** wide on screen, **35 mm** in print.
  Below that, "Hub" closes up. Use `bop-hub-mark.png` instead.
- The site header renders the lockup at 182 px, dropping to 150 px under 40 rem.

### Rules

- The mark is **never recoloured**, including to a single-colour version. There is
  no approved mono variant; if you need one, ask for it to be drawn rather than
  flattening the file yourself.
- It sits on **white or `--wash`**. It is a navy wordmark on paper and has no
  knocked-out version, which is why the site header is white rather than navy.
- Do not add a drop shadow, outline, gradient or container box.
- Do not set the word "BOP-Hub" in type next to the mark. The mark is the wordmark.
- Alt text is `BOP-Hub`, not a description of the drawing.

### Known problem: the archive master is corrupt

`bop-hub-logo-master.png` exists so the other files can be regenerated from it.
It cannot be used for that. Generating the derivatives re-encoded everything to a
64-colour palette, which is lossless for flat artwork **except** that it merged the
orange:

| Colour | Original artwork | In the master | ΔE |
|---|---|---|---|
| navy | `#02264C` | `#02264C` | 0.0 |
| blue | `#00B1DC` | `#00B1DC` | 0.0 |
| green | `#4AA718` | `#4AA519` | 0.6 |
| **orange** | **`#FE6107`** | **`#BA5726`** | **13.3** |

A ΔE of 13 is not a rounding difference; it is a bright orange turned into a muddy
rust. The served `bop-hub-logo.png` is **fine** (`#FE6309`), so nothing on the site
is wrong today — but regenerate from the master and the corruption propagates into
every derivative at once.

Two things to do:

1. **Move `~/Downloads/BOP_Hub_logo_Final_png.png` somewhere durable** —
   `10_Admin/TGX/logo/` beside the TGX marks, or the BOP project folder. Downloads
   gets triaged, and it is currently the only uncorrupted copy of the artwork.
2. **Regenerate the master from it without the palette reduction**, or with a
   palette that keeps the orange.

### Known gap: there is no vector master

Every file is raster, upscaled from a generated image, and its edges carry
compression noise. Survivable on screen; at poster scale it is not — a 1200 px
master at A0 is roughly 40 px/inch. Redraw the mark as SVG on the hexes in §2
before the first printed poster or any journal figure. The tokens already carry
those values, so the redraw brings the artwork to the documentation rather than the
other way round.

---

## 2. Colour

### The mark is drawn in UM house style

Each of the mark's three non-green colours resolves to a published UM colour.
Measured against the **original artwork**. Distances are ΔE in OKLab ×100; below
about 5 the two read as the same colour rendered slightly differently.

| In the mark | UM value | ΔE | Source |
|---|---|---|---|
| `#02264C` navy | **UM Blue** `#001C3D` | 4.2 | style guide |
| `#00B1DC` blue | **UM light blue** `#00A2DB` | 4.3 | style guide |
| `#FE6107` orange | **UM orange** `#EB5B25` | 4.1 | `brand_colours.csv` |
| `#4AA718` green | — | 24+ | no UM equivalent exists |

**The orange belongs to the UM secondary palette, not to the institutional
orange-red.** `#D2460F` is 10.5 ΔE from the mark's orange — a different colour,
darker and redder. It appears in this sheet only where UM publishes it as a web
value, on link hover. If you want one warm colour everywhere rather than two,
that is a decision to take deliberately; the mark is what would have to change.

Two UM palettes are in play and they are not the same list. The authoritative web
spec is `~/Documents/10_Admin/TGX/UM_style_guide/UM_style_guide.zip` (UM Blue,
`#1E5A96`, `#D2460F`, `#333333`, `#E3E3E3`) and everything in this sheet except
`--orange` comes from it. `~/Documents/10_Admin/TGX/brand_colours.csv` is a
different, broader palette whose primaries (`#29235C`, `#E6007E`, `#307BBF`) do not
appear in the style guide at all; `--orange` is its secondary orange, because that
is what the mark is drawn in.

The nearest UM swatch to the green is 24 ΔE away, which is not a match in any
useful sense. The green is BOP-Hub's own, and in the mark it is the node the
pathway resolves into — so here it means exactly that.

### The four

Fills and rules. They never carry text.

| Token | Hex | Source | On white |
|---|---|---|---|
| `--navy` | `#001C3D` | UM Blue | 17.02 : 1 |
| `--blue` | `#00A2DB` | UM light blue | 2.92 : 1 |
| `--orange` | `#EB5B25` | UM secondary orange | 3.47 : 1 |
| `--green` | `#4AA718` | the mark's own | 3.07 : 1 |

`--rust` is an alias of `--orange`, kept so nothing written in November 2026
breaks. Prefer `--orange`; `--rust` should be deleted.

### Text variants

UM documents that several house-style colours fail WCAG contrast, and its own
library works from darkened variants for text. Same here: a plain token is the
house colour, the matching `-ink` token is the only one allowed to carry text.
**Where UM publishes an accessible variant of its own, that value is used** rather
than a derived one.

| Token | Hex | Source | On white | On `--wash` |
|---|---|---|---|---|
| `--blue-ink` | `#1478A1` | derived | 4.96 : 1 | 4.63 : 1 |
| `--orange-ink` | `#AE0B12` | UM orange-red, institutional | 7.35 : 1 | 6.86 : 1 |
| `--green-ink` | `#377F11` | derived | 4.99 : 1 | 4.66 : 1 |
| `--link` | `#1E5A96` | UM link default | 7.10 : 1 | 6.62 : 1 |
| `--link-hover` | `#D2460F` | UM link hover, library | 4.54 : 1 | 4.24 : 1 |
| `--ink` | `#333333` | UM body text | 12.63 : 1 | 11.79 : 1 |
| `--muted` | `#565C66` | derived | 6.73 : 1 | 6.28 : 1 |

Only three values in the whole sheet are invented: `--blue-ink`, `--green-ink` and
`--muted`. Each has a reason.

- **`--blue-ink`.** UM's own accessible light blue is `#007FAD`, which reaches
  4.53 : 1 on white but only 4.22 : 1 on the wash. `#1478A1` is a half-step darker
  on the same hue and clears both.
- **`--green-ink`.** The green has no UM equivalent, so there is nothing to adopt.
- **`--muted`.** UM's medium grey `#999999` is 2.85 : 1 and cannot carry text.

**`--link-hover` is the one published value that does not clear AA everywhere.**
At 4.24 : 1 it fails on the wash, so links on a wash ground — the footer, inside a
caveat — hover to `--orange-ink` instead. The rule is in the stylesheet.

### Surfaces

`--paper` `#FFFFFF` (UM white) · `--wash` `#F6F7F9` (derived) ·
`--rule` `#E3E3E3` (UM light grey) · `--rule-strong` `#C9CED6` (derived)

---

## 3. The two meaning rules

These are the only places colour is allowed to mean anything. Everything else in
the sheet stays out of their way.

### Colour encodes the part an event plays, not how good it is

| Role | Colour | Shape |
|---|---|---|
| Initiating event | `--orange` | filled circle |
| Key event | `--rule-strong` | hollow diamond |
| Beneficial outcome | `--green` | filled square |

Every role carries a shape as well as a colour, so the encoding survives greyscale
printing and colour-vision deficiency. Never ship the colour without the shape.

### Evidence strength is never colour

Confidence and weight-of-evidence are shown as a filled-bar glyph followed by the
word — `▮▮▯ moderate` — and never as a red/amber/green scale.

This is the single rule most worth holding. A green "high" on a page about the
beneficial effects of an intervention reads as *this is good for you*, which is
exactly the misreading a resource of this kind has to avoid. Green already means
"beneficial outcome" on this site; it cannot also mean "well evidenced".

The same follows for figures: **do not build a red–amber–green confidence heatmap.**
Use the sequential blue ramp, or a bar glyph, or a bar chart.

---

## 4. Typography

**Open Sans**, with the platform UI face behind it:

```
"Open Sans", "Segoe UI", system-ui, -apple-system, "Helvetica Neue", sans-serif
```

Open Sans is UM's own named substitute for the licensed Thesis Sans and is what
the university library runs on. It is not fetched from a third-party CDN: where it
is installed it is used, otherwise the stack degrades. Vendoring an Apache-2.0
subset is a follow-up.

| Element | Size | Weight | Colour |
|---|---|---|---|
| h1 | `clamp(1.75rem, 1.2rem + 2vw, 2.6rem)`, `-0.02em` | 600 | `--navy` |
| h2 | 1.4 rem | 600 | `--navy` |
| h3 | 1.1 rem | 600 | `--navy` |
| body | 1.0625 rem / 1.6 | 400 | `--ink` |
| identifiers | 0.8 rem, monospace | 400 | `--muted` |

- Prose runs to **68 ch** (`--measure`). Tables and diagrams may exceed it; running
  text may not.
- **Weight 700 is not used.** Headings are 600; `strong` is 600 in `--navy`.
- An identifier (`BOP:1`, `BOPE:12`) is a handle, not a heading: small, monospaced,
  muted. Never set one as a heading or in bold.
- Links are underlined with a 2 px offset. Underline-on-hover only is not used —
  colour alone is not an affordance.

---

## 5. Figures and charts

Read this before writing the first line of chart code.

### Series colours

Assigned **in this fixed order and never cycled**. Colour follows the entity, not
its rank: if a filter removes a series, the survivors keep their colours.

| Slot | Hex | Source | Token |
|---|---|---|---|
| 1 | `#1478A1` blue | UM light blue, darkened | `--series-1` |
| 2 | `#AE0B12` orange-red | UM institutional | `--series-2` |
| 3 | `#4AA718` green | the mark's own | `--series-3` |
| 4 | `#B972F1` violet | extension | `--series-4` |
| 5 | `#81168C` plum | extension | `--series-5` |
| Other | `#6B7785` grey | extension | `--series-other` |

Five is the cap. A sixth category folds into **Other**, or the chart becomes small
multiples. A sixth hue is never generated.

This set is validated across **all pairs** — not just neighbouring ones — for
deuteranopia, protanopia and tritanopia, for lightness spread, chroma, and 3 : 1
contrast against white. Worst pair: ΔE 9.6 (deutan). Re-run the check if you
change any value.

Slots 1–3 are the UM hues; 4 and 5 extend away from them. The blue is darkened so
it is legible as a thin line on white; slot 2 is UM's own institutional orange-red,
which is already dark enough; the green is the mark's green unchanged.

### Magnitude and polarity

- **Sequential** (counts, densities), the UM light-blue hue light→dark:
  `#DDF2FE → #A6D4EE → #7BB5D4 → #4E96BA → #1477A0 → #0C5877 → #053B51`
- **Diverging** (change, log fold change, over/under a baseline), UM orange-red ↔
  UM light blue through a neutral midpoint:
  `#B14420 · #CA775D · #E0A795 · #F1F1EF · #86BFDE · #3A9BC9 · #13759D`

The diverging scale deliberately does **not** use green as a pole. Green means
"beneficial outcome" on this site, and a diverging scale running into green would
say that the high end of any measure is good.

Never a rainbow. Never a hue at a diverging midpoint.

### Mark and layout rules

- **One y-axis. Never a dual-axis chart.** Two measures of different scale become
  two charts, small multiples, or both indexed to a common base.
- Lines 2 px; markers ≥ 8 px; a 2 px surface gap between adjacent or stacked fills.
- Grid and axes recessive: `--rule` at most, never black.
- Values, labels and legend text wear `--ink` / `--muted`, **never the series
  colour**. The coloured mark beside the label carries the identity.
- Two or more series always get a legend; four or fewer are also directly labelled,
  so identity is never colour-alone. One series needs no legend — the title names it.
- No number printed on every point. Label the endpoints, the extremes, or nothing.
- Every figure that encodes by colour has a table view or a data file beside it.

### Dark surfaces

For slides on the UM Blue ground (`#001C3D`), the series palette re-steps to:
`#20A9E6 · #CF5C16 · #7EB023 · #826CE1 · #DF6EBF`, every one at 4.2 : 1 or better
against that ground. This is a separate validated set, not an automatic inversion
of the light one. Its worst CVD pair sits at ΔE 7.8, which is only acceptable
because direct labels are mandatory above.

### matplotlib

```python
import matplotlib.pyplot as plt
from tools.bophub_palette import SERIES, SEQUENTIAL, DIVERGING, use_style
use_style()            # loads tools/bop-hub.mplstyle
```

`use_style()` sets the cycler, the fonts, the recessive grid and 300 dpi output.
Do not override the colour cycle in a notebook.

### Mermaid diagrams on BOP pages

BOP chain diagrams follow the role encoding of §3 — orange-red for the initiating event,
green for the outcome, navy rule for key events — and nothing else is coloured. The
engine is switchable in `_config.yml` (`diagram_engine: mermaid | table`) so a
broken CDN is one commit away from a table fallback.

---

## 6. Slides, posters and documents

The site's rules carry over; only the measurements change.

- **Ground:** white, or `--navy` `#001C3D` for a title slide. Nothing in between —
  a mid-tone ground makes both the navy type and the white type marginal.
- **Logo placement:** top-left or bottom-right, at the clear space of §1, at a
  consistent size across the deck. Not on every slide — the title and the closing
  slide are enough.
- **Heading colour** is `--navy` on white, white on navy. `--blue` is never type.
- **Accent rule:** a 4 px `--orange` rule under a section title, matching the
  `.caveat` treatment on the site. One accent per slide.
- **Posters:** do not use the raster logo above A3 until the SVG exists (§1).
- **Documents** (deliverables, manuscripts, reports): headings in `--navy`, body in
  `--ink`, identifiers monospaced and `--muted`, figures from §5. A Word or Docs
  file needs only those four mappings; do not rebuild the whole site palette in a
  template.

---

## 7. Naming and voice

- The object is a **BOP**, not a "pathway" and not a "BOP pathway". `BOP-Hub` always
  carries the hyphen and the capital H.
- Spell out **Beneficial Outcome Pathway** on first use in any outward-facing text.
- BOP-Hub is "the beneficial counterpart to AOP-Wiki" — a counterpart, not a fork,
  a clone or a competitor.
- Identifiers are `BOP:n`, `BOPE:n`, `BOPR:n`, formed from `id_prefixes` in
  `_config.yml`. Canonical IRIs are computed from `canonical_base`
  (`https://w3id.org/bop-hub`) and never written into a page, so moving to a custom
  domain does not invalidate them.

---

## 8. Accessibility floor

Non-negotiable, and the reason several values above are darker than the mark's own:

- Body text ≥ 4.5 : 1 against its surface; large text and UI edges ≥ 3 : 1.
- Nothing is encoded by colour alone — a shape, a label or a glyph goes with it.
- Focus is a 3 px `--link` outline at 2 px offset, on links, buttons and summaries.
- `prefers-reduced-motion` is honoured site-wide.
- Figures carry a table view or a data file.

To check a value, the arithmetic is in `tools/bophub_palette.py` (`contrast()`).
