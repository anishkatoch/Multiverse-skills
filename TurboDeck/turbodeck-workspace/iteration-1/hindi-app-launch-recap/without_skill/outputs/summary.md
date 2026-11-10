# Summary: Hindi App-Launch Recap Deck

## Approach
I built the deck programmatically with `python-pptx` (no slide-generation skill was used, per
instructions - this was done as a general capable assistant using judgment). A standalone script
(`make_pptx.py`) constructs a 16:9 (13.33" x 7.5") presentation with 5 short slides:

1. **Title slide** - "हमारा नया मोबाइल ऐप लॉन्च" (Our new mobile app launch), subtitle "पहले 30
   दिनों का संक्षिप्त सारांश" (Short summary of the first 30 days).
2. **Launch background** - 3 short bullet points giving context (launched last month, positive
   early response, key numbers follow).
3. **Key metrics** - the two headline numbers the user gave, shown as large stat cards:
   **12,000** total downloads in the first 30 days, and **4.3 star** average rating.
4. **What it means** - 3 bullets interpreting the numbers (strong start, satisfied users, next
   focus = grow installs while maintaining the rating).
5. **Closing/Thank you slide** - "धन्यवाद!" (Thank you) with a one-line thanks to the team.

The deck intentionally stays short (5 slides, 2-3 bullets per slide max) since the request asked
for "not too long, just the main points." Content is simple, direct Hindi so the whole team can
read it without needing the presenter in the room. No invented numbers were added beyond the two
figures the user supplied (12,000 downloads, 4.3-star rating over the first 30 days).

## Font used for Hindi text
All Hindi (Devanagari-script) text runs explicitly set the font to **"Nirmala UI"**, which is the
standard Unicode Devanagari-script UI font bundled with Windows 8+ and used by default in Microsoft
Office for Hindi text. It was set on each text run's Latin, East Asian (`ea`), and complex-script
(`cs`) typeface properties (via the XML `rPr` element) to make sure the font selection sticks
regardless of how PowerPoint classifies the script of each run. This keeps rendering legible and
consistent whether opened on a Windows machine with standard Office fonts installed.

## Output files
- `app_launch_recap_hindi.pptx` - the final 5-slide presentation (verified by re-opening it with
  python-pptx and reading back every text run to confirm the Hindi text round-trips correctly).
- `summary.md` - this file.

## Assumptions made
- No company/app name was given, so the deck refers generically to "हमारा नया मोबाइल ऐप" (our new
  mobile app) rather than inventing a product name.
- "Rating" was assumed to mean an app-store/play-store user rating (labelled generically as
  "ऐप स्टोर/प्ले स्टोर" on the metrics slide) since the platform wasn't specified.
- A neutral blue/green/orange color palette was used since no brand colors were specified.
