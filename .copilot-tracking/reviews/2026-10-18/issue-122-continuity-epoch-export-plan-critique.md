---
title: Issue 122 continuity epoch and export plan critique
description: Single independent final-candidate assessment of bounded source correction
ms.date: 2026-10-18
---

## Metadata

* Task ID: 122
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-122-continuity-epoch-export-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-122-continuity-epoch-export-phase-details.md
* Research: .copilot-tracking/research/2026-10-18/issue-122-continuity-epoch-export-research.md
* Critique execution status: Complete
* Assessment count: Exactly one independent final-candidate critique.
* Source posture: Read-only. Only this critique artifact is written.

## Inputs and Criterion Boundary

* Caller direction: bounded partial stale-epoch proposal revival and task-release
  offline exports; no issue closure or full acceptance claim.
* Evidence considered: supplied plan, phase details and research, including
  C1-C7 and W1-W2 as supplied research claims. Read-only source inspection covered
  assistants.py, continuity.py, assistant_release.py, rai_release.py,
  ai_tasks.py, relevant store.py and sqlstore.py sections, the continuity and
  assistant API test fixtures, the export HTTP call site and src/check-container.py.
* Repository context considered: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md and
  docs/reference/memory.md. No new regulatory or company-authority conclusion.
* Required execution boundary: actual uniquely owned local MSSQL, independent
  connections and deterministic barriers; actual loopback HTTP/manual actions;
  source-context hardened API image. SQLite or SQL-shape emulation cannot
  substitute for SQL Server.
* Exclusions: no edits to appointments.py, procurement.py, sqlstore.py,
  server.py, projection.py or web app.js/ops.js; no live Azure, private data,
  paid inference, new authority or external notices.
* Decisions and dependencies: existing SQL transactions, no schema migration,
  persisted epoch identity, retained dispositions, audience-safe projections,
  external-head/digest checks and unknown billing. OQ-017 genuine authority,
  witnessed authorized drill, externally immutable Azure head and Azure SQL
  drill remain unmet, not implementation prerequisites for constructed tests.
* Candidate lock: worker-owned focused tests; no removals; maximum 30 added
  semantic test methods, with inherited MSSQL reruns not counted again;
  canonical installed source distributions; only owned generated synthetic,
  SQL and image/container targets; semantic and regression evidence retained.
* Assessment boundary: implementation credibility and falsifiable acceptance
  requirements, not implementation acceptance. No tests, containers, image
  builds, external research or new baseline reproductions were executed here.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; P01-T01; durable creation/claim/dispatch/completion | Covered | Identity gains epoch; old/unbound tasks fail closed; list/detail/review/export share policy. |
| P01-T01; historical ready/accepted and missing epoch | Covered | Original dispositions remain history; missing epoch cannot default to current. Retained claim epoch is usable only as the historical binding described in details, not a fresh claim/admission for unbound work. |
| C5-C6; P01-T01; legacy text/document/priority publication | Partial | Persisted refresh is required, but the atomic check-to-publication boundary and its legacy overlap oracle are not specified. PC-001. |
| C5; P01-T01; briefing cache and template/manual distinction | Covered | Current epoch applies to AI cache/priority, not ordinary template/manual work. |
| C3-C4; P02-T01; retained snapshot and current release status | Covered | Reference-time active snapshot, current status/revision and release-ID events are required; legacy top-level release is retained. |
| C3-C4; P02-T01; independent offline release validation | Partial | Producer-side resolution and incompleteness are specified, but verifier-side reference/lifecycle checks after outer-digest recomputation are not an explicit oracle. PC-002. |
| P02-T01; collection versus outer-export epoch race | Covered | Details explicitly retain no-reliance if epoch changes between collection and outer export. |
| P03-T01; actual SQLite/MSSQL overlap | Covered | Independent connections, competing action started while transaction is open, owned SQL resources and real-versus-emulated distinction are explicit. PC-001 adds the missing legacy publication interleaving. |
| C7; P03-T01; HTTP/manual case, challenge and hazard actions | Covered | Requires actual transactions and negative authority/safety checks, not the existing note-only test. |
| P03-T01; source-context hardened image and static checks | Covered | Explicit source build context, existing container checker, Ruff/format/mypy and cleanup requirements. |
| P03-T02; evidence, history and original Review | Covered | One original independent Review, retained adverse findings, no knowingly defective PR; coordinator corrections are separate. |
| Test ownership and candidate lock | Covered | No removals, maximum additions, canonical/generated targets, semantic/regression coverage and command/count/skip/failure evidence are fixed. |
| OQ-017; Azure head/drill; billing and old-image boundary | Covered | Unmet human/Azure gates retained; unknown charges not erased; gate-aware refresh does not make unsupported pre-gate images safe. |
| Shared #87 files and no-live/private/inference scope | Covered | Exclusions are explicit. Both proposed corrections fit the already active assistants.py, continuity.py, ai_tasks.py and legacy store.py slice plus focused tests. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 0 Medium, 0 Low.
* Rationale: the overall scope and operational exclusions are credible. Two
  security-relevant correctness boundaries need explicit implementation and test
  oracles before handoff: atomic legacy publication and independently checked
  offline release evidence. These are direct planner corrections, not reasons
  to expand scope or seek genuine operational approval.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Persisted epoch refresh alone does not close legacy check-to-publication races

* Related IDs: C5, C6, P01-T01, P03-T01; legacy lifetime, stale-process refresh
  and late-quarantine acceptance.
* Evidence: src/core/src/zava_forward/core/ai_tasks.py:194-229 computes
  `late` before entering the separately locked `add_record` operation;
  quarantine disposition is then saved in another lock acquisition.
  src/core/src/zava_forward/core/store.py:750-813 separately obtains a provider
  result and later publishes the priority record.
  src/core/src/zava_forward/core/sqlstore.py:104-140 refreshes on outer lock
  entry. The phase details require refreshed reads, but their explicit overlap
  example and acceptance oracle concern review/suspension, not the legacy
  check-to-append/return boundary.
* Concern: a refreshed epoch read can still observe E, release its transaction,
  and then allow suspension/restart to commit before the old E result is
  appended or returned as AI output. Merely making `continuity_epoch()` read
  fresh state does not make its result atomic with publication. Text/document
  completion also has an intermediate record save before quarantine status.
  This is a demonstrated source ordering risk, not a claim that an unwritten
  implementation already contains the defect.
* Impact: a gate-aware stale process can publish old-epoch AI output across
  the exact restart boundary this change is meant to close, even if durable
  assistant-task completion and all later review actions are gated.
* Smallest useful change: specify that each legacy AI result's final persisted
  epoch/suspension decision and record publication occur in one existing
  serialized write boundary. Build the returned AI-versus-manual/quarantined
  representation from that decision, with no persisted actionable intermediate
  state. Apply the rule to text/document and priority publication; preserve
  historical disposition and unknown billing. Define the linearization rule:
  publication committed before suspension may succeed, but publication admitted
  after a committed epoch change must quarantine/fall back. Do not promise
  revocation of bytes already delivered before suspension.
* Action owner: planning parent, updating P01-T01 and P03-T01; implementation
  worker owns the corresponding source and regression changes.
* Exact resolving evidence: revised details explicitly state this serialized
  decision/publication rule and name focused failing-first tests for
  text/document and priority. Tests use gate-aware old Store instances,
  independent actual local MSSQL connections and deterministic barriers to
  commit suspension/restart after the provider result is available but before
  final publication. Assert no old AI result is returned as current AI output
  or persisted as an actionable intermediate record; permitted historical
  output/disposition remains inspectable, reservations/unknown usage are not
  cleared, and manual/template paths still work. Record SQLite and actual
  MSSQL results separately. Parameterized cases can stay within the existing
  30-method ceiling; no shared adapter/file edit is required.
* Decision route: Direct planner correction. The user already requires
  cross-epoch denial and late quarantine; no significant or divergent user
  decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Offline verification needs a release-reference oracle beyond the outer bundle digest

* Related IDs: C3, C4, P02-T01, P03-T01; offline reconstructability,
  missing/truncated evidence and preserved digest/head checks.
* Evidence: src/core/src/zava_forward/core/continuity.py:289-325 currently
  verifies outer digest, ledger/head and the producer's `complete` flag, but
  does not resolve proposal/legacy task-release references or validate their
  digests. src/core/src/zava_forward/core/rai_release.py:103-108 binds a
  reference to a full release snapshot. In
  src/core/src/zava_forward/core/assistant_release.py:120-150, immutable body,
  mutable status/revision and lifecycle events are separate; event identity and
  time live in SQL columns, not in the JSON event body. P02-T01 calls for
  resolution, serialization and tampering tests without explicitly requiring
  the offline verifier to check these new relationships.
* Concern: producer-side incompleteness flags plus an ordinary outer-digest
  tampering test can all pass while the offline verifier still accepts an
  unresolvable or mismatched release reference after someone recomputes the
  outer digest and leaves `complete=true`. Exporting event bodies alone also
  loses recorded lifecycle timestamps and stable event identity. The current
  ledger check does not itself validate the separately stored release events.
* Impact: the bundle can be readable and self-consistent at the outer level
  without proving that the claimed task-release evidence is present, matches
  the retained reference, or reconstructs the recorded revocation lifecycle.
* Smallest useful change: explicitly extend the offline verifier contract to
  resolve every retained durable/legacy release reference by ID/version,
  recompute its reference-time snapshot digest, and reject unresolved,
  contradictory or declared-incomplete evidence independently of the outer
  digest and producer completeness flag. Include release-event ID, release
  association, recorded timestamp and body, plus enough bounded-read
  count/truncation metadata to detect the planned missing/truncated fixtures.
  Read each current status/revision and corresponding lifecycle evidence at a
  coherent SQL observation boundary. Preserve the active snapshot separately
  from current revoked status. Do not claim that a self-contained bundle can
  authenticate wholesale adversarial rewriting of an unanchored release event
  history; retain that limitation and the external immutable-head unmet gate.
* Action owner: planning parent, updating P02-T01 and its acceptance oracles;
  implementation worker owns resolver/verifier and focused tests.
* Exact resolving evidence: revised details name verifier-side release checks
  and the event envelope. A serialized active-to-revoked fixture verifies after
  provider/store shutdown using only bundle plus separately held expected
  ledger head. Negative fixtures remove a referenced release, replace its
  ID/version/snapshot, remove lifecycle evidence, and truncate bounded event
  output; recompute the outer bundle digest and force `complete=true` so the
  reference/lifecycle checks, not merely digest mismatch or the producer flag,
  must reject them. Check timestamp/event identity retention and truthful
  current status/revision. Retain existing ledger-tail/external-head negatives
  and audience-projection regression checks. Record the remaining
  unauthenticated-history limitation without upgrading local evidence to
  external Azure acceptance.
* Decision route: Direct planner correction. Independent offline validation
  is already in user scope; no significant or divergent user decision is
  needed.

## Strengths and Residual Risk

* The candidate addresses the reproduced stale-ready revival through shared
  durable views and epoch-qualified identity rather than deleting history or
  only disabling the UI.
* It distinguishes reference-time active release evidence from later mutable
  lifecycle status, avoiding a revoked-versus-active digest false mismatch.
* Actual local SQL, HTTP/manual and hardened-image work are mandatory future
  evidence, not falsely reported completed by research.
* Unsupported pre-gate images require stopping/draining or external serving
  exclusion. This source slice cannot establish that deployment control.
* Genuine OQ-017 authority and witnessed drill, externally immutable Azure
  head and Azure SQL drill remain unmet. No synthetic exercise, passing plan
  critique or implementation Review substitutes for them.
* No remote cancellation, exactly-once billing, real inference, user research,
  general configuration reversibility or full issue acceptance is inferred.

## Questions or Blocking Evidence Gaps

* No unresolved user choice blocks the bounded correction.
* The two findings identify missing plan-level acceptance precision. Neither
  requires additional external research, live access or prohibited file edits.

## Limitations

* Read-only credibility assessment, not an executed regression or exploitation
  result. The supplied baseline reproduction was not rerun.
* GitHub W1-W2 claims were considered as recorded research; no external source
  refresh or open-ended research was performed.
* Event-history authenticity cannot be inferred from a recomputable digest or
  a ledger head that does not bind that event history. This critique requests
  structural/integrity checks, not an unapproved new external trust system.
* Mandatory validation remains for implementation and original Review.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: disposition PC-001 and PC-002 explicitly, revise the
  existing phase details and linked plan acceptance oracles, and finalize the
  candidate without another critique.
* User response required: No.
* Preserve this original adverse verdict and findings unchanged. Any later
  correction evidence is a separate record, not a critique rerun.

| .copilot-tracking/plans/2026-10-18/issue-122-continuity-epoch-export-plan.md | Assessed final-candidate plan |
| --- | --- |
| .copilot-tracking/details/2026-10-18/issue-122-continuity-epoch-export-phase-details.md | Assessed phase details and execution contract |
| .copilot-tracking/research/2026-10-18/issue-122-continuity-epoch-export-research.md | Supplied research and evidence IDs |
| .copilot-tracking/reviews/2026-10-18/issue-122-continuity-epoch-export-plan-critique.md | Original single critique, retained adverse evidence |

## Next Steps

Planning parent: revise and disposition the two direct corrections, then
continue through the existing implementation gate without a second critique.
No user action or new user decision is required. This critic stops here.
