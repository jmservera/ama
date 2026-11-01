<!-- markdownlint-disable-file -->
# Review: rubric PR record and Copilot review advisory (D1, D2)

Date: 2026-11-01. Executed once, independent code-review agent, boundary: commit b0c9190d7 against origin/main 245985722.

## Outcome

Conforms to D1 and D2 with one caveat routed to follow-up. No open blocking findings.

## Findings

| # | Severity | Finding | Routing |
| --- | --- | --- | --- |
| 1 | Medium | The refresh PR is made with `GITHUB_TOKEN`, so it gets no `rubric/score` status or other checks and merges only if the ruleset requires none (true on 2026-11-01: zero approvals, empty required checks) or allows bot bypass. | README now states the condition. Follow-up: post a `rubric/score` status on the refresh commit or enable auto-merge if the ruleset later requires checks. Owner action: confirm on first live run. |

## Checked

Lock matches source (recompile no diff); `prepare.py` and `gate.py` logic; refresh lease, head-OID and `--match-head-commit` handling; new tests pass; 17 test failures are pre-existing and reproduced on a clean tree.

## Not verified

Live refresh merge; ruleset change for D2 (owner action).
