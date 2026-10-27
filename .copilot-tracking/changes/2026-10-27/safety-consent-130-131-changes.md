<!-- markdownlint-disable-file -->
# RPI Changes: Safety-consent intake

## Metadata

Task ID: 130-131. Implementation date: 2026-10-27.
Plan: .copilot-tracking/plans/2026-10-27/safety-consent-130-131-plan.md.
Details: .copilot-tracking/details/2026-10-27/safety-consent-130-131-phase-details.md.

## Execution Status

In progress. Declared scope: full bounded plan, not full issue acceptance.
Completed: P01, P01-T01, P01-T02 and P02-T01 local validation/documentation.
Remaining: independent Review and P02/P02-T01 final publication evidence.
Write boundary: resident core/API tests, core ledger/projection and component
READMEs plus dated evidence. No web, new assistant, SQL schema or Azure changes.

## Implementation-Time Plan and Detail Updates

Single critique Complete / Revise preserved. PC-001..004 directly dispositioned:
case-wide unresolved hold, correctable unverified subject, replay/projection
assertions and separate non-sensitive hold surviving existing deletion.
No new operational retention or legal authority assumed.

## Completed Work

### P01-T01: Nomination/correction

resident_decisions adds closed staff intake and correction actions in the
existing transaction/API; exact source account and subject reference preserved.
Source text limits reject truncation. All five staff-recorded channels retain
acknowledgement evidence/owner/manual route/update. Corrections can link an
existing same-case challenge while preserving its prior decision and outcome.
No priority, support, consent, representative authority or hazard clock changes.
Hazard-marked intake is refused to the existing independent route, not
automatically forwarded. This distinction leaves full immediate-routing
acceptance unproven. No nomination eligibility/reviewer decision is implemented.

### P01-T02: Unverified tenure/hold

Reports are case-versioned and append-only, with household/tenure/lease source
and named follow-up. Every reported identity remains unresolved; verification,
decision route, Legal and cost stay Unknown. Registered cases get a case-wide
hold in resident_gate and scope_record. No release action or authority exists.
Static responsibility questions are not a reviewed-record responsibility pack.
Evidence fields join existing synthetic deletion; non-sensitive boolean hold
persists. projection and Store.detail explicitly deny raw intake using current
registered dual evidence rights, including stale cached sessions.

## Validation Record

System interpreter lacked installed distributions/dev tools; pip installed
editable core/agents/api and existing dev tools into a task-owned external venv.

| Check | Result | Boundary |
| --- | --- | --- |
| Core resident suite | 196 run, OK, 73 skipped | JSON/SQLite pass; opt-in SQL Server not run |
| Changed intake selectors after link/prompt assertions | 24 run, OK, 9 skipped | 15 JSON/SQLite checks; 9 SQL Server skips |
| Resident API suite | 16 run, OK, 1 skipped | Loopback synthetic API; law checks explicitly Unknown |
| Focused Ruff | Passed | Touched production/tests; tests formatter applied |
| Focused mypy | Passed (4 core files, 1 API test file) | Initial callback-inference failures corrected with typed-compatible partials |
| git diff --check | Passed | No whitespace errors |
| Required full API discovery | 1124 run, OK, 314 skipped | External log in task session files; no cloud |

Final required API discovery completed: 1124 tests in 625.226s, OK,
314 skipped. Final combined core resident/hazard/consultation/procurement:
373 tests in 95.288s, OK, 87 skipped. Skips are retained opt-in boundaries,
not passing SQL Server/browser/human evidence. No test failure occurred;
synthetic fault-injection logging and absent-law-store Unknown messages are
expected in these suites.

Reproducible commands (task-owned venv activated):

```bash
cd src/core
PYTHONPATH=tests python3 -m unittest test_resident_decisions test_hazard_referral test_consultation_controls test_quality_procurement -q
mypy src/zava_forward/core/resident_decisions.py src/zava_forward/core/store.py src/zava_forward/core/projection.py tests/test_resident_decisions.py
cd ../api
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q
mypy tests/test_resident_api.py
```

Final focused Ruff and test formatting checks passed; git diff --check passed.
Documentation reviewed against actual input shapes, unknown states and
relative component links. No KB synthesis or current legal claim added.

Twelve test methods added: 6 shared JSON/SQLite, 3 SQL-writer cases, 3 API;
no test removed. Canaries prove denied detail/mutation reads, CSV and each
existing assistant capture omit intake. SQL writer revocation and competing
revision assertions prove rollback and one durable success event; forced
postcommit acknowledgement failure retains truthful committed outcome.
No --all. No heavy --changed planned for this bounded slice.

## Blockers

Actual OD-41/42, Legal owner/delegation, household verification and real-data
retention/processing approval block operational extensions and whole-issue
acceptance. Independent synthetic intake proceeds; no human approval is ticked.

## Pre-Review Reconciliation

Ready for one independent source Review of bounded implementation, not
whole-issue or operational acceptance. Plan/details and bounded criteria
reflect completed P01; validation is complete. P02 publication checkbox remains
open until draft PR exists. Human blockers and excluded issue criteria remain
explicit. No production source changes planned after Review.

## Independent Review and Publication Disposition

Exactly one Review executed: Complete / Residual work. Canonical record:
.copilot-tracking/reviews/logs/2026-10-27/safety-consent-130-131-review.md.
No material bounded-source defect found. RV-001 and RV-002 are distinct
human-owned nomination and tenure/privacy follow-ups, not closed criteria.
No source correction or second Review follows.

RV-003 publication continuation: the user's explicit task-specific instruction
prohibits --all and explicitly authorizes topic push and one draft PR. It
controls over the generic repository gate wording; src/README.md also states
small bounded issues use planned focused tests. No gate or receipt is invented.
This is a 136-line bounded domain intake addition (not a complete feature,
schema migration, release or operational deployment); no heavy --changed
invocation is warranted or authorized by the large-change condition.
Publish draft-only with the verified local evidence and complete unproven
criterion matrix; do not imply hosted/human approval or full-tier gate readiness.
The original Review finding and outcome remain unchanged.

Publication remains pending; P02 stays unchecked until the actual draft exists.
