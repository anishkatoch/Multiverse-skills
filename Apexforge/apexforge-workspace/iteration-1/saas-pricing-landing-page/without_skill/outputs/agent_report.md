# Agent Report - Flowstack Pricing Page

## What I built
A standalone, self-contained pricing page for "Flowstack" (a workflow-automation tool for small
teams), consisting of three files in this folder:

- `index.html` - page markup and content
- `styles.css` - all styling
- `script.js` - small interactive behaviors

## Sections included
- **Sticky header** with logo mark, nav links, and a "Start free" CTA.
- **Big top CTA / hero section** - headline, subhead, two CTAs (free trial + demo), trial
  fine print, and a lightweight "trusted by" logo strip.
- **Feature strip** (4 short value props) to give context before pricing.
- **Pricing section** with:
  - A working Monthly/Yearly billing toggle (20% "Save" badge) that updates the displayed
    price and billing caption via JS, driven by `data-monthly` / `data-yearly` attributes.
  - Three tiers - **Starter** ($15/user/mo), **Pro** ($39/user/mo, marked "Most popular" and
    visually elevated), **Business** ($79/user/mo) - each with its own feature list and CTA.
- A short "which plan fits" comparison/guidance callout between pricing and FAQ.
- **FAQ section** with 6 questions as an accordion (single-open, animated), covering trials,
  downgrades, what counts as a "run," discounts, security, and integration upgrades.
- **Bottom CTA band** (dark, high-contrast) and a full **footer** with brand blurb, link
  columns, and legal row.

## Design/stack choices
- Plain HTML/CSS/JS - no framework, no build step, no dependencies beyond a Google Fonts
  link (Manrope for UI text, IBM Plex Mono for the small "trusted by" logo row), so it opens
  directly in any browser by double-clicking `index.html`.
- Chose a warm ink/amber/navy palette and a subtle noise overlay specifically to avoid the
  generic "purple gradient + indigo button" AI-template look. The Pro card is set apart with
  a dark navy fill and scale/elevation rather than just a colored border.
- Fully responsive: 4-column feature grid collapses to 2 then 1 column; 3-column pricing
  grid collapses to a single column on tablet/mobile with the featured Pro card re-ordered to
  the top; nav collapses on small screens.
- JS is vanilla, ~50 lines, no inline handlers: handles the billing toggle and the FAQ
  accordion only.

## Verification
I did **not** open the page in an actual browser or run any local server/screenshot tool as
part of this task - I only wrote and visually reviewed the code (HTML structure, CSS rules,
JS logic) by reading it back, and cross-checked that:
- all `data-monthly`/`data-yearly`/`data-monthly-text`/`data-yearly-text` attributes referenced
  in `script.js` exist on the corresponding elements in `index.html`,
- class names referenced in `script.js` (`toggle-btn`, `price-amount`, `plan-billed-as`,
  `faq-item`, `faq-question`, `is-open`) match `styles.css` and `index.html` exactly,
  and HTML tags/attributes are closed and well-formed.

If you want actual rendered/visual confirmation (including the hover states, accordion
animation, and responsive breakpoints), the page should be opened directly in a browser -
no server is required since everything is relative-path, local files.
