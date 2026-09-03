# The mountain that fell

**Nepal, the world's carbon, and the flood of 26 August 2026.**

A data investigation into emissions, responsibility, and the Himalayan debris flow that
killed more than a thousand people in a country responsible for 0.04% of global fossil CO₂.

Live at **<https://flashfloodnepal.com>**.

The report is one self-contained HTML file alongside a social card and icons. No build
step, no dependencies, no third-party image rights — every chart, illustration and icon is
original vector work.

---

## Publishing this on GitHub Pages

The repository is <https://github.com/sureshcyadav/flashfloodnepal>.

In the repository: **Settings → Pages → Build and deployment → Source: Deploy from a
branch**, branch `main`, folder `/ (root)`. The site appears at
<https://sureshcyadav.github.io/flashfloodnepal/> within a minute or two.

`.nojekyll` is included so GitHub serves the files as-is rather than running them through
Jekyll.

### Custom domain

Add a `CNAME` file containing the domain, then point a `CNAME` DNS record at
`<your-username>.github.io`.

---

## What's in the repo

| File | What it is |
| --- | --- |
| `index.html` | the whole report, ~149 KB, self-contained apart from two Google Fonts (Archivo and Source Serif 4), which degrade to system serif/sans if unavailable |
| `og.png` | 1200×630 link card for Facebook, LinkedIn, X, Slack, WhatsApp |
| `og-instagram.png` | 1080×1350 portrait for the Instagram feed |
| `og-story.png` | 1080×1920 for Instagram and Facebook stories, with the lower third left clear for a link sticker |
| `favicon.svg` | primary icon, crisp at any size |
| `favicon.ico` | 16/32/48 fallback for older browsers and `/favicon.ico` probes |
| `favicon-32.png` · `apple-touch-icon.png` | PNG fallback and iOS home-screen icon |
| `CNAME` | the custom domain; deleting it unsets it in GitHub Pages |

The card and icons are generated, not hand-drawn — see **Regenerating the social card** below.

### The report

Nine chapters plus method and sources: the collapse and its geography, the emissions clock,
historical and current responsibility, what Nepal actually built, Himalayan cryosphere
change, the cost of one morning, climate finance against need, five self-imposed
qualifications, and six specific remedies.

### Interactive modules

| Module | Chapter | What it does |
| --- | --- | --- |
| **How fast it travelled** | One | Animates the documented first 22 km of the flow against a clock — 6 min 50 s, 193 km/h average |
| **One dot, one person** | One | 1,003 dots, one per confirmed death, coloured north-to-south by district; click to isolate, or add the 3,916 still missing |
| **The counter** | Two | Live tonne-by-tonne CO₂ counters for the world and Nepal, started on page load |
| **Three ledgers** | Three | The same question — who is responsible — answered by cumulative, current, and per-person emissions |
| **Measure any country against Nepal** | Four | Ten countries against Nepal on CO₂ per person, electricity per person, and EV share |

### Motion

Scroll-triggered reveals, bar charts that grow from their axis, the flood path drawing itself
down the map, a staggered timeline, count-up key figures, hero parallax with drifting mist and
snow, a sticky chapter bar with scroll-spy, and a chapter rail on wide screens.

Every animation is disabled under `prefers-reduced-motion: reduce`, and all content is
readable with JavaScript disabled entirely.

---

## Data integrity

Every figure in the interactive modules is drawn from the datasets already charted and
sourced in the report itself. Two exceptions, both flagged in the module footnotes:

1. **Current-emissions shares** in the three-ledger module are this report's own arithmetic
   from the Chapter Two clock (if the world needs 221 minutes to emit Nepal's annual total
   and China needs 690, China's share is 221 ÷ 690 = 32%). The method reproduces the
   published figures for China and India, and yields 13.2% for the United States and 6.0%
   for the EU.
2. **The 22 km / 6 min 50 s reconstruction** comes from published summaries of the flow. A
   separate Stimson Center analysis gives a different average and a 7.5-minute arrival at
   Rasuwagadhi; the two are not fully consistent, so only the first is animated, and the
   discrepancy is stated in the module.

Casualty figures throughout are the NDRRMA bulletin of 1pm, 1 September 2026 — the last one
published with a district-level breakdown. The ribbon at the top of the page carries the
2 September revision to 1,114. **Check current NDRRMA bulletins before republishing
casualty numbers.**

---

## Regenerating the social card

```bash
pip install pillow
python tools/make-images.py
```

Rebuilds all three social images and all four icons from the palette and mountain geometry
in `tools/make-images.py`. It fetches the Archivo TTFs from Google Fonts on first run into
`tools/.fonts` (gitignored), so the cards use the same typeface as the page.

Only `og.png` is referenced by the page's meta tags. The two Instagram images are hosted so
they can be saved straight to a phone from
<https://flashfloodnepal.com/og-instagram.png> and
<https://flashfloodnepal.com/og-story.png> — Instagram only posts from mobile, and
Instagram ignores Open Graph tags entirely. Both carry the domain as printed text because
Instagram does not make links in captions clickable.

**If you change `og.png`, bump the `?v=` number** on the `og:image` and `twitter:image`
tags in `index.html`. Facebook, LinkedIn, X and Slack cache social cards hard and will
otherwise keep serving the old one for weeks. You can also force a re-fetch through
[Facebook's Sharing Debugger](https://developers.facebook.com/tools/debug/) and
[LinkedIn's Post Inspector](https://www.linkedin.com/post-inspector/).

## Local preview

```bash
python -m http.server 8231
```

Then open <http://127.0.0.1:8231>.

---

## Reuse

The report is offered for free republication. Attribute data to the original sources named in
the Method and Sources section rather than to this document.

Suggested citation:

> *The mountain that fell: Nepal, the world's carbon, and the flood of 26 August 2026.*
> Special report, 2 September 2026.
