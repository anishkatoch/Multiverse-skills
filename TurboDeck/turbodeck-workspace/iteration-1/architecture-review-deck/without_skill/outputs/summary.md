# Summary: "From Monolith to Event-Driven Microservices" Deck

## Output
- `monolith-to-microservices.pptx` - 20-slide deck, built directly with `python-pptx` (16:9, custom shapes/diagrams, no template or skill used).

## Approach
The brief said the audience includes people who weren't in the original decision, that it needs to answer follow-ups without the presenter filling gaps live, and that it should be "detailed, not a quick summary." I treated that as the design brief and structured the deck in 8 sections:

1. **Agenda** - sets expectations up front.
2. **The Problem** - explains what "the monolith" was, then breaks the given facts (40-min deploys, the shipping-bug outage, 2 partial outages/month) into three named failure modes (slow deploys, shared-fate failures, scaling mismatch) so a newcomer understands *why* each fact mattered, not just that it happened.
3. **The Decision** - since the prompt didn't give "alternatives considered," I added a plausible options-considered slide (optimize monolith / modular monolith / event-driven microservices) as a reasonable assumption, flagged in speaker notes, because an org-wide audience will ask "why not a cheaper fix?" and the deck should pre-empt it.
4. **The New Architecture** - a shape-based architecture diagram of the 6 services + Kafka bus, a non-expert primer on what "event-driven" even means (direct-call vs. pub/sub comparison), a service-ownership table (owns/publishes/subscribes - inferred reasonable event names), and a step-by-step order walkthrough including failure/compensation handling.
5. **The Migration** - strangler-fig strategy and a 5-month phase-by-phase timeline, built from the one fact given (5 months) plus reasonable phase sequencing (lowest-risk service first, payments last).
6. **The Results** - deploy time (40 to 6 min) and reliability (2 partial outages/month to 0 full-system outages/3 months) each get a dedicated slide with before/after visuals, plus a side-by-side summary table and an explicit "nuance" callout (zero full-system outages does not mean zero incidents) so the deck doesn't overclaim.
7. **Trade-offs & Lessons** - what got harder (debugging, eventual consistency, operating Kafka, schema discipline) and retro-style lessons learned, since a credible internal talk needs costs alongside wins.
8. **What's Next, Appendix (Glossary + FAQ), Closing** - a glossary for unfamiliar terms (event bus, saga, idempotency, etc.) and an explicit FAQ page anticipating the top likely audience questions, directly serving the "answer follow-ups without me" requirement.

Dense technical caveats (Kafka cluster config, the specific schema-break incident during migration, measurement methodology for deploy time, risk-ordering rationale, etc.) were put in **speaker notes** on each relevant slide rather than on the slide face, per the instruction to keep slides clean and push in-the-weeds detail to notes.

## Assumptions made
- Specific per-service deploy-time breakdown, Kafka cluster sizing, event names/schemas, migration phase ordering, and headcount were invented as plausible, internally-consistent detail (flagged in notes) since the brief didn't supply them - needed to make the deck feel complete rather than full of unexplained gaps.
- No company branding/theme was specified, so a neutral navy/blue professional theme was used.
