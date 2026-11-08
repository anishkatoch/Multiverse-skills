# apexforge

A Claude Code skill that makes Claude build frontend UI - landing pages, dashboards, forms, components, full apps - like a design-conscious product team would, instead of a rough first draft.

## Why we made it

Left to its own defaults, Claude tends to ship frontend work that *reads* fine but hasn't actually been run: missing states it didn't think to add (empty states, loading states, hover/focus states), lorem ipsum left in, a layout that only works at one screen width, and code that was read back and assumed to work rather than actually clicked through in a browser. The gap between "looks right in the diff" and "works when a person uses it" is exactly what this skill exists to close - it forces the same discipline a careful frontend engineer applies by habit: fill in the obviously-implied requirements, match the project's existing stack instead of defaulting to React+Tailwind out of reflex, and verify in a real browser before calling anything done.

## How we made it

`SKILL.md` is a set of instructions Claude reads and follows whenever a request matches building/designing/redesigning a frontend. It was written as a checklist distilled from the concrete ways AI-generated frontend work usually falls short - incomplete implied functionality, mismatched stack choices, generic "AI-slop" visual patterns, non-responsive layouts, and unverified claims of correctness - with one rule per failure mode. It was then benchmarked against the same requests run *without* the skill (see [Results](#results) below) across three representative cases, which is also what the [`evals/`](evals/) folder contains: the prompts, grading criteria, and raw with/without outputs used to validate that the skill actually changes the outcome rather than just changing the words Claude uses to describe it.

## What it does

When this skill triggers, Claude is pushed to make the result:

- **Complete** - fills in the obviously-implied functionality you didn't spell out (a "login page" gets a password-visibility toggle, forgot-password link, inline validation, loading state on submit) and never ships lorem ipsum or dead buttons.
- **Matched to context** - reuses an existing project's stack and CSS/color variables instead of defaulting to React+Tailwind out of habit; picks plain HTML/CSS/JS for simple static pages, a real framework for stateful multi-view apps.
- **Actually well-designed** - a real color system, consistent spacing/type scale, real icons, hover/focus/active states everywhere, and deliberate avoidance of generic AI-slop patterns (gradient-blob hero, purple-to-blue gradients, identical feature cards).
- **Responsive from the start** - mobile-first layout with proper breakpoints, not a fixed-width layout bolted on at the end.
- **Verified, not assumed** - actually launches the result in a browser, checks the console, clicks through every interactive element, and resizes to phone/tablet/desktop before calling the work done.

See [SKILL.md](SKILL.md) for the full instructions Claude follows.

## Example

[examples/nimbus-ai-chat](examples/nimbus-ai-chat) - a chat UI ("Nimbus - AI Chat") built with this skill: light/dark theme toggle persisted via `localStorage`, applied before paint to avoid a flash of the wrong theme.

## Results

Benchmarked (see `../apexforge-workspace/iteration-1/`) across 3 cases - a dashboard added to an existing plain-HTML site, a login form with validation, and a SaaS pricing page - comparing Claude with vs. without this skill:

| Metric | With skill | Without skill |
|---|---|---|
| Pass rate | 100% | 64% |
| Time | ~644s | ~97s |
| Tokens | ~97.6k | ~56.2k |

It costs more time and tokens because it's genuinely opening a browser and testing its own work, but that's also what catches real bugs (a mobile overflow, a broken toggle) that the no-skill baseline shipped without ever noticing - it never ran what it wrote.

## Install

Packaged as `apexforge.skill` (a zip) one level up, at `../apexforge.skill`.

Full install instructions (manual unzip paths, verification, uninstall) are in [../apexforge-INSTALL.md](../apexforge-INSTALL.md).

Quick version: unzip `apexforge.skill` into `~/.claude/skills/` (personal, all projects) or `<project>/.claude/skills/` (just one project) so you end up with `~/.claude/skills/apexforge/SKILL.md`, then start a new Claude Code session.

## Repo layout

```
apexforge/
├── README.md          - this file
├── SKILL.md            - the actual skill Claude reads
├── evals/              - test cases used to benchmark the skill (not needed at runtime)
└── examples/            - sample output built with this skill
    └── nimbus-ai-chat/
```
