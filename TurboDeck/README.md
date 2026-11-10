# TurboDeck

A collection of Claude Code skills. Each skill lives in its own folder with its own `SKILL.md`, README, evals, and packaged `.skill` file - this file is just the index.

## Skills

| Skill | What it does |
|---|---|
| [turbodeck](turbodeck/) | Builds real, polished `.pptx` decks - pitch decks, sales/QBR updates, technical reviews, general-purpose presentations - themed to the company/brand or the user's preference, with content written for a reader who wasn't in the room. See [turbodeck/README.md](turbodeck/README.md). |

More skills will be added here over time, each as a sibling folder next to `turbodeck/`.

## Layout

```
TurboDeck/
├── README.md                  - this file
├── turbodeck/                  - the turbodeck skill
│   ├── SKILL.md
│   ├── README.md
│   ├── scripts/                 - build_deck.py (renderer), check_layout.py, summarize_outline.py
│   ├── references/              - outline schema + theme library
│   ├── evals/                   - benchmark test cases
│   └── examples/                 - sample output built with the skill
├── turbodeck.skill             - packaged turbodeck skill (zip, installable)
├── turbodeck-INSTALL.md        - install/uninstall instructions for turbodeck
└── turbodeck-workspace/        - benchmark run data for turbodeck
```

Each skill added later should follow the same pattern: `<skill-name>/`, `<skill-name>.skill`, `<skill-name>-INSTALL.md`, `<skill-name>-workspace/`.
