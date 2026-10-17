---
title: Issue 206 phase details
description: Bounded implementation tasks and exact completion evidence
ms.date: 2026-10-17
---

## Metadata

Task ID 206; slug issue-206-rubric-deleted-head; plan:
.copilot-tracking/plans/2026-10-17/issue-206-rubric-deleted-head-plan.md.
Evidence: research C1-C5/W1-W3. No unresolved research blocker.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete: 159 focused cases passed | P01-T01, P01-T02 |
| P02 | Complete: compiler/invariant audit passed; exact 21 baseline failures unchanged | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Repair recording boundary

<!-- rpi:task id=P01-T01 -->
### P01-T01: Guard PR lifecycle and exact head

Before record checkout, use the existing github-script action/API to read current
PR state. Closed means obsolete notice/output, not rubric pass. Open unchanged
means eligible; moved means block recording but retain the scored-SHA diagnostic.
Any API exception propagates. Checkout event SHA, never branch/main fallback.

Refresh state before recording, and at publication before reporting pass.
A workflow-created private hook directory rejects zero or unexpected advertised
remote OIDs for the explicit `refs/heads/HEAD_REF`. Keep ordinary non-force push;
the server atomically compares its advertised old OID. Never enable repository
hooks. Existing push-failure and record-outcome gates remain in force.

Completion: executable tests show no score publication/ref creation for obsolete
heads; active expected head works; moved/deleted-at-push rejects; API failure
does not become skipped-success. Publication remains original/bot SHA only.

#### Final lifecycle contract after critique

| Producer | Validated output/outcome | Consumers |
| --- | --- | --- |
| lifecycle before checkout | eligible, moved or obsolete; successful API required | Checkout only after success and not obsolete |
| verify after immutable checkout | moved=true if initial state moved or local SHA mismatches | Record forbidden; publish blocked |
| record_head after gate | eligible, moved or obsolete; successful API required | Record requires eligible, verify success and no moved flag |
| Publish verdict fresh read | Explicit closed skips; open requires full 40-hex head SHA | Pass requires all applicable checks/gate/record successful and expected current head |

Unknown/missing state, null data/head and invalid SHA throw, never become
eligible or ordinary movement. Explicit closed state may omit head data.
Initial API failure fails the job before checkout. Later API failure cannot
pass even with a valid saved gate decision. Obsolete runs publish no statuses,
comments or reviews; notices explain the skip. Existing missing-verdict
conclusion only handles a skipped record job, not this successful obsolete step
path, so deliberate obsolescence does not enter that condition.

After a successful push expect current head NEW_SHA; after a legitimate
successful no-commit record step expect SCORED_SHA. Failed/skipped record or
missing lifecycle output cannot choose a passing no-change path. A reset to
SCORED_SHA after a successful bot push is movement, not success.

The isolated pre-push hook requires exactly one input update, correct full
destination, local OID equal to the intended bot commit and nonzero remote OID
equal to SCORED_SHA. Empty/unexpected input fails. Tests separately mutate a
remote before advertisement and after the hook receives expected advertisement;
normal server old-OID validation must reject deletion and forward/backward
movement without recreating/overwriting the ref or emitting new_sha.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Focused executable regressions

One new pytest module in the existing rubric scripts suite. Parse workflow
frontmatter and generated lock using existing PyYAML patterns. Execute extracted
github-script bodies with Node mocks; execute real shell steps/hooks using
temporary repositories/remotes. Cover closed with deleted head, unchanged,
moved (including backward move), late deletion, push failure, API 404/403/500,
and non-PR no-op behavior. Do not duplicate gate evaluation logic.
Include malformed-success API responses, all lifecycle failure/empty/skipped
combinations with a saved passing decision, and normal/post-push/closed
publication heads. Execute source and compiled step bodies.

Completion: targeted runner passes against both source/compiled scripts;
workflow conditions tie eligibility to checkout/record/publication.

<!-- rpi:phase id=P02 -->
## P02: Compile, document and reconcile

<!-- rpi:task id=P02-T01 -->
### P02-T01: Compile and validate

Use `gh aw compile rubric-score --no-check-update`, installed v0.89.21.
Preserve existing pins; missing compiler would block lock changes.
Update `.github/rubric/README.md` with lifecycle handling and test command,
not unrelated KB pages. Run focused tests and full existing rubric runner.
Baseline: 21 failed, 117 passed, 7 skipped. Compare failure identities,
including old seed/registry and path-filter fixture failures.

Completion: compiler-produced lock diff limited to intended workflow; exact
failures distinguished from new regressions; no live run dispatched.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Reconcile implementation evidence

Update phase/task markers, changes artifact, session state and explicit phase
log events. Record all criterion results and any limitations before Review.
No self-approved human gate or live-run claim.

Completion: one coherent candidate ready for one independent Review. Review
findings route to later work; no repeat review or hidden closure claim.

## Completion Evidence

P01-T01/P01-T02: 159 focused cases passed against source/compiled steps.
P02-T01: gh-aw v0.89.21 compilation succeeded and repeated byte-identically;
full existing suite 21 failed, 276 passed, 7 skipped. Exact 21 failing node IDs
match pre-edit baseline; 159 additional passes and no new failures.
Source/lock audit preserved all other jobs, permissions, action/container
manifest, scorer prompt/model, inputs, trusted loading and deterministic gate.
P02-T02: plan markers, details, changes and phase log reconciled before Review.
No remaining implementation task or human operational approval claim.
