---
title: Issue 133 aftercare criteria 1, 2, 4, 5, 6 audit
task_id: 133-aftercare-criteria-2035
date: 2026-11-13
---

## Scope

Audit of unticked criteria of #133 at main `c13d077d29` (branch `feat/demo-133-aftercare-criteria-2035`). Criterion 3 was ticked on 2026-11-13. Research disposition: executed. Planning Readiness: Ready.

## Evidence read

* `src/core/src/zava_forward/core/aftercare.py` (register, guards, pack, evaluator summary)
* `src/core/src/zava_forward/core/aftercare_intake.py` (service, receipts, closures, evaluator view)
* `src/core/src/zava_forward/core/ai_registry.py:127-141` (pack registered, disabled, unapproved)
* `src/api/src/zava_forward/api/web/aftercare.js` (evaluator rendering)
* `src/api/src/zava_forward/api/server.py` (routes `/api/aftercare*` via `AftercareService.handle`)
* Tests: `test_aftercare*` in core and api; there are none in `src/agents` (no aftercare module there; the pack lives in core). `test_content_standard.py` and `test_accessibility_baseline.py` are in `src/api/tests`.
* `staff-intake.js` is the provider job-pack confirmation intake and unrelated to concerns.

## Findings by criterion

### 1 Accessible route including non-digital

* Software proven: staff-recorded route with channel phone, in_person, paper, assisted_visit; representative basis required and kept verbatim; staff identity required; plain-language field errors; native labelled form tests; `ACCESSIBLE_ROUTE` text on every record.
* Not software scope: there is no resident self-service digital portal in this demonstrator (service requires staff roles; `_validate` requires `route == staff_recorded`). Remaining: human assistive-technology sign-off and owner decision on a resident-facing route. Documented, not a code gap.

### 2 Owner, outcome, remedy not erasable by closure

* Existing: register and service closure tests with one concern and one outcome.
* Gap (tests): no regression covering closure before a concern is raised, closure when a concern has an outcome plus a remedy in progress, outcome and remedy recorded after closure, a persisted restart, history untouched, other homes untouched, and an unknown-owner concern.
* Gap (code): `_validate` and `from_state` do not refuse a snapshot where a `completed` or `not_needed` remedy lacks evidence or has no outcome, so a restored store could present a closed remedy without evidence. To be tightened.

### 4 Evaluator view

* API payload carries baseline per home, outcomes, unresolved fraction, households-raising fraction, out-of-scope count, closure-unresolved count and unknowns.
* Gap (rendering): `aftercare.js` omits households raising a concern (with denominator), concerns outside stated scope, unresolved with closure, the baseline window definitions, and the per-home unresolved column has no denominator.

### 5 No causation, blame or savings

* Existing guard: banned phrases and paraphrase patterns, applied to templates, sensor context, evaluator notices, pack text and web static strings.
* Gap: probe of further paraphrases (to be run) such as "reduces your bills", "lower bills", "saves money", "due to the household", "result of the retrofit", "tenant's fault", "overuse". Strengthen patterns conservatively with tests for accepted neutral text.

### 6 Optional AI concern pack

* Existing: pack registered as `aftercare-concern-pack`, disabled, unapproved, `authorizes_live` false; template always available; AI summary guarded; owner-only review; review never changes the concern.
* Gap: `propose_pack` appends `pack_proposed_*` to the concern `history`, a direct record mutation, and the existing test excuses it. Pack provenance should live only on the pack. No API route exposes packs, so no route mutation exists; test to assert that.

## Planning Readiness

Ready. Follow-ups: human AT sign-off (criterion 1), DPO position and evaluator role access (issue), resident self-service route decision.
