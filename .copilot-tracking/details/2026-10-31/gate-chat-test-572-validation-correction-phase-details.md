<!-- markdownlint-disable-file -->
# Phase Details: gate-chat-test-572-validation-correction

Task ID: 572. Date: 2026-10-31. Readiness: Ready after direct critique dispositions.
Research: .copilot-tracking/research/2026-10-31/gate-chat-test-572-validation-correction-research.md.
Parent original Review and changes remain unchanged.

<!-- rpi:phase id=P01 -->
## P01: Actual validation evidence

<!-- rpi:task id=P01-T01 -->
### P01-T01

Reuse the existing restored external venv; do not reinstall unless a selected
command reports a missing dependency. From src/api run unittest discovery with
PYTHONPATH=../core/tests:../agents/tests, Ruff check and Ruff format --check.
From root run tools unittest discovery and pinned tooling Ruff checks.
Write logs only to the current external session files directory.
Current evidence: API Ruff passed (65 files), tooling isolated Ruff passed and
39 regressions passed. Non-editable API attempt failed on missing evaluation
fixtures; editable external git-archive restoration resolved those errors.
Restored rerun complete: 1430 tests in 668.049s, OK, 320 explicit discovery
skips. Source is unchanged by the later a75bbdff merge; final gate runs current
tooling/workflow identities independently.
Integrated tooling rerun: 39 tests passed in 11.491s.

<!-- rpi:task id=P01-T02 -->
### P01-T02

Run test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log
with ZF_BROWSER_TESTS=1, API/core/agents paths and verbose unittest.
Use `flock -w 1800 /tmp/ama-rpi-heavy.lock <command>`, retry once only if
admission times out. Verify one exact success and zero skips.
No foreign holder interruption and no bypass.
Parent Bash is the permitted executor for the unchanged /tmp shared lock;
the critique worker's file-operation limitation is not a parent limitation.
Complete: first admission attempt ran the exact case successfully in 2.379s,
one test and zero skips; correction-chromium-1.log is external evidence.

<!-- rpi:phase id=P02 -->
## P02: Original correction Review and candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01

One independent correction Review examines source carried by the branch, dated
correction evidence and AC1-AC4. It preserves original Review outcomes and
distinguishes final gate pending from a source defect. Required human/hosted
approvals remain unclaimed.
Unresolved blocking source/acceptance findings stop publication; deliberately
later final-gate evidence proceeds to P03. Disposition every residual explicitly.
Complete: sole original correction Review Complete / Residual work, no blocking
source defect. RV-001 [High] routes the planned AC4 final gate and publication
assessment to the parent, not a source correction or repeated Review.

<!-- rpi:task id=P02-T02 -->
### P02-T02

Reconcile plan/details/changes/state before commit. Resolve GitHub identity
with gh api user and repository-local noreply email for author and committer.
Include required Co-authored-by trailer. Final receipt is external; no later
evidence commit may reuse it.
This candidate records evidence immediately before commit; actual commit and
P03 completion belong to the external final status/receipt and delivery PR.

<!-- rpi:phase id=P03 -->
## P03: Final gate and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01

Fetch current main and merge if moved, preserving prescribed conflicts.
Run tools/rpi-checks.py --all --jobs 3 --lock-timeout 1800 --base <main>
--out <new-external-directory>. Its internal lock is the documented equivalent
of the outer wait without self-deadlock. Retry admission once in a new directory.
An assertion, prerequisite or verification failure is retained and corrected
through explicit evidence, never converted to a skip.
Compare any later merge's relevant source/tests/tools with the frozen Review.
Document equivalence for ancestry-only changes; relevant delta requires scoped
independent exact-head assessment and current full execution before publication.

<!-- rpi:task id=P03-T02 -->
### P03-T02

Fetch again, independently assess exact committed head with full receipt,
verify immediately before push against current origin/main. Drift requires
new candidate and full gate. Use git push -u origin HEAD, never force.
PR to main includes original/correction artifact pointers, validation and
accurate Closes/Refs #572 disposition. Final authoritative logs remain external;
post-gate durable status goes in the external session record and PR, not a
new candidate commit that would invalidate the gate.
Independent exact-head assessment must find no unresolved blocking source or
acceptance findings, including relevant changes after the original Review.
