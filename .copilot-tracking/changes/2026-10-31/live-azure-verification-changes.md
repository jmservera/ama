<!-- markdownlint-disable-file -->
# RPI Changes: Live Azure verification

## Metadata

* Task ID: 3a44be57-db3a-46d1-b9e4-fe82bd7c74e7
* Related plan: .copilot-tracking/plans/2026-10-31/live-azure-verification-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/live-azure-verification-phase-details.md
* Implementation date: 2026-10-31

## Execution Status

* Status: Partial; observation/recording complete, publication pending
* Declared scope: Full plan
* Completed markers: P01/P01-T01, P02/P02-T01
* Remaining markers: P03/P03-T01
* First boundary: prepare sole capture-free driver; missing namespace dependencies installed with pip.

## Execution Summary

Implement bounded observation and evidence publication only. No source app
changes, Azure configuration, scaling, jobs or deployment.

## Completed Work

### Bounded actual app observations

* Related task: P01-T01.
* Sole driver and sanitized result: .copilot-tracking/changes/2026-10-31/live-azure-verification.py and live-azure-verification-results.json.
* 2026-10-31 15:42:51-15:45:41Z: employee/resident health200; resident login200 (one attempt), chat geometry/dock/resize/containment and five source-matching first-navigation assets passed.
* Employee independent directory lookup exit1/access denied; zero employee attempts. Chat/map/case/tabs/capacity/metering remain blocked, not failed application assertions.
* No Azure writes/deploy/scaling/jobs, AI send, consent or booking changes.

### Durable documentation and issue records

* Related task: P02-T01.
* Evidence pack and knowledge-base index/log record actual passes, blockers,
  hashes, geometry, command, attempt budget and original executor defects.
* #523 comment: https://github.com/jmservera/ama/issues/523#issuecomment-6545622906
* #524 comment: https://github.com/jmservera/ama/issues/524#issuecomment-6545623482
* #570 comment: https://github.com/jmservera/ama/issues/570#issuecomment-6545623680
* #432 comment: https://github.com/jmservera/ama/issues/432#issuecomment-6545623890
* Related resident #550 comment: https://github.com/jmservera/ama/issues/550#issuecomment-6545624101
* Only #523/#524's literal recorded-or-pending rows ticked; both remain OPEN,
  with actual employee behavior blocked. No new #570/#432/#550 ticks/closures.
* No product failures observed; existing identity dependency on #570, no
  fabricated/duplicate bugs.

## Implementation-Time Plan and Detail Updates

### Critique safety corrections

* PC-002/003/004 applied: durable sole-run attempt counters, pinned origins and semantic observation matrix.
* PC-001 rejected because its asserted runtime prohibition does not exist in this parent's instructions; unchanged complete gate remains mandatory.
* One original Revise critique retained; no second critique.

### Preserve initial executor defects and continue within known budget

* First writer's append-mode output produced a concatenated checkpoint stream.
  The fixed locked r+ writer fsyncs and overwrites one valid JSON object, nesting
  every original checkpoint instead of deleting adverse evidence.
* Employee credentials were password-only; two zero-attempt employee-only
  continuations supported that format and observed actual directory denial.
  Resident's one submission and original geometry/asset evidence were not rerun.
* Guarded continuation checks completed state, exact task and monotonically
  valid counts; it refuses any continuation after an employee submission.
* This is an in-scope automation correction, not product remediation or a new
  sign-in budget. Plan/details reconciled; critique not repeated.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Live driver and actual apps | P01 | Partial live acceptance | Resident passed; employee blocked, exact result JSON |
| Driver --self-test | Attempt safety | Passed | Persisted count==2 refusal and overwrite JSON validity; zero credential access |
| checks.employee_acceptance_check CLI | Unchanged synthetic Chromium | Passed | Three tests, zero skips, 15.627s; not live identity |
| AST, JSON/hash, new links, diff and GitHub readbacks | Evidence integrity | Passed | Result SHA256 4f8091aa304bae20d07e9135430135351c9bdf88f3dcec6df9cd91bbe8c50db7 |
| Full exact-HEAD gate | P03 | Pending | External receipt after final commit |

### Original independent Review

* Execution Complete; outcome Residual work. One original record:
  .copilot-tracking/reviews/logs/2026-10-31/live-azure-verification-review.md.
* No unresolved implementation defect. RV-001 Medium routes independent
  employee identity/live evidence to #570; RV-002 Medium routes economics/
  quality evidence to #432; RV-003 Low retains P03 publication as the next
  authorized parent action.
* Review outcome and original critique are immutable. The final full receipt
  remains external; this committed record is the pre-publication snapshot,
  not a claim that unrun checks or remote publication succeeded.

### Preserve task-generated installation metadata before the gate

* Archived the complete existing tracking snapshot and the exact three
  pip-generated src namespace egg-info directories externally; verified full
  archive readback, selected restore hashes and unchanged protected tracking
  bytes before/after relocation.
* Relocated only the three generated metadata directories to preserved external
  originals; no historical tracking or source deletion.
* External preservation receipt:
  /home/azureuser/.copilot/session-state/3a44be57-db3a-46d1-b9e4-fe82bd7c74e7/files/generated-metadata-preservation/receipt.json.
* Final candidate has no ignored installation inputs. The full gate owns its
  isolated environments and preserves the final receipt externally.

## Pre-Review Reconciliation

* Plan/details/changes/documentation and issue results reconciled.
* Ready for one original Review of delivered P01/P02; P03 publication remains
  visibly pending and is not counted as completed implementation.
* Validation and blockers explicit; employee unavailable evidence routed to
  #570, economics to #432. No human or hosted approval inferred.

## Blockers

* Independent employee tenant/object attestation denied; directory operator
  or independently verified expected IDs needed before guarded employee sign-in.

## Remaining Work

* P03/P03-T01: original independent Review, final commit, full gate/receipt,
  independent exact-head publication assessment, non-forced push and Refs PR.

## Follow-Up Items

* #570 independent identity then authenticated employee surfaces.
* #432 financial/quality/held-out batch gates are outside this live UI check.

## Return-to-Caller State

* Partial full-plan implementation; delivered P01/P02 ready for original Review.
* Original Review Complete / Residual work; automatic parent continues P03
  publication without reimplementing or repeating Review. Canonical committed
  artifacts freeze before the final gate; post-gate receipt/PR evidence stays
  external so it cannot invalidate its own clean exact-HEAD candidate.
