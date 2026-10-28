---
title: Resident document RV-001 implementation continuation
description: Bounded follow-up to the preserved original independent Review
ms.date: 2026-10-28
---

## Scope and authority

Task: 520-documents-rv001, parent 520-documents-correction.
This distinct rpi-implement continuation implements the original Review's RV-001
under the owner's request to deliver a complete working correction. Original
Research/Plan/critique/Review remain preserved, including Complete / Not accepted.
No second original Review or critique will be run. RV-002 human/AT/real-model
acceptance remains a distinct unperformed follow-up.

The approved plan's positive-field requirement and PC-001 strictness remain
authoritative. Exact scope: reconstruct request and issue JSON field by field
in the SQL view instead of copying raw nested objects; retain original type and
length validation before extraction, null/empty distinction and full content.
Add one actual-SQL privacy regression with nested private sentinels. No new
source contract, grant, dependency, UI, cloud operation or dataset access.

## Checklist

* [x] Reconstruct nested allowlists and prove invalidity preservation.
* [x] Prove raw view output contains no nested private sentinels.
* [x] Rerun focused SQL/core/HTTP/browser/lint/types, reconcile publication state.

## Implementation and evidence

The view now reconstructs each request using only id/kind/how_to_provide and each
issue using only severity/message. Original element/scalar types and lengths are
checked before extraction; malformed containers become explicit invalid markers.
No raw nested object is copied to the principal-readable column. Unrelated extra
source fields are omitted, not exposed or sent to Python/model.

Added `test_nested_request_and_issue_private_fields_never_leave_the_sql_view`
in the existing core SQL suite: extra scalar and nested-object private sentinels
are absent from raw SELECT output under the view-only principal, while valid
instructions, issue wording and citations survive. Existing malformed-container,
numeric-scalar, over-limit, exact-boundary and unknown/empty tests still pass.

Actual constructed loopback SQL suite: 33 tests, OK, no skips; runner held
`/tmp/ama-rpi-heavy.lock` nonblocking and removed its owned container.
Focused API chat suite: 9 tests, OK. Final core focused suite: 83 tests, OK,
23 opt-in SQL skips (separate real-SQL evidence above).
Core/API mypy: 156/94 files, pass. Targeted Ruff/check-format and diff checks pass.
Final actual Chromium/pinned-axe browser check passed, with external report and
screenshots at `/tmp/ama-520-documents-browser-rv001`.
No additional original Review or critique was executed. This is implementation
evidence for routed RV-001, not a rewrite of the original Not accepted outcome.
Total added test methods are now 12, within the plan's maximum 24.

## Publication handoff and remaining acceptance

Implementation continuation complete. Commit both original dated evidence and this continuation,
rebase remote branch, run full nonblocking locked exact-head gate, verify receipt,
independent exact-head publication assessment and normal push remain pending.
Read-only remote inspection found bot commit `ca1f11a6` on the remote topic
(rubric score only). The owner explicitly authorized rebase onto that branch.
Resolve author/committer from gh api user: id 8036360, login jmservera,
privacy-safe address `8036360+jmservera@users.noreply.github.com`.
Use the requested Conventional Commit and exact coauthor trailer.

Planned authoritative external gate directory:
`/tmp/ama-520-documents-rpi-final-20261028-1`. Fetch main, record base, use
`python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 0 --base <reviewed-main>
--out <new-external-directory>`. Final receipt remains external to avoid
self-reference. Any later candidate change/rebase requires a fresh run.
This commit-time handoff does not preclaim its future gate or push.

RV-002 remains separate: human/resident/content, AT/native zoom and real-model
acceptance are Not run, not proven by these synthetic checks. Operational view
application is not performed. Keep PR body Refs-only with no closing keywords.

## First committed-candidate gate failure and fixture alignment

Candidate `ba76cc38ce17ca66631db6b3641d772118c59184` includes the implementation
commit rebased onto remote bot `ca1f11a6`; author and committer use the resolved
noreply address and requested trailer. The full gate acquired the heavy lock
immediately with `--lock-timeout 0`, and completed all other required groups.
Its original failed receipt is preserved at
`/tmp/ama-520-documents-rpi-final-20261028-1/receipt.json`.

The full core discovery failed one existing sensor-reader mock fixture:
`test_resident_sensors.SensorProjectionTests.
test_reader_shapes_only_fixed_view_columns_and_parameterises_case`,
KeyError `documents_json`. Core ran 1454 tests, one error and 190 opt-in skips.
This fixture enumerates the fixed SQL columns but lacked the new additive
column; the focused set had not included its module. No runtime source defect
or broad fallback is inferred from this fixture failure.

Ordinary tightly coupled validation correction: align that existing fixture with
the explicit unknown-document JSON envelope and remove its now-replaced typed
documents value. Preserve the parameterization and invalid-sensor assertions.
No tests are removed, no behavior/gate is weakened and no original Review is
rewritten. Include `test_resident_sensors` in the focused rerun.

A new commit and fresh complete gate are required; the failed receipt cannot be
resumed across the fixture/evidence commit. Planned next external directory:
`/tmp/ama-520-documents-rpi-final-20261028-2`. Publication remains blocked until
that exact-head gate, current-main verification and independent assessment pass.

Expanded focused rerun including sensors: 92 tests, OK with 23 opt-in SQL skips.
Fixture Ruff/check-format and core mypy (156 files) pass; diff check passes and
the candidate has no ignored scratch. No additional unit method was added.
