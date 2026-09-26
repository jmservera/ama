<!-- markdownlint-disable-file -->

# Primary Research: AMA Mentor Progress Review Deck

## Purpose and Audience

* Audience: AMA mentor, first mentoring session (week of 28 September 2026).
* Goal: summarise the case, the request, how the gaps were filled, the
  challenges met, and how the repository is organised so every decision can
  be justified or challenged.
* Length: short, about 13 slides for a 20 to 30 minute conversation.
* Topic research (`rpi-research`) skipped: all content comes from the
  repository, supplied by the owner. No external product or standards claims.

## Evidence Used

| Claim in deck | Source in repo |
| --- | --- |
| Case facts: 60,000 homes, five agents L2 to L4, GBP 40m, double delivery | `docs/case_study_48_original.md` |
| Not-for-profit confirmed 26 Sep; legal form unknown | `docs/case_study_48_addendum.md`, log 2026-09-26 |
| 26% below EPC C, 15,600 homes, 3,900 per year, GBP 312m, GBP 7,500 cap, 5,333 homes | Addendum, Provisional Sector Baseline |
| 16 regulatory documents retrieved 19 Sep, four topics | `docs/reference/log.md` 2026-09-19; `docs/reference/regulatory/` |
| Awaab's Law Phase 1 27 Oct 2025, Phase 2 30 Nov 2026 | Original case study, Why Now |
| SRS MEES final policy not evidenced as commenced law | Addendum, Proper Warm table |
| Eight company role agents, labelling rules | `.github/agents/company-*`, repository instructions |
| Role questions (authoritative system for property identity and EPC) | `agent-request-challenge.md`, Questions for Proper North Homes |
| Ten BRD revisions 11 to 26 Sep | `git log --follow docs/brds/agentic-retrofit-programme-brd.md` |
| Agent challenge verdicts and "what to build" | `agent-request-challenge.md`, Summary table |
| Five bounded AI candidates, shared foundation | `agent-request-challenge.md`, Cross-Cutting Findings |
| Control plane and capped readiness plus gated pilots | Addendum, Solution Proposal; BRD Document Status |
| 12 BG, 41 FR, 73 AC, 9 NFR, 6 CON, 23 RULE; 0% to 100% coverage; FAIL | log 2026-09-26 relabel entry; BRD frontmatter; quality report |
| Contradictions: 91% vs 87% interest cover; fuel poverty 10.0% to 11.6% | log 2026-09-25 |
| Divergences: L4 quality flags, L3 digital booking | `agent-request-challenge.md`, Divergences |
| Knowledge base layers, Karpathy LLM Wiki pattern | `docs/reference/README.md` |
| 31 commits, PR #1 | `git log` on 2026-09-26 |
| 85-day plan ending 5 Dec, sessions, fallback demo | `.copilot-tracking/plans/2026-09-19/case-study-85-day-delivery-plan.instructions.md` |
| 15-minute pitch for CEO, CIO, CFO | `docs/reference/memory.md` |

## Storyline

1. Title
2. The request and what it leaves out
3. Five loops (journey)
4. Research
5. Role agents
6. BRD iterations
7. Design thinking: requests as expected value
8. What we really need to build
9. BRD quality review
10. Challenges
11. Knowledge base organisation
12. Traceability chain
13. Next steps and mentor questions

## Global Style

* 16:9, 13.333 x 7.5 in, white content slides, navy title slide.
* Font: Segoe UI (Aptos is not installed locally; Segoe UI renders
  consistently in PowerPoint and exports).
* Palette from the earlier Proper Warm decks: navy #102A43, ink #243B53,
  grey #486581, pale #F0F4F8, line #D9E2EC, teal #1B998B, dark teal #0B625B,
  blue dark #1D5FB8, red #C44536, amber #F2C14E.
* Footer source line on every content slide.

## Gaps and Open Questions

* The owner's name is not in the repository; the title slide omits it.
* `docs/presentations/proper-warm-cxo-initial-proposal.pptx` is deleted in
  the working tree (owner change); not referenced by this deck.
