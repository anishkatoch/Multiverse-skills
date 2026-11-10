---
tags: [turbodeck, technical, architecture]
max_turns: 25
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

I need to present our move from a monolith to event-driven microservices to the wider engineering org next week - a lot of people attending weren't involved in the decision, so the deck needs to actually explain things clearly, not assume context.

Background: our order-processing monolith was hitting scaling limits - deploys took 40 minutes, and a bug in the shipping module once took down checkout entirely because everything shared one process. We split it into 6 services (orders, inventory, shipping, payments, notifications, and a new event bus using Kafka). Rollout took 5 months. Since launch: deploy time is down to 6 minutes per service, and we've had zero full-system outages in 3 months (down from 2 partial outages/month before).

Make it detailed this time, not a quick summary - people will have follow-up questions and I want the deck itself to answer most of them without me having to fill gaps live. Feel free to put the really in-the-weeds stuff in notes if it'd clutter the slide.
