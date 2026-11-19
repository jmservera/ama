# Issue 123 live research (2026-11-19)

Task: issue-123-live. Disposition: executed. Scope: synthetic demo, desktop only, focused tier.

## Criteria under #123

* #123 has two unticked boxes: the #440 stabilization checkpoint, and "all child features closed or deferred".
* #440 criteria 7 (triage confirmed findings into independently scoped issues) and 8 (RPI artifacts, HVE Builder review) are unticked.
* Prior note `docs/reference/research/stabilization-checkpoint-triage-440-live-2026-11-18.md` drafted D1 to D4 findings, none filed or fixed.

## Re-verification on main 05e94d303

| Draft | Re-check | Status |
| --- | --- | --- |
| D1 time status 500 | SQL/Azure SQL scope | FULL tier, out of scope here |
| D2 legacy guard allowlist | `python3 tools/check-legacy-references.py` exits 0 | already fixed on main |
| D3 ChatIsolation.turn unreachable | `def turn` still at chat_isolation.py:173 | open, needs design choice |
| D4 AI golden path | `ai_eval.GOLDEN` resolves under `parents[3]/evals`; a missing file raises a raw FileNotFoundError | open, small, testable |

## Selected slice

D4, named-configuration-error branch: `ai_eval.run_eval` must fail with one clear error naming `ZF_AI_GOLDEN` when the golden file is absent, instead of a bare path error. Planning Readiness: Ready.
