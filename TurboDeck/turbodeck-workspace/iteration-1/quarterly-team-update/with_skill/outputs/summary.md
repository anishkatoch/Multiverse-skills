# Q3 2026 Retro Recap - build summary

## Theme
Picked **warm-startup** (not a preset's "default" corporate-blue). The request was explicitly internal-only, informal ("nothing fancy," "not a formal presentation," "our internal team colors") and about team/people outcomes (hiring, retro recap) rather than a client or external audience. `warm-startup` is the preset built for exactly that: energetic/approachable internal and people-facing decks rather than corporate sales material. `corporate-blue` or `technical-slate` would have read as more formal/client-facing than asked for.

## Slide count & structure
Built 6 slides (within the requested 5-6): title -> Q3 highlights -> ticket-volume KPIs -> team size & NPS KPIs -> Q4 goals -> closing. Each slide is self-contained (states the quarter, states the numbers) since the audience includes people who weren't in the retro meeting.

## How the two data issues were handled

1. **Onboarding launch date (Q2 vs Q3) - treated as a resolved typo.** The notes contain their own correction: the author second-guesses "Q2," checks, and confirms "it went live August 2026 so Q3." Since the author resolved this themselves within the notes, the deck states it plainly as a Q3 ship (slide 2), with a speaker note explaining the correction for anyone auditing the source.

2. **NPS 31 -> 31 - treated as an unresolved, flagged uncertainty, NOT corrected to 38.** The author flagged this number as likely a typo but explicitly said they could not confirm it ("I'd have to check the dashboard but I don't have access right now") and only guessed "maybe 38." This is different from the date issue: there's no self-correction, only a guess. Per the skill's guidance not to invent numbers, the deck does **not** print 38. Slide 4 shows Q2 NPS as the confirmed 31 and Q3 NPS as **"TBD"**, with the takeaway line and speaker notes explaining why it's marked pending rather than quoting either 31 or 38 as fact.

## Other notes/assumptions
- "30% drop" in tickets (412 -> 290) is actually ~29.6%; kept the notes' own rounded "30%" framing since it's a reasonable rounding, not an error.
- No team name, team lead, or contact signature was available, so the closing slide omits a `contact` line rather than inventing one.
- Speaker notes carry the fuller context (the date correction, the NPS caveat) so the slides themselves stay scannable per the "short recap, not a formal presentation" instruction.

## Files in this folder
- `outline.json` - the structured input to the build script
- `Q3_2026_Retro_Recap.pptx` - the generated deck (6 slides, warm-startup theme)
- `summary.md` - this file
