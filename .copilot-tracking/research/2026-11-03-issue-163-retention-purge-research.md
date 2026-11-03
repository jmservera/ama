---
title: "Issue 163 retention purge research (2026-11-03)"
ms.date: 2026-11-03
---
Research disposition: executed (reused prior 2026-11-01 evidence). Planning Readiness: Ready.

* Merged delivery: #281, #286, #503, #649, #727, #735, #745 and the 2026-11-01 owner demo approval. Criteria 1, 3, 4 and 6 are ticked on the issue.
* Unmet: criterion 2 (lawful basis, notice, DPIA decision, no period before approval) and criterion 5 (provider terms and region position). Both need DPO and Legal (named owner Juan Manuel Servera). The owner deferred them to before production; the demo approval covers synthetic data only. No agent can satisfy them.
* Provider page re-read 2026-11-03: updated 2026-06-05, matches the recorded position; nothing new.
* Advanceable gap found in the approval record: the 30-day demo period is not enforced for threads and messages, and nothing purges them.
* Chosen slice: a repository-level purge for threads and messages plus a privacy-layer method that applies the recorded period. No scheduler (infrastructure) in this slice.
