---
title: Employee acceptance gate bootstrap research
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Brief and Scope

Task 570-gate-bootstrap, employee-identity-check-570-gate-bootstrap, child of
completed employee-identity-check-570-correction. Resolve a directly coupled
fresh-browser discovery defect required by the owner's complete-gate request.
Focused convergence; evidence root .copilot-tracking/research/2026-10-31.
Scope test bootstrap and CLI execution count; no changes to BINDING/observers,
gate matrix, browser installation order, identity, Azure or credential handling.
Original correction critique and Review stay immutable.
Repository instructions/rpi-research selected; specialists/design skipped,
small continuous trace. No interaction needed for this bootstrap correction;
owner requires full gate without bypass and required Chromium execution.

## Questions and Prior Knowledge

Q1: Can the fresh full gate discover this module before Chromium installation?
Q2: How does the repository distinguish allowed discovery skips from required
integration execution? Reuse completed correction evidence and current gate.

## Cycle 1, Inline in Order

* Wider: gate isolates PLAYWRIGHT_BROWSERS_PATH under fresh output and makes
  browser depend on project-api. The new unconditional browser tests therefore
  run too early during discovery. Reflection: do not alter the matrix.
* Deeper: an actual reproduction at an absent browser path yields three
  BrowserType.launch errors in 1.561 seconds. Existing browser asset test
  narrowly recognizes the missing executable with an exact approved discovery
  reason; all other launch errors propagate. Reflection: reuse that pattern.
* Contrarian: simply skipping can make unittest wasSuccessful true and turn
  the maintained CLI into a false pass. Required extras already reject skips,
  but CLI must also reject any skips/zero or incomplete execution.
  Reflection: missing browser may be a recorded non-integration discovery skip,
  never a passing required CLI or integration result.

## Evidence and Dispositions

* C1: tools/rpi-checks.py:1144: isolated fresh browser path.
* C2: tools/rpi-checks.py:335 and :1604: API precedes browser installation.
* C3: src/api/tests/test_browser_asset_urls.py:53: exact narrow missing-browser
  discovery handling; approved reason is already enumerated in gate at :80.
* C4: src/api/checks/employee_acceptance_check.py:466: CLI relies on
  wasSuccessful without checking skipped or execution count.
* C5: external chromium-bootstrap-reproduction.log in the session files:
  three actual missing-executable errors, no credential/live operation.
* C6: tools/rpi-checks.py:1039 and :1914: discovery qualification does not
  authorize integration skips; extras require actual execution.

Accepted: narrowly handle only missing executable as existing approved
discovery reason and make CLI fail for any skip or non-three execution.
Rejected: installing into/modifying a running gate environment, pre-seeding
future output, weakening integration receipts, generic exception swallowing
or changing gate dependencies. Current aa531930 gate remains immutable
historical attempt; future source commit requires a fresh gate.

## Readiness and Self-check

Research disposition executed, Complete; Planning Readiness Ready.
All waves completed, exact local failure observed, prior art verified.
No further research needed. Independent expected identity and original live
criterion remain unmet; zero credential reads/sign-ins. Parent continues Plan.
