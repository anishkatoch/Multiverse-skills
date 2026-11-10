# turbodeck

A Claude Code skill that builds real `.pptx` decks - themed to the right brand/mood, structured in the order a cold reader needs, and written so the person reading it later understands it correctly without the presenter in the room.

## What it does

Whenever you ask Claude for a presentation, deck, slides, or pptx - a pitch deck, a QBR/sales update, a project review, a technical/architecture walkthrough, or anything general-purpose - this skill makes it:

1. **Cover the full ask and ask about audience/detail only when genuinely unclear.** Defaults to short, crisp content; expands into more detail (and speaker notes) only if you ask for it.
2. **Pick a theme deliberately, defaulting to light.** Matches a company's real brand colors when the deck represents a specific company, or chooses from a small theme library (`corporate-blue`, `modern-dark`, `minimal-mono`, `warm-startup`, `technical-slate`) based on context, reserving the one all-dark preset for when dark/moody was actually asked for - and tells you which one and why. Every slide shares one consistent background; color shows up only as a gradient accent bar, a title underline, and a soft corner accent, never a full-background swap partway through the deck.
3. **Get the story order right.** Establishes *what this is* before *why it matters* before *what we found/propose* before *what's next*, with a sharp one-line hook opening each section - and a real closing slide with a next step, never a bare "Thank You."
4. **Write for a reader who wasn't in the room.** Skimmable bullets, KPI call-outs with real numbers in a visually-weighted card and a one-line takeaway instead of vague claims, plain professional English.
5. **Only chart real data you were actually given or asked to chart.** It won't invent an "illustrative" chart just because a topic could be visualized - every chart it does build gets real data labels/percentages and a properly-colored legend automatically.
6. **Flag and fix errors in source material** instead of silently repeating a typo or inconsistency you were handed.
7. **Build a real file and check it.** Uses bundled python-pptx scripts for visual consistency, reopens the generated `.pptx` to verify the content landed, and runs a layout checker that catches text too long for its box.
8. **Double-check the result against what you actually asked for.** Compares the built deck point by point against your request - every topic, number, theme preference, and detail-level instruction - and fixes or rebuilds anything that's off rather than shipping a deck that renders cleanly but misses the ask.

## Install

The packaged file is `turbodeck.skill` (a zip archive) at:
`C:\Users\anees\PycharmProjects\pythonProject\Skills\TurboDeck\turbodeck.skill`

### Option A - "Save skill" button (if offered)
If you're handed the `.skill` file inside a Claude surface that renders a file card with a **Save skill** button (e.g. Claude Code in some environments, Cowork), just click it. Skip everything below.

### Option B - Manual install (Claude Code, any OS)

A skill is just a folder containing `SKILL.md`. Claude Code looks for skill folders in two places:

- **Personal** (available in every project): `~/.claude/skills/`
- **Project-only** (available only in this repo): `<project-root>/.claude/skills/`

Steps for personal install on Windows:

```powershell
# 1. Make the destination folder if it doesn't exist
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null

# 2. Unzip the .skill file directly into ~/.claude/skills
#    (the archive already contains a top-level "turbodeck" folder)
Expand-Archive -Path "C:\Users\anees\PycharmProjects\pythonProject\Skills\TurboDeck\turbodeck.skill" `
                -DestinationPath "$env:USERPROFILE\.claude\skills" -Force
```

Or for project-only install, replace the destination with `<project-root>\.claude\skills`.

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

### Requirements

`python-pptx` must be installed in the environment Claude runs commands in: `pip install python-pptx`.

### Verify it installed

Start (or restart) a Claude Code session in the relevant project and either:
- Ask Claude to list its available skills, or
- Just make a request that should trigger it (e.g. "build me a deck on our Q3 numbers") and check that Claude mentions using the `turbodeck` skill.

No restart of anything beyond starting a new session is needed - Claude Code reads the skills folder fresh each session.

## Uninstall

Delete the folder: `~/.claude/skills/turbodeck/` (or the project-level equivalent).
