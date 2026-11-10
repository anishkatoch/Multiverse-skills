# Multiverse Skills

A collection of Claude Code skill packs. Each top-level folder is its own skill pack with its own README, SKILL.md, evals, and packaged `.skill` file.

## Skill packs

| Pack | What it does |
|---|---|
| [Apexforge](Apexforge/) | Builds polished, fully responsive frontend UI - landing pages, dashboards, forms, components, full apps - and verifies it actually works in a browser before calling it done. See [Apexforge/README.md](Apexforge/README.md). |
| [TurboDeck](TurboDeck/) | Builds real, polished `.pptx` decks - pitch decks, sales/QBR updates, technical reviews, general-purpose presentations - themed to the company/brand or the user's preference. See [TurboDeck/README.md](TurboDeck/README.md). |

More packs will be added here over time, each as a sibling folder next to `Apexforge/` and `TurboDeck/`.

## Layout

```
Multiverse_Skills/
├── README.md              - this file
├── CLAUDE.md               - repo rules for Claude Code
├── Apexforge/              - frontend UI builder skill pack
└── TurboDeck/              - PowerPoint deck builder skill pack
```

Each pack follows the same internal pattern: `<pack>/README.md`, `<skill-name>/`, `<skill-name>.skill`, `<skill-name>-INSTALL.md`, `<skill-name>-workspace/`.

## Rules

See [CLAUDE.md](CLAUDE.md) for the hard rules Claude Code follows in this repo (no em dashes, no AI attribution in commits or docs).
