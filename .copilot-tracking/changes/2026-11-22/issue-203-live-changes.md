# Changes: issue-203-live (2026-11-22)

Docs and evidence only; no `src/` or `tools/` edit. Tier: FOCUSED (documentation-only). Not run: `rpi-checks.py --all`; mypy and ruff (no Python changed). No Azure change, no secret read, no throwaway resource.

Files: `docs/reference/research/issue-203-live-20261122-2026-11-22.md` and `issue-203-live-20261122-evidence/` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (appended entry).

## Per-criterion result (unticked criteria)

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | `mvp/` and `prototype/` only intentional historical references; `zavaforward_mvp` only in dated records | Proven at `6a03928cc` (= `origin/main`): checker 0 violations, exit 0; 8 tests pass | `legacy-check.txt`, `legacy-tests.txt`, `heads.txt` |
| 5 | Deployed app and CI green from `src/` | Partly proven. Proven: both apps Succeeded, one active Healthy revision, `/healthz` 200, src-ci green on a post-cut-over main dispatch run. Unproven: images built from `src/` (`commit=unknown`, no `src-deploy.yml` run, registry private); green push run on `main` (none exists, workflow is PR and dispatch only) | `az-apps.json`, `healthz.txt`, `gh-src-ci-main.json`, `gh-src-deploy.json`, `build-commit-line.txt` |

Remaining gap: criterion 5 needs a `src-deploy.yml` run or rebuild with `ZF_BUILD_COMMIT` and redeploy; out of demo scope.
