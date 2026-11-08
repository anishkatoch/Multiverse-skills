---
name: apexforge
description: Build polished, professional, fully responsive frontend UI - landing pages, dashboards, apps, components, forms, or full sites. Use this whenever the user asks to build, design, create, redesign, or improve a frontend, UI, page, screen, dashboard, landing page, website, or web app, even if they don't use the word "frontend" explicitly (e.g. "make me a pricing page", "build a signup form", "design a dashboard for X"). Produces detailed, bug-free, mobile/tablet/desktop-responsive UI with real content instead of placeholders, verified by actually running the result in a browser before calling it done.
---

# Apexforge

Goal: when this skill triggers, the user should get a frontend that looks like a real product shipped by a design-conscious team - not a rough draft. That means three things hold at once: it's **complete** (every piece of functionality and content the user described is actually there, not stubbed out), it's **responsive** (works cleanly on mobile, tablet, and desktop without the user asking), and it's **verified working** (you've actually run it and clicked through it, not just read the code and assumed).

## 1. Understand what "everything the user wants" means

Before writing code, make a quick mental list of every screen, section, state, and interaction implied by the request - including the ones the user didn't spell out but would obviously expect. A "login page" implies a password-visibility toggle, a "forgot password" link, inline validation errors, and a loading state on submit, even if the user only said "make a login page." A "dashboard" implies empty states (no data yet) and not just the happy path with fake numbers.

If the request is genuinely ambiguous about scope (e.g. "build me a frontend for my app" with no detail on what the app does), ask one focused question rather than guessing wildly - but don't ask about things you can reasonably infer or default (visual style, exact copy, color choices). Default to filling those in yourself with good, real-feeling content. Never ship placeholder text like "Lorem ipsum," "Section title here," or a button that does nothing - if a feature can't be made fully real (e.g. it needs a backend that doesn't exist), implement the frontend behavior as far as it can go (local state, mock data, visual feedback) rather than leaving a dead element.

For apps people spend real time in - chat interfaces, dashboards, editors, anything with a settings/account area - a light/dark theme toggle is one of these implied expectations, not a nice-to-have to wait for a request. Default the theme to the user's OS preference (`prefers-color-scheme`), let them override it, and persist that choice (`localStorage` is fine for a frontend-only build) so it survives a reload. A one-off static landing page usually doesn't need this - use judgment based on whether the thing being built is a "visit once" page or a "come back to repeatedly" app.

## 2. Pick the stack by matching context, not habit

Don't default to React+Tailwind out of reflex. Look at what you're dropping into:

- **Existing project**: check `package.json`, existing component files, and whatever CSS approach is already in use (Tailwind config, CSS modules, styled-components, plain CSS). Match it. Introducing a second styling system into a codebase that already has one creates exactly the kind of mess this skill exists to avoid.
- **New, simple, mostly-static page** (landing page, single form, a one-off tool): plain HTML/CSS/JS is often the right call - it's zero-dependency, loads instantly, and is easy for the user to drop anywhere.
- **New, stateful, multi-view app**: a component framework (React is the safe default, but match what the user mentions - Vue, Svelte, etc. - if they name one) pays for itself.

Whatever you choose, say which one you picked and why in one line, so the user isn't surprised.

## 3. Design like it's going to be judged

Read the `artifact-design` and `dataviz` skills' underlying principles even if you're not publishing an Artifact - they apply just as much to project code: a real color system (not a dozen ad-hoc hex values), a consistent spacing scale, deliberate typography (don't mix more than 2 font families), and visual hierarchy that makes the most important action on each screen obvious at a glance. Generic AI-slop tells: centered hero text with a vague gradient blob, purple-to-blue gradients, three identical feature cards with the same icon style, buttons with no hover/focus/active states. Avoid all of these by default - be opinionated about layout instead of falling back on the safest, blandest template. Use real icons (inline SVG or an icon library already in the project) instead of emoji as UI icons.

Interactive states are not optional polish - they're part of "no bugs." Every clickable element needs a visible hover and focus state; every form needs inline validation and a disabled/loading state on submit; every list or data view needs an empty state and, where data loads asynchronously, a loading state.

For any feed-like view where new content can arrive while the user is reading older content (chat threads, live logs, notification lists), don't yank their scroll position to the bottom every time something new appears - only auto-scroll if they were already at the bottom; otherwise show a small "jump to latest" affordance. This is the same instinct as an empty state: an obvious case the user won't think to ask for but will immediately notice if it's missing.

## 4. Build responsive from the start, not as a pass at the end

Design mobile-first: lay out the smallest viewport first (fluid widths, stacked sections, touch-sized tap targets ≥44px), then add breakpoints that reorganize the layout for tablet and desktop (e.g. a nav that collapses to a hamburger below ~768px, a grid that goes from 1 column to 2 to 3/4 as width grows). Use relative units (`rem`, `%`, `fr`, `clamp()`) over fixed pixel widths for anything that should flex. Never hardcode a layout that only works at one width and call it done.

## 5. Verify it actually works before calling it done - this is the step most likely to get skipped

Reading the code back is not verification. Use the **`run`** skill to actually launch the result (dev server, or open the static HTML) and drive it in a real browser:

- Load the page/app and check the browser console for errors or warnings - zero tolerance for console errors.
- Click through every interactive element you built: forms submit and show validation, buttons do what they claim, navigation goes where it says, modals open and close.
- Resize to at least three widths - a phone width (~375px), a tablet width (~768px), and a desktop width (~1440px) - and confirm nothing overlaps, overflows horizontally, or becomes unusably cramped at any of them.
- If you built a light/dark theme toggle, actually click it and check both states - a hardcoded color that only got tested in the default theme is a common way "supports dark mode" quietly becomes "half-supports it."
- If anything breaks, fix it and re-check. Only report the work as done once you've watched it work, not once you've finished writing it.

If there's truly no way to run the output in this environment (no browser tooling available at all), say so explicitly to the user instead of claiming it's verified - don't let "I wrote responsive-looking CSS" quietly stand in for "I confirmed it's responsive."

## 6. Hand it back

Tell the user, briefly: what you built, the stack you chose and why, and what you actually verified (including viewport sizes checked). If something in the original request couldn't be fully realized (e.g. needs real backend data), say so plainly rather than silently shipping a mock and letting them discover it later.
