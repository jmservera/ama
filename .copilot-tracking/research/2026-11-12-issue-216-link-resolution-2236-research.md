---
title: Research for #216 citation and card link resolution regression
ms.date: 2026-11-12
---

* Task: issue-216-link-resolution-2236, Refs #216 (parent #208). Base eac1206c6.
* Research disposition: executed (issue body and all comments, main source, existing tests, local probes). Mandatory case-study, reference index, memory and agents README reads done.
* Delivered and excluded (not duplicated): #355 gates, #506 usage, #684 limit guard, #834 paired scorer, #890 alert scorer, #963 owner-agreement check, PR1379 constructed paired-report consumer.
* Still human/live/unadmitted (not touched): owner thresholds and independent grader (AC1), staff paired trial (AC4), cost per accepted check and live run authority (tokenomics).
* Finding: `regulatory_gates.grade_answer` states its oracle is "fixture-authored, not actual retrieval or output citation membership". Citation `link` and card `link` are only compared as exact strings. `card["link"]` truthiness is the only link check in the paired comparison. No test follows an emitted `/api/law/provisions/...` or `/api/law/cards/...` link through the real HTTP routes. `regulatory_ux_check` follows one link, but only in the opt-in browser harness.
* Local probes (scratch, removed): base, long-text (excerpt_truncated) and v2 scenarios all resolve; id, version, hash, status match; quote is a prefix of resolved text; hash equals sha256 of the full resolved text. No defect found, so the gap is a missing regression, not a bug.
* Candidate scope: one loopback API regression in `src/api/tests/test_regulatory_chat_api.py` that follows every emitted citation and card link and checks the resolved target matches the cited content, with negative controls (dangling and swapped links fail). Synthetic data only; zero provider calls.
* Planning Readiness: Ready.
