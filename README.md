# Thinkinghaus palette

Version 0.5 · September 29, 2026

Warm neutrals for reading, with deliberate accents for interaction. View the
[palette and contrast examples](https://keeping.haus/thinkinghaus-palette/) or the
[UI style guide](https://keeping.haus/thinkinghaus-ui/).

## Files

- [thinkinghaus.css](thinkinghaus.css) — CSS variables and light/dark roles.
- [thinkinghaus.figma.json](thinkinghaus.figma.json) — Figma color tokens for Tokens Studio.
- [ghosttyhaus.conf](ghosttyhaus.conf) — Ghostty terminal configuration.
- [thinkinghaus.tokens.json](thinkinghaus.tokens.json) — values, aliases, roles, and measured contrast.

## Foundation colors belong to the scale

| Foundation color | Neutral step | Hex |
| --- | --- | --- |
| Ivory | 0 | #F4EDDF |
| Body | 400 | #AFADA6 |
| Taupe | 500 | #9C9281 |
| Charcoal | 1000 | #1C1811 |

The neutral scale has 15 steps, including its endpoints. Version 0.5 gently warms
every v0.4 scale and solid fill, including the four foundation colors, while
retaining the same role mappings and scale positions. Numbers indicate order,
not equal lightness intervals. Existing color names remain available as aliases.

The warmth adjustment is +0.0015 on Oklab a and +0.006 on Oklab b, with lightness
retained before sRGB rounding. Out-of-gamut colors reduce chroma at fixed
lightness and hue. The source JSON records the conversion and contrast results.

Clay, ochre, moss, and patina are the core accents. Slate and heather are optional.
Text accents use 400 on dark surfaces and 600 on light surfaces. Dedicated solid
fills are paired with ivory text. Faint text is decorative only.

## CSS

Include `thinkinghaus.css`, then use the semantic properties:

```css
body {
  background: var(--th-bg);
  color: var(--th-text-body);
}
a { color: var(--th-link); }
```

Dark is the default. Set `data-theme="light"` on the document root for light mode,
or `data-theme="dark"` for dark mode. The existing `--blog-background`,
`--blog-foreground`, `--blog-body`, and `--blog-muted` aliases are included.
The CSS contains colors only; it does not set typography or layout.

## Figma

Download `thinkinghaus.figma.json` and load the JSON file into **Tokens Studio for
Figma**. This is a Tokens Studio import file, not a native `.fig` document.

It contains a `primitives` set with all scales, fills, and foundation aliases,
plus `dark` and `light` sets with semantic color aliases. Set `primitives` as the
source and enable one mode at a time. Use **Styles & Variables → Export Styles &
Variables** to create Figma colors. The included theme definitions also support
Dark/Light modes when using Tokens Studio's theme export.

Free Tokens Studio accounts can [export token sets](https://docs.tokens.studio/figma/export/token-sets)
as separate collections. [Exporting themes](https://docs.tokens.studio/figma/export/themes)
as modes requires Tokens Studio Pro and a Figma plan that supports those modes.
Keep the other mode disabled when applying colors through token sets.

## Ghostty

Save `ghosttyhaus.conf` locally and include its absolute path from your existing
Ghostty configuration:

```ini
config-file = /absolute/path/to/ghosttyhaus.conf
```

This file includes the established 20px window padding, Paper Mono at size 15,
and 10% additional cell height. Paper Mono must be installed separately; change
the font-family setting to use another font. No fonts are distributed here.

Every terminal color maps to a named palette token. ANSI black now uses neutral
850 (`#3A352A`); ANSI white uses body/neutral 400, and bright white uses ivory/0.
The existing terminal accent assignments are preserved. Web contrast checks do
not certify arbitrary ANSI foreground/background combinations.

## Updating and checking

`thinkinghaus.tokens.json` is the versioned palette data. Regenerate the three
exports together after editing it:

```sh
python3 export.py
python3 export.py --check
```

Publication also updates the canonical Keepinghaus palette documents and admitted
download checksums. The website's CSS, token JSON, and Ghostty downloads match
these versioned files; the Figma download links directly to this repository.

The JSON records 112 exact opaque sRGB contrast pairs. All 106 functional pairs
meet their targets: 4.5:1 for text and 3:1 for focus/control boundaries. Six faint
text pairs are decorative only. Ratios are rounded for display; pass/fail uses
unrounded values. Validate new combinations and translucent colors in context.
