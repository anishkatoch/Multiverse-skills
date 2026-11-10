# Monthly Leadership Sync Deck - Summary

## Deliverable
`Monthly_Signup_Growth_Deck.pptx` - a 4-slide PowerPoint deck built with `python-pptx`, using native, editable PowerPoint chart objects (not static images), so the charts can be reformatted or have data updated directly in PowerPoint.

## Approach
Kept the deck deliberately short for a recurring internal sync - 4 slides, one idea per slide, no extraneous content:

1. **Title slide** - dark navy cover stating the purpose ("Signup Growth & Channel Performance") and the reporting window.
2. **Signup Growth (Jan-Jun)** - a native clustered-column chart plotting the 6 monthly signup totals (850 -> 1,600) with data labels on each bar, paired with a side panel calling out the headline stat (+88% growth) and two supporting observations (accelerating month-over-month growth, strongest month in June).
3. **Channel Mix (this quarter)** - a native pie chart (Organic 45%, Paid ads 30%, Referral 15%, Partnerships 10%) with in-slice percentage labels, color-coded to a breakdown list on the right, plus a one-line insight that Paid + Organic drive 75% of signups.
4. **Summary** - closing slide distilling the two data stories into three labeled takeaways (Growth, Channel mix, Watch list) for quick executive scanning.

## Design choices / assumptions
- Used a simple navy/blue palette with one accent color per channel in the pie chart - consistent, not flashy, appropriate for an internal monthly sync.
- Assumed "this quarter" refers to the current quarter (Q2, Apr-Jun) given the Jan-Jun data provided; channel percentages were taken as given (45/30/15/10, summing to 100%).
- Assumed a generic "June 2026" sync date since no specific date was given; this is cosmetic and easy to edit.
- No company name/logo was provided, so the deck uses a neutral "Marketing - Monthly Leadership Sync" header/footer instead of a fabricated brand identity.
- Built with real `python-pptx` chart objects (`XL_CHART_TYPE.COLUMN_CLUSTERED` and `XL_CHART_TYPE.PIE`) rather than screenshots, so the data and formatting remain editable in PowerPoint.

## Files in this folder
- `Monthly_Signup_Growth_Deck.pptx` - the deck
- `summary.md` - this file
