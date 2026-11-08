# apexforge

A Claude Code skill that makes Claude build frontend UI like a design-conscious product team would - complete, responsive, and actually verified in a browser - instead of a rough first draft.

## What it does

Whenever you ask Claude to build/design/redesign a frontend - a landing page, dashboard, form, component, or full app - this skill makes it:

1. **Fill in the unstated obvious stuff.** A "login page" request implies a password-visibility toggle, a forgot-password link, inline validation, and a loading state on submit - even if you didn't ask for those by name. No lorem ipsum, no dead buttons.
2. **Match the existing stack instead of defaulting to React+Tailwind.** If you're dropping a new page into a plain-HTML/CSS project, it stays plain HTML/CSS and reuses your existing color variables. New simple static pages get zero-dependency HTML/CSS/JS. Stateful multi-view apps get a real framework.
3. **Look like a shipped product, not an AI template.** Real color system, consistent spacing/type scale, real icons instead of emoji, hover/focus/active states on everything clickable - and it actively avoids the generic AI-slop tells (centered gradient-blob hero, purple-to-blue gradients, three identical feature cards).
4. **Be responsive from the start.** Mobile-first layout, proper breakpoints, no fixed-width layouts that only work at one size.
5. **Actually verify it works before calling it done.** It launches the result in a real browser (via the `run` skill), checks the console for errors, clicks through every interactive element, and resizes to phone/tablet/desktop widths to confirm nothing breaks - rather than just reading its own code back and assuming it's fine.

### Why it's worth installing

Benchmarked across 3 test cases (a dashboard dropped into an existing plain-HTML site, a login form with validation, and a SaaS pricing page) comparing Claude with this skill vs. without:

| Metric | With skill | Without skill |
|---|---|---|
| Pass rate | 100% | 64% |
| Time | ~644s | ~97s |
| Tokens | ~97.6k | ~56.2k |

It takes longer and costs more tokens - because it's actually opening a browser and checking its work - but it reliably catches real bugs (e.g. a mobile layout overflow, a broken icon-toggle) that the no-skill baseline shipped without noticing, since the baseline never ran what it built.

## Install

The packaged file is `apexforge.skill` (a zip archive) at:
`C:\Users\anees\PycharmProjects\pythonProject\Skills\Apexforge\apexforge.skill`

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
#    (the archive already contains a top-level "apexforge" folder)
Expand-Archive -Path "C:\Users\anees\PycharmProjects\pythonProject\Skills\Apexforge\apexforge.skill" `
                -DestinationPath "$env:USERPROFILE\.claude\skills" -Force
```

Or for project-only install, replace the destination with `<project-root>\.claude\skills`.

You should end up with:
```
~/.claude/skills/apexforge/
└── SKILL.md
```

### Verify it installed

Start (or restart) a Claude Code session in the relevant project and either:
- Ask Claude to list its available skills, or
- Just make a request that should trigger it (e.g. "build me a pricing page") and check that Claude mentions using the `apexforge` skill.

No restart of anything beyond starting a new session is needed - Claude Code reads the skills folder fresh each session.

## Uninstall

Delete the folder: `~/.claude/skills/apexforge/` (or the project-level equivalent).
