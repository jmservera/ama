# Details: FULL handoff

Plan: [plan](../plans/2026-11-07-assistant-release-integrity-107-full-handoff-plan.md).

## FULL own-runner scope (from the repository guide, to be re-read at run time)

* Command shape: `python3 tools/rpi-checks.py --all --base <admitted-main-sha> --out <new-external-directory>`; the receipt stays outside the repository; verify with `--verify-receipt <receipt.json> --base <current-origin-main-sha>` immediately before push and exact-head review. Fetch main first.
* The commands come from the repository's current tool and guide, never imported from a prior receipt. Use the tool's non-queued lock options only as the coordinator permits; do not wait on the heavy lock unadmitted.
* Resources expected: heavy lock, Python package environments from pip, Chromium, local disposable SQL service, scanners and images, several tens of minutes and ample disk. A clean ignored-inclusive tree, committed implementation and dated RPI evidence are required before the run.
* Invalidators: any later commit, rebase, source/base/tool/image change, or dirty, untracked or ignored input.
* Missing SQL/browser/scanner prerequisites block publication; no cloud fallback, skip token or fabricated status.

## Then

Independent actual-head assessment, normal hosted CI and human approvals. Eventual PR uses Refs #107 and #104, no closing keyword.

## Prospective amendment 2026-11-07

* Scratch and caches: external `/mnt/ama-gates/g107-755-preparation-1107` (venv, `XDG_CACHE_HOME`, ruff and mypy caches); existing retained receipt environments untouched.
* The user-level editable installs of zava-forward-core, agents and api point at the canonical main checkout, so imports from them would not test this worktree. The preparation therefore installs own-worktree editable packages with pip into the scratch venv and records import origins.
* No SQL Server, browser, scanner, image, provider or Azure service is started; SQL skips are reported, not counted as FULL.
