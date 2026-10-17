<!-- markdownlint-disable-file -->
# RPI Phase Details: iteration-scenario-manifest-103

Task #103, 2026-10-17. Plan:
.copilot-tracking/plans/2026-10-17/iteration-scenario-manifest-103-plan.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02, P01-T03 |

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
review binding and SN-11. Prefer approved inventories already present; exact
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
