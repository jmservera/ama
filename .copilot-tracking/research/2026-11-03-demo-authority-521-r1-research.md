# Research: resident demo authority extension (Refs #521)

Date: 2026-11-03. Disposition: executed. Planning Readiness: Ready.

## Merged evidence (do not redo)

| PR | Delivered |
| --- | --- |
| #590 | Shared policy file, core, SQL, helpers, January tests |
| #690 | Browser-check fixture moved to the shared authority end; coordinator steps |
| #742 | Live SQL window renewal to 2027-02-01 recorded as evidence |

## Owner decision

2026-11-03: authority extended to 31 Dec 2027, replacing the end of January 2027. Exclusive instant 2028-01-01T00:00:00Z. Supersedes the 2026-10-28 and 2026-10-30 decisions.

## Findings

* One source of truth: `src/core/src/zava_forward/core/resident-demo.json`. `AUTHORITY_END`, the SQL renderer, secret helper, deploy helper and browser checks all derive from it.
* Hard-coded copies remain only in tests (core, infra, api check test) and prose (infra README, API README, knowledge-base index, one check docstring).
* The AI tariff expiry (2026-11-01, `ai_consumption_demo.py`, `assistant.py`) is a separate approval and is out of scope.
* SQL migration is generic (drop and re-add the check), so no new SQL is needed.

## Acceptance criteria status before this slice

* 1 (consistency and tests): source done by #590/#690; the date must move again.
* 2 and 3 (cost, rotation docs): already ticked; need updated estimate for the longer window.
* 4 (live apply): unmet; needs explicit owner confirmation of the exact change.
