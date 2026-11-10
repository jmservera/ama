---
title: Issue 131 read-only diagnostics of independent REVISE findings (research)
ms.date: 2026-11-10
task_id: 131-readonly-diagnostics-1110
---

## Status

Research stub created before research-open. Substantive research follows below after the witness event.

Scope: diagnostic only. No product or test fix, no Source Correction grant. The original candidate `7f8af9b329186cdb0f72de73a00fbcc5fe72798f`, its guarded critique, Review, state, witness and failed logs are immutable. The historical issue 131 corrective balance stays UNKNOWN.

## Disposition and scope

Research executed 2026-11-10 (UTC 08:03 onward) after the research stub, state file and `research-open` witness event. Planning Readiness: Ready.

This task is a read-only diagnostic of the independent assessment `8f0786` (disposition REVISE, 12 files, verdict approve_with_comments, two Medium findings, no hold-release bypass found; not a blanket acceptance and not a Source Correction grant). It reproduces each claim with the smallest owned synthetic fixture and compares typing and format results with the base. It makes no product or test change. The old issue 131 corrective balance stays UNKNOWN; this task is not a corrective count and makes no fresh-five or exhaustion claim. Retained 131 history was not read for authority or cycle debits (optional step not needed for a diagnostic that grants nothing).

## Evidence used

* Independent assessment files: `independent-131-household-inventory-1110/functional-findings.json` and `metadata.json` (Root external copies; status complete, REVISE).
* Original candidate source at `7f8af9b329186cdb0f72de73a00fbcc5fe72798f`, read from the working tree (clean, same HEAD): `resident_decisions.py` helpers `_inventory_fill`, `tenure_inventory_view`, `_inventory_rows`, `_inventory_refusal`, action `_res_tenure_inventory_record`, consumers `resident_gate` and `_res_scope_record`.
* Root configured-tool logs: `131-root-configured-mypy-1110.log` (exit 1, 288 files, three errors in `tests/test_resident_decisions.py`: lines 447 `no-any-return`, 526 `var-annotated`, 4649 `attr-defined` on `Store.db`), `131-root-configured-format-1110.log` (exit 1, one file would reformat, 234 formatted), `131-root-api-pinned-typing-1110.log` (exit 0).
* Owned venv `venv-131-household-inventory-1110` now reports mypy 2.4.0, Ruff 0.17.1, Playwright 1.64.0 (Root pins restored); the earlier native 2.4.1 runs and raw checks remain retained and are not rewritten. Editable installs point at the candidate worktree.

## Finding 1 (Medium): malformed inventory history can look valid

Static reading. `_res_tenure_inventory_record` only checks that history elements are dicts, then `_version` compares `expected_version` with the last element. `_inventory_fill` only checks that the last element's `version` equals `len(inventories)` and that each row of the last revision has an `str` ref and a typed link. Earlier revisions are never validated, and the latest rows are not re-checked for blank or duplicate refs.

Consequence if reproduced: a corrupt history such as `[{"version": 99, "households": null}]` accepts `expected_version=99` and appends version 2; the view reports Declared. The unconditional `TENURE_HOLD` still blocks scope and work. The path needs corrupt stored data: the supported action cannot write blank or duplicate refs or a skipped version.

Probe design (smallest): record a valid inventory through the supported action, then inject three corrupt histories into an owned temp store (version-99 singleton, malformed earlier dict plus valid-looking last revision, blank and duplicate latest refs); observe writer outcome, view status, gate and scope. Controls through the supported path: valid history, report change making the link stale, a re-recorded valid revision.

## Finding 2 (Medium): ambiguous identity and Unknown route omitted from refusal reasons

Static reading. `_inventory_fill` copies `identity_state` and `decision_route` into each entry but counts refusal reasons only for missing links, stale bindings, a verification text that does not start with `Verified`, and open triggers. `tenure_verify` records verification and route without changing the stored intake `identity_state`, so a Verified report can still carry `Ambiguous` (the new refreshed-data test builds exactly that state and asserts no reasons).

Probe design: through the supported action path only, verify both reports (legal position, then verify), link both, read the view, gate and scope. Then, labelled corrupt-store injection, set one linked report's `decision_route` to `Unknown` (the supported verify sets the route) and read again. Control: an open trigger still yields a reason.

## Typing and format

* The configured mypy applies to `tests/test_resident_decisions.py` (not on the ignore list), while `resident_decisions.py` is `ignore_errors = true`. Format is configured to exempt `resident_decisions.py` but not this test file.
* My earlier claim that the base is not format clean was made by running Ruff on base files extracted outside the configuration. It is unproved at the pinned version and is not repeated.
* One bounded baseline comparison: export `fe59ef56a0084dd975fd7e5c342670bb8f788fb0` `src/core` to an owned external directory (no candidate checkout, no config edits) and run the configured no-selector mypy and `ruff format --check .` with the pinned tools there. Compare counts only with evidence.

## Limits and non-goals

* No product, test, config, README or rubric edit. No new dependency (install only on a new missing-dependency failure). No browser, SQL Server, cloud, model, provider, deployment or private data.
* Probes use the actual candidate module (origin asserted) on the JSON `Store` and the SQLite `SqlStore` subclass only. MSSQL is not run and not claimed.
* A claim not reproduced is reported as unreproduced, and static reading is never reported as confirmed.
* The result is local evidence only: no acceptance, no C1/C2 universal compliance, no hold release, no publication.

## Planning Readiness

Ready: bounded probes, one baseline comparison, fixed artifact set and a diagnostic-only implementation phase are defined.
