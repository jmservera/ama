---
title: Issue 164 / PR 1641 gate failure correction changes
date: 2026-11-17
---

## Changes

* Added research, plan, details, critique, changes, review and state records under `.copilot-tracking/`.
* No source, tool, check or manifest edits. Browser recipe SHA and Core manifest tests: not applicable.

## Validation (FULL tier required for publication; this correction is record-only)

* Browser check `checks.design_system_browser_check`: main pass; candidate 1 failure in the first run, then 68 passes (see research).
* Core suite sequential: main 3529 tests 1085 s; candidate 4059 tests 1535 s, one identical env-caused failure on both.
* `git diff --check` and staged-path review: see review.
* Not run: `rpi-checks.py --all` (coordinator owns the gate; lock not taken). A new full receipt is still required before publication and the Core timeout (1800 s) needs an owner decision.

## Divergences

None from the plan.

## Correction 5 (2026-11-18): hosted job timeout

* `.github/workflows/src-ci.yml` job `project`: `timeout-minutes` 25 to 45. Hosted `src-api` was cancelled at the 25-minute limit twice (browser-check step, then SBOM step); the unit suite alone takes about 22 minutes and no test failed.
* Classification: no permission, action pin, image, package, secret, deployment or gate-semantics change, so the focused tier applies to this edit; the PR keeps the FULL tier. Basis: a duration limit only.
* Searched `tools/`, `src/*/tests` and docs for assertions of 25 on this workflow: none. `src-deploy.yml` 25 is a separate workflow and is unchanged.
* Ran: YAML parse, `tools.test_ci_affected`, `tools.test_src_cutover_repoint`, `tools.test_src_coverage_baseline_parity`. No Python touched, so ruff/mypy not applicable.
