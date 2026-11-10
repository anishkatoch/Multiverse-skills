# TurboDeck

A Claude Code skill that builds real, downloadable `.pptx` PowerPoint decks - pitch decks, sales/QBR updates, project reviews, technical/architecture presentations, or anything general-purpose - and writes them so the person reading the deck later, without the presenter in the room, actually understands it correctly.

## What is this for?

TurboDeck is for turning a request like *"make me a deck about X"* into an actual, polished `.pptx` file - not a text outline, not a markdown description of slides, a real file you can open in PowerPoint and hand to someone. It's built for Claude Code (or any Claude surface that supports skills) to use automatically whenever a presentation is needed, so you don't have to hand-build slides yourself or describe every visual detail.

**Use it whenever you want:**
- A pitch deck ("build me a seed-round pitch deck for my startup")
- A sales, QBR, or leadership-sync update ("put our Q3 numbers into slides for the team")
- A project or status review ("make a deck recapping this quarter's retro")
- A technical/architecture presentation ("I need to present this migration to engineering")
- Any general-purpose explainer deck, in any language, about any topic

You don't need to say "PowerPoint" or "pptx" explicitly - just describe the deck and what it's for. Claude picks the theme, structure, and content automatically and hands you back a finished file.

## What it actually does

1. **Understands the full ask first.** Covers every part of the topic you described, asks about audience/detail-level only when genuinely ambiguous, and defaults to short/crisp content unless you ask for more detail.
2. **Picks a theme that fits, not a default.** Matches a company's real brand colors when the deck represents a specific company, or picks from a small theme library (see below) based on context - defaulting to a light theme unless a dark/moody mood was actually asked for - and says which one it picked and why. Every slide in the deck shares the exact same background color; a thin gradient accent bar, a title underline, and (on the title slide) a soft corner accent are the only color accents, never a full-background swap mid-deck.
3. **Gets the narrative order right.** Defaults to establishing *what this is* before *why it matters* before *what we found/propose* before *what's next* - the order a cold reader needs, not the order it's easiest to write in.
4. **Writes for the reader who wasn't in the room.** Short, skimmable bullets; KPI call-outs with numbers instead of vague claims, each in a compact, visually-weighted card and paired with a one-line takeaway; plain professional English; a sharp one-line hook opening each section instead of a flat title restatement; no generic "Thank You"/"Questions?" closing with nothing behind it.
5. **Only uses a real chart (line/bar/column/pie, with real data labels and a legend) when you asked for one, or gave it real multi-point data.** It won't invent an "illustrative" chart just because a topic could theoretically be visualized - a single number is a `kpi` card, a list of qualities is bullets.
6. **Catches and flags source-material errors.** If the notes/draft you hand it have an inconsistency or obvious typo, it fixes it and tells you what changed, rather than repeating the error - and never invents a number or fact it wasn't given.
7. **Actually builds and verifies the file.** Uses the bundled `scripts/build_deck.py` (python-pptx) so every slide stays visually consistent, reopens the generated `.pptx` to confirm the content landed, and runs `scripts/check_layout.py` to catch text that's technically present but too long for its box.
8. **Checks the result against the actual request, not just that it built cleanly.** Uses `scripts/summarize_outline.py` for a compact slide-by-slide view and checks it point by point against what was asked - every explicit instruction, every implied expectation, whether a theme or chart choice still holds up - and fixes/rebuilds anything that's off instead of shipping a deck that renders fine but misses the ask.
9. **Matches the language of the request.** Writes the deck in whatever language you asked in or asked for (including non-Latin scripts), picking a font that actually renders that script.

## Themes

| Theme | Best for |
|---|---|
| `corporate-blue` | Safe default for business/sales/QBR decks and most companies with a blue-leaning or unspecified brand |
| `warm-startup` | Pitch decks, culture/people decks - energetic and approachable rather than corporate |
| `minimal-mono` | Editorial, design-forward, or leadership-review decks where content should carry the weight |
| `technical-slate` | Architecture reviews, engineering deep-dives, incident postmortems |
| `modern-dark` | The one all-dark-background preset - only used when a dark/moody/premium feel is explicitly asked for |

Every slide in a deck uses the exact same background from whichever theme is picked - color only shows up as accents (a gradient bar, a title underline, a KPI card's accent chip, chart colors), never as a full-slide background swap partway through. If a specific company's brand colors are known, an inline custom theme can be built to match them instead of using a preset.

## Slide layouts available

| Layout | Use |
|---|---|
| `title` | Deck opener - title, subtitle, one-line hook |
| `section` | Section divider between parts of a longer deck |
| `content` | The workhorse slide - title, optional hook, bullets |
| `kpi` | A row of metric cards (value + label + optional delta), with a takeaway |
| `chart` | A real line/bar/column/pie chart with data labels and a legend - only for real, given data |
| `two-column` | Side-by-side comparison (e.g. "before vs. after," "handles directly vs. escalates") |
| `quote` | A pull-quote slide |
| `closing` | Final slide - a real next step/ask, never a bare "Thank You" |

## Example

`examples/q3-retention-review/` has a sample outline (`outline.json`) and the deck it produces (`q3-retention-review.pptx`) - a 6-slide internal update using the `corporate-blue` theme, showing the title/section/content/kpi/two-column/closing layouts in use.

## Files

```
turbodeck/
├── SKILL.md                      - the skill itself (full instructions Claude follows)
├── README.md                     - this file
├── scripts/
│   ├── build_deck.py             - outline JSON -> .pptx (python-pptx)
│   ├── check_layout.py           - heuristic check for text overflowing its box
│   └── summarize_outline.py      - compact slide-by-slide view for auditing against the request
├── references/
│   ├── outline-schema.md         - the JSON format build_deck.py reads
│   └── themes.json               - the theme preset library
├── examples/
│   └── q3-retention-review/      - sample outline + generated deck
└── evals/                        - benchmark test cases
```

## Requirements

- Claude Code (or another Claude surface that supports skills)
- `python-pptx` installed in the environment Claude runs commands in: `pip install python-pptx`

## Install

The packaged file is `turbodeck.skill` (a zip archive), a sibling of this skill's parent folder:
`TurboDeck/turbodeck.skill`

### Option A - "Save skill" button (if offered)

If you're handed the `.skill` file inside a Claude surface that renders a file card with a **Save skill** button (e.g. Claude Code in some environments, Cowork), just click it. That's the whole install - skip everything below.

### Option B - Manual install (Claude Code, any OS)

A skill is just a folder containing `SKILL.md`. Claude Code looks for skill folders in two places:

- **Personal** (available in every project you open): `~/.claude/skills/`
- **Project-only** (available only inside one repo): `<project-root>/.claude/skills/`

**On Windows (PowerShell):**

```powershell
# 1. Make the destination folder if it doesn't exist
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null

# 2. Unzip the .skill file directly into ~/.claude/skills
#    (the archive already contains a top-level "turbodeck" folder)
Expand-Archive -Path "<path to>\turbodeck.skill" `
                -DestinationPath "$env:USERPROFILE\.claude\skills" -Force
```

**On macOS/Linux:**

```bash
mkdir -p ~/.claude/skills
unzip -o "<path to>/turbodeck.skill" -d ~/.claude/skills
```

For a project-only install instead, replace the destination with `<project-root>/.claude/skills`.

You should end up with:

```
~/.claude/skills/turbodeck/
├── SKILL.md
├── README.md
├── scripts/
│   ├── build_deck.py
│   ├── check_layout.py
│   └── summarize_outline.py
├── references/
└── examples/
```

### Verify it installed

Start (or restart) a Claude Code session and either:
- Ask Claude to list its available skills and confirm `turbodeck` appears, or
- Make a request that should trigger it (e.g. "build me a deck on our Q3 numbers") and check that Claude mentions using the `turbodeck` skill.

No restart beyond starting a new session is needed - Claude Code reads the skills folder fresh each session.

### Uninstall

Delete the folder: `~/.claude/skills/turbodeck/` (or the project-level equivalent).
