---
title: Issue 93 live research (2026-11-23)
ms.date: 2026-11-23
---

Research disposition: executed. Head 3a18e32175 equals origin/main. Scope: the one unticked criterion C1 (stabilization checkpoint #440), synthetic demo, desktop only.

Evidence (folder `.copilot-tracking/evidence/2026-11-23/issue-93-live-20261123T150451Z/`):

* Issues by REST: #94 #95 #96 #99 closed; #2140 open `delivery:deferred`; #440 open (two unticked criteria); #2301 open (demo-scope checkpoint for nine epics, owns the evidence-pack record); no open `bug` issue; #1837 open.
* Azure read-only: revision `ca-cutover-test-demo-api--0000055` (0000038 on 2026-11-21).
* Live read-only probe, 5 GETs all 200: 13 invoices (7 Received, 6 Exceptions, 6 on hold, none paid); exposure Held with `pause_signal.automatic_cut` false and no decision owner; 167 funding cases (1 Draft ready, 25 To prepare, 141 Not started; grants 163 "No grant record", 4 "Not recorded"); form schemas empty.
* Offline core run, 12 finance/grant/form test modules: 270 tests, 1 FAILURE, 45 skipped. Failure: `test_form_review_pack.test_public_payload_is_registered_and_passes_privacy_checks`; `privacy.public_issues` reports three `unregistered_public_payload` files added by the latest main commit (#2316): `src/agents/evals/eval-manifest.schema.json`, `synthetic-eval-manifest.json`, `synthetic-eval-predictions.json`. Cause: they are absent from `docs/reference/research/retrofit-synthetic-data/provenance-register.json`. The same check backs the finance form review pack, so this is a real regression in the finance test tier, not environment noise.
* Root cause fix candidate: register the files (marker fields `version` for the two synthetic-named files via one glob entry, `description` for the schema, adding a description to the schema).

Planning Readiness: Ready.
