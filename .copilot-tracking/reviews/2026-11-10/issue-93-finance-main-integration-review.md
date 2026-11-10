---
title: Issue 93 finance main integration review
description: Single post-implementation review of the merged finance candidate
ms.date: 2026-11-10
---

Execution: once, 2026-11-10T01:06Z, by the implementing author against the merged tree after the changes record. Independent exact-head assessment by the coordinator remains required and is not replaced by this review. Changes: [changes](../../changes/2026-11-10/issue-93-finance-main-integration-changes.md).

## Outcome

Conformant for the stated bounded scope, with no open material finding and no correction cycle used (0 of 5). Boundary: the merged local tree at the commit holding this record, selected Core form tests, the complete main form-staging API module, strict mypy for Core and API, and Ruff on the six Core product paths. Not assessed: MSSQL (no contract exists), browser, full gate, hosted CI, human approvals.

## Assessment

| Check | Result |
| --- | --- |
| Ordering of RPI evidence | Research, plan, details and critique were committed (`05aaca608`) before either merge or any test; observations and this review follow. |
| Ordinary merges, no rewrite | `9fce46fb4` and `fff8cbe25` are `--no-ff` merges; first parent chain keeps finance `4642b55f`, `05aaca608`; no cherry-pick, reset, rebase or force. |
| Product preservation | Six product blobs equal `4642b55f`; `src/core/README.md` differs from main by exactly the parent delta (39 added, 7 removed from the merge base). Ordered detached history and Invalid-and-regenerate semantics unchanged. |
| Main ownership | `server.py` and `test_form_staging_api.py` blobs equal main; no reserved hook, store, sqlstore, schema or `resident_decisions` path edited. |
| Verification records | Seven records byte-identical to `ef63d180`; process deviation (heredoc creation by original author) preserved. |
| Tests | 67 Core plus 14 API unique, 0 skips; 2 history tests inside the 67. Not counted as a pass for MSSQL. |
| Static | Core and API strict mypy pass; Ruff check and format pass on the six paths. Adverse intermediate mypy runs were missing dependencies, resolved by the pinned hashed requirements, not by code changes. |
| Authority boundary | No automated submission, match-funding approval, claim certification or cash recording introduced; export stays `Held`, `reviewed=False`, `Not submitted`. No approval inferred; BRD 0.21 draft and PRD 0.21 in-review unchanged. |

## Findings routed to later work

* R1 (limit, not defect): the MSSQL form and history contract is absent. Routed to a later user-selected research item to decide whether one is needed; not invented here.
* R2 (limit): the API form-staging tests ran after the finance modules without reserved-hook changes, but #132 integration order may later alter shared hooks; re-observe after that freeze.
* R3 (limit): Core observation B and API observation C ran before the pinned API requirements were installed; the API module's imports did not need them, and strict mypy passed after. Rerun was not made, to avoid repeating tests as unique.
* R4 (limit): Ruff was run on the six Core product paths only; the README is Markdown without a configured gate.

## Routing

No further work inside this task. Coordinator exact-head assessment, then hosted CI and integration gates before any publication.
