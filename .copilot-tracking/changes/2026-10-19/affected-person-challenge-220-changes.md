<!-- markdownlint-disable-file -->
# RPI Changes: affected-person challenge

## Metadata

* Task ID: 220
* Task slug: affected-person-challenge-220
* Implementation date: 2026-10-19
* Plan: .copilot-tracking/plans/2026-10-19/affected-person-challenge-220-plan.md
* Details: .copilot-tracking/details/2026-10-19/affected-person-challenge-220-phase-details.md
* Original critique: .copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md

## Execution Status

P01-P03 complete; original implementation Review executed Partial / Not accepted.
Frozen-head gate pending at this committed evidence snapshot.
Original critique executed once with Revise and seven planner-owned dispositions;
original unchanged.
Approved writes: existing core/API/workbench/test owners, one browser harness,
related component docs and KB index/log, dated issue tracking. No remote writes.

## Execution Summary

Implement the bounded retained-priority supplied-challenge path. First run
actual failing-before behavior tests, then implement identity/version/dependency
controls, browser and docs; original Review precedes frozen commit/full gate.

## Completed Work

### P01-T01: Actual missing-feature proof

Initially added core and two HTTP methods in existing
test owners. Before production changes, actual workflow-only generation/review
succeeded; core challenge tests failed at missing `challenge_targets` and
`source_versions`. First combined command also exposed an existing test import
path need (`tests.test_mvp`); corrected runner PYTHONPATH to include src/api.
Reexecuted HTTP case reached actual loopback login/GET and failed specifically
on missing `challenge_targets`, not fixture setup. Outputs:
/tmp/ama-220-failing-first.log and /tmp/ama-220-failing-http.log. No real AI call.

### P02: Version binding, selective invalidation and existing workbench

New priority creation captures hashes of the original audience-filtered source
labels before generation. Reused existing hashing helper and resident operation,
current registry identities, writer-time replay and committed acknowledgement
contract. Added exact proposal/source/policy dependencies and separate observed
human-decision token. Current dual-entitled owner records supplied opening and
one immutable terminal resolution. No automatic correction of source/policy,
redress, resident choice or human disposition.

Views derive matching stale proposal/review sets, preserve historical statuses
and disable reliance. SQL accept/edit rechecks current corrections inside the
writer, including cross-case policy causes; reject/manual work remains.
Projection explicitly strips both fields without resident AND reason rights.
Metadata-only audit and continuity stale metadata never copy raw challenge text.

Added native Fluent-aligned panel with labelled fields, focused live validation,
busy state, manual/safety wording and cancellable correction. Unsaved actual DOM
drafts retain old target tokens across unrelated refreshes and route warnings.
No CSS/framework/workflow changes.

### P03: Actual checks and durable documentation

Final additions: ten core methods (seven JSON inherited by SQLite, three SQL
writer interleave methods), two HTTP methods and one actual browser harness;
no test removals. Tests create workflow-only priority drafts and actual accepted/
edited human reviews, exact independently expected dependency sets and negative
state comparisons. Emergency hazard intake still succeeds after correction.
Existing core/API guides, resident journey synthesis, index and append-only log
describe the bounded contract and remaining gaps. Memory remains unchanged.

## Implementation-Time Plan and Detail Updates

Original critique PC-001..007 incorporated before source work: writer-time
acceptance fence, original source capture, terminal resolution, explicit
dual-entitlement projection, non-vacuous manifest, honest SQLite/native SQL
scope and conditional gate prerequisites. No divergent user decision needed.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Development import | system Python | Failed, missing dependency | ModuleNotFoundError: zava_forward; permits isolated pip installation |
| Failing-first behavior | core and actual HTTP before production edit | Failed as expected | external failing-first/http logs; missing catalog/hash, not mock-only acceptance |
| Focused behavior | JSON/SQLite and real HTTP | 19 passed, no skips | /tmp/ama-220-focused.log |
| Surrounding regression | resident identity, priority, AI tasks, continuity/export | 238 discovered, OK; 38 existing opt-in skips | /tmp/ama-220-regression.log; no native SQL claim |
| Static | complete core/API Ruff, format, strict mypy; changed JS syntax | Passed; 128/62 Python sources | /tmp/ama-220-static.log; node --check app.js/panels.js |
| Browser | actual SQLite app, Chromium 156.0.8078.4 | Passed | /tmp/ama-220-browser-results.json; four scoped axe 4.10.3 scans, zero violations/incomplete |
| Manual/qualified | screen reader, resident comprehension, legal/RAI | Not run | owner acceptance required |
| Original independent Review | full retained-priority candidate | Partial / Not accepted | original review logs/2026-10-19/affected-person-challenge-220-review.md |
| Full 17-group | frozen exact HEAD | Pending at freeze | requires this source/evidence commit; authoritative final result external only |

Intermediate evidence is preserved here rather than rewritten as clean first
attempts: browser initially waited for hidden native-details text, then for a
staff-only heading on the contractor route. Harness corrected to expand the
actual disclosure and use the actual contractor heading; rerun passed. Expanded
forms were then included in axe/reflow checks rather than claiming closed-form
coverage. Strict mypy initially found three new test-typing defects; fixed with
typed dict copy/callback and an actual SqlStore guard, no exemptions. Added
hazard proof first expected the supplied timezone string; existing hazard
contract correctly normalizes the instant to 2026-01-01T09:00+00:00. Corrected
only that oracle; final 19-case run passed. Rule checks honestly log Unknown
because the test fixture has no law store; no legal-rule acceptance inferred.

Full web guidelines successfully retrieved before implementation and freshly
retrieved in full again before Review. Repo Fluent 2/plain language/native
semantics take precedence over generic title-case/curly-quote preferences.
No screen-reader, whole-page WCAG or human conformance claim.

## Pre-Review Reconciliation

Ready for one original independent Review. P01-P03 markers/details agree with
implemented source and actual evidence. P04 original Review/freeze/gate remains
pending, not checked prematurely. Other assistant/form and qualified acceptance
are explicitly later work, not hidden partial implementation.

## Blockers

No local product-policy blocker. Missing development distributions restored
using pip-only /tmp/ama-220-dev after actual import failure. Publication and
whole-issue acceptance remain gated by exact-head checks, coordinator review
and owner-qualified/resident acceptance. No private app data was read.

## Remaining Work

P04-T01: frozen commit and actual full external gate; original Review has run.
Post-freeze receipt verification and handoff remain external so no later commit
invalidates exact-head evidence. Passing that gate cannot resolve RV-001 or
rewrite Partial / Not accepted.

## Follow-Up Items

Other assistant/form integration and qualified human/legal/RAI/resident acceptance
remain outside the bounded slice. No claim of whole-system AC-071 or live AI.

## Return-to-Caller State

Automatic RPI task completed its one original Review; session remains running
at Follow-up with no selected child. Parent finishes the explicitly requested
freeze/gate/handoff, not a new implementation or repeat Review.

## Original Review Handoff (2026-10-19)

Independent general-purpose reviewer activated rpi-review, retrieved fresh full
web guidelines, read actual artifacts/source and live issue, ran JS/whitespace
checks and reproduced historical reachability with actual panel code in Node.
Original execution Partial; outcome Not accepted. Immutable review path:
.copilot-tracking/reviews/logs/2026-10-19/affected-person-challenge-220-review.md.
SHA256: eec22d64aea801d63ae007c5c8b6e4b69709099d70f4e3a7c9b8f4dc2744fc8e.
Original critique SHA256:
1a37cbb8f57d8e673eac17d86b81b983ec6244a09eb104d7c157109ac16ffaf0.

| Finding | Severity | Unresolved disposition |
| --- | --- | --- |
| RV-001 | Medium | Actual last-50 UI cutoff hides older retained targets and open resolution actions; later rpi-implement, no repair/re-Review now |
| RV-002 | Medium | Independent executor could not inspect temporary-path raw logs; eligible coordinator/evidence verification follow-up, original Partial preserved |
| RV-003 | Medium | Separate assistant/form dependency integration; product-owned distinct follow-up, whole-system AC-071 unmet |
| RV-004 | Medium | Qualified/live/native-specific/human accessibility acceptance unperformed; named owner/exercise follow-up |

Parent directly observed and retained the actual test/browser/static outputs;
that is not a claim of the reviewer's independent log inspection. Coordinator
must receive original adverse findings plus external evidence, perform an
independent exact-head assessment before any future publication, and flag owner
qualified/resident review needs. Tenant setup remains separately interactive.
No source fix, second critique, second Review or issue checkbox change follows
the original adverse Review in this task.

## Selected Finding Continuation (2026-10-19)

Current user/coordinator direction selects RV-001/RV-002 for later ordinary
implementation in the same worktree and stable identity. This explicitly
supersedes the historical no-fix routing above, not the original Review.
P05 is active: failing-before actual historical-browser action, bounded history
correction, focused fresh evidence in the permitted session review bundle,
bounded independent finding disposition, then corrected freeze/all17 gate.
No original critique/Review change, repeated Review, content-exclusion bypass,
issue360 operator edits or source publication is authorized.

### P05-T01: Actual historical action correction

Extended the existing browser owner with `--history`; actual HTTP records and
workflow-only targets expose the former missing Older suggestions control at
52 records before production edits. The new history controls render at most 50
records with older/newer access, URL-bound reload and focused status. Exact
reference entry accepts any retained authorized target; suggestions come from
the visible bounded page. The opener retains its draft/binding across target
paging; leaving an unsaved resolution page asks first. Core authority, version
binding, manual/hazard and selective invalidation implementations are unchanged.

Final actual browser proof: 52 targets, new CH-53 against oldest target, terminal
CH-1 correction and CH-2 historical resolution visible; only the independently
expected oldest proposal is stale and its original review is byte-identical.
Invalid typed reference does not write; three denied role projections remain
stripped. Actual negative-state comparisons preserve decisions/service/hazards.
Original small browser flow also passes. Seven combined pinned axe 4.10.3 scoped
scans report zero violations/incomplete, not full accessibility acceptance.
Fresh focused core/HTTP: 19 OK, no skips; API Ruff/format/mypy 62 sources and
changed JS syntax/whitespace pass.

Fresh permitted substantive evidence is retained at
`/home/azureuser/.copilot/session-state/bc713866-d9c3-479b-acc9-bb5780f2ebcd/files/issue220-evidence/`.
It includes manifest, failing-before log, final core/HTTP/browser/static outputs,
browser JSON scans and SHA256 bindings. No excluded historical log was copied
or reconstructed; original reviewer's historical access gap is not rewritten.
The initial new fixture used a nonexistent recommendations attribute; corrected
to actual data collection before meaningful failing-before proof. Subsequent
locator ambiguity between summary/submit was retained in history-after.log,
fixed with the existing first-match disclosure pattern and rerun successfully.
No product failure is hidden as a successful initial run.

### P05-T02: Bounded independent history/evidence disposition

Independent assessor inspected actual three-file correction, fresh permitted
raw outputs/JSON and source/result hashes. Disposition: RV-001 corrected within
the retained-priority boundary; RV-002 fresh primary evidence accessible, with
original historical exclusion limits preserved. No introduced defect found.
Report: reviews/finding-dispositions/2026-10-19/affected-person-challenge-220-findings.md.
This is not a repeat original Review or publication/whole-issue approval.

### P05-T04: Directly coupled full-gate regression

The coordinator added the historical all17 outcome to the same directive:
16 passed, project-api failed with nine TaskReleaseRecord identity errors.
Before another expensive gate, actual fresh API reproduction ran 16 existing
TaskReleaseRecord tests and reproduced all nine errors. The new guard correctly
rejects a fixture that changes a registered actor's code to an unrelated
original case owner's code. Correct the fixture's synthetic case ownership
instead; production current-identity and release guards remain byte-unchanged.
Added a JSON/SQLite forged-field/action no-write regression with a valid
registered rejection positive control. Fresh combined release/challenge run
and narrow independent identity disposition are pending. The historical failed
receipt is immutable and never presented as passing.

### P05-T04 completion and corrected freeze readiness

Combined fresh actual `test_assistant_release` plus JSON/SQLite resident and
HTTP resident suites: 139 tests, 137 pass, two explicit skips (SQLite JSON
file rollback only; existing opt-in local browser commitment/reassignment).
All 17 TaskReleaseRecord methods pass. No existing assertions were removed;
template acceptance/edit/rejection and revoked/changed-release denials remain.
Independent narrow identity disposition inspects source/primary evidence and
finds fixture correction justified, with no production authorization weakening:
reviews/finding-dispositions/2026-10-19/affected-person-challenge-220-identity-findings.md.
Production core files are unchanged from the original candidate.

P05-T01/T02/T04 complete. Current scope is ready to freeze, not accepted as a
whole issue. Both bounded reports preserve original Partial / Not accepted
Review and Revise critique. Original historical gate's 16-pass/one-failure
outcome remains failed; no receipt is reused. P05-T03 all17/verification/handoff
must follow the corrected commit. Current fetched/reviewed base is unchanged
eeb6c3aba5d07244ae3cc0e53d839617fd928e3b. Final results/state/receipt and exact
commit/base hashes will be external, with no subsequent commit or publication.

P05-T01 checked; P05-T02 independent bounded assessment and P05-T03 corrected
freeze/full gate remain. Original Review/critique hashes still match the
immutable values above; no second Review or critique was run.
