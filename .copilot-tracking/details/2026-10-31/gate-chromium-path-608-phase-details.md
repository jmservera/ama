<!-- markdownlint-disable-file -->
# RPI Phase Details: Chromium pathname admission

## Metadata

* Task ID: 608
* Task slug: gate-chromium-path-608
* Related plan: .copilot-tracking/plans/2026-10-31/gate-chromium-path-608-plan.md
* Evidence: .copilot-tracking/research/2026-10-31/gate-chromium-path-608-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Implement bounded admission | Complete | P01-T01, P01-T02 |
| P02 | Validate and hand off | Complete | P02-T01 |
| P03 | Hosted fixture correction | Complete | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Implement bounded admission

Context: main resolves new external output, then Runner sets output/tmp.
Intent: fail impossible socket paths before execution without moving scratch.
Boundaries: tooling and local-gate docs only; no workflow or package tests.
Validation: exact byte boundary, CLI ordering, direct constructor backstop.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add selection-aware byte bound

Define Linux socket capacity 107 bytes and Chromium suffix
`/org.chromium.Chromium.XXXXXX/SingletonSocket` (45 bytes). Derive TMPDIR
limit 62 and output limit 58 rather than unrelated magic thresholds.
Helper checks only selections containing browser. CLI passes resolved output
and selected groups after changed selection resolution, moving its tool
identity probe after pathname admission and before mkdir. Runner uses the same
helper immediately after selecting groups and before owned folder writes.
For resume, add optional new-output admission argument to validate_receipt:
after integrity/schema/recomputed-selection/source checks, call helper on new
output and trusted selection before tool_identity or image probes. The default
None leaves standalone and recursive historical verification unchanged. Main
still completes all parent validation before mkdir/lock/Runner. This directly
resolves PC-001 without unchecked JSON admission or skipping validation.
No receipt or scratch semantics change; existing ownership checks stay intact.
Completion: rejection includes measured lengths, limits and short external example.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add tooling regression coverage and documentation

Depends on P01-T01. Test ownership/budget are locked in the plan.
Test exact 58/59-byte output boundary, reported ~130-byte shape and Unicode
filesystem encoding. Use a real AF_UNIX bind at the supported boundary to test
the formula, not just its constants. CLI mocks may isolate dispatch, but assert
no tool probes, lock, Runner, verification, output or receipt on rejection.
Resume subcases use real validate_receipt and sealed fixture receipts, not a
mock hiding its nested probes: reject impossible output before tool/Docker
probes, preserve admitted-path validation and tampered-receipt rejection.
Resolved symlink aliases cannot conceal long output; existing/source paths
retain original rejection. Direct Runner rejection leaves its output empty;
browser-free selections admit long output. Update src/README.md local gate
section with byte bounds, ambient-TMPDIR override and short new output guidance.
No new generated outputs or knowledge-base page.

<!-- rpi:phase id=P02 -->
## P02: Validate and hand off

Depends on completed P01. Focused tier intentionally excludes heavy full gate.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused suite and ruff

Run python3 -m unittest tools.test_rpi_checks and existing ruff check/format
selectors on both tools files using line length 100. If chosen command fails
because dependency is missing, restore with pip in external environment.
Record commands/counts/exits in changes evidence, reconcile plan/task markers,
state, amendments/divergences and unresolved full-run follow-up before Review.
Independent Review once; no human/hosted approval checkbox is marked complete.

Completion evidence: all six planned tooling methods added, no removals.
Focused suite passed all 54 tests after formatting. Existing isolated Ruff
selectors passed. Changes record carries exact commands and initial lint-selector
correction; full browser/SQL and hosted approval remain unproven.

<!-- rpi:phase id=P03 -->
## P03: Hosted fixture correction

User-selected later hosted work; the original critique and Review are unchanged.
Merge main, preserve its rubric score and both log histories. Real socket,
Unicode, CLI byte-bound and admitted-resume fixtures own short `/tmp` roots
with cleanup. Mock-only runners declare no browser selection; cancellation
selects preflight only. Production byte admission remains unchanged.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Merge and correct fixtures

Complete: main 9c67a399 merged without conflicts; fixture correction implemented.
Added one nested regression using actual Runner-owned TMPDIR at 18/58/100-byte
outer output. It runs ten affected fixture cases with tempfile's cached root
reset so ambient TMPDIR is actually exercised.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Validate and publish

Focused unittest and existing isolated lint/format passed: 55 tests ordinarily
and the complete suite under gate-owned TMPDIR at 18/58/100-byte outer outputs.
Current changes/review addenda retain the hosted finding and bounded assessment.
Complete: correction committed at de0aa9aa, published through 7fb024e2 after
the required non-rebase pull/merge retry, retaining main's rubric score.
GraphQL reply PRRC_kwDOUU8JX88AAAABCDNZ5g posted; thread isResolved verified true.
Final evidence publication remains on this branch; no source changes follow.
No heavy/full gate required by the user; no issue-closing claim.
