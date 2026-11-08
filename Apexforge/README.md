# Apexforge

A collection of Claude Code skills. Each skill lives in its own folder with its own `SKILL.md`, README, evals, and packaged `.skill` file - this file is just the index.

## Skills

| Skill | What it does |
|---|---|
| [apexforge](apexforge/) | Builds polished, fully responsive frontend UI - landing pages, dashboards, forms, components, full apps - and verifies it actually works in a browser before calling it done. See [apexforge/README.md](apexforge/README.md). |

More skills will be added here over time, each as a sibling folder next to `apexforge/`.

## Layout

```
Apexforge/
├── README.md                  - this file
├── apexforge/                   - the apexforge skill
│   ├── SKILL.md
│   ├── README.md
│   ├── evals/                  - benchmark test cases
│   └── examples/                - sample output built with the skill
├── apexforge.skill              - packaged apexforge skill (zip, installable)
├── apexforge-INSTALL.md         - install/uninstall instructions for apexforge
└── apexforge-workspace/         - benchmark run data for apexforge
```

Each skill added later should follow the same pattern: `<skill-name>/`, `<skill-name>.skill`, `<skill-name>-INSTALL.md`, `<skill-name>-workspace/`.
