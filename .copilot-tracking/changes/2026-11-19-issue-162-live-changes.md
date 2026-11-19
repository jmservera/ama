# Changes: issue 162 (2026-11-19)

Tier: FOCUSED (documentation only; no src, SQL, infra or deployment change). Refs #162.

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1 Queries keyed by authenticated user | Proven (ticked) | 2026-11-18 live and local notes |
| 2 Role matrix covers all chat and memory endpoints | Proven locally (ticked) | 35 tests OK, 2026-11-19 |
| 3 Retrieved context projected | Proven (ticked) | tests |
| 4 No cross-user prompt sharing | Proven (ticked) | tests |
| 5 Prompt injection test set | Proven (ticked) | tests |
| 6 Admin and break-glass audited with purpose, policy decided | Unproven for the demo | Refusals audited live and grants tested locally; live grant needs an unauthorised app config change; admin Entra role, user notification and retention are undecided owner policy |

Validation: `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests.test_chat_isolation` gave 35 tests OK. mypy, ruff and rpi-checks not applicable (no source change).

Files: docs/reference/research/issue-162-live-criterion6-stop-2026-11-19.md, docs/reference/README.md, docs/reference/log.md.
