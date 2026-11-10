# Outline JSON schema

`scripts/build_deck.py outline.json output.pptx` reads this format. Write the outline file yourself (don't hand-build the .pptx with raw python-pptx calls - the script already handles layout, color, and font so every slide stays visually consistent).

Top level:

```json
{
  "title": "Deck title (used as fallback for the title slide)",
  "theme": "corporate-blue",
  "slides": [ ... ]
}
```

`theme` is either the name of a preset in `references/themes.json` (`corporate-blue`, `modern-dark`, `minimal-mono`, `warm-startup`, `technical-slate`), or an inline object with the same keys (`bg`, `bg_alt`, `primary`, `accent`, `text`, `text_muted`, `heading_font`, `body_font`) when you've matched the deck to a specific company's actual brand colors/fonts instead of a preset.

## Slide layouts

Every slide object needs a `layout` key. All layouts accept an optional `"notes"` string, which becomes the slide's speaker notes - put supporting detail there when the slide itself needs to stay short.

- **`title`** - deck opener. `title`, `subtitle`, `hook` (one line above the title - a sharp question or stat, not a generic tagline).
- **`section`** - a section divider, on the theme's normal background with an accent bar and colored heading (same background as every other slide - not a full-bleed color swap). `title`, optional `number` ("01"), `subtitle`.
- **`content`** - the workhorse slide. `title`, optional `kicker` (small label above the title, e.g. "PROBLEM"), optional `hook` (one-line framing sentence), `bullets` (list of strings, or `{"text": "...", "level": 0|1|2}` for sub-bullets).
- **`kpi`** - a row of metric cards. `title`, `kpis`: list of `{"label": "...", "value": "...", "delta": "..."}` (delta is optional, e.g. "+18% YoY") - needs at least one entry, the script raises a clear error otherwise. Optional `takeaway` line below the cards - say in one sentence what the numbers mean, don't make the reader infer it.
- **`chart`** - a real chart, for anything that's a trend over time or a comparison across several categories (a single before/after pair is usually clearer as `kpi`). `title`, `chart_type` (`"line"` for trends over time, `"column"`/`"bar"` for comparing categories, `"pie"` only for a simple part-of-whole breakdown with a handful of slices), `categories` (x-axis labels, or slice labels for a pie), `series` (list of `{"name": "...", "values": [...]}}` - needs at least one entry, and keep it to 4 or fewer, more gets unreadable on a slide), optional `y_axis_title`, optional `takeaway` (say what the chart means, same reasoning as `kpi`).
- **`two-column`** - side-by-side comparison. `title`, `left`/`right`: each `{"title": "...", "bullets": [...]}`.
- **`quote`** - a pull-quote slide. `text`, optional `attribution`.
- **`closing`** - final slide (same background and accent-bar treatment as `section`). `title`, optional `bullets` (next steps / ask - never leave this as a bare "Thank You"/"Questions?" with nothing else), optional `contact`.

## Writing the content that goes into this schema

The schema is just plumbing. See `SKILL.md` for how to actually decide what goes on each slide - narrative order, how much to write per bullet, when to use `kpi`/`chart` vs `content`, matching the audience's domain vocabulary, and matching the request's language.

## Non-Latin scripts

The preset `heading_font`/`body_font` values (Calibri, Segoe UI, Georgia, Verdana, Consolas) cover Latin scripts well but not others. If the deck's content is in a script those don't render well (Devanagari, Arabic, CJK, etc.), override `heading_font`/`body_font` in an inline theme object with a font known to support that script (e.g. "Nirmala UI" for Devanagari on Windows) rather than leaving the preset's Latin font in place.
