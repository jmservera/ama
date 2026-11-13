# Review: 202 criteria 5 and 6 audit proof table (2026-11-13)

Outcome: one overclaim to fix, otherwise verified.

## Finding (Medium)
Row 1 states "Dip and recovery recorded in `.github/rubric/README.md`" and treats "dip recorded" as proven substance. The README records the 47 baseline, the 77 current score, the recovery route, and the #851 expectation that no dip would occur. It says the historical per-pull-request dip records are "not reconstructed here". PR #851 lists AC 3 (per-PR dip records) as unmet and not provable retroactively. The accepted dip and its per-PR record are therefore not proven. Reword to: baseline and recovery are recorded; per-PR dip records are not, and need owner acceptance.

## Verified
- #300 and #302 removed the `mvp/` globs on 2026-10-15; #302 removed the last one, `mvp/README.md`. #499 deleted `mvp/` on 2026-10-27. #851 on 2026-11-03 removed the excludes after the deletion.
- `artifacts.json` has 0 `mvp/` or `prototype/` matches.
- `latest.json` scores 79 at dad57ef4f.
- `mvp-ci.yml` and `mvp-validation.yml` are `workflow_dispatch`-only and are named Source CI and Source validation. `src-ci.yml` lists both in its path filter. `tools/rpi-checks.py` pins both and `infra/tests/test_pipeline.py` reads `mvp-validation.yml`.
- `branches/main/protection` returns 404. Ruleset `mainprotect` (24504150) is active with the rules stated. Ruleset `main` (24682333) is disabled. #714 says main had no branch protection.
