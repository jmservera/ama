<!-- markdownlint-disable-file -->
# RPI Phase Details: iteration-scenario-manifest-103

Task #103, 2026-10-17. Plan:
.copilot-tracking/plans/2026-10-17/iteration-scenario-manifest-103-plan.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02, P01-T03 |
| P02 | Implementation complete; independent verification pending | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Enforce and publish current manifest

Context: scenario v0.1.0 labels all entries deferred without approval;
test_needs_inventory currently requires that state. Shared IA remains partial.
Include only offline manifest engineering; exclude all application deployment,
private datasets, UI and new fixture generation. No dependencies.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Contract tests first

Add focused valid-manifest and destructive-copy mutations for missing,
duplicate, unknown profile/workflow, invalid status, unsupported represented/
deferred, unsafe paths, stale hashes/version, missing evidence/defaults,
false synthetic declaration. Demonstrate failure before adding helper behavior.
Existing reciprocal inventory tests must continue to pass after deliberate
obsolete blanket-deferred assertions are replaced with validator invocation.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Shared validator and versioned existing metadata

Targets: core synthetic helper, current scenario-manifest.json, inventory
review binding and SN-11. Prefer the existing PRD-proposed inventory; exact
IDs cross-checked against PRD and chat PERSPECTIVES, not invented roles.
Manifest records source file hashes/version, existing fixture recipe,
expected IDs/count/order/selection and paths. No new actual residents/homes.
Statuses describe full journeys, subordinate IA checks are not promotions.
Keep application and operational acceptance unknown/not run.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Verify and publish synthesis

Use smallest core tests plus Ruff/mypy on changed Python. Reuse component
dev dependencies only after missing tooling failure; own editable packages.
Review all changed Markdown links and git diff. Update existing synthetic
README, core guide, reference index and append log; memory untouched.
Record exact counts, commands, failures, divergences in changes artifact.
One post-implementation Review; findings route later, no review loop.

## Completion Evidence

All three tasks complete. Test-first status assertion failed on original
unsupported deferrals; new helper import failed before implementation.
Malformed metadata mutations exposed 11 non-actionable exception cases before
guards. Final combined 29 focused tests pass (manifest, inventory, routing,
two public provenance checks). Scoped Ruff/format/mypy and 12 added relative
links/anchors pass. No browser/runtime changes or results; no generated data.
Actual commands and intermediate failures are in the changes record.

<!-- rpi:phase id=P02 -->
## P02: Correction ONE authority attribution

<!-- rpi:task id=P02-T01 -->
### P02-T01: Retain provisional/proposed authority

Caller-relayed independent Revise on 7c3c6a7 identifies false approval
attribution. Correct only owned current claims; preserve original review and
critique verdicts as history with explicit correction notices. Add a structured
inventory-authority contract that keeps coverage status separate from
provisional roles/proposed constructed journeys and absent customer/owner
approval. Reject promotion or loss of these authority fields with meaningful
mutation tests. Do not invent approval or actual deferrals; all twenty full
journeys stay unavailable. Focused scenario/inventory tests plus changed-Python
lint/format/types, links and diff. Independent final-head review remains pending.

Completion evidence: five authority promotions failed the new test before
the guard; all reject after it, plus absent authority metadata. Nineteen
scenario/inventory tests pass; scoped Ruff/format/mypy and four changed
production links/anchors pass. Manifest v0.2.1 retains exact identities and
twenty unavailable statuses, with proposal/approval state represented separately.
Historical verdicts retained with correction notices; last supplied independent
verdict remains Revise pending final-head verification.
