# Changes: #142 (2026-11-01)
* infra/secret-inventory.json: resident demo secrets added; owner named (pending confirmation).
* infra/scripts/secret_lifecycle.py: `rotation_timeline`, `rotation-simulate`, `review_status`, `review-status`.
* infra/tests/test_secret_lifecycle.py: inventory coverage, no-downtime model (safe and failing orders), review status.
* infra/README.md, docs/reference/log.md.
Validation: test_secret_lifecycle 18 OK. Full infra/tests has 10 pre-existing environment errors, identical before and after (stash comparison). ruff --select F clean; ruff default/format and EXE001 findings pre-exist in this infra file (not in a src project; not reformatted to keep diff scoped). mypy on the script: no issues.
Divergence: ruff format --check not applied to infra script because the file was never ruff-formatted.
Review round 2: `review_status` strips whitespace-only reviewer names (regression test added); resident secret `rotation` entries now point to the README "Credential and SQL access rotation plan" because `resident_demo_secrets.py` is creation-only.
