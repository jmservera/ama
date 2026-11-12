<!-- markdownlint-disable-file -->
# Narrow engineering proposal for the #184 live demo: plan (2026-11-12, Refs #184)

Task `issue-184-narrow-design-proposal-1112`. Research: [research](../../research/2026-11-12/issue-184-narrow-design-proposal-1112-research.md). Details: [details](../../details/2026-11-12/issue-184-narrow-design-proposal-1112-details.md). Critique: [critique](./issue-184-narrow-design-proposal-1112-critique.md). **NO IMPLEMENTATION, NO EXECUTION.** Base `b6f61b12`.

## Objective

Answer the single owner design question left by PR 1454 with one focused, reviewable proposal inside the existing IoT research synthesis, so the owner can later decide, separately, whether to permit implementation and, separately again, whether to authorize a named finite live, model and spending run. The proposal approves neither.

## Scope

In scope: documentation only.

* Proposal section in [the IoT research synthesis](../../../docs/reference/research/iot-sensor-analytics-research-plan.md), with an index pointer in [the knowledge-base index](../../../docs/reference/README.md) and an entry in [the log](../../../docs/reference/log.md).
* These dated tracking artifacts and their state record.

Out of scope and unchanged: all source, tests, infrastructure and workflows; the 2026-11-11 plan set and the adverse report; the guards F11 in the research; issue, board and pull request state; any run, install, cloud, SQL, model or spend.

## Content map (the five requested areas)

| # | Area | Where it lands |
| --- | --- | --- |
| 1 | Run-specific message, receipt, reading, same-home and Quality proposal correlation; historical versus current; start, checkpoint and bounded completion | details section 1, doc subsection 1 |
| 2 | Expiry and total attempts across retries and replicas, durable shared fence, failure and manual path; no false cancellation or exactly-once billing | details section 2, doc subsection 2 |
| 3 | Finite call, token, reservation and compute admission; retries counted; bytes versus tokens; unknown liabilities; enforceable versus illustrative | details section 3, doc subsection 3 |
| 4 | Smallest behavior-preserving source changes with anchors, stages, tests, evidence plan, prerequisites and decisions | details section 4, doc subsection 4 |
| 5 | Exact future approval handoffs | details section 5, doc subsection 5 |

## Design stance (fixed for the proposal)

* Default-off optional parameters. Every proposed change keeps today's behavior when the new input is absent, and each has a regression test for that.
* Fail closed, count conservatively, never refund an uncertain attempt.
* Do not weaken the captured-reading guard, the scanner scope claims, expiry, currency, headroom, OD-51, #440 or any human, resident, consent or professional boundary. Record the guard as an owner decision, not a proposal.
* Distinguish enforced limit, arithmetic envelope and illustration in every number.
* No price is certified as current; the 2026-11-11 record is cited as a historical illustration.

## Phases

* [x] Research (executed)
* [x] Plan (this file)
* [x] One critique pass (see critique file; execution and disposition recorded separately)
* [x] Documentation implementation
* [x] One Review (author, not independent), then stop

Independent exact-head review stays with the coordinator before any publication. No second critique, review or correction cycle is run.

## Follow-ups (not selected)

1. Owner decisions D1 to D6 in details section 4.
2. Separate implementation permission, then separate named execution authorization (details section 5).
