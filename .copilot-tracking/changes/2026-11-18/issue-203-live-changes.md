# Changes: issue-203-live

Docs and evidence only; no `src/` or `tools/` edit. Tier: FOCUSED (documentation-only; basis: no executable, workflow, SQL, security or infrastructure change). Not run: `rpi-checks.py --all` (not required), mypy/ruff (no Python changed).

Files: `docs/reference/research/issue-203-live-references-evidence-2026-11-18.md` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (appended entry).

## Per-criterion result (unticked criteria)

| # | Criterion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | `mvp/` and `prototype/` only intentional historical references; `zavaforward_mvp` only in dated records | Unproven, failing | `tools/check-legacy-references.py`: 11 violations in three `tools/test_*` regression files; `test_repository_has_no_violations` fails; documents clean |
| 5 | Deployed app and CI green from `src/` | Partly proven (observed; raw output not retained) | Revision `--0000031` Healthy, `/healthz` 200 (API and resident app), `Source projects CI` green on latest 8 pull-request runs; unproven: digest built from `src/` (private registry, no deploy run) and push CI on `main` (workflow is PR-only) |

Commands run: `git grep` stale-reference search; `python3 tools/check-legacy-references.py` (exit 1); `python3 -m unittest tools.test_check_legacy_references` (7 tests, 1 failure, preserved); `check-legacy-references.py --files <changed docs>` (links: 0 violations); `gh run list`; read-only `az containerapp show/revision list`; `curl` health paths. No secrets read; no Azure resource created.
