---
title: Issue 96 criteria 5 and 6 plan
description: Close the proposal-staleness exposure gap and prove criteria 5 and 6 end to end
ms.date: 2026-11-13
---

Details: [96-export-stale-isolation-2035-details.md](../../details/2026-11-13/96-export-stale-isolation-2035-details.md). Research: [96-export-stale-isolation-2035-research.md](../../research/2026-11-13/96-export-stale-isolation-2035-research.md).

## Phases

* [x] P1 Core end-to-end tests for criterion 5 (whole-store no-write, Held metadata) and criterion 6 (source, rule, schema selectivity incl. approvals); already passing.
* [ ] P2 Failing-first: Core and API tests that the served review view carries per-proposal staleness limited to dependents.
* [ ] P3 Add `dependency_impact.proposals` to `form_review.view`; make P2 pass.
* [ ] P4 Show dependent proposals and approvals needing re-review in the funding panel; no new banned terms; no new request.
* [ ] P5 API end-to-end test of criteria 5 and 6 over HTTP, including another case left untouched.
* [ ] P6 Validate (targeted tests, ruff, mypy), remove only `/tmp/venv-96se-2035`, commit `Refs #96`.

## Boundaries

No push, no GitHub edit, no schema, approval or eligibility authority. Form-wide rule references stay broad.
