<!-- markdownlint-disable-file -->
# RPI Phase Details: setup-profile-evidence-360

## Metadata

* Task ID: issue-360-followup
* Task slug: setup-profile-evidence-360
* Related plan: .copilot-tracking/plans/2026-10-17/setup-profile-evidence-360-plan.md
* Evidence: .copilot-tracking/research/2026-10-17/setup-profile-evidence-360-research.md
* Initial direction: narrow setup classifier; no live setup or cloud writes.
* Blockers: none for offline implementation.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Reproduce and implement | Complete | P01-T01, P01-T02 |
| P02 | Validate and document | Complete | P02-T01, P02-T02 |
| P03 | Review and deliver | Complete; authorized integration published | P03-T01, P03-T02 |
| P04 | Authorized correction ONE | Complete; independent acceptance pending | P04-T01, P04-T02 |

<!-- rpi:phase id=P01 -->
## P01: Reproduce and implement

C2 falsely appends production for arbitrary profile-neutral app staging.
C1 proves actual main has production default; C3 module passes tags instead.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Install distributions and capture failing-first regression

Use an isolated session venv; install editable core/agents/api/orchestrator first.
Run existing setup and staff suites to establish fresh baseline (historical counts
147/143 are not assumed). FakeAzure must model deployment names and raw CLI export
template shape. Regression calls require_demo directly: profile absent on API,
development/test on exact bound environment, successful neutral app stage,
successful module tags and successful explicit main parameters for environment.
Capture failing-first assertion before source changes, not a proxy helper test.

Completion: editable distributions installed in isolated session venv; fresh
baseline 104 setup and 43 staff_azure tests passed (147 total). Staff first
exposed missing cryptography; installed the existing hashed API requirements
then reran successfully. Actual-shape regression failed with original source's
Automatic demo roster refused SetupError (1 test, errors=1) before implementation.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Resolve bound contracts and preserve safety

Use group export -g ama -n exact list-returned name, through existing Azure.call
subscription scoping. Validate template object and parameter-declaration map;
do not use templateLink URLs or current local Bicep for historic defaults.
Recognized deploymentProfile/environmentName must be literal strings; tags must
be object with present recognized keys retaining even nulls for rejection.
Absent undeclared parameters are neutral; declared missing required/default
unresolved/malformed evidence rejects. Check both explicit and default forms,
including default-production alongside tags-development.
Validate all evidence containers and environment readback identity. Do not
change discover(), roster/random/admin behavior, credentials or staff transports.

Completion: narrow resolver and require_demo guards implemented; 117 setup
tests pass including actual shape and read-only fake preview/admin role counts.

<!-- rpi:phase id=P02 -->
## P02: Validate and document

<!-- rpi:task id=P02-T01 -->
### P02-T01: Negative matrix and existing suites

Within at most 18 added methods, cover neutral-only insufficiency; explicit and
omitted production defaults; development default plus required safe environment;
module tags defaults; unknown/null/empty/expressions/wrong-type defaults/values;
denied/malformed export; failed binding; unrelated deployments; environment
contradiction and wrong environment readback ID. Assert only metadata calls and
no Graph/SQL/roster changes on refusal. Run full test_setup_entra and staff_azure;
also complete existing initializer compatibility suites when practical.
Run README's configured ruff scope, plus line-aware checks of changed setup
logic without reformatting legacy files. No Bicep/Docker/SQL/Azure deployment
needed for parser-only change.

Completion: combined 200 tests passed (117 setup, 43 staff_azure, 15 staff
initializer, 17 legacy auth, eight secret lifecycle). Four in-memory unsafe
mutations killed by focused regressions: ignore production default, fabricate
production for neutral patch, hide production behind module tags, accept wrong
environment identity. Configured three-file ruff lint/format passed; changed
setup-line ruff zero new diagnostics, 225 untouched legacy diagnostics retained.
compileall and git diff --check passed. Full repository/Bicep suite not run:
no Bicep/source runtime change; required complete setup/staff suites executed.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Runbook and artifact reconciliation

Update infra/README's exact automatic roster step with export/default semantics,
new read-authority prerequisite, neutral-not-approval caveat and unresolved live
gates. Update existing docs/reference/README route and append log entry.
Record actual test outputs, no full-setup-success claim. Before Review synchronize
plan markers, details completion evidence, changes, divergences and open gates.

Completion: runbook explains actual exports/defaults and read-permission
prerequisite; existing KB index route updated and log entry appended. No
case-study, memory or architecture acceptance rewrite needed.

<!-- rpi:phase id=P03 -->
## P03: One Review and delivery

<!-- rpi:task id=P03-T01 -->
### P03-T01: One Review

Activate rpi-review once. Boundary is this source/test/doc change plus its
evidence; no broader Azure acceptance. Preserve immutable original Review and
route material findings to later work instead of reporting conformant.

Completion: one direct Review executed Complete / Residual work, no source
defects identified. RV-001 routes unmet live credential/publication and genuine
setup acceptance to owner/coordinator follow-up. Not an independent coordinator
Pass. Original review will remain unchanged.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Commit and main PR

Use fresh authenticated account id/login and repository-local noreply author and
committer, required trailer. Push current topic, open main PR Refs #360 (no close
keyword). Wait for relevant checks or report exact pending/failing gates.
Stop with clean pushed head and durable resume state, no merge/rebase/force push.

Completion: ac4b28590d8885b314f81be02c2371398270ccd4 pushed and main PR #391
opened. Authenticated GitHub id/login used fresh for repository-local noreply
author/committer with required Copilot trailer. Clean source head equals remote.
Concurrent main #387 advanced to 3f544fb9; GitHub reports CONFLICTING/DIRTY and
no check runs. Coordinator integration authorization is a follow-up blocker;
no merge/rebase/force push attempted. Delivery receipt commit follows without
source changes or alteration of the original Review.

Integration continuation 2026-10-17: coordinator authorized own topic rebase
and exact expected-old-remote lease. Rebased onto 3f544fb9; only log conflict,
complete upstream prefix and own entry preserved. Source/test binary patch and
original critique/Review byte parity verified; all src equal new base. Fresh
200 tests and existing static checks pass. No new Review, source correction,
main write or live operations. Publication/check receipt is recorded in changes.
Exact-lease push succeeded at 9c0ffe22, PR #391 MERGEABLE; automatic ordinary
Source CI/MVP validation queued without manual dispatch. Final receipt is a
normal fast-forward; exact final-head check outcome is on PR #391.

<!-- rpi:phase id=P04 -->
## P04: Authorized coordinator correction ONE

<!-- rpi:task id=P04-T01 -->
### P04-T01: Failing-first repro and bounded correction

Complete: two independent repro methods failed before source edits (four
invalid export acceptances, one valid mixed-case binding refusal). Anchored
case-insensitive group ARM identity and supported schema/language/resource
envelope validation now implemented. No new dependency or general ARM
interpreter; unsupported nested deployment parameter/default contracts refuse
explicitly. Six new correction methods, original adverse disposition retained.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Validation and same-PR publication

Final combined 206 tests pass in 4.500 seconds; configured lint/format, correction
line lint, syntax and whitespace pass. Original critique/Review hashes match;
append-only log prefix and unchanged src verified. Normal source commit/push
ed29c364f4656e9c091b907c8fced30dba266f03 verified on remote and PR #391.
Fresh gh api user supplied repository-local noreply author and committer;
required coauthor trailer retained. Final receipt is a normal fast-forward.
Original critique/Review must remain byte-identical. Separate disposition:
.copilot-tracking/changes/2026-10-17/setup-profile-evidence-360-correction-one.md.
No new full Review, self-Pass, merge, issue closure or live setup. Fresh main
22670277 recorded read-only; no additional rebase authorized.
PR #391 now CONFLICTING; no exact corrected-head checks appeared automatically.
Read ordinary src-ci/mvp-validation triggers and downstream infra-plan/
src-deploy gates: dispatch validation only, no rubric/deployment. Final-head
dispatch/result belongs in PR handoff; absence/pending never treated as green.
