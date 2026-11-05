---
title: Issue 82 quality gate plan (2026-11-05)
ms.date: 2026-11-05
---

## Plan

* [x] Phase 1: failing regression tests for quality evidence at acceptance and handover (details: `../../details/2026-11-05/issue-82-quality-gate-details.md`).
* [x] Phase 2: `gates.quality_gate` with a rule record, `quality.evidence_gaps`, Store `require_quality_evidence`, wiring into `accept_quality`, `hand_over_quality` and `handover_blockers`.
* [x] Phase 3: focused tests, ruff, mypy (tests included), related quality and gate suites, knowledge-base log.
* [x] Phase 4: commit implementation and RPI evidence, then probe the heavy lock with `--lock-timeout 0` (result: see changes record).

Research: `../../research/2026-11-05/issue-82-quality-gate-research.md`. Parent TARGET `feat/controlled-lifecycle-integration-81` at `ead177ef90d24666557708ea344848a1be43bdf8`. Refs #82 only; no closing keyword.

## Critique (single pass, self-run, final candidate)

* Reviewer text stays `Unreviewed exercise rule: named reviewer required before live use`; no sign-off is created. Applied.
* Do not call the gap a bypass: it is stored non-conforming evidence reaching a transition. Applied (research wording).
* Preserve error ordering: wrong-state errors stay `ValueError`; evidence gate runs only for the legitimate source state. Applied.
* Unreadable `items` is unknown and blocks; an empty list is a fail listing every check. Applied.
* Capacity, authority, finance and eligibility are left visibly unconverted. Applied.
* Residual: a Submitted or Fixed record with missing evidence is refused with owner and next action but cannot be resubmitted until a human decides the replacement route; recorded as follow-up, not invented here.
