---
title: Issue 223 human-review effectiveness test research
ms.date: 2026-11-01
---

## Task

Issue #223 (AC-070, FR-026, FR-027, NFR-009, OQ-017). Research disposition: executed. Planning Readiness: Ready.

## Evidence

* `src/core/src/zava_forward/core/ai_tasks.py` `review()` records reviewer, disposition, reason, compared AI and workflow outputs and source hashes in `review_evidence`; accepting never satisfies an approval (FR-026). `source_labels()` lists every citable case fact.
* `src/agents/src/zava_forward/agents/ai_eval.py` is the offline harness (scripted model, no network); `run_task_checks` shows citation validity is checked by the store, so a wrong claim with a valid citation passes citation checks (the gap AC-070 targets).
* `src/agents/evals/` holds golden data outside the package; tests live in `src/agents/tests/`.
* PRD AC-070: seeded wrong, stale, unsupported and incomplete critical proposals plus correct controls; defects detected and kept from a controlled gate; reviewer, source, reason retained; detection, corrections and effort reported against the same workflow-only scenarios; default acceptance and citation validity alone cannot pass.
* OQ-017 (reviewer authority and meaningful-oversight evidence) is open; no authorised human participant protocol exists (`OPEN_ITEMS` in ai_eval.py).
* Dependency #106 closed; #108 open (harness exists offline).

## Findings and decisions

* Deliver an offline module `zava_forward.agents.review_effectiveness` plus `evals/review_effectiveness_golden.json`, driving the real `Store.ai_run` and `Store.review_ai`.
* A controlled gate is evaluated by the harness: a seeded defect satisfies it only if a competent reviewer edits or rejects it with a reason and a source label that resolves in the case; an accepted defect is a failure.
* Reviewer panels are scripted: competent, default-accept and citation-valid-only (automation-bias). Scripted panels prove the gate and measurement, not human competence.
* Provisional reviewer authority for the run: the case owner in the Resident Liaison role (as enforced by `review`); real OQ-017 authority stays an open owner decision.
* Unmet by this slice: evidence from authorised competent human reviewers (AC-070 as written), so use `Refs #223`.
