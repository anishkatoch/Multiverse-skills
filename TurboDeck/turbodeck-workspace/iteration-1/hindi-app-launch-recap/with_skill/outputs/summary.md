# Summary - Hindi App Launch Recap Deck

## Request
Internal team recap of a mobile app's first 30 days: 12,000 downloads, 4.3-star rating. Deck requested in Hindi, short, main points only.

## Theme & font
Used an inline custom theme based on the `modern-dark` preset (dark background 14161A, teal accent 5CE1C6) - the preset's own description calls it suited to "tech/product launches... sleek high-contrast feel," which fits a mobile app launch recap well.

The preset's default fonts (Segoe UI) are Latin-only and render Devanagari poorly/inconsistently in PowerPoint. Per references/outline-schema.md's "Non-Latin scripts" note, heading_font and body_font were overridden to "Nirmala UI", a Windows system font with full native Devanagari glyph support, while keeping the rest of the modern-dark palette unchanged.

## Hindi content confirmation
All slide content (titles, hook, KPI labels/values, takeaway, closing bullets, speaker notes) was written directly in natural Hindi, not translated word-for-word from English. Verified by re-opening the built .pptx with python-pptx and dumping every text frame (confirmed proper Devanagari Unicode throughout); sample output:
- Slide 1 hook: "30 दिनों में 12,000 डाउनलोड और 4.3 स्टार रेटिंग"
- Slide 2 KPIs: कुल डाउनलोड (12,000), औसत रेटिंग (4.3 ★), लॉन्च अवधि (30 दिन)
- Slide 2 takeaway: "अच्छी डाउनलोड संख्या के साथ यूज़र्स को ऐप भी पसंद आ रहा है - शुरुआत मजबूत रही है।"
- Slide 3: "शुरुआत अच्छी रही - अब आगे बढ़ना है" with two closing bullets

## Structure (3 slides - kept intentionally short)
1. Title slide - headline with both key numbers (12,000 downloads, 4.3 stars) in the hook line.
2. KPI slide - three metric cards (total downloads, average rating, launch window) with a one-line takeaway.
3. Closing slide - brief forward-looking note, thanking the team and signaling that next steps will be discussed separately.

Ran check_layout.py - no overflow warnings. Ran summarize_outline.py - confirmed both given facts (12,000 downloads, 4.3 rating) and the 30-day window are traceable to slide 1 and slide 2, matching the request.

## Assumptions made
- Audience = internal team, informal/celebratory tone (not an external investor/press deck).
- No specific "next steps" or action items were given in the request, so the closing slide deliberately stays generic (thanks + "next steps to be discussed") rather than inventing fabricated plans.
- Launch date/app name were not provided, so the deck refers generically to "our new app" rather than guessing a name.
