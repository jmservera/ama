# Changes: issue 202 criteria 5 and 6 audit (2026-11-13)

Scope: read-only audit; no workflow, protection, registry or issue edits. Base `origin/main` 31c31b2e1. Tier: Focused (tracking documentation only).

## Proof table

| Criterion (issue 202 step 2) | Evidence | Verdict | Residual owner action |
| --- | --- | --- | --- |
| Rubric registry PR dropping `mvp/` globs merged first; dip accepted, recorded, recovery expectation | Include globs removed in #300 (e01929344) and #302 (a381532dd, last glob `mvp/README.md`), both 2026-10-15, before `mvp/` deletion in #499 (4a02baf6f, 2026-10-27). Dead excludes `mvp/data/**` and `mvp/web/vendor/**` removed in #851 (a81329ef9, 2026-11-03), AFTER deletion. `artifacts.json` now has no `mvp/` or `prototype/` string. README records the 47 baseline, 77 historical, recovery by re-evidencing from `src/**/*` and current `latest.json` 79 (dad57ef4f, 2026-11-13); per-PR dip records are explicitly not reconstructed (#851 lists them unmet), so dip acceptance and a recovery expectation are not proven. Registry changes were in #300/#302 (code moves, README split) and #851, not one dedicated registry-only PR before deletion. | Partly satisfied. Substance (no mvp globs; sequencing of includes; baseline and recovery) is proven; dip acceptance is not; the literal "dedicated registry PR merged first" is not, and the excludes followed deletion. | Owner decides whether #300/#302 plus #851 meet the criterion and records explicit acceptance of the dip; no code action needed. |
| Old workflows (`mvp-ci`, `mvp-validation`) removed or replaced | `.github/workflows/mvp-ci.yml` (name `Source CI`) and `mvp-validation.yml` (`Source validation`) still exist, `workflow_dispatch` only (renamed in #714, consolidated in #414). `src-ci.yml` runs on pull requests and lists both files in its path filter. `tools/rpi-checks.py` pins both by SHA-256 and `infra/tests/test_pipeline.py` reads `mvp-validation.yml`. | Not removed; arguably replaced by `src-ci.yml`. Not satisfied literally. | Owner chooses: accept dispatch-only retention as "replaced", or authorise a full-tier PR removing both files, pins, path filters and tests. |
| Branch protection required checks updated | Read-only GET: `branches/main/protection` returns 404 (not protected). Active ruleset `mainprotect` (24504150, updated 2026-11-03, default branch): rules deletion, non_fast_forward, pull_request (0 approvals), required_status_checks with `required_status_checks: []`. Ruleset `main` (24682333) disabled. #714 states main had no branch protection so no required check was dropped. No historical update event found. | Current state: no required check names a legacy workflow, so none is stale. Historical "updated" is unproven and vacuous. | Owner records acceptance that an empty required list satisfies "updated", or adds required checks (a protection change, owner only). |

## Conclusion

Neither criterion can be newly ticked on evidence alone. Both reduce to owner decisions above; the only code-bearing option (deleting the legacy workflows) is a gate-tool change requiring the full validation tier and was not attempted.

## Validation

* Commands: `gh issue view 202 --comments`, `gh api repos/jmservera/ama/branches/main/protection`, `gh api repos/jmservera/ama/rulesets` and `rulesets/{id}` (GET only), `git log`/`git show` on `artifacts.json`, `git ls-tree v0.21.0`.
* `git diff --check` on the commit; no executable change, so no tests.
