#!/usr/bin/env python3
"""Heuristic check for text that likely overflows its box in a built .pptx.

python-pptx can't tell you how PowerPoint will actually render text (no layout
engine), so this estimates: given the box width, font size, and character count,
roughly how many lines the text needs, and flags it if that's more than the box
has room for. Treat every flag as "go look at this slide," not as certain proof -
but a slide this script flags is worth a second look before calling the deck done.

Usage:
    python check_layout.py deck.pptx
"""
import math
import sys
from pptx import Presentation
from pptx.util import Emu

CHARS_PER_INCH_AT_12PT = 11.0  # rough average-width-character estimate for common fonts
LINE_HEIGHT_FACTOR = 1.35
DEFAULT_MARGIN_LR_IN = 0.1  # python-pptx's own default inset when a shape hasn't set one
DEFAULT_MARGIN_TB_IN = 0.05


def _margin_in(value, default_in):
    return Emu(value).inches if value is not None else default_in


def estimate_overflow(shape):
    if not shape.has_text_frame:
        return None
    tf = shape.text_frame
    box_w_in = Emu(shape.width).inches
    box_h_in = Emu(shape.height).inches
    if box_w_in <= 0 or box_h_in <= 0:
        return None

    # Text wraps inside the frame's internal margins, not the shape's full
    # bounding box - ignoring them (especially on shapes like KPI cards that
    # set a deliberately wide margin) overestimates how much room the text
    # actually has and can hide a real overflow.
    usable_w_in = max(box_w_in - _margin_in(tf.margin_left, DEFAULT_MARGIN_LR_IN)
                       - _margin_in(tf.margin_right, DEFAULT_MARGIN_LR_IN), 0.1)
    usable_h_in = max(box_h_in - _margin_in(tf.margin_top, DEFAULT_MARGIN_TB_IN)
                       - _margin_in(tf.margin_bottom, DEFAULT_MARGIN_TB_IN), 0.1)

    height_needed_in = 0.0
    sample_text = []
    for para in tf.paragraphs:
        text = "".join(r.text for r in para.runs)
        if not text.strip():
            continue
        sizes = [r.font.size.pt for r in para.runs if r.font.size]
        size = sizes[0] if sizes else 18
        # Line height must track this paragraph's own font size - using a fixed
        # size here (e.g. always 18pt) flags small text (footers, page numbers,
        # kickers) as overflowing boxes it trivially fits in.
        chars_per_line = max(CHARS_PER_INCH_AT_12PT * usable_w_in * (12.0 / size), 1)
        # A partial line still costs a full line of height once text actually
        # wraps, so round up rather than leaving it fractional.
        lines_needed = max(math.ceil(len(text) / chars_per_line), 1)
        line_height_in = (size * LINE_HEIGHT_FACTOR) / 72.0
        height_needed_in += lines_needed * line_height_in
        sample_text.append(text)
    if not sample_text:
        return None

    if height_needed_in > usable_h_in * 1.15:  # 15% slack before flagging
        return {
            "box_h_in": round(box_h_in, 2),
            "estimated_height_needed_in": round(height_needed_in, 2),
            "preview": " / ".join(sample_text)[:80],
        }
    return None


def check(path):
    prs = Presentation(path)
    flagged = 0
    for i, slide in enumerate(prs.slides, start=1):
        for shape in slide.shapes:
            result = estimate_overflow(shape)
            if result:
                flagged += 1
                print(f"SLIDE {i}: possible text overflow - box is {result['box_h_in']}in tall, "
                      f"estimated text needs ~{result['estimated_height_needed_in']}in. "
                      f"Text: \"{result['preview']}...\"", file=sys.stderr)
    if flagged == 0:
        print(f"No likely overflow found across {len(prs.slides)} slides (heuristic check).")
    else:
        print(f"{flagged} shape(s) flagged for possible overflow - shorten the text, "
              f"reduce bullet count, or split the slide.", file=sys.stderr)
    return flagged


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_layout.py deck.pptx", file=sys.stderr)
        sys.exit(1)
    n = check(sys.argv[1])
    sys.exit(1 if n else 0)
