<!-- markdownlint-disable-file -->

# Primary Research: AMA Mentor Progress Review Deck

## Purpose and Audience

* Audience: AMA mentor, first mentoring session (week of 28 September 2026).
* Goal: summarise the case, the request, how the gaps were filled, the
  challenges met, and how the repository is organised so every decision can
  be justified or challenged.
* Length: 13 slides plus one appendix slide, speaker notes capped at about 2,000 words (about 14 minutes) so the mentor has 10 to 15 minutes for questions.
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
| 12 BG, 44 FR, 85 AC, 9 NFR, 6 CON, 24 RULE; 0% to 100% coverage; six runs; FAIL | BRD v0.5.0; quality report Runs 1 to 6 |
| Agent-led modernisation, digital foundation, one locality with existing teams | Addendum (Executive Proposition; Where Agents Fit); BRD Document Status owner decision; log 2026-09-26 reframe entry |
| Comparison 1 and 2, dashboard versus scorecard, RULE-024, OD-34 proposal | pilot-measurement-challenge.md (Summary; Owner Decision); BRD RULE-019, RULE-024 |
| CON-003 Article 22 fix (local text: 22A to 22D; CON-003 cites 22A to 22C), AC-079, FR-042 to FR-044, OD-39 | log 2026-09-26 transparency entry; BRD v0.5.0 |
| Contradictions: 91% vs 87% interest cover; fuel poverty 10.0% to 11.6% | log 2026-09-25 |
| Divergences: L4 quality flags, L3 digital booking | `agent-request-challenge.md`, Divergences |
| Knowledge base layers, Karpathy LLM Wiki pattern | `docs/reference/README.md` |
| 35 commits, PR #1; 12 commits touch the BRD | `git log` on 2026-09-27 |
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
8. What we build: digital foundation, bounded agents, accountable people
9. Proving and explaining the value
10. BRD quality review
11. Challenges and lessons
12. Traceability chain
13. Next steps and mentor questions
14. Appendix: knowledge base organisation

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
* `docs/presentations/proper-warm-cxo-initial-proposal.pptx` was deliberately
  removed by the owner (confirmed 2026-09-27). This deck is published to
  `docs/presentations/ama-mentor-progress-review.pptx`.
