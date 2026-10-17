<!-- markdownlint-disable-file -->
# RPI Changes: climate-source-evidence-178

## Metadata

Task 178; 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/climate-source-evidence-178-plan.md
Details: .copilot-tracking/details/2026-10-17/climate-source-evidence-178-phase-details.md

## Execution Status

Current P04 rebase-only continuation: implementation Complete; resolution
Review Complete, Conformant for rebase only; parent delivery next, then STOP.
Original P01-P03 completion
below is retained as historical evidence. Original review findings are not
being implemented or re-accepted. Caller explicitly authorizes this topic's
rebase and one lease-push after validation, not a main rewrite or feature work.

## P04-T01: Rebase Resolution and Validation (2026-10-17)

Before implementation: clean status on caller's exact topic/head f4ea754;
PR #371 open/main; fetched main pinned to
4e4a389f53870137a0f0582861766be5983a8f96. gh api user returned id 8036360,
login jmservera; privacy-safe repo-local author/committer email resolved.
Original remote topic head is the exact lease expectation, never bare force.
Owned research/plan/state evidence checkpointed before rebase to keep its
working tree clean.

Executed git rebase 4e4a389f53870137a0f0582861766be5983a8f96.
Index conflict combined #176 replay route with #178 online climate route,
leaving #360 current/historical auth routes and #175 privacy route unchanged.
Log conflict retained complete upstream log then appended original climate
entry. Core README auto-combined #176 provenance/CLI with the existing climate
status paragraph; reviewed without further source edits.
Replayed feature/ledger commits db5d23e/6435ffb; planning checkpoint e2c0a19.
No ambiguous source intent, new feature, production additions or deletions.

| Exact command / check | Observed result |
| --- | --- |
| python3 -m unittest discover -s tools -p 'test_climate_station_bounds.py' -v | PASS, eight methods |
| python3 -m compileall -q tools/climate_station_bounds.py tools/test_climate_station_bounds.py | PASS |
| Exact P01-T01 retained-input invocation, output piped to session replay JSON then cmp against committed JSON | PASS; input d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9; output f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615 |
| From src/core: /tmp/ama-360-rebase-ZSRcWK/bin/python -m ruff check . | PASS, All checks passed |
| From src/core: /tmp/ama-360-rebase-ZSRcWK/bin/python -m ruff format --check . | PASS, 47 files already formatted |
| From src/core: /tmp/ama-360-rebase-ZSRcWK/bin/python -m mypy | PASS, no issues in 100 source files |
| Tool availability | Default Python has no Ruff/mypy; recorded #176 recovery venv absent. Existing #370 rebase environment has Ruff 0.17.1/mypy 2.4.0; reused read-only, no downloads/installs |
| Complete main tree outside original feature paths compared byte-for-byte | PASS, 2,129 files; includes all privacy/determinism/infra/auth source and evidence |
| Feature-only production blobs versus f4ea754 | PASS, helper, tests, derived JSON and full sensor synthesis byte-identical |
| Every main-added nonblank line in the three shared files | PASS; no upstream source/evidence addition lost |
| Complete log-entry identity/order checks against main and f4ea754 | PASS, 267 upstream entries and 266 feature entries exactly once in original stream order; complete main log byte-prefix retained |
| git range-diff 4ca6c73..f4ea754 4e4a389..HEAD | PASS, original feature difference only changed README/log surrounding context; ledger equivalent; tracking checkpoint added |
| Added local links/anchors in the three combination files | PASS, four references |
| git diff --check and git diff --check origin/main...HEAD | PASS |

Validation-command refinement is an immediately relevant environment update,
not a new requirement: run exact existing core CI commands using recorded
available tooling. No tools-wide lint/type target exists; core CI passes do
not claim newly configured climate-tool typing or application acceptance.
Independent numerical derivation is not rerun: output and parser are unchanged,
and exact byte replay verifies retention of the previously reviewed result.
No full app, infra execution, Azure, private/live datasets or deployment checks
needed or run. Original approval/access/RH and candidate-specific gaps remain.

Pre-Review reconciliation: P04 markers checked, details/changes agree; original
P01-P03/critique/review preserved as historical evidence. One bounded resolution
Review next, then parent-owned final evidence commit, one topic-only
force-with-lease push and PR #371 update with Refs #178. No tracking-only
successive pushes or inferred owner/full-issue acceptance.

Parent handoff after resolution Review: execution Complete/outcome Conformant
for P04 only, no new findings; original RV-001/002/003 and human gates retained.
No additional source changes or test rerun is required for tracking-only
closeout. Final commit/remote SHA and PR delivery outcomes will be recorded
externally in PR/coordinator evidence, avoiding a self-referential ledger and
successive tracking-only pushes. This record does not claim a push or PR update
before those actions occur.

Complete, full plan P01-P03 and P01-T01/P02-T01/P03-T01. No remaining active-plan
markers. Canonical edits followed numerical evidence. Approved scope excludes runtime,
stock/infra, downloads, copied provider pages/raw datasets and human approvals.

## Completed Work

### P01-T01: Reproducible temperature evidence

Added local-only standard-library tools/climate_station_bounds.py and
tools/test_climate_station_bounds.py; generated derived-only
docs/reference/research/climate-source-evidence-178.json.
Eight unittest methods passed. Actual Durham invocation from the phase details
passed input SHA guard; 360 calendar months, 351 accepted pairs and nine estimated
exclusions per field. Report SHA-256
f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615.
No RH inferred, no raw file copied into repository, no downloader.

### P02-T01: Canonical comparison and source register

Integrated dated online section into existing sensor synthesis, explicitly
retaining the prior offline section as historical. Compared all named candidates
and owner leads; locked regional HadUK UUID, citation, OGL/access distinction,
actual login response, Durham measured values and original criterion audit.
Updated reference index/log and the directly coupled core README status.
The generator remains unchanged; owner approval UNMET and RH unavailable.

### P03-T01: Evidence reconciliation

Completed validation below; plan markers/details and handoff synchronized.
No issue checkbox changed. Research records region product lock from PC-003.
All four phase artifacts use the stable task identity/date.

## Implementation-Time Plan and Detail Updates

Immediately relevant current-state update: added the core README's existing
climate-status paragraph to P02 targets because its "not retrieved" wording
and offline-only routing became stale after real retrieval. No runtime change,
new requirement or user decision. Plan scope/details/test ownership reconciled;
no new critique needed. CLI also requires explicit source URL to avoid false
attribution when analyzing a different station; exact details command updated.
Critique PC-001/002/003 remain resolved.

## Validation Record

| Command / check | Result |
| --- | --- |
| python3 -m unittest discover -s tools -p 'test_climate_station_bounds.py' -v | PASS: eight test methods, including CLI success/nonzero hash failure, synthetic quality/missing/duplicate/schema/date/empty cases |
| Exact real-record command in details P01-T01 | PASS: 360 present calendar months, 351 valid pairs, nine estimated exclusions per field, zero missing/provisional in window, 1,401 out-of-window rows |
| Independent inline Python Decimal calculation, not importing helper | PASS: every min/max value and all tied month/source-line occurrences; counts and input hash independently checked |
| Helper replay piped to cmp against committed-target JSON | PASS: byte-identical; SHA-256 f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615 |
| python3 -m compileall -q tools/climate_station_bounds.py tools/test_climate_station_bounds.py | PASS |
| Added relative-link/anchor check | PASS: six added local targets/anchors |
| Append-only log byte-prefix and excluded-path git diff check | PASS: original/addendum/memory/regulatory snapshots/core runtime/infra/support unchanged |
| git diff --check | PASS |
| Initial all-history link scan | FAILED on pre-existing docs/reference/log.md link to retired mvp/README.md#entra-id-on-container-apps. Not introduced here; no unrelated repair. Changed-link scan above passed |
| Ruff/mypy | Not run: not installed/on PATH and no tools-wide configured lint/type target; no dependency installs added for this standard-library tool |
| App build/live DB/Azure/model/full-stock checks | Not applicable/not run: no runtime/deployment/generator changes; no delivered application acceptance claimed |

## Pre-Review Reconciliation

Ready: P01-P03 and all tasks checked with evidence; details/changes/handoff
agree. Owner reuse approval and paired-record access remain unmet issue gates,
not uncompleted implementation markers or permission to expand implementation.

## Blockers and Follow-Up Items

Owner reuse/automated-access review, authorized paired RH/temperature packet
and competent geography/cadence interpretation remain outside this delivery.

## Return-to-Caller State

Implementation complete for the bounded full plan; original issue partially
evidenced, not accepted. One post-implementation Review is next, owned by
the active RPI parent. No source changes should be made to close findings in
that same Review; route later work and then commit/push/open PR as requested.
