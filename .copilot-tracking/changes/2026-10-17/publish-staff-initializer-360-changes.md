<!-- markdownlint-disable-file -->
# RPI Changes: Publish staff initializer #360

## Metadata

* Task ID: 360
* Task slug: publish-staff-initializer-360
* Date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/publish-staff-initializer-360-plan.md
* Details: .copilot-tracking/details/2026-10-17/publish-staff-initializer-360-phase-details.md

## Execution Status

Complete for full bounded plan; P01/P01-T01/P01-T02 and P02/P02-T01 complete.
No remaining active implementation marker. Approved writes: dated evidence and directly related runbook,
evidence pack/index/log; task-owned local validation scratch/venv.
Production changes are only two removed .dockerignore directory exceptions and
eight existing context-test assertion lines; no runtime code or cloud resource
writes. Real image delivery is blocked.

## Ordered Phase Log

| Phase | Actual execution |
| --- | --- |
| Research | rpi-research first; wider/deeper/contrarian complete inline; Ready for bounded plan, private route blocked |
| Plan | rpi-plan second; one independent critique Revise, PC-001 scratch isolation applied directly; Ready for bounded validation/evidence |
| Implement | rpi-implement third; all bounded markers complete, concrete route blocker retained; no image publication/pin |
| Review | rpi-review fourth; exactly one independent full-task Review Complete, outcome Residual work, no source defects; RV-001 High private image delivery blocker and RV-002 Medium human acceptance routed distinctly |

## Execution Summary

Normal Docker 29.9.0 works with docker group; this supersedes the old socket
blocker. Existing private login 10.40.4.21 and data 10.40.4.20 each time out
at 10 seconds. Public DNS/HTTP403 is not private reachability or an AcrPush
test. No authenticated login, base pull/build, push or pin is authorized over
the public route. No new digest or real image smoke available.

## Implementation-Time Plan and Detail Updates

### Explicit validation scratch and dependency recovery

P01-T01 binds TMPDIR to one exact task-owned path before interpreter startup,
asserts its resolution and performs exact-path cleanup. PC-001 resolved without
a second critique or new authority. Early Plan discovery failed before tests:
ModuleNotFoundError zava_forward. Recover missing dependencies in isolated venv,
not PYTHONPATH=mvp or system installs. Source-only checks cannot prove unavailable
image behavior. No user decision or material scope change required.
P01-T01 local validation refinement permits native scratch/COPY-only context
audit with network disabled, no execution/base pull/cloud access; exact cleanup.
This tests Docker ignore semantics rather than assuming a custom matcher proves
the actual context. It is explicitly not the retained-base proof build.

### Native context discovery and directly coupled packaging correction

P01-T01: First actual scratch/COPY audit transferred 272.43 kB and showed every
infra/scripts file plus generated __pycache__ rather than the claimed file
allowlist. Directory negations !scripts/ and !entra/ reinclude all descendants.
No secret contents inspected or cloud upload; audit container was never started
and exact named container/image were removed. Remove those two directory-wide
exceptions; preserve exact file exceptions, Dockerfile, base and runtime code.
Extend existing BuildContextTests method with unwanted script/.env/pyc/profile/
data exclusions (no new test methods). This is an immediately relevant current
packaging correction permitted by caller, not a new owner decision or critique.
Reconciled plan/details. Final native audit lists exactly seven regular files:
cutover-proof.Dockerfile, entra/app-registration.json, and the five reviewed
Python COPY files. No unrelated scripts, generated pyc, .env or private-profile
files. It is a local scratch/COPY-only audit, not a proof image, has no base,
does not run any code and was never pushed. Exact audit container/image removed
after both audits. BuildKit cached transfer size is not a total context-size
metric; use the exported path list, not its displayed 390 B increment.

### Initial focused/source checks

83 focused tests passed, zero failures/errors/skips. Five source imports passed
with socket connections forbidden; two source --help calls passed in isolated
environment with no private inputs. These precede packaging correction and are
not real image smoke. Final focused rerun after correction: 83 tests, zero
failures/errors/skips. TMPDIR preflight passed. P01-T01 complete.

## Validation Record

| Check | Result | Boundary |
| --- | --- | --- |
| Initial discovery | Failed: zava_forward missing | Before test execution; isolated source dependency restore followed |
| Final focused suite | 83 pass, zero failures/errors/skips | Four named infra modules; source-only |
| Source import/help | Five imports, two --help pass | Network blocked during imports; no worker main |
| Native context audit | Seven exact files after two-line correction | Local scratch/COPY only, no start/base/private build/upload |
| Mutation | Restored original directory exceptions rejected | New exclusion assertion catches unwanted setup script |
| Ruff check/format | Pass for modified test | Exact existing workflow flags; missing Ruff restored in task venv after failure |
| Preservation | Equal job fingerprints; registry restrictions/API deny-all retained | Read-visible metadata only; no secret-payload or historic equivalence claim |
| Cleanup | Exact local audit images/containers and task scratch absent | No shared cleanup |
| Documentation | Seven new local links pass, append-only prefix exact, git diff --check pass | No repository docs build exists |
| Real image smoke/push/digest/pin/idempotency | Blocked/Not run | Existing private-route gate fails |

### P01-T02 sanitized preservation evidence

.copilot-tracking/changes/2026-10-17/publish-staff-initializer-360-live-receipt.json
records actual refs, private DNS/NIC/IP probes, normal Docker and two readbacks.
SHA256 72a8698127f8d85a15fb47c2561e8bf81c615d90ee93f076324bd84fa209e211
matches for identity/configuration/template/environment. No raw values retained.
Final readback at 2026-10-17T16:54:43Z: old proof image/Manual initialize args
unchanged; registry publicDisabled/bypassNone/adminFalse; demo deny-all retained.

### P02-T01 factual documentation and handoff

infra/README.md, docs/architecture/cutover-evidence-pack.md, reference index and
append log distinguish resolved Docker/IAM from current route failure. Exact
conditional future publication commands remain unexecuted, not next actions
permitted on the current public route. All active markers reconciled.

## Pre-Review Reconciliation

Plan/details markers, current summary, completed-work evidence, validation,
blockers and handoff were reconciled before Review for bounded delivered
packaging/evidence work, with live publication/acceptance explicitly blocked.
The one independent Review subsequently completed; no correction loop.

## Review Outcome and Terminal Parent Handoff

.copilot-tracking/reviews/logs/2026-10-17/publish-staff-initializer-360-review.md:
execution Complete, outcome Residual work. No source defect found. RV-001 High
routes actual private build/smoke/push/digest/pin to an existing authorized
private publisher; RV-002 Medium retains human #360 d/e gates. No conformant
overall delivery or runtime acceptance claimed. No code changes after Review.
The automatic task lifecycle is complete, but actual image delivery remains
blocked. Session stopped under explicit caller boundary, not a follow-up choice.
Terminal parent resolves gh api user, configures repository-local privacy-safe
author/committer email and Copilot trailer, commits all actual phase artifacts,
pushes ordinarily, opens main PR Refs #360 and verifies exact remote/PR head.
Publication success is checked externally rather than attempting to embed a
commit's own hash or creating a gratuitous receipt-only commit.

## Blockers

private-acr-route: existing approved private publisher route unavailable here;
no network changes, new roles or builder fallback permitted.

## Remaining Work and Follow-Up Items

No remaining active P01/P02 markers. Later owner/publisher: working existing private route,
real retained-base build/push/digest/package smoke and reviewed image-only pin.
Human tenant/browser/roles/SQL/AI and separately authorized retirement remain;
#360 d/e UNMET. No child work selected; stop after final PR publication.

## Owner-Authorized Main Integration (2026-10-17, PR #381)

Owner explicitly authorized rebase onto latest origin/main after #380 merged.
Old local/origin/PR head and exact push lease:
a606258bdc3b01664fb67c874f19dc0455453c0d.
New base: adedf1f232e567d3a22a623d9c871513fa6b7cdc.
Rebased implementation candidate:
e31a1ae5705287f92729b031fedbc280324afce7.
Only docs/reference/README.md and log.md conflicted. Resolved additively:
both complete index row sets retained; current log begins with the exact
upstream log and retains the entire prior topic append. All 15 other #380
files, including manifests/source/tests/research, are byte-for-byte main.
infra/.dockerignore, test_staff_azure.py and cutover-proof.Dockerfile are exact
a606258; no runtime/source/recipe changes during integration.

Minimal validation only: extracted and executed the unchanged existing
BuildContextTests class using stdlib AST/unittest, one test passed without
importing unrelated dependency-heavy test modules. Native normal-Docker
FROM scratch/COPY-only --network=none --pull=false context audit confirms exact
seven intended files; no container start, private base pull or registry request.
The first audit assertion incorrectly counted Docker-generated runtime files
outside /context; narrowed the harness assertion to copied /context files and
reran successfully. No source fix was needed. Exact named audit container/image
cleaned after each attempt; no task/reviewer environment deleted.
The prior task venv had already been removed before this continuation; disclosed
to final reviewer, not restored or needed for these minimal checks. No full
suite rerun, dependency install or reuse of historical test results as fresh.
Diff checks and exact preservation verification pass.

Independent reviewer 463ad179 is assessing old a606258; that result does not
cover this final integration head. Final exact-head follow-up is required and
will be sent on PR #381 after one privacy-safe integration-record commit and
authorized topic-only --force-with-lease push. No new full RPI/critique/Review
loop or fabricated independent Pass. Ordinary Source projects CI may be
dispatched if final-head checks are absent; paid rubric is not dispatched.
Final head/run verification and reviewer notice occur externally without another
receipt-only commit. Stop after terminal push/handoff, no merge.

No private ACR probe repeated, Azure/resource/role/network change, public-registry
attempt, secret/private-data read or workload execution. Existing private
10.40.4.20/.21 timeout evidence remains the blocker, not an authorization failure.
Image publication/digest/pin and #360 d/e remain unmet.
