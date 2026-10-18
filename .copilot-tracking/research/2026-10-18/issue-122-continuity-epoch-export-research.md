<!-- markdownlint-disable-file -->

# Task Research: issue-122-continuity-epoch-export

| Field | Value |
| --- | --- |
| Date | 2026-10-18 |
| Researcher / agent | RPI worker, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-18/issue-122-continuity-epoch-export-research.md |

## Research Brief

Investigate stale continuity epoch revival and supplier-independent task-release
exports for the coordinator's bounded partial #122 follow-up. Audience: delivery
coordinator and independent reviewers. Output mode: convergence for planning.
Scope: assistants.py, continuity.py, ai_tasks.py and focused tests. No web,
appointment semantics, shared SQL refactor, live data, inference or Azure changes.
Success requires actual epoch reproductions, retained history, offline release
evidence, real local SQL concurrency, HTTP/manual exercises and image evidence.

## Research Parameters

Focused posture selected from bounded caller scope and supplied hypotheses.
Resolved evidence root: .copilot-tracking/. Research is source-read-only.
Initial internal candidates: core continuity, API assistants, legacy ai_tasks,
release storage, component READMEs, workflows and existing tests.
External candidates: current #122 and merged PR #269, retrieved 2026-10-18.
No arbitrary cycle ceiling. One independent final-candidate critique and one
original post-implementation Review; never amend adverse evidence.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md and supplied repository guidance | Selected; branch/privacy, source layout, evidence and safety boundaries |
| Skill | rpi-research | Selected; ordered wider/deeper/contrarian investigation |
| Specialist | Independent plan critic and original reviewer | Reserved for their later phases, not research delegation |
| Skill | Web/design skills | Skipped; no web edits authorized |

## User Participation and Direction Controls

Caller explicitly directs full ordered RPI execution autonomously. No intake
question needed. Safe constructed fixtures are not genuine approvals.
Preserve #87 shared-file exclusions. No rebasing, merging or issue closure.
Current branch is the requested topic, clean at base
99056cae7bc679d2ace3e42c75f28577cfce8887, with no open PR.

## Research Questions

1. Where can old-epoch ready/accepted proposals regain reliance after restart?
2. Which enqueue, claim, completion and legacy gates need coherent enforcement?
3. Can retained task releases and lifecycle events be reconstructed offline with
   audience-safe projection and explicit incomplete evidence?
4. Which actual local SQL, HTTP/manual and hardened-image checks are supported?

## Research Cycle Log

Cycle 1 opening: Wider maps lifecycle and test tooling; Deeper reproduces exact
failures; Contrarian checks compatibility, projections and simpler alternatives.

### Wider

Mapped durable assistants, legacy records/priority, release admission, continuity
export and SQL adapters. Existing SQL writer uses independent connections and
application-level serialization; no shared adapter change is needed. Component
CI uses pip editable installs, unittest, Ruff/format and mypy. Docker daemon and
mssql-python are available. Installed missing source distributions in local .venv.

Reflection: one coherent epoch identity must span enqueue through read/review,
not only completion. Legacy priority and briefing cache are relevant surfaces.

### Deeper

Executed a synthetic baseline reproduction using existing Suspension fixture:
ready claim_epoch=0, persisted epoch=2 after suspension/restart, actionable=True;
accept succeeded; export relied_on=True; fresh invoke reused the same proposal ID.
Export had no task-release key, only governance protocol_versions/releases/breaches.
No source implementation was edited during this reproduction.

Reflection: source/release equality alone demonstrably permits stale revival.
Current `_view` feeds list/detail/review, so fixing that shared read policy is
preferable to changing individual HTTP routes.

### Contrarian

Checked alternatives and compatibility. Retaining state/disposition plus a derived
epoch denial preserves history better than deleting or rewriting accepted records.
Missing historical epoch must fail closed rather than assume current epoch.
Templates/manual work must not be treated as AI reliance. Global persisted epoch
is conservative across task-scoped suspension and already defines completion
semantics. No schema migration is needed for an added body field.
Release reference digest includes active status, whereas retained release status
can later become revoked: export must preserve both reference-time active snapshot
and current lifecycle status, not compare a revoked snapshot to an active digest.
An image predating these gates cannot be made safe by process refresh; it must
be stopped/drained or denied serving access by an external deployment boundary.

Reflection: full release evidence must retain release-ID lifecycle events,
explicitly flag missing evidence and avoid exporting model input prompts.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/122, retrieved 2026-10-18:
  blockedBy empty; parent #113 is hierarchy, not a dependency. Genuine authority,
  witnessed drill, immutable external Azure head and Azure SQL evidence unmet.
* W2: https://github.com/jmservera/ama/pull/269, retrieved 2026-10-18:
  merged 59236636cc29708301bbcf78c68dba10559cd514; original continuity baseline,
  not evidence that current epoch/export gaps are closed.
* C1: src/core/src/zava_forward/core/assistants.py:600-626 excludes epoch from
  enqueue identity; :648-671 derives actionability without epoch; :524-539 exports
  accepted reliance without epoch. Baseline reproduction above confirms reachability.
* C2: src/core/src/zava_forward/core/assistants.py:762-817 assigns claim_epoch
  only at claim; :831-868 checks completion epoch; :932-936 dispatch checks only
  suspension and release. Pending work can cross a restart before first claim.
* C3: src/core/src/zava_forward/core/continuity.py:236-287 omits assistant_releases
  and legacy top-level release references. :289-325 verifies ledger/head/digest.
* C4: src/core/src/zava_forward/core/assistant_release.py:120-150 retains body
  separately from status and writes lifecycle events keyed by release ID.
  rai_release.py:103-108 supplies ID/version/digest, not full release evidence.
* C5: src/core/src/zava_forward/core/ai_tasks.py:194-262 records epoch for text/
  document completion but :265-288 review checks only active suspension/release.
  store.py:720-726 caches briefing without epoch; :750-813 and :842-862 legacy
  priority lacks epoch lifetime checks.
* C6: src/core/src/zava_forward/core/sqlstore.py:104-140 refreshes on outer lock;
  :247-251 suspension reads SQL. ContinuityMixin.continuity_epoch currently
  reads cached data outside a lock, affecting old-process late-result checks.
* C7: src/api/tests/test_continuity.py:133-154 tests a note, not manual actions,
  and joins suspension before review, not real overlap.

## Findings, Alternatives and Decision State

Accepted: bind new proposal identity to creation epoch, fail closed for missing/
mismatched epoch at all admission/reliance surfaces; preserve dispositions and
permitted output history. Reuse existing transaction boundaries and task release
records. Include retained reference snapshots/current status/lifecycle evidence
and explicit incompleteness in offline bundle.

Rejected: UI-only disabling, deleting old evidence, changing shared SQL adapter,
claiming change register controls serving configuration, and declaring old images
safe merely because current code refreshes persisted state.

Participation: no delegated research was needed for this continuous trace.
Cycle complete; further source search is redundant for the selected bounded fix.

## Risks and Residual Uncertainty

Gate-aware stale processes and images predating the gate are different threats.
No remote cancellation, exactly-once billing or operational acceptance claim.
Registers are not serving configuration control.

## Planning Readiness

Ready for bounded source planning. Research disposition: executed.
All three waves ran in order; evidence IDs map to each question. Actual SQL,
HTTP/manual and image execution belong to implementation validation, not research
claims. Genuine authority, Azure immutable external head and Azure SQL witnessed
drill remain unmet and do not block constructed source correction.
