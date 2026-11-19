---
title: Research for issue 138 summarize_plan Unsupported rejection
ms.date: 2026-11-18
---

## Scope

Refs #138. Task: make `summarize_plan` (`infra/scripts/pipeline.py`) reject `Unsupported`
what-if entries and add a regression test. Synthetic demo, desktop only. Research disposition:
executed (opening note; findings appended below).

## Findings

* `summarize_plan` already allows only `Create`, `Modify` and `NoChange`; any other `changeType`
  raises `PipelineError`. `Unsupported` is therefore already rejected.
* `infra/tests/test_pipeline.py::test_plan_rejects_delete_unknown_out_of_scope_and_public_sql`
  covers `Unsupported` only as a lone entry, bundled with other kinds, so a failure would not
  name `Unsupported`, and no case proves a single `Unsupported` entry among valid entries fails.
* Prior notes (r3, r4) record that the live what-if has 14 `Unsupported` and 81 `Ignore`
  entries, so the live plan is refused. Rejecting is the stated goal; accepting them would be a
  separate owner decision and is not made here.
* Planning readiness: Ready. Change is test-only; no behaviour change.
