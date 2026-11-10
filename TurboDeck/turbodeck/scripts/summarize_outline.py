#!/usr/bin/env python3
"""Print a compact, slide-by-slide summary of an outline.json for auditing
against the original request - see SKILL.md step 7 ("check it against what
was actually asked"). Reading this summary line by line next to the user's
request is much faster than re-reading the whole deck's text dump, and makes
it obvious when something asked for (a topic, a chart, a theme, a language)
didn't actually make it into the outline.

Usage:
    python summarize_outline.py outline.json
"""
import json
import sys


def describe_theme(theme):
    if isinstance(theme, dict):
        return f"inline custom theme (primary={theme.get('primary', '?')}, accent={theme.get('accent', '?')})"
    return theme or "corporate-blue (default)"


def describe_slide(i, spec):
    layout = spec.get("layout", "???")
    bits = [f"{i}. [{layout}]"]

    if spec.get("title"):
        bits.append(spec["title"])
    elif spec.get("text"):
        bits.append(spec["text"][:60])

    extra = []
    if spec.get("hook"):
        extra.append(f"hook: \"{spec['hook'][:50]}\"")
    if spec.get("kpis"):
        labels = ", ".join(k.get("label", "?") for k in spec["kpis"])
        extra.append(f"KPIs: {labels}")
    if spec.get("series"):
        names = ", ".join(s.get("name", "?") for s in spec["series"])
        extra.append(f"chart ({spec.get('chart_type', 'column')}): {names}")
    if spec.get("bullets"):
        extra.append(f"{len(spec['bullets'])} bullets")
    if spec.get("left") or spec.get("right"):
        sides = [c for c in ("left", "right") if spec.get(c)]
        extra.append(f"two-column: {' / '.join(sides)}")
    if spec.get("takeaway"):
        extra.append("has takeaway")
    if spec.get("notes"):
        extra.append(f"notes: {len(spec['notes'])} chars")

    line = " | ".join(bits)
    if extra:
        line += "  ->  " + "; ".join(extra)
    return line


def summarize(path):
    outline = json.loads(open(path, encoding="utf-8").read())
    print(f"Deck title: {outline.get('title', '(none)')}")
    print(f"Theme: {describe_theme(outline.get('theme'))}")
    slides = outline.get("slides", [])
    print(f"Slides: {len(slides)}")
    print("-" * 60)
    for i, spec in enumerate(slides, start=1):
        print(describe_slide(i, spec))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python summarize_outline.py outline.json", file=sys.stderr)
        sys.exit(1)
    summarize(sys.argv[1])
