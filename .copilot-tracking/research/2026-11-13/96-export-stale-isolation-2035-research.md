---
title: Issue 96 criteria 5 and 6 research (export non-submission, scoped staleness)
description: Audit of Core export and staleness propagation against the two open software criteria
ms.date: 2026-11-13
---

Research disposition: executed. Planning Readiness: Ready. Task slug `96-export-stale-isolation-2035`, branch `feat/demo-96-export-stale-isolation-2035`. Refs #96 (the issue stays open; schema approval and Finance, Legal and privacy authority are outside this task).

## Evidence

| Area | Finding | Source |
| --- | --- | --- |
| Export content | `draft_export` is read-only under `store.lock`, returns status Held, reviewed false, submission "Not submitted", eligibility "Not assessed" and a notice that it does not submit or establish eligibility | `src/core/src/zava_forward/core/form_export.py` |
| Export mutation | Existing tests compare only the audit log; no test compares the whole store or case after export and freshness check | `src/core/tests/test_form_export.py`, `src/api/tests/test_form_held_download_api.py` (API state check covers store data) |
| Web copy | Held download and saved-copy check copy states Not submitted, eligibility Not assessed, and no approval or submission; the content-standard scan covers all web JS lines | `src/api/src/zava_forward/api/web/role-screens.js`, `src/api/tests/test_content_standard.py` |
| Schema impact | `schema_impact` narrows to changed fields, declared `required_when` dependents and calculation inputs; form-wide references (template, rule_refs, funding, reviewer, form_type) stale every field because rule-to-field links are undeclared | `forms.py` |
| Source impact | `_report` marks only fields whose bound source changed; `_proposals` marks only candidates of the changed source or field; `_approvals` marks only bound fields | `form_review.py` |
| Gap G1 | Proposal freshness exists only as `form_review.proposal_freshness`; no API route and the served review view carries approvals and schema impact but not per-proposal staleness, so the API and web cannot show which proposals are dependent | `form_review.view`, `api/server.py` |
| Observation | A source change to a field also changes the open issue of declared dependents (area requires epc), so a saved export names them stale; this is declared dependency, not over-breadth | probe test run 2026-11-13 |

## Probe result

New Core tests (source, rule-version and schema changes with approvals bound to each field) passed without code changes, so the Core propagation is selective for declared dependencies. The one reproducible gap is G1.

## Not changed

* Form-wide rule reference changes stay broad because the schema declares no rule-to-field link; narrowing would invent a dependency.
* No schema approval, Finance or eligibility authority is created.
