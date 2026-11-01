# Research: issue 203 verify references after cleanup (2026-11-01)

Research disposition: executed. Planning Readiness: Ready.

## Prior delivery (merged PRs referencing #203)

* #289 ADR 0006, #291 parity matrix, #321 CI/image cut-over (no Azure), #499 retire mvp/prototype (no literal zero-token, no post-merge rubric, no hosted-green claim), #613 closure audit (criteria 1, 2, 4, 5 unmet). No open PR for #203.

## Fresh evidence on main 77b55415

* `mvp/` and `prototype/` do not exist. Token search outside `.copilot-tracking` finds historical records, defensive `mvp/data` checks (src-ci, mvp-validation, rpi-checks, .gitignore, tests), rubric README history and generic "prototype/PoC/MVP" wording.
* One live stale pointer: `docs/reference/regulatory/README.md:108` (`mvp/law/law-source-register.json`; now `src/core/src/zava_forward/core/law/law-source-register.json`).
* Link audit (all tracked Markdown, excluding tracking and support): 102 unresolved, from capstone reorganisation (`docs/capstone/history/*` 74), `docs/reference/log.md` (17, immutable), addendum (2), architecture README (1), reference README (2), rubric-score.md template placeholder (2). None caused by cleanup except old `mvp/README.md` anchors in the immutable log.
* Rubric: baseline_total 77. Recent main runs of Capstone Rubric Scorer are mostly cancelled/skipped; run 41281943087 logged "Daily workflow AIC guardrail exceeded 10370/10000". No post-cleanup main total is retrievable.
* src-ci triggers on pull_request/workflow_dispatch only; last main runs 2026-10-18. No deployed-app evidence; Azure-live not authorised.

## Decision

Deliver only doc fix, log entry and evidence; keep all unmet criteria open.
