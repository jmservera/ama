# Changes, issue 79 live (2026-11-19)

Source changes: none. Tier: FOCUSED (record-only). `rpi-checks.py --all` not run.
Validation: `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_ranking_publication tests.test_ranking_publication_runner tests.test_ranking_archive_blob -q` -> 136 tests OK. mypy/ruff not applicable (no Python edits).

| Criterion | Status | Basis |
| --- | --- | --- |
| Same data and policy version give the same order (ticked) | Proven (2026-11-18 live, retained) | docs/reference/research/issue-79-live-ranking-2026-11-18.md |
| Policy changes versioned and hash-verified (ticked) | Proven (same note) | same |
| Named policy owner signs first rule order | Unproven; cannot be proven for the demo | Policy owner "to be named", draft; signature is a human act by an unnamed person |
| Snapshot publication scheduled and retained | Unproven; code and cron definition exist, deployment and WORM retention not shown | Needs infra/deployment (FULL tier) and Legal-set retention; ACR 403 blocked image build on 2026-11-18 |
