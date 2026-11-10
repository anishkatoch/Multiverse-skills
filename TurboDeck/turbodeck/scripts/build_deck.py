#!/usr/bin/env python3
"""Build a .pptx deck from a JSON outline. See references/outline-schema.md for the format.

Usage:
    python build_deck.py outline.json output.pptx
"""
import json
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.chart.data import CategoryChartData
from pptx.oxml.ns import qn

THEMES_PATH = Path(__file__).parent.parent / "references" / "themes.json"
SLIDE_W, SLIDE_H = Inches(13.333), Inches(7.5)  # 16:9

CHART_TYPES = {
    "line": XL_CHART_TYPE.LINE_MARKERS,
    "bar": XL_CHART_TYPE.BAR_CLUSTERED,
    "column": XL_CHART_TYPE.COLUMN_CLUSTERED,
    "pie": XL_CHART_TYPE.PIE,
}
# Extra series beyond accent/primary fall back to this fixed palette - keep series
# count low (<=4) on one slide regardless, a chart with more gets hard to read.
CHART_EXTRA_PALETTE = ["8E8E8E", "C9A227", "4F9D69", "A23B3B"]

BULLET_WARN_CHARS = 110
KPI_LABEL_WARN_CHARS = 28
TITLE_WARN_CHARS = 100
# hooks and chart takeaways live in boxes sized for exactly one line - if it's
# long enough to wrap, it overflows, since (unlike a title) there's no second
# line budgeted for it by design.
ONELINER_WARN_CHARS = 90
# content/kpi/two-column/chart all share this title box. 28pt bold needs ~0.9in
# for one line; a "hook"-style title (which this skill asks for, so it WILL
# happen regularly) often wraps to two, which needs ~1.15in - size for that
# case rather than overflowing into whatever sits below the title.
TITLE_BOX_HEIGHT = Inches(1.15)


def load_theme(outline):
    themes = json.loads(THEMES_PATH.read_text(encoding="utf-8"))
    theme_ref = outline.get("theme", "corporate-blue")
    if isinstance(theme_ref, dict):
        # inline custom theme, e.g. matched to a company's brand colors
        base = dict(themes["corporate-blue"])
        base.update(theme_ref)
        return base
    if theme_ref not in themes:
        raise ValueError(f"Unknown theme '{theme_ref}'. Known: {list(themes)} or pass an inline theme object.")
    return themes[theme_ref]


def rgb(hex_str):
    return RGBColor.from_string(hex_str.lstrip("#").upper())


def set_background(slide, color_hex):
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = rgb(color_hex)


def add_textbox(slide, left, top, width, height, text, size, color_hex, font, bold=False,
                 align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False, line_spacing=1.08):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font
    r.font.color.rgb = rgb(color_hex)
    return box


def add_bullets(slide, left, top, width, height, bullets, size, color_hex, font, line_spacing=1.25,
                 space_after=10):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    for i, bullet in enumerate(bullets):
        text = bullet["text"] if isinstance(bullet, dict) else bullet
        level = bullet.get("level", 0) if isinstance(bullet, dict) else 0
        if len(text) > BULLET_WARN_CHARS:
            print(f"WARNING: bullet is {len(text)} chars (keep it skimmable, aim under "
                  f"{BULLET_WARN_CHARS}): {text[:60]}...", file=sys.stderr)
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        p.level = max(0, min(level, 2))
        r = p.add_run()
        r.text = ("—  " if level == 0 else "•  ") + text
        r.font.size = Pt(size - level * 2)
        r.font.name = font
        r.font.color.rgb = rgb(color_hex)
    return box


def add_footer(slide, theme, label, page_num):
    add_textbox(slide, Inches(0.6), Inches(7.08), Inches(8), Inches(0.35), label,
                9, theme["text_muted"], theme["body_font"])
    add_textbox(slide, Inches(12.3), Inches(7.08), Inches(0.6), Inches(0.35), str(page_num),
                9, theme["text_muted"], theme["body_font"], align=PP_ALIGN.RIGHT)


def add_notes(slide, notes):
    if notes:
        slide.notes_slide.notes_text_frame.text = notes


def warn_if_long_title(title, page_num):
    if len(title) > TITLE_WARN_CHARS:
        print(f"WARNING: title on slide {page_num} is {len(title)} chars - even wrapped to two "
              f"lines this risks overflowing its box, shorten it: {title[:60]}...", file=sys.stderr)


def warn_if_long_oneliner(text, kind, location):
    if text and len(text) > ONELINER_WARN_CHARS:
        print(f"WARNING: {kind} on {location} is {len(text)} chars - it's meant to be one "
              f"line and its box isn't sized for a wrap, shorten it: {text[:60]}...", file=sys.stderr)


def add_title_rule(slide, theme, x, title_top):
    """A short accent-colored rule under a slide's title - a small typographic
    signature that gives every content-bearing slide the same considered feel,
    instead of a plain text heading with nothing to anchor it."""
    rule_top = title_top + TITLE_BOX_HEIGHT - Inches(0.08)
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, rule_top, Inches(0.55), Inches(0.045))
    rule.fill.solid()
    rule.fill.fore_color.rgb = rgb(theme["accent"])
    rule.line.fill.background()
    rule.shadow.inherit = False


def add_accent_bar(slide, theme):
    """A vertical gradient (accent -> primary) rather than a flat color - a
    flat bar reads as a default-template afterthought, a gradient reads as
    a deliberate design choice."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.25), SLIDE_H)
    bar.fill.gradient()
    stops = bar.fill.gradient_stops
    stops[0].position = 0.0
    stops[0].color.rgb = rgb(theme["accent"])
    stops[1].position = 1.0
    stops[1].color.rgb = rgb(theme["primary"])
    bar.fill.gradient_angle = 90.0
    bar.line.fill.background()


def add_corner_accent(slide, theme):
    """A large, soft circle bleeding off the bottom-right corner - a common
    motif in modern product/launch decks that gives the title slide some
    depth instead of being flat color + text with nothing else going on."""
    size = Inches(4.5)
    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, SLIDE_W - Inches(2.2), SLIDE_H - Inches(2.2), size, size
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = rgb(theme["bg_alt"])
    circle.line.fill.background()
    circle.shadow.inherit = False
    return circle


def layout_title(prs, theme, spec, deck_title):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    add_corner_accent(slide, theme)
    add_accent_bar(slide, theme)
    if spec.get("hook"):
        warn_if_long_oneliner(spec["hook"], "hook", "the title slide")
        add_textbox(slide, Inches(0.9), Inches(2.3), Inches(11), Inches(0.6), spec["hook"],
                    16, theme["accent"], theme["body_font"], italic=True)
    add_textbox(slide, Inches(0.9), Inches(2.9), Inches(11), Inches(1.6), spec.get("title", deck_title),
                40, theme["primary"], theme["heading_font"], bold=True)
    if spec.get("subtitle"):
        add_textbox(slide, Inches(0.9), Inches(4.3), Inches(10.5), Inches(0.8), spec["subtitle"],
                    18, theme["text_muted"], theme["body_font"])
    add_notes(slide, spec.get("notes"))
    return slide


def layout_section(prs, theme, spec, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    add_accent_bar(slide, theme)
    if spec.get("number"):
        add_textbox(slide, Inches(0.9), Inches(2.6), Inches(2), Inches(1), spec["number"],
                    28, theme["accent"], theme["heading_font"], bold=True)
    warn_if_long_title(spec["title"], page_num)
    add_textbox(slide, Inches(0.9), Inches(3.2), Inches(11), Inches(1.4), spec["title"],
                34, theme["primary"], theme["heading_font"], bold=True)
    if spec.get("subtitle"):
        add_textbox(slide, Inches(0.9), Inches(4.3), Inches(10), Inches(0.7), spec["subtitle"],
                    16, theme["text_muted"], theme["body_font"])
    add_notes(slide, spec.get("notes"))
    return slide


def layout_content(prs, theme, spec, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    add_textbox(slide, Inches(0.6), Inches(0.4), Inches(12), Inches(0.3), spec.get("kicker", ""),
                12, theme["accent"], theme["body_font"], bold=True)
    warn_if_long_title(spec["title"], page_num)
    add_textbox(slide, Inches(0.6), Inches(0.68), Inches(12), TITLE_BOX_HEIGHT, spec["title"],
                28, theme["primary"], theme["heading_font"], bold=True)
    add_title_rule(slide, theme, Inches(0.6), Inches(0.68))
    if spec.get("hook"):
        warn_if_long_oneliner(spec["hook"], "hook", f"slide {page_num}")
        add_textbox(slide, Inches(0.6), Inches(1.95), Inches(12), Inches(0.5), spec["hook"],
                    15, theme["text_muted"], theme["body_font"], italic=True)
        bullets_top = Inches(2.55)
    else:
        bullets_top = Inches(2.0)
    if spec.get("bullets"):
        bullets_height = Inches(6.9) - bullets_top
        add_bullets(slide, Inches(0.6), bullets_top, Inches(12.0), bullets_height, spec["bullets"],
                    18, theme["text"], theme["body_font"])
    add_footer(slide, theme, spec.get("footer_label", ""), page_num)
    add_notes(slide, spec.get("notes"))
    return slide


def layout_kpi(prs, theme, spec, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    warn_if_long_title(spec["title"], page_num)
    add_textbox(slide, Inches(0.6), Inches(0.4), Inches(12), TITLE_BOX_HEIGHT, spec["title"],
                28, theme["primary"], theme["heading_font"], bold=True)
    add_title_rule(slide, theme, Inches(0.6), Inches(0.4))
    kpis = spec["kpis"]
    if not kpis:
        raise ValueError(f"'kpi' layout on slide {page_num} needs at least one entry in 'kpis'.")
    n = len(kpis)
    card_w = Inches(12.0 / n - 0.25)
    gap = Inches(0.25)
    left = Inches(0.6)
    top = Inches(2.0)
    # Sized to what a value+label+delta stack actually needs - a much taller
    # card than its content leaves a card that reads as mostly empty space.
    card_h = Inches(2.3)
    for kpi in kpis:
        label = kpi.get("label", "")
        if len(label) > KPI_LABEL_WARN_CHARS:
            print(f"WARNING: KPI label is long ({len(label)} chars) - shorten for scannability: {label}",
                  file=sys.stderr)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = rgb(theme["bg_alt"])
        card.line.fill.background()
        card.shadow.inherit = False
        # A small accent "chip" near the top gives the card a focal point and
        # a sense of hierarchy - a plain flat box with centered text reads as
        # a placeholder, not a deliberately designed stat card.
        stripe_inset = Inches(0.18)
        stripe = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Emu(left + stripe_inset), Emu(top + Inches(0.16)),
            Emu(card_w - 2 * stripe_inset), Inches(0.09)
        )
        stripe.fill.solid()
        stripe.fill.fore_color.rgb = rgb(theme["accent"])
        stripe.line.fill.background()
        stripe.shadow.inherit = False
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = Inches(0.25)
        tf.margin_right = Inches(0.25)
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.CENTER
        r0 = p0.add_run()
        r0.text = kpi.get("value", "")
        r0.font.size = Pt(40)
        r0.font.bold = True
        r0.font.name = theme["heading_font"]
        r0.font.color.rgb = rgb(theme["primary"])
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.CENTER
        p1.space_before = Pt(6)
        r1 = p1.add_run()
        r1.text = label
        r1.font.size = Pt(14)
        r1.font.name = theme["body_font"]
        r1.font.color.rgb = rgb(theme["text"])
        if kpi.get("delta"):
            p2 = tf.add_paragraph()
            p2.alignment = PP_ALIGN.CENTER
            p2.space_before = Pt(4)
            r2 = p2.add_run()
            r2.text = kpi["delta"]
            r2.font.size = Pt(12)
            r2.font.bold = True
            r2.font.name = theme["body_font"]
            r2.font.color.rgb = rgb(theme["accent"])
        left = Emu(left + card_w + gap)
    if spec.get("takeaway"):
        add_textbox(slide, Inches(0.6), Inches(4.6), Inches(12.0), Inches(1.0), spec["takeaway"],
                    16, theme["text_muted"], theme["body_font"], italic=True)
    add_footer(slide, theme, spec.get("footer_label", ""), page_num)
    add_notes(slide, spec.get("notes"))
    return slide


def layout_two_column(prs, theme, spec, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    warn_if_long_title(spec["title"], page_num)
    add_textbox(slide, Inches(0.6), Inches(0.4), Inches(12), TITLE_BOX_HEIGHT, spec["title"],
                28, theme["primary"], theme["heading_font"], bold=True)
    add_title_rule(slide, theme, Inches(0.6), Inches(0.4))
    for col, (x) in zip(("left", "right"), (Inches(0.6), Inches(6.85))):
        data = spec.get(col, {})
        if not data:
            continue
        add_textbox(slide, x, Inches(1.7), Inches(5.9), Inches(0.5), data.get("title", ""),
                    17, theme["accent"], theme["heading_font"], bold=True)
        if data.get("bullets"):
            add_bullets(slide, x, Inches(2.25), Inches(5.9), Inches(4.3), data["bullets"],
                        16, theme["text"], theme["body_font"])
    add_footer(slide, theme, spec.get("footer_label", ""), page_num)
    add_notes(slide, spec.get("notes"))
    return slide


def layout_chart(prs, theme, spec, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    warn_if_long_title(spec["title"], page_num)
    add_textbox(slide, Inches(0.6), Inches(0.4), Inches(12), TITLE_BOX_HEIGHT, spec["title"],
                28, theme["primary"], theme["heading_font"], bold=True)
    add_title_rule(slide, theme, Inches(0.6), Inches(0.4))

    chart_type = CHART_TYPES.get(spec.get("chart_type", "column"))
    if chart_type is None:
        raise ValueError(f"Unknown chart_type '{spec.get('chart_type')}'. Valid: {list(CHART_TYPES)}")

    series_list = spec["series"]
    if not series_list:
        raise ValueError(f"'chart' layout on slide {page_num} needs at least one series in 'series'.")
    if len(series_list) > 4:
        print(f"WARNING: chart on slide {page_num} has {len(series_list)} series - a slide chart "
              f"gets hard to read past ~4, consider splitting or picking the key ones.", file=sys.stderr)

    categories = spec["categories"]
    for s in series_list:
        if len(s["values"]) != len(categories):
            raise ValueError(
                f"'chart' layout on slide {page_num}: series '{s.get('name', '?')}' has "
                f"{len(s['values'])} values but there are {len(categories)} categories - "
                f"they must match 1:1, or the chart renders misaligned/corrupted."
            )

    chart_data = CategoryChartData()
    chart_data.categories = categories
    for s in series_list:
        chart_data.add_series(s["name"], s["values"])

    has_takeaway = bool(spec.get("takeaway"))
    chart_top = Inches(1.65)
    chart_bottom_margin = Inches(1.15) if has_takeaway else Inches(0.5)
    cx = Inches(12.0)
    cy = SLIDE_H - chart_top - chart_bottom_margin
    frame = slide.shapes.add_chart(chart_type, Inches(0.6), chart_top, cx, cy, chart_data)
    chart = frame.chart

    palette = [theme["accent"], theme["primary"]] + CHART_EXTRA_PALETTE
    is_pie = spec.get("chart_type") == "pie"
    plot = chart.plots[0]
    if is_pie:
        points = plot.series[0].points
        for i, point in enumerate(points):
            point.format.fill.solid()
            point.format.fill.fore_color.rgb = rgb(palette[i % len(palette)])
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.RIGHT
        chart.legend.include_in_layout = False
        # A pie slice with no label on it is just a colored wedge - the reader
        # can't tell what it means without one, so this is never optional.
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.show_percentage = True
        dl.show_value = False
        dl.show_category_name = False
        dl.number_format = "0%"
        dl.number_format_is_linked = False
        dl.font.size = Pt(13)
        dl.font.bold = True
        dl.font.name = theme["body_font"]
        dl.font.color.rgb = rgb("FFFFFF")  # sits on a filled, mid-to-dark wedge regardless of theme
    else:
        for i, series in enumerate(plot.series):
            series.format.fill.solid()
            series.format.fill.fore_color.rgb = rgb(palette[i % len(palette)])
            series.format.line.color.rgb = rgb(palette[i % len(palette)])
        chart.has_legend = len(series_list) > 1
        if chart.has_legend:
            chart.legend.position = XL_LEGEND_POSITION.BOTTOM
            chart.legend.include_in_layout = False
        plot.has_data_labels = True
        dl = plot.data_labels
        dl.show_value = True
        dl.number_format_is_linked = True
        dl.font.size = Pt(11)
        dl.font.name = theme["body_font"]
        dl.font.color.rgb = rgb(theme["text"])  # labels sit on the slide background, not the fill

    # python-pptx's default legend/label text color is black regardless of the
    # slide's own background - on a dark theme that's invisible text on a near-
    # black background, which looks exactly like "the legend is missing."
    if chart.has_legend:
        chart.legend.font.size = Pt(12)
        chart.legend.font.name = theme["body_font"]
        chart.legend.font.color.rgb = rgb(theme["text"])

    chart.has_title = False
    if not is_pie:
        category_axis_font = chart.category_axis.tick_labels.font
        category_axis_font.size = Pt(12)
        category_axis_font.name = theme["body_font"]
        category_axis_font.color.rgb = rgb(theme["text_muted"])
        value_axis_font = chart.value_axis.tick_labels.font
        value_axis_font.size = Pt(12)
        value_axis_font.name = theme["body_font"]
        value_axis_font.color.rgb = rgb(theme["text_muted"])
        if spec.get("y_axis_title"):
            chart.value_axis.axis_title.text_frame.text = spec["y_axis_title"]
            chart.value_axis.has_title = True

    if spec.get("takeaway"):
        warn_if_long_oneliner(spec["takeaway"], "chart takeaway", f"slide {page_num}")
        add_textbox(slide, Inches(0.6), SLIDE_H - Inches(1.05), Inches(12.0), Inches(0.55),
                    spec["takeaway"], 15, theme["text_muted"], theme["body_font"], italic=True)
    add_footer(slide, theme, spec.get("footer_label", ""), page_num)
    add_notes(slide, spec.get("notes"))
    return slide


def layout_quote(prs, theme, spec, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    add_textbox(slide, Inches(1.5), Inches(2.4), Inches(10.3), Inches(2.2), f"“{spec['text']}”",
                26, theme["primary"], theme["heading_font"], italic=True, align=PP_ALIGN.CENTER)
    if spec.get("attribution"):
        add_textbox(slide, Inches(1.5), Inches(4.7), Inches(10.3), Inches(0.5), f"— {spec['attribution']}",
                    15, theme["text_muted"], theme["body_font"], align=PP_ALIGN.CENTER)
    add_notes(slide, spec.get("notes"))
    return slide


def layout_closing(prs, theme, spec, page_num):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, theme["bg"])
    add_accent_bar(slide, theme)
    warn_if_long_title(spec["title"], page_num)
    add_textbox(slide, Inches(0.9), Inches(2.3), Inches(11), Inches(1.4), spec["title"],
                34, theme["primary"], theme["heading_font"], bold=True)
    if spec.get("bullets"):
        add_bullets(slide, Inches(0.9), Inches(3.8), Inches(11), Inches(2.0), spec["bullets"],
                    17, theme["text"], theme["body_font"])
    if spec.get("contact"):
        add_textbox(slide, Inches(0.9), Inches(6.3), Inches(11), Inches(0.5), spec["contact"],
                    14, theme["accent"], theme["body_font"])
    add_notes(slide, spec.get("notes"))
    return slide


LAYOUTS = {
    "title": lambda prs, theme, spec, pn, dt: layout_title(prs, theme, spec, dt),
    "section": lambda prs, theme, spec, pn, dt: layout_section(prs, theme, spec, pn),
    "content": lambda prs, theme, spec, pn, dt: layout_content(prs, theme, spec, pn),
    "kpi": lambda prs, theme, spec, pn, dt: layout_kpi(prs, theme, spec, pn),
    "chart": lambda prs, theme, spec, pn, dt: layout_chart(prs, theme, spec, pn),
    "two-column": lambda prs, theme, spec, pn, dt: layout_two_column(prs, theme, spec, pn),
    "quote": lambda prs, theme, spec, pn, dt: layout_quote(prs, theme, spec, pn),
    "closing": lambda prs, theme, spec, pn, dt: layout_closing(prs, theme, spec, pn),
}


def build(outline_path, output_path):
    outline = json.loads(Path(outline_path).read_text(encoding="utf-8"))
    theme = load_theme(outline)
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    deck_title = outline.get("title", "")

    slides = outline.get("slides")
    if not slides:
        raise ValueError("Outline has no 'slides' list (or it's empty) - nothing to build.")
    if len(slides) > 25:
        print(f"WARNING: {len(slides)} slides is a lot for one sitting - confirm the user wants "
              f"this long a deck rather than a shorter cut.", file=sys.stderr)

    for i, spec in enumerate(slides, start=1):
        layout_name = spec.get("layout")
        if not layout_name:
            raise ValueError(f"Slide {i} is missing a 'layout' key.")
        layout_fn = LAYOUTS.get(layout_name)
        if not layout_fn:
            raise ValueError(f"Unknown layout '{layout_name}' on slide {i}. Valid: {list(LAYOUTS)}")
        try:
            layout_fn(prs, theme, spec, i, deck_title)
        except KeyError as e:
            raise ValueError(f"Slide {i} (layout '{layout_name}') is missing required field {e}.") from e

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    prs.save(output_path)
    print(f"Built {len(slides)} slides -> {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python build_deck.py outline.json output.pptx", file=sys.stderr)
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
