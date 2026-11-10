# Q3 2026 Team Retro Recap - Approach Summary

## Output
`Q3_2026_Team_Retro_Recap.pptx` - 6 slides, built with python-pptx (no external template/assets).

## Slide structure
1. Title - "Q3 2026 Retro: What Happened and What's Next" (sets context for readers who weren't in the meeting)
2. Highlight - new onboarding flow shipped
3. Support ticket volume (412 -> 290, -30%)
4. NPS & team growth
5. Q4 2026 goals (3 goal cards)
6. Closing summary / recap of key numbers

## Design
Internal-facing, "nothing fancy" per the request: a simple navy/slate + teal palette with amber reserved only for the one flagged/unconfirmed data point, on a light neutral background. No logos, stock photography, or client-style polish - just clean stat cards and bullet lists, since this is an internal recap, not an external deck.

## How I handled the Q2/Q3 onboarding date confusion
The raw notes first say the onboarding flow shipped "in Q2" but then self-correct ("wait, I think it was actually Q3... yes it went live August 2026 so Q3"). August falls in Q3, and that's the self-corrected, more specific claim, so I went with Q3 2026 throughout the deck and explicitly noted the correction on Slide 2 ("not Q2, as some early notes suggested") so the deck is self-documenting for people who never saw the raw notes or the back-and-forth.

## How I handled the NPS number
The notes say NPS went "from 31 to 31 again in Q3," which the author immediately flags as likely a typo, guessing it might actually be 38 - but without dashboard access to confirm. Since this deck is going to the wider team and needs to stand on its own, I did not guess or silently insert the speculative "38" as a fact - presenting an unverified number as confirmed data would be misleading to people who weren't in the room to hear the caveat. Instead, Slide 4 shows the confirmed Q2 figure (31), marks Q3 as "unconfirmed - pending dashboard check," and includes a short note explaining why (apparent data-entry error, real Q3 number believed higher, to be verified). This is called out again in the closing slide so it doesn't get lost. The deck's author should fill in the real Q3 NPS once they've checked the dashboard, then this slide can be simplified to a normal before/after stat.

## Other notes / assumptions
- Support ticket drop is attributed to two factors per the notes: the new onboarding flow and the additional Q3 support hire - both are called out rather than oversimplifying to a single cause.
- Team size change (7 -> 9) is presented as a Q2-start-to-Q3-end trend, matching how the note was phrased.
- Kept to 6 slides as requested, avoided dense paragraphs in favor of stat cards/bullets so it can be skimmed by people outside the original meeting.
- Color palette (navy #1F2A44, teal #2EC4B6, slate #4A5568, amber #E8A62E for the flagged item) is a guessed sensible internal scheme per the request, not an actual brand kit - easy to swap if the team has real brand colors.
