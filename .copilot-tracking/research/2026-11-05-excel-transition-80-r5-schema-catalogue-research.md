---
title: Issue 80 round 5 research
description: Form-schema catalogue CSV, replacing the pending checklist-only handoff
ms.date: 2026-11-05
---

Research disposition: executed (source verification) plus reuse of rounds 1 to 4. Planning readiness: Ready.

## Coordinator decision

The pending checklist-only frozen head `7e1566ebab45900afb2afb2abcde9249c2a7ef74` (tree `2aa032dff1b6b6de9944f2f0bc9deec54fe4647a`, merged main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, parent `ead177ef90d24666557708ea344848a1be43bdf8`) is replaced by a combined checklist plus catalogue candidate on the same branch. 7e1566 stays historical and unamended; it has no FULL receipt, so no earlier evidence counts as final-head validation.

## Verified facts in current source

* `forms.list_schemas(store, user)` (`core/forms.py`) calls `_actor`, which requires current Finance (`FINANCE_VIEW`), resident-record (`RESIDENT_VIEW_ROLES`) and reason-view rights, re-reads the registered staff record, and calls `store._doc_role(actor, "read")`; it returns a deep copy of `form_schemas`. Rows are `definition, digest, approval, approval_evidence, source_policy_status, recorded_by, recorded_at`; new rows are `Unapproved` with null evidence. Definitions carry reviewer and evidence references, so this is not a public constant.
* `get_kind("/api/form-schemas")` is `forms`, already in `STAFF_GET`; the export registry (`LIST_EXPORTS`, `EXPORT_KINDS`) maps a `.csv` path to a kind, so no new permission kind is needed. `list_export.to_csv` handles nested JSON and formula prefixes.
* JSON route wraps the list as `{"schemas": [...]}`; the export route uses the list directly.
* RULE-026/AC-096 forbids management export of individual conversation or memory content; no chat export is added.

## Overlap

No `quality.py` or core edit, so the #82 conflict surface is unchanged. Nothing from #96 financial-review or #79 is touched.

## Scope limit

No web edit: no download link on form screens, so the form-screen affordance is not claimed. Every-list and owner-threshold criteria stay open.
