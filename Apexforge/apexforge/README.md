# apexforge

A Claude Code skill that makes Claude build frontend UI - landing pages, dashboards, forms, components, full apps - like a design-conscious product team would, instead of a rough first draft.

## Why we made it

Left to its own defaults, Claude tends to ship frontend work that *reads* fine but hasn't actually been run: missing states it didn't think to add (empty states, loading states, hover/focus states), lorem ipsum left in, a layout that only works at one screen width, and code that was read back and assumed to work rather than actually clicked through in a browser. The gap between "looks right in the diff" and "works when a person uses it" is exactly what this skill exists to close - it forces the same discipline a careful frontend engineer applies by habit: fill in the obviously-implied requirements, match the project's existing stack instead of defaulting to React+Tailwind out of reflex, and verify in a real browser before calling anything done.

## How we built it

A Claude Code skill is nothing exotic: it is a folder with a `SKILL.md` file in it, and Claude reads that file's instructions whenever a request matches what the skill says it covers. Here is the actual process we followed, step by step, for anyone who wants to build their own.

1. **Pick one narrow trigger, not a vague topic.** Not "frontend stuff" but "a request to build, design, redesign, or improve a UI." A skill that tries to cover everything never triggers reliably and never gives focused instructions.
2. **List the concrete ways work in that area usually falls short.** We did not start from "be a good frontend engineer." We started from specific failure modes we had actually seen: implied requirements left out (a "login page" with no forgot-password link), defaulting to React+Tailwind out of habit instead of matching the existing project, generic AI-slop visuals (gradient-blob hero, purple-to-blue gradient, three identical feature cards), layouts that only work at one screen width, and code that was read back and assumed to work instead of actually run.
3. **Turn each failure mode into one rule, not a paragraph of vague advice.** `SKILL.md` has one numbered section per failure mode (see [SKILL.md](SKILL.md)), each with a concrete example of the mistake and what to do instead. A rule that just says "write good code" does not change behavior; a rule that says "a login page implies a password-visibility toggle and a loading state on submit, even if the user did not ask" does.
4. **Write the YAML frontmatter description to match how people actually phrase the request.** Claude decides whether to load a skill based on the `description` field, so it has to cover the phrasing people use ("build me a pricing page," "design a dashboard for X") and not just the formal name of the task.
5. **Build small test cases before trusting it works.** The [`evals/`](evals/) folder holds three representative requests (a dashboard dropped into an existing plain-HTML site, a login form with validation, a SaaS pricing page), each with a `prompt.md` describing the request and `graders/` files describing what a passing result looks like.
6. **Run each case twice, with the skill and without it, and compare.** This is the only way to know the skill actually changes the outcome rather than just changing the words used to describe the outcome. Our with/without results are in `../apexforge-workspace/iteration-1/` and summarized in [Results](#results) below.
7. **Package it and write install instructions.** Zip the skill folder into a `.skill` file and write down exactly where it needs to be unzipped (`~/.claude/skills/` for personal use, `<project>/.claude/skills/` for one project) so someone else can install it without guessing. See [Install](#install) below.

That is the whole recipe: narrow trigger, list real failure modes, one rule per failure mode, test cases, with/without comparison, package and document. Nothing about it is specific to frontend work, so the same process is how we plan to build the next skills in this [repo](../README.md).

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
