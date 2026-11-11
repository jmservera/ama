---
title: Issue 131 inherited correction batch for the household inventory primitive (research)
ms.date: 2026-11-10
task_id: 131-inherited-repair-1110
---

## Status

Research stub created before the research-open witness event. Substantive research follows below after that event.

Scope: one inherited correction batch for the two independently confirmed introduced Medium findings and the three introduced Core typing errors plus one format failure. Authority: Root brief `brief-131-inherited-repair-1342.txt` after the dated D2 audit `handoff-131-dated-budget-audit-1336.md`. The original candidate `7f8af9b`, the D1 diagnostic `9f9f66f`, the D2 audit and all earlier reports stay immutable.

## Disposition and scope

Research executed 2026-11-10 (UTC 13:45 onward) after the research stub, state file and `research-open` witness event (seq 2, ok). Planning Readiness: Ready.

This is a prospective correction of the introduced defects of the initial household inventory primitive; it is not a new initial slice and not a repair of the earlier R1-R4 slices. In scope: Core `resident_decisions.py` inventory history validation and refusal reasons, the direct existing tests in `src/core/tests/test_resident_decisions.py`, and the three introduced mypy errors plus the one format difference in that test file. Out of scope: new endpoint, SQL schema, UI, role, shared adapter, authority model, roster, Legal interpretation, attestation, hold release, RV-001 API assertion strengthening (kept as a remaining follow-up because the Root brief limits the batch to the two Mediums and the typing and format results), and issues 1360, 132 and 233.

## Authority and budget (Root-recorded, not decided here)

* Root explicitly authorizes ONE inherited correction batch after the dated D2 audit (`handoff-131-dated-budget-audit-1336.md`). The exact balance of the historical issue 131 allowance is not provable; the proved lower bound is at least one cycle. Under the owner default of up to five total cycles per issue (2026-11-09 08:00:39Z) and the one-time addition of five to exhausted issues (2026-11-09 08:02:51Z), pre-grant debits d of 2 to 5 leave 3, 2, 1 or 5.
* This batch consumes exactly one cycle. Afterwards the conservative proved minimum is 0: no fresh five, no reset, no second automatic cycle and no self-retry.
* The dated chronology and CASE debits are in the D2 handoff and are repeated in the changes record. The initial inventory slice (7f8af9b) and the read-only diagnostics (9f9f66f, D1) are not source corrective debits. Three possible CASE debits (PR 509 fix cycle 1, and the format-only CI repairs on PRs 903 and 1034) all predate 2026-11-09 and stay uncertain.
* This resolves the prior numerical admission hold only. It grants no human, Legal or hold-release authority.

## Evidence used

* D1 handoff `handoff-131-readonly-diagnostics-1110.md` and committed D1 records (`readonly-diagnostics-131`): finding 1 confirmed only on corrupt-store injection (JSON and SQLite), finding 2 confirmed on the supported path for Verified reports with stored Ambiguous identity and by injection for an Unknown route; `TENURE_HOLD` never released; three mypy errors and one format difference introduced versus a clean `fe59ef56` baseline at pinned mypy 2.4.0 and Ruff 0.17.1.
* Independent assessment `independent-131-household-inventory-1110/functional-findings.json` (8f0786): two Medium findings with suggested fixes, RV-001 residual, no hold-release bypass.
* Current source read from the working tree at `9f9f66fc` (source equal to `7f8af9b`): `_inventory_fill`, `tenure_inventory_view`, `_inventory_rows`, `_inventory_refusal`, `_res_tenure_inventory_record`, the `resident_gate` and `_res_scope_record` consumers, `tenure_verify`, `tenure_intake` and `tenure_review_trigger`.
* Current `origin/main` fetched at `c9e15acbf4c0893358818e562d034d62321ea6d4` (13 commits ahead of base `fe59ef56`, includes the Bicep and metadata composition `0a6dc0b3f`, `83503b74e`, `c9e15acbf`). Main changes none of `resident_decisions.py`, its test file or `test_resident_api.py`. It changes `src/core/README.md` and `src/api/README.md` (different hunks from the candidate), `server.py`, and unrelated Core modules. A read-only dry run `git merge-tree --write-tree HEAD origin/main` reported a clean merge (tree `418f118c`). Main adoption by an ordinary merge, not rebase, reset or amend, is authorized inside the implementation after the marker; both intents and all earlier RPI records are preserved. No material conflict exists.
* Baseline before any change (owned venv `venv-131-household-inventory-1110`, module origin `src/core` of this worktree, owned synthetic `ZF_DATA`): Core `test_resident_decisions.py` Ran 410 OK skipped=146, exit 0; API `test_resident_api.py` Ran 21 OK skipped=1, exit 0 (`phase131-inherited-repair-evidence-1110/run/base-*.log`). So there is no product failure that blocks the correction.

## Finding 1 (Medium): corrupt persisted history can look valid

Confirmed by D1 only via corrupt-store injection; the supported action cannot write a skipped version, blank or duplicate references or a wrong case. The writer checks that history elements are dicts and `_version` compares only the last element; the view checks only the last revision's `version` and loosely types its rows. So `[{"version": 99, "households": null}]` accepts `expected_version=99` and appends version 2 (history `[99, 2]`) and then reads as Declared. The hold still holds.

Smallest correct fix: one non-mutating validator of the whole stored history used by both the writer (before appending) and the view (before projecting coverage). It requires a non-empty list of dicts, each with `version` an exact int equal to its position, `case_id` equal to this case, and `households` either null or a bounded non-empty list of rows with exactly `household_ref`, `report_version` and `report_digest`, a not blank, trimmed, at most 100 characters reference unique ignoring case, and a null link with a null digest or an exact int link with a string digest. Historical digests are not compared with current reports, so legitimate older snapshots whose reports changed remain valid. The writer refuses without mutation or audit; the view reports Malformed with the existing generic reason. Row reference rules are shared with the input check so they cannot drift.

## Finding 2 (Medium): ambiguous identity and Unknown route add no refusal reason

Confirmed by D1 on the supported path: after intake with `identity_state` Ambiguous and a Verified verification, the stored identity state is unchanged and the reasons list was empty. `identity_state` is never read or changed by any other action; `tenure_verify` records confirmation in its own record. Decision: stay fail closed. The view does not infer that a later verification supersedes the stored intake state; it adds count-only reasons for linked reports whose stored identity is Unknown, Ambiguous or not a string, and for linked reports whose decision route is not one of the existing route values (Unknown or invalid). The reasons carry counts only, never references, owners, sources or digests. The unconditional hold stays; nothing is released. A consequence is that fully linked current inventories always list the identity count until a future explicit identity action exists; that is intended and documented.

The existing refreshed-data test asserted `reasons == []` for exactly the Verified plus Ambiguous state, so its expected value is the old behaviour and must change with the fix.

## Typing and format

The three mypy errors (test lines 447 `no-any-return`, 526 `var-annotated`, 4649 `attr-defined` on `Store.db`) and the format difference at line 439 are in the new test code. Fixes use real types: a typed local dict in the `inventory` helper, a typed annotation for the `bad` collection and the file's existing `assert isinstance(other, SqlStore)` narrowing; then `ruff format` of the one test file only. The Core module is exempt from mypy and format by configuration but not from `ruff check`.

## Regression plan (red on the old code, green on the new)

* Behaviour 1: injected corrupt histories (version-99 singleton, malformed earlier dict plus a valid-looking last revision, blank and duplicate latest rows, wrong case id) are Malformed in the view, refuse the writer with no mutation or audit, keep the hold and refuse scope; a valid history whose earlier snapshot digest is stale still records a new revision. JSON base and inherited SQLite store.
* Behaviour 2: a Verified report with stored Ambiguous identity, and a report with an injected Unknown route, give count-only reasons in the view, `resident_gate` and a refused `scope_record`, with no supplied reference, owner or digest in the text.
* Existing controls (valid, held, unmanaged legacy, deletion hold, roles, races) stay and are re-run.

## Limits

* No product change beyond the Core module, no schema or shared store edit, no new dependency, no browser, SQL Server, cloud, model, provider or private data. MSSQL is not run and not claimed.
* Local evidence only: no publication, acceptance, universal C1 or C2 compliance, or hold release.

## Planning Readiness

Ready.
