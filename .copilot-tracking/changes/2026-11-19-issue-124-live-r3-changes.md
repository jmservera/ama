# Changes: issue #124 live audit, third pass

Status: complete. Tier FOCUSED. No source edit, no Azure resource created or changed (nothing to delete), `rpi-checks.py` not run.

## Files

* `docs/reference/research/issue-124-live-r3-phase0-discovery-audit-2026-11-19.md` (new)
* `docs/reference/README.md`: one index sentence; `docs/reference/log.md`: appended entry.
* `.copilot-tracking/evidence/2026-11-19/issue-124-live-r3/`: `unittest.txt`, `consumers.txt`, `azure_cli_outputs.txt`, `live_discovery_probe.py` and `.json`. Screenshot deleted (signed-in view).
* Tracking artifacts `*-issue-124-live-r3-*` and the state file.

## Validation

| Check | Result |
| --- | --- |
| unittest discovery contract, flow, register (from `src/core`) | 59 OK |
| Consumer search | Only contract, flow and README |
| Live probe | openapi 404, discovery paths 403 (default deny, same as control path) |
| Link check, `git diff --check`, secret scan | See review |
| mypy, ruff | Not applicable (no src or infra Python changed) |
| Hosted CI | Not observed; nothing pushed |

## Per-criterion table

| Criterion (issue state) | Proven for the demo | Unproven | Gap class |
| --- | --- | --- | --- |
| Discovery owner nominated and endpoint agreed (unticked) | Rule only | Named nomination and endpoint agreement | Owner/person-only |
| Lifecycle and event dictionary validated (unticked) | Schema, counts, gap gating | Operational-owner validation | Owner/person-only |
| Constraint register supporting and contradicting evidence (unticked) | Two-sided rule | Real extract evidence and validation | Owner/person-only plus approved data |
| Findings are not company findings until owners validate (ticked) | Re-confirmed | None | None |

## Deviations

* The first live probe run timed out on navigation (cold start); a retry with no timeout succeeded.
