# Issue 360 live changes, run b

Refs #360. Tier FOCUSED; documentation-only artifacts. No `src/`, infra, workflow or dependency file changed; mypy, ruff and unit tests are not applicable; `rpi-checks.py --all` not run. No Azure action, no secret read.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| a | Proven | Ticked; live evidence in docs/reference/research/issue-360-live-20261119-2026-11-19.md |
| b | Proven (offline) | Ticked; unit tests |
| c | Unproven | Owner approval; an agent cannot supply it (#2121) |
| d | Partly proven | Earlier live run proves health, welcome, sign-in, role claim; browser-mode 401, AI call, second role and restart persistence unproven; the 401 fix is a FULL-tier infra change (#2121) |
| e | Unproven | Needs explicit owner authorisation after d (#2121) |
| f | Proven | Ticked; documentation |

Stop: every remaining criterion is human-gated or production-tier.
