---
title: "Changes: issue 1362 inherited one correction"
description: Changes, the inherited-authority debit and evidence for the exact Current design version field assertion
author: Copilot
ms.date: 2026-11-10
ms.topic: reference
---

Registered prospectively before implement-start (source clean at `0a6dc0b3f0b3ecf098536369a8308b02226b98b8`) and completed with real results below. Evidence root (external): `ROOT/phase1362-inherited-one-evidence-1110/` (`baseline/`, `candidate/`, `candidate/amended/`, `diagnostic/`, witness `issue-1362/events.jsonl`).

## Authority and debit

* ONE inherited #233 to #1362 correction, authorised by Root on 2026-11-10 after the dated minimum-balance proof (research record). Not a fresh C1, not a fresh five, no reset, no borrowing of the #135/#1360 zero. Earlier UNKNOWN reports are preserved unchanged.
* DEBIT: this task produced worker output, so exactly ONE inherited cycle is consumed. Conservative proven remaining minimum afterwards: ZERO. Exact balance remains UNKNOWN. No further automatic correction or self-retry is authorised.

## Source changes (two files)

* `src/api/checks/atlas_tensions_browser_check.py`: new `DESIGN_VERSION_FIELDS` (in-page function) and `check_design_version`. `check_technical` now requires exactly one Design version panel, scrolls it into view, and calls the helper: exactly one `dt` whose trimmed text is `Current design version`, a directly following `dd`, visible, non-blank, and exactly `str(technical["design_version"])`. The design version was removed from the whole-panel substring loop. `design_name`, the latest note, every other check, the fixtures and the product are unchanged.
* `src/api/tests/test_atlas_tensions_checker.py`: `_Section` double and `DesignVersionFieldTests` (exact pass; `2`, `Unknown`, `10`, `v1`, `1 (draft)`, empty, whitespace, null, missing label, duplicate label with a correct first value, invisible field all raise `AssertionError`). 17 tests (11 before).
* Resulting blobs: checker `dad25ca526a24b7718aeb9c45b477c16b5199081`, test `b53e39d9dde911207d4b91b21546f10c5d53711b` (base `e3aa4790...`, `9774b84a...`).

## Environment

Own venv `/tmp/ama-1362-env` (`--system-site-packages`) with the declared dev pins installed because the system site had Playwright 1.64.1, Ruff 0.17.3 and mypy 2.4.1: Playwright 1.64.0 (import origin `/tmp/ama-1362-env/lib/python3.12/site-packages/playwright`), Ruff 0.17.1, mypy 2.4.0. Chromium 156.0.8078.4 (cached) launches under 1.64.0. Imports resolve to this worktree (`baseline/env.log`). The D1 Playwright 1.64.1 mismatch and harness-leak records stay adverse history for D1. UTC, Python 3.12.3. No shared install, no repository venv, no bytecode.

## Baseline (unchanged current main, before the edit)

* Checker and test blobs equal the D1 diagnosed blobs; not already fixed.
* `tests.test_atlas_tensions_checker`: 11 OK. Full Atlas browser check: exit 0, COMPLETE, 362 PASS, one SKIP (screenshots, by design).
* D1 mutation diagnostic (real `check_technical`, only the associated dd mutated): control fixture: `2`, Unknown, empty, missing label FAILED at the version assertion; `10` and duplicate label WRONGLY PASSED. Mask fixture (recorded-at `21 Oct 2026`): all six mutated cases WRONGLY PASSED. Positive control PASSED. This confirms the false positives on current main.

## Candidate

* RED: the new test module against the unchanged checker fails on import of `check_design_version` (`candidate/red-unit.log`, exit 1). GREEN: 17 tests OK.
* Attempt 1 of the full browser check FAILED at technical-queue 320px: `'Current design version' value is not blank` (`candidate/browser-attempt1-FAILED-320px.log`, preserved). Cause, shown by an external read-only probe (`candidate/probe-320.log`): `dd.innerText` was empty at 320px while `textContent` was `1`, because the panel uses `content-visibility: auto` and the in-page read occurred before rendering. This was a defect of the candidate itself, fixed inside this same single inherited correction by reading `textContent` (one-line change; no second correction, no scope change). The diagnostic control and mask runs on attempt 1 already showed every negative rejected (`candidate/diag-*.log`).
* Declared deviation from the predeclared run budget: one extra candidate browser run (the amended candidate) and one extra read-only probe run. Nothing is retried until green; a failure of the amended run would have stopped the task.
* Amended candidate (`candidate/amended/`): full Atlas browser check exit 0, COMPLETE at 1280px and 320px, 370 PASS, one SKIP (screenshots); unit 17 OK; `tests.test_role_screens_conformance` 11 OK; `tests.test_atlas_screen_trace` OK and trace complete; Ruff lint, Ruff format check (line length 100) and `mypy --strict` on both files exit 0.
* Amended D1 diagnostic, control and mask: positive control PASSED; every mutation FAILED at the intended assertion: `2`, `Unknown`, `10` with `value is exactly '1', not ...`; empty with `value is not blank`; missing label and duplicate label (`1` then `2`) with `exactly one ... field: 0` and `: 2`.

## Limits

* Engineering check on one synthetic home. The in-page script is proven by the browser mutation controls, not by the unit doubles. Axe, assistive technology, WCAG, usability, production, live and whole #233, #149 or #1362 acceptance are not claimed. Heavy runs held `flock -n /tmp/ama-rpi-heavy.lock` (never busy). No push, PR, GitHub, merge, board or nested agent. Old read-only worktree and records untouched. Local assertions are not host or model attestation.
* Cleanup: no process or listener from these runs remains, lock free, own `.ruff_cache` removed, no bytecode in the worktree.
