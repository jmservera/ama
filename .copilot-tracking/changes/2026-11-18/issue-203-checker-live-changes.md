# Changes: issue-203-checker-live

Tier: FOCUSED. Basis: only `tools/` Python and docs change; no `src/`, workflow, dependency, SQL, security, infrastructure or deployment impact. Not run: `rpi-checks.py --all` and the full gate (forbidden, no `src/` change); mypy (no `src/<project>` modified; `tools/` is not in src-ci mypy scope).

Files: `tools/check-legacy-references.py` (three guard files, `RECORD_PATTERN`, `is_exempt`), `tools/test_check_legacy_references.py` (one test), `docs/reference/research/issue-203-checker-live-evidence-2026-11-18.md` (new), `docs/reference/README.md` (row), `docs/reference/log.md` (appended entry).

Commands: before, checker exit 1 (47 violations), 7 tests with 1 failure; after, checker exit 0, `python3 -m unittest tools.test_check_legacy_references` 8 OK, `ruff check` pass, `ruff format --isolated --line-length 100 --check` pass. Live: `az containerapp show` (revision 0000032 Running), `/healthz` 200 on both apps, `gh run list`. No secret printed.

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Literal search only intentional history | Unproven | Checker passes only via exemptions; owner agreement needed (issue comment 2026-11-17) |
| 5 Deployed app and CI green from `src/` | Unproven (partly) | Health and PR CI observed; no build provenance for the digest, no push CI on `main` |
