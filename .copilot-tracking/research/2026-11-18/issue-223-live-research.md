# Issue 223 live demo research (opened 2026-11-18)

Refs #223. Scope: synthetic desktop demo; owner decisions of 2026-11-18 apply (live Azure authorised, rg `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Production-only criteria stay deferred (#1905-#1908).

## Research disposition

Disposition: executed. Existing harness `src/agents/src/zava_forward/agents/review_effectiveness.py` (scripted panels, `--worksheet`, `--score`) and `src/core/.../human_review_effectiveness.py` are the baseline; the live demo app `ca-cutover-test-demo-api` provides the real review path (`/api/cases/<id>/ai`, `/api/ai/review/<rec>/<action>`).

## Questions

1. Does the committed harness run and fail default-accept, automation-bias and unauthorised panels (criteria 1, 4, 5)?
2. Does the live demo retain reviewer, source and reason on a review (criterion 2)?
3. Can a competent human exercise be recorded for the demo (criteria 1, 3, 5)? An agent is not a competent human participant and OQ-017 holders are unappointed.

## Planning readiness

Ready: evidence plan is local harness run, live browser review through the employee test account, a research note under `docs/reference/research/`, no source edits.

## Findings

* Harness run (`harness.json`): competent panel detects 4 of 4 seeded defects (3 corrections, 1 rejection), 0 uncorrected through the gate, gate passed; default-accept and automation-bias panels detect 0 of 4 and fail; unauthorised reviewer fails; per-class sensitivity panels and an over-rejecting panel fail; audit chain verifies. Effort 23 units against 24 workflow-only (scripted comparison units, not measured time).
* Focused tests: `tests.test_review_effectiveness` 37 OK; `tests.test_human_review_effectiveness_223` 6 OK.
* Live demo app: the deployed `ca-cutover-test-demo-api` runs the real `ai_run` and `review_ai` path. AI mode falls back to the workflow template (`source: template`, `model: null`) because no live model task is activated, so a live seeded-defect trial cannot be injected without a source change or a production-style activation.
* Live review retention: a rejection without a reason is refused (400); a rejection with a named source records `reviewer_action`, `reviewer_reason`, `resolved_by`, `source_hashes`, `case_version` and the compared AI and workflow output; a second review is refused.
* Adverse attempts kept: three failed driver runs (zero cases from a wrong response key; HTTP 403 from the Playwright request context even with `X-ZF-CSRF`; missing `record_id` key). The in-page fetch route is what the web app itself uses.
* No competent human participant or appointed OQ-017 holder exists; the owner removed legal, privacy and assistive-technology approvals from demo scope, but an agent run is not human evidence.

## Planning readiness (updated)

Ready.
