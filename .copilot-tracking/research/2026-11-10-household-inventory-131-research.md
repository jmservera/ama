---
title: Issue 131 case-local expected-household inventory primitive research
ms.date: 2026-11-10
task_id: 131-household-inventory-1110
---

## Disposition and scope

Research executed 2026-11-10 (UTC 07:19 onward), after the research stub, state file and `research-open` witness event. Planning Readiness: Ready.

Scope is exactly the INITIAL, explicitly deferred and unprovided case-local expected-household inventory primitive selected by Root from `demo-131-bounded-inventory-refinement-1110.md` (a source-qualified engineering proposal, not tested behaviour and not company fact). It is not a repair or rebranding of the existing #131 tenure intake, verification, question-pack or review-trigger work, and it is not a new corrective budget. The historical numeric corrective balance is UNKNOWN and no post-review grant exists. R1 to R4 are functionality stages, not correction counts.

Out of scope and unchanged: new endpoint, SQL schema, UI, role, Legal interpretation, actual company roster, attestation or approval authority, hold release, store/sqlstore/server/projection edits, and unrelated owner hunks (#153 app, #130 tab, #230 paging, #231 role checker, #233 atlas, #156 design).

## Identities

| Item | Value |
| --- | --- |
| Worktree | `/home/azureuser/source/ama-demo-wt/issue-131-household-inventory-1110` |
| Branch | `feat/demo-household-inventory-131-1110` |
| Base (main) | `fe59ef56a0084dd975fd7e5c342670bb8f788fb0`, clean worktree at start |
| Python origins | owned external venv `venv-131-household-inventory-1110` (Root files folder); editable installs resolve to this worktree: `src/core/src/zava_forward/core`, `src/api/src/zava_forward/api`, `src/agents/src/zava_forward/agents` |
| Pre-existing editable install | system site-packages points at a different worktree (`/home/azureuser/source/ama`); not used and not modified |
| Dependency note | first install into a fresh venv failed with `invalid command 'bdist_wheel'` (log kept as `venv-install-attempt1-wheel-missing.log`); `wheel`, `setuptools`, `ruff 0.17.3`, `mypy 2.4.1` were then installed with pip into the owned venv only |
| `ZF_DATA` | owned synthetic path under the Root evidence `run/zfdata-baseline/`; no default private dataset read |

## Unchanged baseline (before any edit)

| Command (from the component folder, owned venv) | Result |
| --- | --- |
| `python -m unittest discover -s tests -p test_resident_decisions.py -q` (src/core) | `Ran 371 tests`, `OK (skipped=132)`, exit 0 |
| `PYTHONPATH=../core/tests:../agents/tests python -m unittest discover -s tests -p test_resident_api.py -q` (src/api) | `Ran 20 tests`, `OK (skipped=1)`, exit 0 |

Raw logs: Root evidence `run/baseline-core-resident.log` and `run/baseline-api-resident.log`. The tenure, verification, question-pack and review-trigger tests live in these two files. Skips are the opt-in MSSQL, Azure, browser and JSON-only or SQL-only cases; SQLite `SqlStore` runs through `SqlResidentDecisions`. No baseline product failure; no earlier failed or reviewed candidate for the same inventory contract was found (the source and tracking contain no inventory action). The STOP condition does not apply.

## Verified code hooks (all in `src/core/src/zava_forward/core/resident_decisions.py`)

| Hook | Evidence | Use |
| --- | --- | --- |
| `RESIDENT_ACTIONS`, `INTAKE_ACTIONS` tuples (lines 29 to 48) | action registry and `_operation` routing in `resident_action` | add `tenure_inventory_record` |
| `RESIDENT_FIELDS` | deletion loop in `delete_resident_records`, retention listing in `doc_controls.py`, resident data copy in `projection.redact_staff_detail` | add the raw field so deletion and role copies cover it; `tenure_review_required` is not in the tuple so deletion retains the durable flag |
| `INTAKE_FIELDS` | popped by `projection.redact_staff_detail` and `Store.detail` for readers without current evidence rights | add raw field and derived view key, so both current read paths strip them without edits to those modules |
| `_intake_fields`, `_intake_text`, `_intake_owner`, `_version`, `_day`, `_digest`, `_identity`, `_time` | shared strict-input, owner, version and digest conventions | reused unchanged |
| `_res_tenure_intake` (about line 1025) | report version is the list position; `household_ref` opaque 100 characters | linked reports are addressed by that version |
| `followup_view` (line 341) | called on the detached JSON copy by `Store.detail` | add the pure derived view |
| `resident_gate` (line 818) and `_res_scope_record` (line 1343) | both return or raise the unconditional `TENURE_HOLD` when a tenure flag or reports exist | add inventory-specific refusal reasons before the hold; keep the hold |
| `_operation` and `validate_sql` | atomic writer, rollback, SQL replay on the current persisted case with current actor and owner | new action joins via `INTAKE_ACTIONS`; no other writer |

Existing tests assert `resident_gate(case) == [TENURE_HOLD]` for cases that have reports but no inventory (about eleven assertions). Decision D1 below keeps those unchanged.

## Design decisions (Root's selected slice applied)

* D1: inventory refusal reasons appear in `resident_gate` and `scope_record` only when the inventory field is present (recorded, Unknown or malformed). A managed case with reports or the flag but no inventory field keeps exactly `[TENURE_HOLD]`; the pure view still reports "no inventory recorded" as a reason. This preserves existing behaviour and tests, and a missing inventory still refuses through the unconditional hold.
* D2: field presence, not truthiness, detects the inventory field; a non-list `tenure_reports` is also treated as managed and malformed so corruption cannot opt a case out.
* D3: reasons contain counts only, never household references, sources, owners or digests, so generic gate text cannot leak them to denied roles. The detailed view lives only under the intake-stripped key.
* D4: the server derives each linked report's digest with the existing `_digest` over the raw stored report at record time. A caller digest, approval, route or verification field fails the exact-key check.
* D5: a linked report must be the latest report for that exact supplied reference. Currentness at read time requires the report to exist, match the reference, remain latest for the reference and keep the same digest.
* D6: `households: null` records valid Unknown. Empty, more than 100 rows (transport safety bound only, never truncated), duplicate (exact or case-insensitive) or surrounding-whitespace references, bool or non-positive versions, mismatched, missing or non-latest links are rejected before any mutation.
* D7: successful record sets `tenure_review_required=True`. There is no clear or release path, and a fully linked and current inventory still returns the existing hold.

## Risks and limits

* Legacy unmanaged cases (no inventory, no reports, no flag) keep current behaviour; this is an explicitly partial opt-in primitive, not universal C1 or C2 compliance.
* Caller-declared coverage is not "all actual households"; actual roster completeness, identity, authority appointments, Legal interpretation, Finance cost, accepted package handoffs, universal pre-offer integration and any release stay pending.
* SQLite `SqlStore` and JSON are tested. MSSQL is not run and not claimed; no SQL schema or `sqlstore.py` change is planned.
* If shared store, sqlstore, server, projection or schema edits prove necessary the work stops for a bounded decision.

## Planning Readiness

Ready. Baseline passes, hooks are verified at the cited lines, and no blocker is open.
