---
name: turbodeck
description: Build real, polished .pptx PowerPoint decks - pitch decks, sales/QBR decks, project updates, technical/architecture reviews, or any general-purpose presentation. Use this whenever the user asks for a "presentation," "deck," "slides," or "pptx," or describes something that should become one (e.g. "put this update into slides for my team", "make a deck explaining our Q3 numbers", "I need to present this architecture to the team"), even if they don't say "PowerPoint" explicitly. Produces a real downloadable .pptx file via a bundled python-pptx script, with a theme matched to the company/brand or the user's stated preference, crisp audience-ready content (not walls of text), correct narrative ordering (what before why), and content the audience can understand without the presenter in the room.
---

# TurboDeck

Goal: when this skill triggers, the user should get a deck they can actually hand to someone else - a boss, a client, a room of engineers - and that person should understand it correctly **without the user standing there explaining it**. That's the test for every slide: if the presenter weren't in the room, would the next reader get it right?

## 1. Understand the request before writing anything

Before touching the outline, make sure you know:

- **Topic and purpose** - what is this deck for (inform, pitch, review, decide)? Cover every part of the topic the user described - don't quietly drop a section because it's harder to summarize. If the request implies sections the user didn't spell out (a "pitch deck" implies problem, solution, market, and an ask, even if they only said "make me a pitch deck for X"), include them.
- **Audience** - who reads this when the presenter isn't talking them through it? A deck for the person's own team reads differently than one for an external client or executive.
- **Detail level** - if the user says "make it detailed" or "keep it short," build to that explicitly. If they don't say, default to **short and crisp**: this skill exists because the audience should be able to scan a slide and get the point, not read a memo. When the user wants detail that would clutter a slide, put the long version in `notes` (speaker notes) and keep the slide itself scannable - that way both the short-slide reader and the fuller record exist in the same file.
- **Source material accuracy** - if the user hands you notes, numbers, or a rough draft to turn into slides, treat it as raw material, not gospel. If something in it is internally inconsistent, factually off, or clearly a typo (a date that doesn't match the quarter being discussed, a percentage that doesn't add up, a name spelled two ways), fix it and say what you changed and why - don't silently ship a deck repeating an error, and don't silently "correct" something that might be an intentional stylistic choice without flagging it.

If the request is genuinely ambiguous on one of these (especially audience or detail level), ask one focused question. Don't ask about things you can reasonably default (which theme preset, exact wording, slide count) - make a good call and say what you picked.

## 2. Pick a theme that fits who this is for

Don't default to the same blue-corporate look for everything. `references/themes.json` has presets (`corporate-blue`, `modern-dark`, `minimal-mono`, `warm-startup`, `technical-slate`) - read it once to see the full palette/font of each before picking.

- **If the deck represents a specific company** (the user's employer, a client, a prospect) - look for that company's actual brand: ask the user for their brand colors/logo if you don't have them, or check for them in the project/workspace (a style guide, an existing deck, a website if you have browsing available) rather than guessing. When you find real brand colors, build an inline theme object (see `references/outline-schema.md`) matching them instead of forcing a preset.
- **If it's personal or informal** (a side project, an internal update with no brand requirement) - ask what mood fits, or pick based on context: `warm-startup` for something energetic and early-stage, `minimal-mono` for something that should feel serious and understated.
- **If it's technical** (architecture review, engineering deep-dive, postmortem) - `technical-slate` is built for dense KPI grids and staying legible next to diagrams/code.
- **Default to a light preset when nothing points elsewhere.** `corporate-blue`, `warm-startup`, `minimal-mono`, and `technical-slate` all keep the background on every single slide the same light/white tone - color is used as an accent (a title's color, a KPI number, a chart, a thin accent bar), never as a full-slide background swap partway through the deck. That's the safer default for ordinary business/explainer content, and it's also just correct: every layout (including `section` and `closing`) renders on the theme's one `bg` color, by design - the deck should never look like two different themes stitched together.
- **`modern-dark` is the one preset that puts a dark background on every slide instead of a light one** - it's internally just as consistent (every slide is still the same one background color), it's simply a dark color rather than a light one. Reach for it only when the user explicitly asks for a dark/moody/premium feel, or the deck is unmistakably a flashy investor-reveal where that's the convention - never just because the topic happens to be "tech" or "product." Inferring "tech topic -> dark theme" is a real mistake this skill has made before: it turns an ordinary explainer into something that looks like a nightclub, which is the opposite of what most requesters want. If you're not sure, pick light.

Say in one line which theme you picked (or what brand colors you matched) and why, so the user isn't surprised.

## 3. Structure the narrative so it reads in the right order

Readers get lost when a deck explains *why something matters* before establishing *what it even is*. As a default spine - adapt it, don't force it onto content where it doesn't fit:

1. **What this is** - establish the subject/context first. A reader who just opened the deck needs to know what they're looking at before they can care about it.
2. **Why it matters** - the stakes, the problem, the opportunity - now that they know what it is.
3. **What we found / did / propose** - the substance: the data, the plan, the architecture.
4. **What it means / what's next** - the takeaway and the ask.

Each section slide or content slide should open with a **hook** - one sharp line (a stat, a question, a tension) that earns the reader's attention, not a flat restatement of the title. "Churn dropped for the first time in four quarters" is a hook; "This slide is about churn" is not.

The closing slide gets the same standard. "Thank You" or "Questions?" with nothing else is the slide equivalent of a flat title restatement - it fills the `closing` layout's space without telling the reader anything. Give the close a real title and `bullets` that are an actual next step, ask, or takeaway (see step 4 for the "what we found -> what's next" shape), and only add a courtesy line like thanks or contact info as a small addition to that, never as the whole slide.

## 4. Write content for the reader who wasn't in the room

This is the main discipline this skill exists to enforce:

- **Bullets are cues, not paragraphs.** Each bullet should be one clear idea a reader can absorb in a glance - the builder script warns (doesn't block) on bullets over ~110 characters as a sanity check, but aim well under that by habit.
- **Use KPIs/numbers wherever the slide is making a claim that has a number behind it.** "Churn improved" is vague; the `kpi` layout with "3.1%, -1.0pt QoQ" is what lets a reader who wasn't in the meeting trust the claim. Always pair a KPI row with a one-line `takeaway` - the number alone doesn't tell a cold reader what it means, the takeaway does.
- **Plain, professional English.** Avoid jargon the audience may not share; if a technical term is necessary (even for a technical deck), use it but don't stack three in one bullet. Write like you're briefing a smart colleague, not writing an abstract.
- **Self-contained slides.** A reader flipping to slide 7 out of order, or seeing it screenshotted into a chat, should be able to tell what it's claiming without the slides around it.
- **Only build a `chart` when the user actually asked for one, or gave you real multi-point data to show.** This skill got this wrong before by reaching for a chart on its own initiative - inventing an "illustrative" pie split or trend just because a slide's topic could theoretically be visualized. Don't do that. A chart is for data: the user's own numbers across months, categories, or a breakdown they gave you, or an explicit "make me a chart/graph of X." If you don't have real data and the user didn't ask for a chart, don't manufacture one to fill the slide - use a `kpi` card for a single standout number, or plain `bullets` for anything qualitative. A deck with zero charts is the right, unremarkable outcome for most requests; a chart is the exception that needs a reason, not a default you reach for because the layout exists.
- **When you do have real data with a shape** - the user's own numbers trending over months, or a comparison across several categories - that's exactly when `chart` earns its place over bullets (line for trends over time, column/bar for comparing categories, pie only for a simple part-of-whole split with real figures). The builder always adds real data labels/percentages and a properly-colored legend to any chart you build - you don't need to also restate the same numbers in a bullet underneath it.
- **Use a `kpi` card readily whenever a number is the point of the slide**, even just one number - a single standout figure in its own card reads as more important than the same figure sitting mid-sentence in a bullet. Don't reserve `kpi` only for slides with three-plus metrics side by side; one real, well-chosen number in a card is still worth the emphasis.
- **Use the vocabulary the audience's domain actually uses**, on chart axes/series names and everywhere else - mirror the terms already present in the user's notes or request rather than generic labels. A SaaS/startup deck earns MRR, ARR, CAC, LTV, churn, NRR; an engineering deck earns deploy frequency, MTTR, latency, throughput; a finance/ops deck earns revenue, margin, EBITDA, burn. If the user's own notes mix registers (some business terms, some technical), match that mix instead of flattening it into one vocabulary - they know their audience better than a default would.
- **Match the language of the request.** Default to plain, simple English. If the user writes to you in another language, or asks for the deck in one (including a regional Indian language or an Indian-English register), write the slide content in that language natively - meaning the way a fluent speaker would actually phrase a hook or a takeaway, not a literal word-for-word translation - while keeping every other discipline in this section (short bullets, KPI-with-takeaway, hooks, narrative order) exactly the same. If the script needs a font the theme's default doesn't cover well, say so and pick a font with better coverage for that script.

## 5. Build it

Read `references/outline-schema.md` for the exact JSON shape, then write an outline file and run:

```
python scripts/build_deck.py outline.json output.pptx
```

Don't hand-roll python-pptx calls directly - the script keeps every slide's color, spacing, and type consistent, and its warnings (stderr) catch long bullets, long KPI labels, and decks that have gotten too long for one sitting (>25 slides) before the user does.

## 6. Verify before calling it done

Reopen the generated file and sanity-check it rather than assuming the outline rendered the way you intended:

```python
from pptx import Presentation
p = Presentation("output.pptx")
for i, s in enumerate(p.slides, 1):
    print(i, [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.text_frame.text])
```

Then run the layout checker, which catches the thing the text dump above can't - text that's technically present but too long for its box:

```
python scripts/check_layout.py output.pptx
```

This is a heuristic (python-pptx has no real layout engine, so it estimates line count from box width/font size/character count) - treat a flag as "go look at this slide," not certain proof, but don't ignore it either. Confirm: the slide count and order match the narrative spine you intended, no slide's text frame is empty where content was meant to be, and every warning from either the build script or the layout checker has been addressed (shortened a bullet, trimmed a KPI label, split an overloaded slide, or - rarely - confirmed the flag was a false positive and the slide is genuinely fine).

## 7. Check it against what was actually asked - fix or redesign whatever's off

Steps 1-6 catch "does this deck render correctly." This step catches something more important and easier to miss: "is this actually the deck the user asked for." A deck with zero layout warnings can still be the wrong deck - wrong theme for the context, a topic quietly dropped, the wrong detail level, data that doesn't match what was given, or a chart where a KPI card would've served the claim better (or vice versa).

Run this for a compact slide-by-slide view instead of re-reading the whole text dump:

```
python scripts/summarize_outline.py outline.json
```

Then go back to the original request and check it point by point against that summary, not against your memory of what you intended to build:

- **Every explicit instruction shows up.** A topic they named, a number or fact they gave you, a theme/mood preference, "keep it tight" vs. "make it detailed," a specific chart or comparison they asked to see, the language they asked for - each one should be traceable to a specific slide in the summary. If you can't point to where an instruction landed, it probably didn't.
- **Every implied expectation from step 1 is really there** - the standard arc for this kind of deck, the audience-appropriate vocabulary, KPIs paired with takeaways - not just planned in your head while you were writing the outline.
- **The design choices still make sense on a second look.** Does the theme actually fit, now that the content is in front of you? If a slide has a `chart`, does it still meet step 4's bar - real, user-given data with an actual trend/comparison shape - or did one sneak in for data that's really just a single before/after pair better served by a `kpi` card? Never go the other direction and add a chart here that wasn't already justified in step 4, even if the data would technically plot.

If anything's missing, mismatched, or the design choice doesn't hold up, **fix the outline and rerun `build_deck.py`** - don't paper over the gap by explaining it away in the hand-back message. This is the same instinct as "reading the code back is not verification": a deck that builds cleanly and passes the layout checker can still fail to be the deck that was actually asked for, and that failure matters more than a cosmetic one.

## 8. Hand it back

Tell the user, briefly: the theme you chose and why, the detail level you built to (and that you can expand/shrink specific sections if that's wrong), and any corrections you made to source material and why. If a section couldn't be filled in because the information wasn't available, say so rather than inventing numbers or claims to fill the gap.
