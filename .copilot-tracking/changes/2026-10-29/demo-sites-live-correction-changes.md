---
title: Demo sites live correction changes
description: Sanitized command results for the owner-authorized live continuation
ms.date: 2026-10-29
---

## Boundary and Intake

Task 5a7ca259-9fe8-407c-accf-fc965757c10e; full plan.
Research executed Ready; one independent critique Complete / Revise, all five
findings applied directly in details. Original parent artifacts preserved.
Current owner authorizes az, superseding historical no-az instruction.
No gh, push, .env, secret-value operations, private dataset, auth smoke or
cost query. No source changes and no repeated local validation.

## P01-T01: Backups

Full raw management backups captured privately under
/home/azureuser/.copilot/session-state/5a7ca259-9fe8-407c-accf-fc965757c10e/files/.
Full app GET/auth/all revisions for each app, all eight complete Manual jobs,
and ACR. Files0600. No listSecrets or vault data-plane read.

| App | Before revision | Before digest |
| --- | --- | --- |
| ca-resident-demo | ca-resident-demo--rollback-20261029-073718 | sha256:fab6a85318f65db006bc610f3b3aff8ae799046d1b9a1813662b3b315c1b6fc7 |
| ca-cutover-test-demo-api | ca-cutover-test-demo-api--emp-main-20261029-072248 | sha256:41db94689ae934e3daa6c7f8fb57d8de5cc58a53995efd50217189231ac1f0c1 |

Resident10 env/2 secretrefs, min0/max1; employee30 env/min0/max4.
Init retry1/timeout600/Manual parallelism1/completion1. Temporarily suppress
retry for the single SQL execution then restore exact job configuration.

## Command Results Before Implementation

| Operation | Result |
| --- | --- |
| git status/branch/log/remote | exit0; only owner-named uncommitted parent evidence; continuing topic ops/sites-redeploy-20261029b |
| git fetch origin main / rev-parse | exit0; main77c87e0d76b827544fde9b2f2ce7dfbd9d879232 |
| #543 stat/docs, #521 exact diff/runbook | exit0; January commit unmerged; parent local evidence reusable |
| az account show | exit0; expected subscription Enabled |
| az app/job/ACR inventory | exit0; named apps, eight Manual jobs, ACR public Disabled |
| initial resident auth-current GET and unsupported collection GET | exit1 AuthConfigNotFound; explicit absence, no mutation |
| corrected full backup sequence | exit0; resident auth explicitly absent, employee auth captured |
| initializer config and job start help | exit0; execution template override supported, retry1 identified |
| independent critique | Complete / Revise; PC-001..005 applied, original preserved |

Subprocess journal commands.jsonl stores every live helper command timestamp,
argv, exit and output hashes externally; sanitized export will be committed.
Read tools and source inspection returned the named evidence without private
data access. Full publication gate, human acceptance and push remain unperformed.

## P01-T02 and P02/P03

SQL view committed by execution job-cutover-test-init-h6mm4i9, Succeeded.
Before16 columns, after17 including documents_json. Allowlist522/view522,
unchanged allowlist aggregate, exact resident SID/narrow rights and effective
principal projection verified within transaction. No row or secret output.
All eight complete job configurations equal backups after restoration, all
Manual, initializer retry1 restored.

Original tooling failures preserved: first PATCH accepted an empty202 response,
JSON decoder failed, immediate restore conflicted with provisioning. Read-only
inspection then exact restore succeeded before any job start. CLI start argument
parsing rejected -c locally (exit2); no execution. Correct REST execution template
started exactly one worker. Its committed result was initially missed because
Azure wraps unescaped nested JSON in Log with an F prefix. Recovered the inner
JSON read-only from captured logs; no SQL reapply or second execution.

## P02-T01: Images and ACR

Both images built locally from the immutable fetched-main tracked src archive,
then published to ACR through the previously approved VM-only route. These
are NOT hosted ACR Tasks builds. Main
77c87e0d76b827544fde9b2f2ce7dfbd9d879232; src tree
22af89af213f65d89011ea264f4f653de35dbeac; archive SHA256
eca35aaab6c6921c0fc898b8d36d17f61ae50a168f2c32ef6ca1ea1b58b2fe4a.
Nonblocking shared heavy admission succeeded; no tests repeated.

| App | Index/deployment digest | Platform manifest | Config digest |
| --- | --- | --- | --- |
| Resident | sha256:3ab5febcc40429fd709940b272fc58ab33ff14190494e45c87eb55f307491086 | sha256:2789f0ec74cbbb64939dcad55907dd6062da8e78802edf8fa8deab8c7a7e6746 | sha256:81ec6192fb7843145269a4043baaf2c4331791321e09782c31dfa8d440b16efd |
| Employee | sha256:5215e019a78a8c7ae07987dcd26dbcabbe87eb4b5ecf2077688f7a9ca5f9034e | sha256:023b10a7c6a8dd334bd568fa082d8a29852ac792ade5d43138b23bc3c02b90f8 | sha256:6a81e24720ebaf0edade4cf4e51605f20e92dc942e10a1316786dea93ca5d015 |

Remote manifest body hashes, local RepoDigests, actual docker-save config bytes,
remote config digests and exact source labels agree. Both old live digests
verified present before/after; no tag/image deletion or old-tag overwrite.

ACR exception 10:20:14.786348Z to10:20:58.956781Z,44.170433s including
exact restoration proof. Public closed first. Initial removal using /32 returned
exit0 but left Azure-normalized bare-IP rule; strict equality caught it before
app writes. Removed only that exact returned rule while public Disabled,
then complete stable ACR response equality passed. No policy timestamps excluded.
Owned Docker credential file/directory removed. No tokens printed or persisted.

## P02-T02: Successful Resident-Then-Employee Deployment

| App | Before revision | After revision | After digest |
| --- | --- | --- | --- |
| Resident | ca-resident-demo--rollback-20261029-073718 | ca-resident-demo--res-live-20261029-102142 | sha256:3ab5febcc40429fd709940b272fc58ab33ff14190494e45c87eb55f307491086 |
| Employee | ca-cutover-test-demo-api--emp-main-20261029-072248 | ca-cutover-test-demo-api--emp-live-20261029-102306 | sha256:5215e019a78a8c7ae07987dcd26dbcabbe87eb4b5ecf2077688f7a9ca5f9034e |

Both latest=ready, Healthy/Provisioned, active100%, one ready replica each.
Exactly one added revision each, none removed. Resident rollback retained.
Full protected raw app equality, separate auth equality and exact job equality
passed. Every env entry/value/secretref, identity, registry, ingress and
min0/max1 resident / min0/max4 employee unchanged. Only image/suffix differ.

Resident became healthy on the first forward revision. A local assertion
selected two resident index.html source candidates; corrected to the exact
resident_demo/web/index.html and resumed READ-ONLY verification of the same
revision. No second update, runtime failure or rollback occurred.
Employee deployed only after resident's complete acceptance.

| App | Anonymous path | HTTP | Meaning |
| --- | --- | --- | --- |
| Resident | /health | 404 | No such route; recorded as requested, not claimed200 |
| Resident | /healthz | 200 | Actual health route, target revision independently Healthy |
| Resident | / | 200 | Byte-equal current-main static synthetic sign-in shell |
| Employee | /health | 401 | Protected/nonpublic path, not claimed200 |
| Employee | /healthz | 200 | Actual health route, target revision independently Healthy |
| Employee | / | 200 | Byte-equal current-main public welcome shell |
| Employee | /app, /app.js, /ops.js | 401 each | Anonymous denial preserved |

Both console/system log retrievals exit0, no bounded startup-error marker
matches; system streams contain ContainerStarted. Bounded logs do not establish
exhaustive error absence. No authenticated smoke, chat/model call or real sign-in.
Local employee-chat regression/browser evidence is reused from the parent.

## P03-T01: January Authority Parked After Both Healthy

No authority, credential or SQL-row rotation performed. Exact #521 commit
edd7f4dedd4b602a55bf2bc651c81b1b85521aed is not in deployed main.
Its packaged policy changes to exclusive2027-02-01T00:00:00Z; current image
cap is December and configured expiry remains unchanged. January settings
would fail closed and need another resident revision, outside this allowance.

Owner/coordinator must:

1. Integrate/review #521 into main, reconcile its original Review and runtime
   evidence, then separately authorize the necessary resident revision/config
   refresh beyond this task's now-used single forward revision.
2. Supply owner-held password-manager replacement password privately, generate
   verifier and fresh signing key without exposing values, and use a separately
   reviewed exact-version Modify write for existing secret names. The current
   helper permits Create only; do not weaken it or add roles.
3. Identify individually approved existing synthetic SQL row IDs/provenance/
   windows. Through the existing private init job apply #521's transactional
   WITH CHECK constraint migration, then renew only those rows, preserving
   revocations/provenance. Managed-identity SQL authentication has no password
   rotation. No mass update, admission inference or broader SELECT.
4. Record secret expiry/7-day alerts,30-day rotation, bounded prior-version
   rollback interval, versionless-reference refresh (up to30min), narrow SID/
   rights checks and owner-performed sign-in/cross-case/logout/1800s session
   acceptance. Operator must not receive the password or perform live login.
5. Record January funding/all-in USD700 headroom and delayed commitments as
   required by #521 before paid extension. No cost query performed here.

This parking is the owner's expressly permitted outcome when a safe secret
operation or prerequisite is unavailable, not completion of #521.

## Pre-Review Reconciliation and Remaining Gates

Final read-only full app/auth/job/ACR comparisons passed; both target revision
pointers still latest=ready. Final git fetch/main SHA unchanged, source/infra/
canonical docs diff exit0, git diff --check exit0. No repeated test suites.
Original parent artifacts are preserved byte-for-byte, including their prior
Review outcome/state; this child supersedes the operational no-az blocker only.
P01/P02 and P03-T01 complete; P03-T02 Review and local commit pending.

Research/plan/implement executed in order, single critique retained, ready for
one original independent Review of this new live boundary. No future failure-
path correctness claim is inferred from this successful execution.
January authority remains unmet; exact parking accepted, not issue completion.
Complete publication gate, exact-head assessment, hosted/human approval and
push remain coordinator responsibilities. No receipt fabricated.

Supplemental terminal commands outside the helper: initial git/source/Azure
inspection returned0 except expected #521 negative ancestry1; installed CLI
schema lookup returned0 except two grep selectors returned1/no match; all
read tools completed or explicitly reported oversized/not-found as reflected
in the parent evidence. Build wrapper exit0; SQL wrappers returned1 for the
documented parsing errors and no ambiguous SQL retry; push wrapper returned1
on exact-restoration assertion, corrected cleanup wrapper exit0; first
resident wrapper returned1 on asset selector after runtime success, read-only
resident continuation/employee wrapper exit0. Final comparison/fetch/diff
wrapper exit0. No failed wrapper is silently relabelled successful.


## Original Independent Review

One original independent child Review executed Complete, outcome Residual work,
two Low evidence findings; no material live-delivery defect. Reviewer independently
compared retained raw app/auth/jobs/ACR projections, histories/replicas, HTTP bytes,
SQL worker/batch/archive/source hashes and189 journal entries without new cloud
operations or repeated tests. Original Review retained unchanged.

RV-001: four historical log streams overwritten by repeated labels, matching
the export's disclosed false retention flags. Route later evidence-tooling work
to invocation-unique append-only filenames; never fabricate lost bytes.
RV-002: prior16-column view names were recorded but no prior definition fingerprint
was captured. New batch hash is not old-definition evidence. Preserve this
permanent limitation; later SQL evidence work must capture it before any future
authorized change, not query the changed view and mislabel it historical.
Neither finding triggers reimplementation, SQL reapply or another Review here.

All reviewer read-only validation scripts completed successfully with the two
explicit historical limitations; repository source remained unchanged.
Local evidence commit follows Review, using existing historical authenticated
noreply identity because gh is prohibited. Original parent artifacts are
included as explicitly requested, without modifying their historical content.

## Local Persistence and Final Task Status

`git config --local user.email` used the existing historical authenticated
8036360+jmservera noreply identity, no global change and no forbidden gh call.
`git diff --check`, explicit16-file `git add`, `git diff --cached --check`,
`git diff --cached --stat`, local `git commit`, identity/trailer inspection and
`git status --short` all exit0. Evidence commit
11f58b9064046d5ced32778dfe8e81e3c3f73543 contains preserved original/new
evidence; both author/committer use the privacy-safe identity and exact
Copilot coauthor trailer. No closing keywords or push. Worktree clean after
that commit. Final state/plan completion bookkeeping is persisted separately.

Task complete for the authorized deployment plus permitted authority-parking
branch. Automatic session remains running at Follow-up, awaiting owner-selected
later work; no child task starts autonomously. Both sites current-main delivery
succeeded, #521 remains parked, original Review Residual work unchanged.
Full publication gate/receipt, hosted checks, human approval and PR remain
unperformed and coordinator-owned.

## Generated Complete Command Ledger

Every helper subprocess command result is included below in execution order;
full argv, UTC timestamps, output hashes and retained-log match flags are in
demo-sites-live-correction-evidence.json. Token/stdin values are withheld.
This appendix is generated directly from the append-only subprocess journal.
Exit1 AuthConfigNotFound is explicit expected resident auth absence.

Early repeated labels overwrote some external stdout/stderr files; original
per-command hashes/results remain in the journal, but those bytes are NOT
claimed retained where retained_*_matches is false. Later unique labels and
final operational proofs remain available. No missing historical log is
fabricated, and final proof is not substituted for historical execution.

| # | UTC start | Command/result label | Exit |
| --- | --- | --- | --- |
| 1 | 2026-10-29T10:10:45.517964+00:00 | backup-ca-resident-demo | 0 |
| 2 | 2026-10-29T10:10:46.062190+00:00 | auth-ca-resident-demo | 1 |
| 3 | 2026-10-29T10:11:01.943728+00:00 | backup-ca-resident-demo | 0 |
| 4 | 2026-10-29T10:11:02.677446+00:00 | auth-list-ca-resident-demo | 1 |
| 5 | 2026-10-29T10:11:13.986055+00:00 | backup-ca-resident-demo | 0 |
| 6 | 2026-10-29T10:11:14.455326+00:00 | auth-current-ca-resident-demo | 1 |
| 7 | 2026-10-29T10:11:15.769188+00:00 | revisions-ca-resident-demo | 0 |
| 8 | 2026-10-29T10:11:16.826349+00:00 | backup-ca-cutover-test-demo-api | 0 |
| 9 | 2026-10-29T10:11:17.282408+00:00 | auth-current-ca-cutover-test-demo-api | 0 |
| 10 | 2026-10-29T10:11:17.772612+00:00 | revisions-ca-cutover-test-demo-api | 0 |
| 11 | 2026-10-29T10:11:18.927051+00:00 | jobs-before | 0 |
| 12 | 2026-10-29T10:11:20.811735+00:00 | backup-job-cutover-test-init | 0 |
| 13 | 2026-10-29T10:11:21.348801+00:00 | backup-job-cutover-test-verify | 0 |
| 14 | 2026-10-29T10:11:21.871570+00:00 | backup-job-cutover-test-ledger-verify | 0 |
| 15 | 2026-10-29T10:11:23.026729+00:00 | backup-job-cutover-test-import | 0 |
| 16 | 2026-10-29T10:11:23.521410+00:00 | backup-job-cutover-test-orchestrator | 0 |
| 17 | 2026-10-29T10:11:24.079613+00:00 | backup-job-cutover-test-smoke | 0 |
| 18 | 2026-10-29T10:11:24.613034+00:00 | backup-job-cutover-test-mi-http | 0 |
| 19 | 2026-10-29T10:11:25.111626+00:00 | backup-job-cutover-test-public-audit | 0 |
| 20 | 2026-10-29T10:11:25.614746+00:00 | acr-before | 0 |
| 21 | 2026-10-29T10:15:57.531379+00:00 | sql-main-pin | 0 |
| 22 | 2026-10-29T10:15:57.534810+00:00 | sql-pinned-source | 0 |
| 23 | 2026-10-29T10:15:57.539502+00:00 | sql-verifier-source | 0 |
| 24 | 2026-10-29T10:15:57.544581+00:00 | sql-job-preflight | 0 |
| 25 | 2026-10-29T10:15:58.310554+00:00 | init-executions-before | 0 |
| 26 | 2026-10-29T10:15:59.707675+00:00 | sql-disable-retry | 0 |
| 27 | 2026-10-29T10:16:01.387541+00:00 | sql-restore-job | 1 |
| 28 | 2026-10-29T10:16:18.851675+00:00 | job-convergence-1793268978851667231 | 0 |
| 29 | 2026-10-29T10:16:19.362351+00:00 | sql-restore-job-reconciled | 0 |
| 30 | 2026-10-29T10:16:20.030970+00:00 | job-convergence-1793268980030959608 | 0 |
| 31 | 2026-10-29T10:16:25.591160+00:00 | job-convergence-1793268985591147139 | 0 |
| 32 | 2026-10-29T10:16:26.092633+00:00 | sql-main-pin | 0 |
| 33 | 2026-10-29T10:16:26.095995+00:00 | sql-pinned-source | 0 |
| 34 | 2026-10-29T10:16:26.100793+00:00 | sql-verifier-source | 0 |
| 35 | 2026-10-29T10:16:26.105961+00:00 | sql-job-preflight | 0 |
| 36 | 2026-10-29T10:16:26.590376+00:00 | init-executions-before | 0 |
| 37 | 2026-10-29T10:16:27.764922+00:00 | sql-disable-retry | 0 |
| 38 | 2026-10-29T10:16:28.556493+00:00 | job-convergence-1793268988556486268 | 0 |
| 39 | 2026-10-29T10:16:34.021119+00:00 | job-convergence-1793268994021105232 | 0 |
| 40 | 2026-10-29T10:16:34.458876+00:00 | sql-start | 2 |
| 41 | 2026-10-29T10:16:35.070394+00:00 | job-convergence-1793268995070388279 | 0 |
| 42 | 2026-10-29T10:16:36.280957+00:00 | sql-restore-job | 0 |
| 43 | 2026-10-29T10:16:37.080652+00:00 | job-convergence-1793268997080646333 | 0 |
| 44 | 2026-10-29T10:16:42.535813+00:00 | job-convergence-1793269002535799836 | 0 |
| 45 | 2026-10-29T10:16:43.040823+00:00 | job-preservation-job-cutover-test-init | 0 |
| 46 | 2026-10-29T10:16:43.469202+00:00 | job-preservation-job-cutover-test-verify | 0 |
| 47 | 2026-10-29T10:16:43.910383+00:00 | job-preservation-job-cutover-test-ledger-verify | 0 |
| 48 | 2026-10-29T10:16:44.385952+00:00 | job-preservation-job-cutover-test-import | 0 |
| 49 | 2026-10-29T10:16:44.829365+00:00 | job-preservation-job-cutover-test-orchestrator | 0 |
| 50 | 2026-10-29T10:16:45.348799+00:00 | job-preservation-job-cutover-test-smoke | 0 |
| 51 | 2026-10-29T10:16:45.798707+00:00 | job-preservation-job-cutover-test-mi-http | 0 |
| 52 | 2026-10-29T10:16:46.243863+00:00 | job-preservation-job-cutover-test-public-audit | 0 |
| 53 | 2026-10-29T10:17:14.643431+00:00 | sql-main-pin | 0 |
| 54 | 2026-10-29T10:17:14.646727+00:00 | sql-pinned-source | 0 |
| 55 | 2026-10-29T10:17:14.651157+00:00 | sql-verifier-source | 0 |
| 56 | 2026-10-29T10:17:14.656693+00:00 | sql-job-preflight | 0 |
| 57 | 2026-10-29T10:17:15.218102+00:00 | init-executions-before | 0 |
| 58 | 2026-10-29T10:17:16.198447+00:00 | sql-disable-retry | 0 |
| 59 | 2026-10-29T10:17:17.065845+00:00 | job-convergence-1793269037065839797 | 0 |
| 60 | 2026-10-29T10:17:22.570423+00:00 | job-convergence-1793269042570403771 | 0 |
| 61 | 2026-10-29T10:17:23.083382+00:00 | sql-start-rest | 0 |
| 62 | 2026-10-29T10:17:23.915298+00:00 | sql-status-1793269043915292165 | 0 |
| 63 | 2026-10-29T10:17:34.781220+00:00 | sql-status-1793269054781207696 | 0 |
| 64 | 2026-10-29T10:17:45.619760+00:00 | sql-status-1793269065619749332 | 0 |
| 65 | 2026-10-29T10:17:56.398283+00:00 | sql-status-1793269076398270634 | 0 |
| 66 | 2026-10-29T10:18:07.171912+00:00 | sql-status-1793269087171898838 | 0 |
| 67 | 2026-10-29T10:18:08.000173+00:00 | sql-console | 0 |
| 68 | 2026-10-29T10:18:10.306824+00:00 | job-convergence-1793269090306818327 | 0 |
| 69 | 2026-10-29T10:18:10.991381+00:00 | sql-restore-job | 0 |
| 70 | 2026-10-29T10:18:11.721691+00:00 | job-convergence-1793269091721681405 | 0 |
| 71 | 2026-10-29T10:18:17.153153+00:00 | job-convergence-1793269097153140401 | 0 |
| 72 | 2026-10-29T10:18:17.603610+00:00 | job-preservation-job-cutover-test-init | 0 |
| 73 | 2026-10-29T10:18:18.045947+00:00 | job-preservation-job-cutover-test-verify | 0 |
| 74 | 2026-10-29T10:18:18.528432+00:00 | job-preservation-job-cutover-test-ledger-verify | 0 |
| 75 | 2026-10-29T10:18:18.951732+00:00 | job-preservation-job-cutover-test-import | 0 |
| 76 | 2026-10-29T10:18:19.400620+00:00 | job-preservation-job-cutover-test-orchestrator | 0 |
| 77 | 2026-10-29T10:18:19.849052+00:00 | job-preservation-job-cutover-test-smoke | 0 |
| 78 | 2026-10-29T10:18:20.331599+00:00 | job-preservation-job-cutover-test-mi-http | 0 |
| 79 | 2026-10-29T10:18:20.799306+00:00 | job-preservation-job-cutover-test-public-audit | 0 |
| 80 | 2026-10-29T10:19:24.310668+00:00 | build-main-pin | 0 |
| 81 | 2026-10-29T10:19:24.313932+00:00 | source-archive | 0 |
| 82 | 2026-10-29T10:19:24.360941+00:00 | source-extract | 0 |
| 83 | 2026-10-29T10:19:24.400759+00:00 | source-tree | 0 |
| 84 | 2026-10-29T10:19:24.404163+00:00 | build-resident | 0 |
| 85 | 2026-10-29T10:19:51.107749+00:00 | inspect-resident | 0 |
| 86 | 2026-10-29T10:19:51.163455+00:00 | save-resident | 0 |
| 87 | 2026-10-29T10:19:53.280404+00:00 | build-employee | 0 |
| 88 | 2026-10-29T10:20:08.980815+00:00 | inspect-employee | 0 |
| 89 | 2026-10-29T10:20:09.035234+00:00 | save-employee | 0 |
| 90 | 2026-10-29T10:20:13.804623+00:00 | acr-preflight | 0 |
| 91 | 2026-10-29T10:20:14.518135+00:00 | vm-egress | 0 |
| 92 | 2026-10-29T10:20:14.786467+00:00 | acr-immediate-prewrite | 0 |
| 93 | 2026-10-29T10:20:15.426263+00:00 | acr-vm-rule | 0 |
| 94 | 2026-10-29T10:20:18.089297+00:00 | acr-rule-readback | 0 |
| 95 | 2026-10-29T10:20:18.885650+00:00 | acr-export-enable | 0 |
| 96 | 2026-10-29T10:20:20.905458+00:00 | acr-export-readback | 0 |
| 97 | 2026-10-29T10:20:21.529835+00:00 | acr-public-vm-only | 0 |
| 98 | 2026-10-29T10:20:23.708336+00:00 | acr-public-readback | 0 |
| 99 | 2026-10-29T10:20:24.306284+00:00 | acr-token | 0 |
| 100 | 2026-10-29T10:20:24.306284+00:00 | docker-login | 0 |
| 101 | 2026-10-29T10:20:26.481814+00:00 | push-resident | 0 |
| 102 | 2026-10-29T10:20:29.670879+00:00 | pushed-inspect-resident | 0 |
| 103 | 2026-10-29T10:20:29.834572+00:00 | acr-midway-resident | 0 |
| 104 | 2026-10-29T10:20:30.684395+00:00 | push-employee | 0 |
| 105 | 2026-10-29T10:20:33.865975+00:00 | pushed-inspect-employee | 0 |
| 106 | 2026-10-29T10:20:34.016591+00:00 | acr-midway-employee | 0 |
| 107 | 2026-10-29T10:20:34.647146+00:00 | acr-private-first | 0 |
| 108 | 2026-10-29T10:20:36.536472+00:00 | acr-restoration-preflight | 0 |
| 109 | 2026-10-29T10:20:37.220251+00:00 | acr-remove-owned-rule | 0 |
| 110 | 2026-10-29T10:20:38.857826+00:00 | acr-policy-restore | 0 |
| 111 | 2026-10-29T10:20:40.691033+00:00 | acr-final-readback | 0 |
| 112 | 2026-10-29T10:20:56.017488+00:00 | acr-rule-recovery-preflight | 0 |
| 113 | 2026-10-29T10:20:56.646293+00:00 | acr-remove-normalized-owned-rule | 0 |
| 114 | 2026-10-29T10:20:58.319973+00:00 | acr-final-exact-recovery | 0 |
| 115 | 2026-10-29T10:21:35.671679+00:00 | acr-deploy-preflight-resident | 0 |
| 116 | 2026-10-29T10:21:36.352399+00:00 | job-deploy-preflight-resident-job-cutover-test-init | 0 |
| 117 | 2026-10-29T10:21:37.100633+00:00 | job-deploy-preflight-resident-job-cutover-test-verify | 0 |
| 118 | 2026-10-29T10:21:37.549161+00:00 | job-deploy-preflight-resident-job-cutover-test-ledger-verify | 0 |
| 119 | 2026-10-29T10:21:38.327579+00:00 | job-deploy-preflight-resident-job-cutover-test-import | 0 |
| 120 | 2026-10-29T10:21:38.880303+00:00 | job-deploy-preflight-resident-job-cutover-test-orchestrator | 0 |
| 121 | 2026-10-29T10:21:39.520742+00:00 | job-deploy-preflight-resident-job-cutover-test-smoke | 0 |
| 122 | 2026-10-29T10:21:39.957883+00:00 | job-deploy-preflight-resident-job-cutover-test-mi-http | 0 |
| 123 | 2026-10-29T10:21:40.407596+00:00 | job-deploy-preflight-resident-job-cutover-test-public-audit | 0 |
| 124 | 2026-10-29T10:21:40.982107+00:00 | app-preflight-resident | 0 |
| 125 | 2026-10-29T10:21:41.520564+00:00 | auth-preflight-resident | 1 |
| 126 | 2026-10-29T10:21:42.160216+00:00 | deploy-resident | 0 |
| 127 | 2026-10-29T10:21:42.709348+00:00 | wake-res-live-20261029-102142 | 0 |
| 128 | 2026-10-29T10:22:07.000591+00:00 | revision-res-live-20261029-102142-1793269327000586369 | 0 |
| 129 | 2026-10-29T10:22:17.811054+00:00 | revision-res-live-20261029-102142-1793269337811042374 | 0 |
| 130 | 2026-10-29T10:22:28.675494+00:00 | revision-res-live-20261029-102142-1793269348675482307 | 0 |
| 131 | 2026-10-29T10:22:39.542541+00:00 | revision-res-live-20261029-102142-1793269359542524336 | 0 |
| 132 | 2026-10-29T10:22:40.639666+00:00 | after-app-res-live-20261029-102142 | 0 |
| 133 | 2026-10-29T10:22:41.106883+00:00 | auth-after-res-live-20261029-102142 | 1 |
| 134 | 2026-10-29T10:22:41.608389+00:00 | revisions-after-res-live-20261029-102142 | 0 |
| 135 | 2026-10-29T10:22:42.379398+00:00 | replicas-res-live-20261029-102142 | 0 |
| 136 | 2026-10-29T10:22:44.192293+00:00 | http-res-live-20261029-102142-_health | 0 |
| 137 | 2026-10-29T10:22:44.310185+00:00 | http-res-live-20261029-102142-_healthz | 0 |
| 138 | 2026-10-29T10:22:44.418232+00:00 | http-res-live-20261029-102142-_ | 0 |
| 139 | 2026-10-29T10:22:52.723242+00:00 | wake-res-live-20261029-102142 | 0 |
| 140 | 2026-10-29T10:22:52.833102+00:00 | revision-res-live-20261029-102142-1793269372833095570 | 0 |
| 141 | 2026-10-29T10:22:53.622834+00:00 | after-app-res-live-20261029-102142 | 0 |
| 142 | 2026-10-29T10:22:54.090659+00:00 | auth-after-res-live-20261029-102142 | 1 |
| 143 | 2026-10-29T10:22:54.598233+00:00 | revisions-after-res-live-20261029-102142 | 0 |
| 144 | 2026-10-29T10:22:55.396211+00:00 | replicas-res-live-20261029-102142 | 0 |
| 145 | 2026-10-29T10:22:56.578679+00:00 | http-res-live-20261029-102142-_health | 0 |
| 146 | 2026-10-29T10:22:56.693162+00:00 | http-res-live-20261029-102142-_healthz | 0 |
| 147 | 2026-10-29T10:22:56.801602+00:00 | http-res-live-20261029-102142-_ | 0 |
| 148 | 2026-10-29T10:22:56.907188+00:00 | logs-healthy-console-ca-resident-demo | 0 |
| 149 | 2026-10-29T10:22:59.442840+00:00 | logs-healthy-system-ca-resident-demo | 0 |
| 150 | 2026-10-29T10:23:01.234709+00:00 | acr-deploy-preflight-employee | 0 |
| 151 | 2026-10-29T10:23:01.968106+00:00 | job-deploy-preflight-employee-job-cutover-test-init | 0 |
| 152 | 2026-10-29T10:23:02.530565+00:00 | job-deploy-preflight-employee-job-cutover-test-verify | 0 |
| 153 | 2026-10-29T10:23:03.076495+00:00 | job-deploy-preflight-employee-job-cutover-test-ledger-verify | 0 |
| 154 | 2026-10-29T10:23:03.525776+00:00 | job-deploy-preflight-employee-job-cutover-test-import | 0 |
| 155 | 2026-10-29T10:23:03.973140+00:00 | job-deploy-preflight-employee-job-cutover-test-orchestrator | 0 |
| 156 | 2026-10-29T10:23:04.472653+00:00 | job-deploy-preflight-employee-job-cutover-test-smoke | 0 |
| 157 | 2026-10-29T10:23:04.913986+00:00 | job-deploy-preflight-employee-job-cutover-test-mi-http | 0 |
| 158 | 2026-10-29T10:23:05.375428+00:00 | job-deploy-preflight-employee-job-cutover-test-public-audit | 0 |
| 159 | 2026-10-29T10:23:05.830750+00:00 | app-preflight-employee | 0 |
| 160 | 2026-10-29T10:23:06.308080+00:00 | auth-preflight-employee | 0 |
| 161 | 2026-10-29T10:23:06.791099+00:00 | deploy-employee | 0 |
| 162 | 2026-10-29T10:23:07.529986+00:00 | wake-emp-live-20261029-102306 | 0 |
| 163 | 2026-10-29T10:23:43.222941+00:00 | revision-emp-live-20261029-102306-1793269423222935499 | 0 |
| 164 | 2026-10-29T10:23:44.543942+00:00 | after-app-emp-live-20261029-102306 | 0 |
| 165 | 2026-10-29T10:23:45.008237+00:00 | auth-after-emp-live-20261029-102306 | 0 |
| 166 | 2026-10-29T10:23:45.453739+00:00 | revisions-after-emp-live-20261029-102306 | 0 |
| 167 | 2026-10-29T10:23:46.241607+00:00 | replicas-emp-live-20261029-102306 | 0 |
| 168 | 2026-10-29T10:23:47.438468+00:00 | http-emp-live-20261029-102306-_health | 0 |
| 169 | 2026-10-29T10:23:48.513608+00:00 | http-emp-live-20261029-102306-_healthz | 0 |
| 170 | 2026-10-29T10:23:48.696837+00:00 | http-emp-live-20261029-102306-_ | 0 |
| 171 | 2026-10-29T10:23:48.803146+00:00 | http-emp-live-20261029-102306-_app | 0 |
| 172 | 2026-10-29T10:23:48.917295+00:00 | http-emp-live-20261029-102306-_app.js | 0 |
| 173 | 2026-10-29T10:23:49.020485+00:00 | http-emp-live-20261029-102306-_ops.js | 0 |
| 174 | 2026-10-29T10:23:49.122105+00:00 | logs-healthy-console-ca-cutover-test-demo-api | 0 |
| 175 | 2026-10-29T10:23:52.440163+00:00 | logs-healthy-system-ca-cutover-test-demo-api | 0 |
| 176 | 2026-10-29T10:24:37.435117+00:00 | final-app-ca-resident-demo | 0 |
| 177 | 2026-10-29T10:24:37.976214+00:00 | final-auth-ca-resident-demo | 1 |
| 178 | 2026-10-29T10:24:38.482440+00:00 | final-app-ca-cutover-test-demo-api | 0 |
| 179 | 2026-10-29T10:24:40.942288+00:00 | final-auth-ca-cutover-test-demo-api | 0 |
| 180 | 2026-10-29T10:24:41.593096+00:00 | final-job-job-cutover-test-init | 0 |
| 181 | 2026-10-29T10:24:42.442394+00:00 | final-job-job-cutover-test-verify | 0 |
| 182 | 2026-10-29T10:24:43.050451+00:00 | final-job-job-cutover-test-ledger-verify | 0 |
| 183 | 2026-10-29T10:24:43.477081+00:00 | final-job-job-cutover-test-import | 0 |
| 184 | 2026-10-29T10:24:44.023769+00:00 | final-job-job-cutover-test-orchestrator | 0 |
| 185 | 2026-10-29T10:24:44.651220+00:00 | final-job-job-cutover-test-smoke | 0 |
| 186 | 2026-10-29T10:24:47.275970+00:00 | final-job-job-cutover-test-mi-http | 0 |
| 187 | 2026-10-29T10:24:47.730301+00:00 | final-job-job-cutover-test-public-audit | 0 |
| 188 | 2026-10-29T10:24:48.310023+00:00 | final-acr | 0 |
| 189 | 2026-10-29T10:24:49.160064+00:00 | final-local-main | 0 |
