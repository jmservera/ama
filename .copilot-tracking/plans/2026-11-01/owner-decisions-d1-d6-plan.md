# Plan: record owner decisions D1 to D7

* [x] Mark each decision with date and outcome in the bottleneck analysis; record #466 and #163 deferrals as deferrals, not met criteria.
* [x] D4: amend local gate paragraph in .github/copilot-instructions.md (focused default; complete gate for big features, releases, infrastructure, deployment, SQL, security-sensitive; review, hosted CI, human approvals kept).
* [x] D5: amend coordinator agent correction-cycle step.
* [x] Append log entry.
* Critique: executed once, compatible. Risk: D4 wording must not weaken human approval; it keeps them. D3 needs no coordinator edit.
* Validation: focused gate `rpi-checks.py --changed`, git diff review.
