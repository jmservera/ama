<!-- markdownlint-disable-file -->
---
title: Case view review fixes 552 phase details
description: Evidence-based tasks and local completion expectations
ms.date: 2026-10-29
---

## Metadata

Task ID: 552-pr554-review-fixes. Slug: case-view-review-fixes-552.
Plan: .copilot-tracking/plans/2026-10-29/case-view-review-fixes-552-plan.md.
Research: .copilot-tracking/research/2026-10-29/case-view-review-fixes-552-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Complete; local commit verified | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct and validate both findings

Context: C1-C4 show reproduced summary assertion failure and zero packaged icons.
No production markup or serving changes are necessary (C5).
Boundary: only named assertion/manifest plus one preventive test and guide.
Dependencies: critique dispositions resolved. Completion: exact diff and evidence
for AC1-4; unavailable checks stay explicit.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Apply selector, packaging and documentation corrections

* `src/api/checks/case_journey_browser_check.py`: exact direct-child selector.
* `src/api/pyproject.toml`: add explicit nested PNG glob to zava_forward.api.
* `src/api/tests/test_case_journey.py`: stdlib TOML parse and Path.match each of the
  six known expected relative paths against declared API package-data patterns;
  assert expected source files exist. One new method maximum, no removals.
* `src/api/README.md`: state nested icons are included in installed API wheels.

Existing browser test supplies semantic DOM coverage; existing presentation
test remains. New test should fail before package glob is added and pass after.
No hidden generated targets, fixture changes or dependency installation.
Completion evidence: exact selector/manifest/README diff and one added test;
pre-fix regression failed all six icon subtests. UI source is unchanged.
Local judgment: use existing pathlib Path.match rather than fnmatch, whose
wildcard crosses path separators and would falsely accept `web/*`.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate actual output and local browser behavior

From `src/api`:

```bash
export PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests
/tmp/mv/bin/python -m unittest test_case_journey test_workspace_scripts \
  test_design_system test_accessibility_baseline test_content_standard -q
/tmp/mv/bin/ruff check checks/case_journey_browser_check.py tests/test_case_journey.py
/tmp/mv/bin/ruff format --check --force-exclude checks/case_journey_browser_check.py tests/test_case_journey.py
node --check src/zava_forward/api/web/case-workspace.js
node --check src/zava_forward/api/web/app.js
/tmp/mv/bin/python -m checks.case_journey_browser_check \
  --axe /tmp/ama-526-evidence/axe-4.10.3.min.js \
  --out /tmp/case-552-review-fixes-20261029-journey
/tmp/mv/bin/python -m checks.case_view_ux_browser_check \
  --out /tmp/case-552-review-fixes-20261029-compact
```

From root build a new API wheel with pip wheel --no-deps into
`/tmp/case-552-review-fixes-20261029-wheel-after`. Inspect ZIP names for exactly
the six expected PNGs and compare every member byte to tracked source. An
additional temporary-target install is allowed but not required by AC2.
Do not treat source HTTP success or the manifest regression as wheel proof.
The browser harness verifies its loopback server and cleans owned processes.
If unrelated later assertions fail, preserve that outcome and scope; AC1 can
still be proven without claiming the entire browser suite passed.

Completion: five modules, 55 tests passed; lint and both JS syntax checks passed.
Explicit formatting of the legacy browser file failed on pre-existing content
(confirmed against starting HEAD). Respect the repository's existing checks/*.py
format exclusion with --force-exclude; test_case_journey.py is formatted.
No unrelated legacy reformat. Both complete browser runs passed; journey
recorded 87 axe scans, zero violations, 50 incomplete checks (not acceptance).
Fresh wheel contains exactly the six expected PNG paths and source-equal bytes.

<!-- rpi:phase id=P02 -->
## P02: Review and persist locally

Context: explicit full loop and local-only commit; full publication gate is
neither executed nor waived. Prior task artifacts remain immutable.
Dependency: reconcile P01 markers/details/changes and actual validation first.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Execute one independent Review and commit locally

One reviewer, one review artifact:
.copilot-tracking/reviews/logs/2026-10-29/case-view-review-fixes-552-review.md.
Provide absolute external evidence paths with explicit read authority and
include exact commands, exits, wheel-member/byte results and concise browser
result extracts in the tracked changes artifact. PC-001's worker-specific
filesystem limitation is not a parent limitation: parent already ran baseline
commands using /tmp. Do not copy generated trees into the repository merely
to work around another executor's restrictions. If raw inspection is unavailable
to the reviewer, label it explicitly; a source/record review is not independently
rerun browser or rendered acceptance.
Require execution, outcome, findings and routing separately. No repeat Review.
No mandatory human approval is completed by this local exercise.

Resolve `gh api user` before configuring local git email from returned id/login.
Use both author/committer privacy-safe identity, Conventional Commit with Refs
#552 and the exact requested Copilot trailer. Commit only task-owned paths,
verify final commit/trailer/worktree, and leave all remote state unchanged.
Completion means persistent local correction and evidence, not merge acceptance.

Completion evidence: one Review Complete / Conformant with justified divergence,
no new findings; source and original dated evidence committed as 5a3edfe6.
Author/committer privacy-safe email, exact Copilot trailer and clean worktree
verified. Final documentation-only closeout records this result separately.
No push, az, manual rubric edit, repeated Review or publication gate waiver.
