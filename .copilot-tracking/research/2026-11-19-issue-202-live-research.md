---
title: Issue 202 live research, 2026-11-19
---

Scope: the only unticked criterion of #202 is "Old workflows (`mvp-ci`, `mvp-validation`) removed or replaced, and branch protection required checks updated".
Planning Readiness: Ready (disposition: executed; evidence below).

## Evidence (read-only `gh api`, 2026-11-19 14:26Z, no secrets)

* `git ls-files mvp prototype | wc -l` returned 0.
* Workflow states: `mvp-ci.yml` and `mvp-validation.yml` are `disabled_manually` and trigger only on `workflow_dispatch`; `src-ci.yml` is active.
* Ruleset `mainprotect` (24504150, active) has a `required_status_checks` rule with an empty `required_status_checks` list; classic branch protection returns 404. No `mvp-*` check is required.
* The workflow files still exist and are referenced by `tools/rpi-checks.py` (name list and SHA-256 pins, lines 72-81, 2517-2520), the `src-ci.yml` path filter and actionlint step, `infra/tests/test_pipeline.py`, and `tools/test_src_cutover_repoint.py`.

## Conclusion

Removing the files edits gate tooling (hash pins, job-to-check map, actionlint list), which the repository classifies as the FULL tier (complete local gate and external receipt; `rpi-checks.py --all` is barred for this run). Setting required checks to a new list changes shared GitHub protection, which the owner decision excludes (no production changes). The criterion is therefore unprovable and not buildable for the demo under this brief; it stays unticked.

## Re-verification run r2 (15:30Z)

The unticked criterion is unchanged on a fresh worktree: `.github/workflows/mvp-ci.yml` and `mvp-validation.yml` still exist, `gh api repos/jmservera/ama/branches/main/protection` returns 404 (no classic protection), and the prior conclusion holds. No criterion is provable or buildable for the demo.
