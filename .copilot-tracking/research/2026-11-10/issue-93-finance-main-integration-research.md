---
title: Issue 93 finance parent main integration research
description: Prospective research for the bounded integration of the finance parent branch, its verification records and pinned main
ms.date: 2026-11-10
---

## Scope and disposition

* Research disposition: `executed` (new, bounded; written 2026-11-10T01:00Z to 01:10Z before any merge or test). Refs #93 only. Not epic completion, not new #96 features, not #440 closure.
* Brief: coordinator common brief plus the task brief. The task brief overrides stale ownership text: Quality1288 is evidence-only, #132 still reserves shared API, navigation, store, procurement and sqlstore hooks, and #1238 owns `resident_decisions` and its test module.
* Issue #93 body (read from the coordinator file) lists three unticked criteria: the #440 stabilization checkpoint, all children closed or deferred, and no automated path submits, approves match funding, certifies a claim or records cash. This work ticks none; it is a Refs-only integration.
* Contract documents: BRD 0.21 is `draft` and PRD 0.21 is `in-review` per the verification research of the same day; neither is approved by this work.
* Not duplicated: the post-#1233 documentation checkpoint was consumed through #1234 (#440 comment `6679709806`). The approved synthetic full-history export and Invalid-and-regenerate semantics for pre-history copies are preserved, not reopened.

## Identities read from local Git objects (before any merge)

| Item | Exact identity |
| --- | --- |
| Worktree | `/home/azureuser/source/ama-demo-wt/issue-93-finance-main-1110` |
| Branch | `feat/finance-integration-93` |
| Branch ref at session start | `0472fd5d5625bb610b5ac65ad177026953802830` (the local ref lagged the brief) |
| Brief pin and `origin/feat/finance-integration-93` | `4642b55fdbafec564b67803420439b91d7ea8ce1` |
| Action taken | `git merge --ff-only 4642b55f`: a non-destructive fast-forward (HEAD was an ancestor), only to reach the brief's stated pin; no reset, rebase or force |
| Verification branch | `test/demo-finance-parent-440-1110` at `ef63d180dcdd2684dad8e1f9df6016619f104ef7`, one commit ahead of the finance pin, adds exactly seven records under `.copilot-tracking/` (235 insertions) |
| Main pin | `5318f738f6bc58a10a9d4df1ca18ae51c1547a79`, equal to `origin/main` after fetch |
| Merge base (finance and main) | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`; 83 commits only on main; finance adds #1223 and #1233 |
| Git author and committer email | repository-local `8036360+jmservera@users.noreply.github.com`, matching `gh api user` (id 8036360, login jmservera) |

## Exact parent delta (finance head versus merge base, excluding tracking)

Seven `src` files plus one log entry: `core/form_export.py` (+7), `core/form_review.py` (+210/-31 net), `core/forms.py` (+104), `core/README.md` (+46), `tests/test_form_dependencies.py` (+360, new), `tests/test_form_export.py` (+57), `tests/test_form_review.py` (+12), and `docs/reference/log.md` (+3). Behaviours:

* `forms.schema_impact` and `_lineage`: read-only, field-level schema-impact narrowing, `Unknown` when lineage is missing or malformed; undeclared links stay stale.
* `form_review.proposal_freshness`, `_proposals`, `_approvals`, `_bound_causes`: read-only per-candidate and approval-reference evaluation; nothing is approved, staged or written.
* `form_export` (#1233): the Held export body now carries the ordered per-field `history`, `schema_impact`, and `export_freshness` reports `Invalid` for copies lacking `history`, which must be regenerated as a new Held export.
* The product never submits, approves, certifies, calculates eligibility or records cash. `status="Held"`, `reviewed=False`, `submission="Not submitted"` are preserved.

## Current-main overlap

| Surface | Main change since merge base | Class |
| --- | --- | --- |
| Finance product source and test files (six of the seven) | none (`git diff --numstat` empty) | no conflict possible |
| `src/core/README.md` | +356/-10 | append-style documentation overlap; `git merge-tree` of verification branch with main reports a clean tree (no conflict) |
| `docs/reference/log.md` | +711/-1 | append-only; clean in the same dry run |
| `src/api/src/zava_forward/api/server.py` | `/api/form-schemas.csv` list export (`LIST_EXPORTS`, row map, `list_rows`) and unrelated hunks | MAIN-owned shared hook; byte-preserved, not edited |
| `src/api/tests/test_form_staging_api.py` | +149/-1 CSV export and projection tests | MAIN-owned; byte-preserved |
| `core/store.py`, `sqlstore.py`, `procurement.py`, `mssqlstore.py`, role-screens | other issues' changes; zero form-related changed lines beyond generic `form_schemas` document handling | reserved #132 hooks; no edit |

Dry-run `git merge-tree --write-tree test/demo-finance-parent-440-1110 5318f738` returned a tree and no conflict list. That is a prediction; the real merge result is recorded in the changes record.

## Contracts and selectors

* Form modules `forms.py`, `form_review.py`, `form_export.py`, `form_staging.py` are unchanged on main apart from the parent delta. The dependency-pointers imports (`ai_registry`, `identity`, `controls`, `documents`, `change_provenance`) were checked by the earlier verification as unchanged; `projection.py` and `doc_controls.py` have small main drift and are exercised by the selected tests only if imported.
* Core selectors (from `src/core`, ordered): `tests.test_form_dependencies`, `test_form_review`, `test_form_review_pack`, `test_form_export`, `test_form_staging`, plus the two history tests the earlier observation named. Main API selector: the complete `tests.test_form_staging_api` module from `src/api` (including the 149 added lines). Project gates: strict mypy for `src/core` and `src/api` per each `pyproject.toml` (`strict = true`, `files = ["src", "tests"]`), and Ruff check/format for the seven product paths, honouring the per-project `ruff` pins (`ruff==0.17.1`, `mypy==2.4.0` in the core dev extra). `src/api/pyproject.toml` pins are read at execution.
* The ambient pip editable installs of `zava-forward-{core,api,agents}` point at the primary checkout. They must not be used. A new isolated environment installs this worktree's projects with direct_url proof.

## SQL and MSSQL contract search

* Searched main and the merged candidate for MSSQL or SQL tests referencing `form_reviews`, `form_staging`, `form_schemas`, `form_review` or `form_export`: matches exist only in `core/tests/test_form_*.py`, `test_funding_automation_boundary.py` and `api/tests/test_finance_grants_screens.py`, `test_form_staging_api.py`; none is an MSSQL/SQL-backed test and none uses `sqlguard`. `sqlstore.py` mentions `form_schemas` once, as one generic document name in a document list (`DOCS`).
* The parent product does not modify `sqlstore.py`, `mssqlstore.py`, schema or any persisted record shape: new report fields are computed read-only and returned, and exports are returned to the caller, not stored in SQL.
* Finding: no MSSQL form-review, history or form-export contract exists to run. This is reported as an absent contract, not a pass. SQL is not materially impacted by this integration, so no heavy-resource admission is planned or taken. If critique disagrees, the plan reverts to one nonqueued admission with owned localhost disposable SQL only.

## Environment and tooling findings

* Python 3.12.3. Pinned tool versions come from the project files at execution (core dev extra `ruff==0.17.1`, `mypy==2.4.0`; hashed build requirements `src/build-requirements.txt`, as the earlier verification used). Install happens only into a fresh external environment `/tmp/issue93-finance-main-1110/venv`, no `uv`, no `PYTHONPATH` source hack, no global install.
* Core test module names that also exist under `src/api/tests` are not selected from Core. Core runs from `src/core` and API from `src/api` in separate invocations; resolved paths are recorded.
* `api` runtime dependencies (aiohttp, Azure SDKs, `core[sql,blob]`) may be heavy. The earlier observation ran the API module with imports that resolve without them; if main's API module or strict mypy need them, install only after a recorded missing-dependency failure.

## Boundaries and stop rules

* Edits limited to tracking records and, if the ordinary merges conflict, append-only resolution in `src/core/README.md` and `docs/reference/log.md` preserving both histories. No edit to `server.py`, role-screens, store, sqlstore, mssqlstore, procurement, schema, tests owned by main or #1238, or finance rules, eligibility, calculation, approval or submission. Any semantic reconciliation outside the seven product files stops the loop with the exact conflict.
* Five total review-correction cycles maximum; this is the first loop. A source or test failure is reproduced and scoped before repair; a significant unexpected defect pauses for the coordinator.
* No Azure, private data, credentials, model or provider call, release activation, financial commitment, named approval or role grant. No push, PR, issue or board write.
* Process deviation to preserve: the verification records were created by their original author through shell heredocs. This task writes its records with the file edit tool only.

## Planning Readiness

Ready. Unknowns before execution: real merge result, whether API imports and strict mypy resolve in the isolated environment, and whether the main CSV tests pass with the finance modules.
