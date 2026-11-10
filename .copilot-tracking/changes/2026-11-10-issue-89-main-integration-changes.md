---
title: Issue 89 main adoption changes
ms.date: 2026-11-10
---

## Source integration performed (local only)

* Fast-forward only: local `a8593a7a8670aab27329a81fedee605b4913e7e9` to published `a05b7e6b29145e620ca70f69c6f3f5c00be493c2` (no new commit).
* Ordinary merge commit `8fe3416d50a5ae2e75603e75a40c93b8af5a51cf`, tree `08fb66ce707518ddedb33dd53ed8362171869284` (equal to the `git merge-tree` prediction), parents `a05b7e6b2...` and `a6002219581b983132465e9dd1680f78e6aca542`. Zero conflicts, no hand resolution. Author and committer `8036360+jmservera@users.noreply.github.com`; Copilot trailer; `Refs #89`.
* No rebase, force, reset, amend, hook bypass, push, PR or GitHub write. No source file was edited by hand.

## Preservation evidence

* Merge result versus main differs only in the eight Stage A paths (aftercare.js, test_aftercare_screen.py, test_accessibility_baseline.py, aftercare_intake.py, test_aftercare_intake.py, core README, WCAG baseline, log). Merge result versus a05 differs in exactly the 59 non-tracking paths of main's own delta from the merge base `a8593a7a8` (set identical).
* Stage A files equal a05 byte for byte; `src/core/README.md` is the only Stage A file that differs from a05, because main's #1238 paragraph was auto-merged in; both paragraphs are present.
* `docs/reference/log.md`: every line of main's log and every entry of a05's log is present in order; the only a05 line not carried is the frontmatter `ms.date: 2026-11-09`, replaced by main's `2026-11-10`. 11373 lines merged (a05 11301, main 11359).
* No tracking file of either parent was deleted. Original RPI artifacts and witness records are unchanged bytes.
* Main a600 differs from e951 only in `.github/rubric/scores/latest.json`; src and infra tree equality was proved by Root and is consumed.

## Checks (owned venv `/tmp/i89-1110`, Python 3.12.3, ruff 0.17.1, mypy 2.4.0, aiohttp 3.14.5, playwright 1.64.0; editable installs of this worktree; raw logs and SHA256SUMS in the external `checks-89-main-integration-1110`)

* Core `test_aftercare_intake` 39 OK; `test_aftercare` 21 OK; `test_resident_decisions` 371 OK (132 skipped, opt-in SQL); `test_resident_showcase` 41 OK; `test_resident_showcase_verifier` 9 OK. A first invocation via module names failed on import path only (`c2-invocation-error-core-resident.log`, retained) and was re-run with the repository's discover form.
* API (with the repository's documented test-helper `PYTHONPATH=../core/tests:../agents/tests`): `test_aftercare_screen` 13, `test_accessibility_baseline` 12, `test_static_assets` 5, `test_auth` 41, `test_role_endpoint_inventory` 24, `test_role_screens_conformance` 11, `test_simulator_admin` 30, `test_live_control` 34: all OK.
* Core and API `ruff check`, `ruff format --check` and configured `mypy`: all exit 0 (Core 290 files, API 216 files).
* Browser: the recorded e951 results (217 local and 58 browser checks) are consumed by matching tree inputs; nothing was re-run. The base Stage A screen is unwired, so no maintained aftercare browser check exists: unavailable baseline, not a pass.
* Not run: full gate, `--changed`, SQL/MSSQL, four-image, model, cloud, private `ZF_DATA`, assistive technology. No heavy shared lock was needed.

## Limits

* Local synthetic engineering evidence only; no #133, #132, #134 or whole #89 acceptance, no human, legal, resident, evaluator, model or live approval, no hosted CI.
