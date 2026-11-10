# Summary: Monolith to Event-Driven Microservices deck

## Theme
**technical-slate**. This is an internal engineering architecture review for an audience that
includes people who weren't in the original decision, so it needed to stay legible with dense
KPI grids and plain technical language rather than a sales/pitch feel. `themes.json` describes
this preset as built exactly for "architecture reviews, engineering deep-dives" - a direct match,
so no inline/brand theme was needed.

## Narrative order
Followed the skill's default spine, adapted to this story:
1. **What this is** - title + an explicit agenda slide (added because so many attendees weren't
   in the room; it tells them up front which question each later section answers).
2. **Why it matters** - the monolith's real costs (40-min deploys, 2 partial outages/month) and
   the concrete shipping-bug-took-down-checkout incident, so the audience feels the problem before
   seeing the solution.
3. **What we did** - the decision rationale (why microservices, why event-driven specifically,
   not direct calls), the six services, and a walk-through of one order's event flow.
4. **How we got there** - the five-month phased/strangler-fig rollout, called out as a separate
   section since "how do you migrate a live revenue system without downtime" is its own common
   follow-up question.
5. **What it means / what's next** - results (deploy time, outage counts), an honest trade-offs
   slide (eventual consistency, more moving parts, rebuilt on-call), and a forward-looking slide
   before Q&A.

Every content/section slide opens with a one-line hook (a stat or tension), per the skill's rule
against flat restatement titles.

## Slide vs. speaker notes
As requested, slides stay scannable; the heavy detail lives in notes:
- **On slides**: the five given facts (40 min -> 6 min deploys, 2 partial outages/month -> 0 full
  outages in 3 months, 6 services incl. Kafka, 5-month rollout), the architecture shape, the
  phased migration strategy, and an explicit trade-offs slide.
- **In notes**: Kafka mechanics (topic naming, partitioning by order ID, consumer groups,
  dead-letter queues, idempotency/at-least-once delivery), alternatives considered and rejected
  (modular monolith, horizontal scaling), team-ownership model, distributed tracing/observability
  investment, on-call restructuring, and guidance for the presenter on what *not* to improvise
  live (e.g., exact incident date/revenue figures, which weren't in the source material).

## Assumptions / things flagged for the presenter
- The source material didn't give a month-by-month migration sequence, only "5 months" total and
  the final six services. Slide 14 ("Five months, one domain at a time") states the *sequencing
  logic* (event bus first, lowest-risk domain first, payments/orders last) rather than inventing
  specific month-to-service assignments presented as fact. The slide notes flag this explicitly so
  the presenter can drop in real per-service dates before presenting if available.
- No partial-outage figure for the post-launch period was given (only the pre-migration baseline:
  2/month). The results KPI slide shows this as "down from 2/mo" rather than fabricating a new
  number, and the notes say to describe it as an improving trend, not a specific resolved metric,
  if asked live.
- The shipping-bug incident slide deliberately has no invented date, duration, or revenue-impact
  figure - only what was given (shipping bug -> shared process -> checkout down, recovery via a
  full 40-min redeploy). Notes direct the presenter to the incident postmortem for specifics if
  pressed, rather than the deck guessing.

## Files
- outline.json - the full 20-slide outline built from the schema.
- architecture-review-deck.pptx - the generated deck (20 slides, no build-script warnings).
- summary.md - this file.
