---
title: Issue 131 read-only diagnostics changes
ms.date: 2026-11-10
task_id: 131-readonly-diagnostics-1110
---

## Status

Prospective stub created after the plan, details and critique and the `plan-done` witness, before `implement-start`. Diagnostic results, divergences and validation are appended during implementation. No product, test, README or configuration change is planned or permitted; the only committed change is this set of new dated RPI records.

## Implementation outcome (diagnostic, no repair)

Raw artifacts are under the external evidence `run/` folder: `probe131.py`, `probe131-observations.json`, `probe131.stdout.log`, `probe131.stderr.log`, `probe131.exit`, and `base-` and `cand-` mypy and format logs with exits. Tools: mypy 2.4.0 and Ruff 0.17.1 (Root pins), candidate module origin asserted under the worktree `src/core`. Product source stayed equal to `7f8af9b` (`git diff 7f8af9b -- src` empty, HEAD and tree unchanged).

### Functional probes (JSON `Store` and SQLite `SqlStore`, owned temp stores, synthetic data only; exit 0 for the probe run)

| Finding | Path | Observation | Status |
| --- | --- | --- | --- |
| 1 malformed history looks valid | corrupt-store injection only (supported action cannot write these) | A1 singleton `[{version: 99, households: null}]`: view Malformed before, the writer accepted `expected_version=99` and appended version 2 (history `[99, 2]`), view then Declared. A2 malformed earlier dict plus valid-looking last revision: Declared. A3 blank and case-duplicate latest refs: Declared (3 of 3 unlinked). Same on JSON and SQLite | Confirmed by execution |
| 2 ambiguous identity omitted | supported API path | B1 both reports verified via legal position then `tenure_verify`, stored `identity_state` still `Ambiguous`, both links current: reasons `[]`. Same on JSON and SQLite | Confirmed by execution |
| 2 Unknown route omitted | corrupt-store injection of `decision_route`, inventory re-recorded after injection | B2 reasons `[]`. The supported verify action sets the route, so this is an injection case, not a supported-path defect | Confirmed for injected data only |

Controls preserved: a valid supported inventory is Declared with count-only reasons and scope refuses; a report change makes links stale; a re-recorded valid revision is accepted; an open trigger yields a reason; the hold was present in every observation and every scope attempt was refused, so no hold release or bypass was observed.

### Typing and format baseline (pinned mypy 2.4.0 and Ruff 0.17.1, configured, no selectors, own caches)

| Run | mypy | `ruff format --check .` |
| --- | --- | --- |
| Base `fe59ef5` owned export | exit 0, 288 files, no issues | exit 0, 235 files formatted |
| Candidate `7f8af9b` | exit 1, three errors in `tests/test_resident_decisions.py` (lines 447 `no-any-return`, 526 `var-annotated`, 4649 `attr-defined` on `Store.db`), matching Root's log | exit 1, one file would reformat (`tests/test_resident_decisions.py`), 234 formatted |

All three typing errors and the one format difference are introduced by the candidate's new test lines; the base is clean at the pinned versions. The earlier authored claim that the base was not format clean is retired as an invalid out-of-config check.

### Divergences and disclosures

* The plan, details, critique and research body were written with shell heredocs and the state file by a create-then-`mv`; this deviates from the create/edit-tool rule, and content was reviewed afterwards.
* The probe script was revised once before its only run (B2 re-records the inventory after injection so the digest is current); the probe ran once with no retry.
* Owned scratch (base export, mypy caches, synthetic data directory) was removed; raw logs and observations are retained. Tool runs left ignored cache directories in the worktree (`__pycache__`, `.ruff_cache`); they are untracked and ignored.
* MSSQL, browser, cloud, model and private data were not used or claimed.
