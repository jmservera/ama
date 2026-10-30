---
title: Admitted demo redeployment changes
ms.date: 2026-10-30
---

## Execution Boundary

Task 8053a799-0279-4f5c-b23b-adea3537291b, demo-sites-redeploy-admitted.
Full plan declared. Research Complete / Ready; one critique Complete / Pass,
zero findings. New child continuation preserves original blocked Review.
Manual full sequence explicitly requested, no automatic follow-up session.
Clean matching branch chore/ops-redeploy-both-sites-1030, no PR lifecycle.
Intake HEAD4cea6c1077e6a6e5b5b652ba8f1666f0fe016c29.
Fetched main unchanged ffd8f35e63b24905b9aeb937dbf2a7fe9968747f.

Owner decision 2026-10-30 08:36Z verbatim:
"Proceed: RG cost 337.19 of 700 is sufficient headroom for this redeploy".
Admission accepted for this redeploy only; no new/broader cost query.
Standing authority through2026-11-15; existing IoT role/in-VNet SQL approved.

## Initial Commands and Results

| Command | Result |
| --- | --- |
| git status --short; git branch --show-current; git log -3 --oneline | Clean matching topic, prior local handoff commits retained |
| gh pr view --json number,state,headRefName,baseRefName | No current PR; explicit head listing resolved lifecycle |
| gh pr list --head chore/ops-redeploy-both-sites-1030 --state all --json number,state,baseRefName | exit0, [] |
| git rev-parse HEAD origin/main; date -u +%FT%TZ | exit0, intake/source pins recorded |
| git fetch origin main --quiet; git rev-parse origin/main | exit0, pinned source unchanged |
| docker image inspect <two retained unique tags> --format <ID and source label> | exit0, both IDs/labels exactly match prior build proof |
| az account show --query '{state:state,id:id}' -o json --only-show-errors | exit0, expected enabled subscription |

Tool file reads/searches recorded in research. A mistaken nonexistent prior
plan.instructions path was corrected to the actual plan.md; a wrong shallow
mssqlstore path was corrected to src/core/src. No source or secret read resulted.

## P01-T01 Active

Fresh execution root:
/home/azureuser/.copilot/session-state/8053a799-0279-4f5c-b23b-adea3537291b/files/redeploy/
Private backups/raw outputs remain external; sanitized command journal/hashes
and proof will be exported. No .env/private dataset/model/secret read intended.
`python3 -m py_compile <root>/ops.py && python3 <root>/ops.py` exit0.
Fresh full private backups match previous final baseline exactly; resident auth
explicitly absent, employee auth unchanged. Existing approved Hub role retained;
no role created. Full raw outputs remain private0600.

`python3 -m py_compile <root>/publish.py && flock -n -E 75
/tmp/ama-rpi-heavy.lock python3 <root>/publish.py` exit0. Lock held over
actual image-save config rehash and publication; both actual config digests and
OCI source labels match original tracked-source build. Retained source archive
hash matches. No rebuild or secret-bearing output recorded.

ACR exception 08:41:37.948Z to08:42:11.596Z,33.648s. VM/32 only with
defaultDeny; publicDisabled restored first, normalized exact owned rule removed,
original export/default policy restored. Fresh full expected-state comparison
before every cleanup mutation; full stable ACR equality passed. Exact owned
Docker credential file removed. Old remote manifests present before/after.
Remote index/platform/config chain and actual config label verified:

| Image | Immutable pushed index digest | Platform digest |
| --- | --- | --- |
| resident | sha256:885014246f83819475af0d4ffaadd898776253fb089cb36b765527b92f52bf93 | sha256:8d666868b9e56cf6a7bcf8eff6dd529dcfefeb6bd4b359ab41a6b0ef4d806b56 |
| employee | sha256:e4fa88041d4f4fedfdd230fa3e3eb5f73a53c89c43bace46e0658dcf30cf9799 | sha256:4971d864e87529fb49cfc4a8a7976bcbb1365d9a31a9e2adaf09b3f847f25032 |

P01 complete. SQL and app phases next, not yet claimed.

## P02-T01: Initial SQL Failure and Safe Diagnostic Amendment

SQL preparation compiled successfully; six table definitions captured from
pinned source without configure/seed. Driver introspection identified query
timeout on Connection, not Cursor, corrected before execution.
`python3 <root>/sql_init.py` exit1 after one execution
job-cutover-test-init-tenr1in. Azure terminal Failed; retained counts-only worker
marker reports AssertionError, committed=false. Transaction rollback ran before
the marker. No app writes occurred. Initial log parser also failed because Azure
wraps embedded JSON without escaping; this is a tooling error, not success.
Read-only recovery from the SAME retained console output found exactly one
failure marker. Job retry restored1 and all eight full definitions equal baseline.

Implementation discovery: exact live schema verification failed before COMMIT;
the error marker lacked a stage. Preserve failed executor/worker/journal hashes.
Amend the active plan to permit one bounded read-only in-VNet schema/count
diagnostic execution, then a corrected write ONLY after a specific safe root
cause and explicit non-commit are established. No ambiguous reapply, ALTER,
data/permission change, broader scope or automatic retry is authorized. This
preserves owner intent and rollback-on-failure, rather than blindly replaying.
SQL acceptance must retain the original failure and enumerate every execution.

Diagnostic start first received explicit HTTP400 validation rejection:
StartJobExecutionTemplate disallows volumes (even empty/null). No execution
created by that request; jobs restored. Removed the service-only volumes field
and issued the one diagnostic execution. TerminalSucceeded, six sensor tables
all absent, independently corroborating rolled-back creation. No rows read.
SESSIONPROPERTY probe returned null and is not treated as default-option proof.
All eight jobs again restored.

Potential root cause: canonical sensor_register optional columns omit NULL,
so connection/database ANSI null defaults can make actual shape nonnullable.
Corrected bounded worker will query session/database options FIRST and refuse
all DDL unless effective implicit nullable=false is proven. Only then set
session ANSI_NULL_DFLT_ON and run canonical DDL. It also reports failure stage
and null-option metadata, and parses Azure's malformed wrapper using the
embedded counts-only JSON marker. This is a guarded corrective execution,
not blind replay; original failed worker/executor/proof retained separately.

Guarded execution job-cutover-test-init-sx1wezt terminalFailed before BEGIN/DDL:
effective nullable=true, disproving the null-default hypothesis. No DDL ran;
jobs restored. Preserve this rejected hypothesis, not a purported fix.
Owned disposable LOCAL SQL Server diagnostic under flock-n reused the existing
image, no dependency install. Canonical DDL and all column predicates pass
locally, zero mismatches; exact owned container and generated credential file
removed. This does not substitute for Azure results.

Further bounded diagnostic amendment: one in-VNet transactional rehearsal of
the exact original worker, with COMMIT replaced by unconditional ROLLBACK and
metadata/failing-line instrumentation, to identify the actual predicate.
No view/schema/data changes may persist. No forward app writes before actual
committed SQL proof. This replaces speculative correction with direct evidence.

Rollback-only rehearsal job-cutover-test-init-quk2ac7 isolated failure_line114:
all expected user columns/types/nullability match, but Azure ledger adds four
hidden generated BIGINT columns to every table. Local nonledger SQL correctly
had no mismatch. Root cause is verifier counting system ledger columns as
application columns, not canonical DDL or null defaults. Rehearsal rolled back;
jobs restored. Correction: compare is_hidden=0 user columns exactly AND separately
require the exact four known ledger-generated columns/types/nullability/
generated_always_type5..8 plus ledger_type2 for every new table. Preserve ledger
behavior, no schema ALTER or ledger disable. This root-cause-corrected write is
now justified by direct safe metadata, not the rejected prior hypothesis.

First ledger-aware attempt job-cutover-test-init-7znxvjx also failed/rolled
back at shape verification: the generated-type code assumption5..8 was wrong.
Rather than repeat cloud speculation, reproduced on an owned disposable local
LEDGER=ON database. Actual hidden/generated flags are transaction7/8 and
sequence9/10. Updated exact checker and executed that SAME generated function
locally against all six tables, including primary keys, column predicates and
ledger_type2: pass. This is the resolving executable root-cause evidence.
All owned local containers/credential files removed, all cloud jobs restored.
Microsoft Learn updatable-ledger documentation fetched2026-10-30 also confirms
the four automatic default columns and ledger database default; no weakening
of ledger is permitted. Prior failed workers/results remain distinct.

## P02-T01: Final Committed SQL Result

Corrected execution job-cutover-test-init-1iytu3x terminalSucceeded, exactly one
replica with retry0, one hash-bound post-COMMIT marker. Worker SHA256
842e0b81f3d01cda6c6d7056ac09c1867df2fdc5769fbece7311eb497b16e30c,
input58004fbdc3f8a5247b2156b632c55f08bb7bdaee542555fa262f7de8c72c7ceb.
Six previously absent sensor tables now exist, each count0; exact user shapes,
PKs, four hidden ledger columns/generated7..10 and ledger_type2 verified.
Resident principal SID/narrow rights verified before/after; exact17-column
projection/count verified under EXECUTE AS with REVERT. View/allowlist counts522,
allowlist aggregate unchanged. No seed, policy/control/data/grant/consent change.
All eight complete job definitions restored, Manual, initializer retry1.
Final source SQL batch hash5dab38a4b536391ca3e462fcc11bd876312bc3677d1cb32fb96fa69741b55c38.
Initial failed and guarded/rehearsal executions remain failures, not relabelled
as success; final success is a distinct bounded corrective execution.

## P02-T02 Active

SQL and registry restoration gates now pass; resident then employee rollout next.
First resident template PATCH accepted. Initial /healthz cold-start curl timed
out exit28 before revision acceptance, not proof of actual startup failure.
No second forward mutation or premature rollback. Resume convergence read-only
against the recorded exact target; transient curl timeouts remain journaled,
and bounded convergence will trigger recovery only on actual startup failure.

Subsequent full-projection aggregate probe (not record reads) established a
coupled view defect: all522 sensors_json values NULL when empty sensor tables
are bound, zero valid JSON arrays. Initial TOP0/count checks pruned this
expression and missed it. Pending own convergence process stopped before ANY
recovery PATCH (journal recovery count0). No second forward revision requested.
Plan amended for minimal SQL empty-history correction plus one actual SQL
regression, preserving built-image pin; source SQL input is separately hashed.
This is rollback of broken view behavior, not a sensor-data or rights change.
Console/system log CLI validation failure (--revision unsupported for system)
was corrected; private logs retained, no app output/secret printed. System
ProbeFailed/ProcessExited2 observed; no clean-start claim. Two ad hoc diagnostic
one-liners failed locally (one Python syntax error, one incorrect active filter);
corrected read-only queries used, no resource mutation from those failures.

Actual local-SQL reproduction failed as expected: sensors_json `(None,)`
instead of `("[]",)`. Minimal canonical SQL change wraps the optional-history
scalar subquery in COALESCE(..., N'[]'); exact matching/filter/order/null-channel
semantics and grants untouched. One regression added to existing SQL boundary
module, normalizing driver Row objects to tuples for assertions. Both selected
modules now pass44 tests on owned disposable SQL Server; zero opt-in skips.
Initial test setup failed because base Python lacked installed core; installed
the distribution into an owned private venv after that actual missing-package
failure. Missing bdist_wheel restored using pinned src/build-requirements.txt;
no dependency manifest change or global environment change. Each owned local
SQL container and generated credential file removed. Infra guide updated only
for evaluated empty-history verification.

Corrective SQL execution will bind the working-tree SQL hash separately from
the retained image/source pin, preserve original committed receipt, and require
all522 projected sensor histories to be valid JSON arrays BEFORE COMMIT under
the actual resident principal. No data rows or credentials returned.

View correction execution job-cutover-test-init-7gj1y4f terminalSucceeded with
bound post-COMMIT marker. All six counts remain0, allowlist/view522, valid sensor
JSON-array count522 under resident identity. SQL source SHA256
625c141707c5bc983c19f81f3c2c7daafc27feb0318896a40af1659d478be939,
batch86747aa207f64341ec341910396b91fc57454bb8c1d58644c4710f7f3860ef70.
Initial corrective invocation stopped on read-only ARM GET timeout124 before
worker generation/start; read-only preflight resumed, not an ambiguous write
retry. Job definitions again restored exactly.

Existing single forward resident revision remained ActivationFailed with
zero replicas after the SQL dependency was repaired. Admit one restart of that
EXACT revision to reset failed activation; no new revision, image/template/
auth/scale change. Read-only convergence remains against the same target.

Restart accepted but zero-replica ActivationFailed state did not reset.
HTTP200 at this point was served by the healthy old fallback revision, so is
explicitly NOT new-revision acceptance. Paused own read-only convergence before
recovery; admit one deactivate/activate cycle for the exact failed owned new
revision to reset activation after repaired dependency. Retain the old healthy
revision and require full protected/traffic/target proof afterward. No new
forward revision, min change or credential operation.

## P02-T02 Complete

Exact resident deactivate/activate reset succeeded. Same original single new
revision res-live-20261030-085634 is now latest=ready Healthy/Provisioned,
active100%, ready replica, expected resident digest. Employee then rolled once
to emp-live-20261030-091952 with identical success criteria. Full protected
app and separate auth comparisons pass; exactly one added revision each,
all prior history retained. No recovery-image PATCH was needed or executed;
view correction plus same-revision reactivation recovered actual startup.
Both minReplicas0. Old digests/history retained. P02 complete.

## P03-T01 Active

Final curl/source-byte and public Playwright receipts next. Authenticated
owner-held resident sign-in and employee Entra journeys remain separate.

## P03-T01 Complete: Final Live Evidence

`git fetch origin main --quiet; python3 -m py_compile <root>/verify.py;
python3 <root>/verify.py` exit0. Main remains original image pin.
Both healthz/public shells200; shells source-byte-equal. Resident shared
JS/CSS, demo.js and assistant.js200/source-byte-equal; /demo/view401.
Employee /app,/app.js,/ops.js,/api/me,shared JS/CSS401. No auth bypass.
Final exact protected app/auth/history/ready-replica readback passes, all four
app minima0, eight full Manual job definitions equal baseline, ACR stable exact
equality, Hub management and approved role IDs preserved.

Real Playwright fresh anonymous context,09:22:06Z-09:22:11Z, both public pages
1365x900 and390x844:200 and no horizontal overflow. Resident shared script1,
runtime object, launcher1 visible, dialog1; password not entered. Employee
public shell has sign-in link; /app reaches login.microsoftonline.com sign-in.
No authenticated/private page or model call. Native public trace32 DOM
snapshots plus four nonempty screenshots retained ignored, modes0600.
Direct raw result provenance: own session tool event
3d0f3a71-73ca-44ef-9e12-5d29fb579a4c, parsed automatically by exporter,
not transcribed DOM literals. Entra OAuth parameters omitted and not traced.
First browser attempt failed before navigation because dynamic imports are
unsupported; retried using native trace/screenshot APIs, not filesystem escape.

Console residuals: initial resident public load reports one resource404
(shared widget assets independently200); employee public page reports blocked
image CSP error at both widths. These are not fixed or relabelled clean.

| Feature | Actual boundary |
| --- | --- |
| Refs #550/#556 shared widget | Resident assets/runtime/launcher/dialog live; authenticated conversation/input/selector/consent/errors owner-run |
| Refs #551/#553 expanded map | New employee image live; Entra sign-in required for marker/header/filter acceptance |
| Refs #552/#554 single-case UX | New image live; Entra sign-in required for icons/steps/blocker/tabs |
| Refs #503 privacy/grounding | No actual model or authenticated privacy acceptance claimed |

## Evidence Export and Review Handoff

Exporter exit0 after correcting an initial schema parser error on non-JSON
apply_patch event arguments. Sanitized evidence JSON contains679 actual child
journal records with unique labels/output hashes and74 completed outer bash
command records recovered from own session, plus direct browser provenance,
executor/source/proof hashes, both SQL commit receipts and failures. Future
administrative closeout commands remain in the durable own-session transcript.
`git diff --check` passes; all five exact browser artifacts confirmed ignored.
44 real-SQL/sensor tests pass,0 skips; pinned Ruff lint/format passes. No .env
or private dataset read, no secret output, no RG deletion or remote write.
Application tests beyond affected SQL boundary are not a new-image acceptance
proxy; retained original builds remain distinct from SQL correction.
Implementation complete, ready for exactly one independent current Review.
