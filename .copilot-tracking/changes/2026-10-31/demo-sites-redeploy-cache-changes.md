---
title: Redeploy 8 immutable versioned cache changes
ms.date: 2026-10-31
---

## Execution Boundary

Task 2c99fa13-81cb-4fd2-af53-81ad16cb565a; demo-sites-redeploy-cache.
Full plan explicitly requested, manual full-loop advancement authorized.
Clean chore/ops-redeploy-cache, no open PR; fetched current main and HEAD
d20bc50c4b664521f72446e5d0c85cc576ef0850. Research Complete / Ready.
Single independent critique Complete / Revise: PC-001 applied pre-push
build-proof input, PC-002 rejected unsupported temporary-path prohibition;
required shared lock retained. No second critique.

Owner verbatim: "Always allow a short public-access window on the ACR, but if
not possible, use `az acr build` command". Standing deployment authority through
2026-11-15; resident AI OFF. No sign-in, .env, private datasets, secrets, new
RBAC/endpoints/public SQL/RG deletion, push or source repair.

## Intake Commands and Results

`git status --short && git branch --show-current && git log -3 &&
git show origin/main:.copilot-tracking/changes/2026-10-31/demo-sites-redeploy-1031-changes.md`
exit0: clean expected topic/source and #596 exact prior procedure.
`git fetch origin main --quiet && git rev-parse HEAD origin/main &&
gh pr list --head chore/ops-redeploy-cache --json number,state,url &&
git diff --name-only 4cb5964f HEAD -- src infra &&
az account show --query '{subscription:id,state:state}' -o json &&
docker info --format '{{.ServerVersion}}'` exit0:
HEAD=main=d20bc50c, no open PR, Enabled expected subscription, Docker29.9.0.
Original/latest changes records and required project context read.
Full src/infra diff since4cb5964f inspected: cache source/docs/tests only,
no SQL/schema/DDL/migration touch. SQL init explicitly skipped, no SQL action
or historical-success-shaped receipt will be generated.

## P01-T01 Preparation

Retained helpers and all executed transitive bodies read.
Private current execution root:
/home/azureuser/.copilot/session-state/2c99fa13-81cb-4fd2-af53-81ad16cb565a/files/redeploy.
Raw full config and operation outputs remain external0700/0600.
Current adapters retain guarded publisher/rollout/protected comparisons.
Concrete resource-subdir image paths and local proof outside live compensation
retained; current pre-push image proof reads build-proof only.
Implementation in progress; no deployment mutation yet.

## P01-T01 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/preflight.py &&
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/ops.py &&
flock -n -E75 /tmp/ama-rpi-heavy.lock env PYTHONDONTWRITEBYTECODE=1
python3 ROOT/build.py && PYTHONDONTWRITEBYTECODE=1 python3 ROOT/verify.py --images`
exit0. Complete fresh private backups: both min0, eight full Manual definitions,
ACR private/admin off/exports off/no rules; resident assistant setting names
absent/OFF. All selected executors compile/hash-bound.
Both tracked src builds and pre-publication packaged web proofs pass.
Source archive SHA25628c7fa1eacee5753a7d815c936a4a1b15b18c55ae102104edcf6fa132dbabd90;
src tree0fd94c69365573bef73426237221180d4a398b3c.
Release prefix main-20261031-d20bc50c4b66-cache8, resident/employee suffixes.
Local resident config fed6eff1e397117f009d462b3ef5c99c6007726f634e20f04e4f8243fd61d132,
employee705da53bda9e83791d8e47a81927ef5abd97f75963578c235b989b4e5204417c.
No SQL or cloud mutation occurred. P01-T02 next.

## P01-T02 First Window Failure and Reconciliation

`flock -n -E75 /tmp/ama-rpi-heavy.lock env PYTHONDONTWRITEBYTECODE=1
python3 ROOT/publish.py` exit1 at token acquisition before either image push.
Original guarded finally restored exact private ACR; no app write/SQL.
Enable acknowledged02:34:46.857728Z, private confirmed02:34:52.204086Z,
exact restored02:35:00.847016Z. Acknowledged-to-disabled5.346s; not exact
service-side exposure. First failed restoration receipt preserved separately.

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/diagnose_publish.py &&
az acr build --help` exit0: exact stable ACR equals baseline, both complete
apps unchanged, no pushed images. Private-registry login diagnostic exit1,
firewall/public-network category only; token/raw error not printed. Fallback
command interface inspected. Failed open-window login output was withheld,
so transient propagation is a possibility, not established root cause.

Immediately relevant adapter update: retain all publisher guards and add bounded
same-window token acquisition attempts with3/6/12s backoff. No blind repeat push
or app write; new attempt only from confirmed fully restored baseline.
If still unavailable, close private and use/assess owner-authorized az acr build.
No critique repetition, source change, authority widening or live compensation.

## P01-T02 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/preflight.py &&
flock -n -E75 /tmp/ama-rpi-heavy.lock env PYTHONDONTWRITEBYTECODE=1
python3 ROOT/publish.py` exit0. Same guarded publisher/current hash-bound
token adapter; second window token succeeded first attempt. No propagation retry
or az acr build fallback exercised.
Public enable acknowledged02:36:31.266137Z; Disabled confirmed02:36:46.241132Z;
exact restore02:36:51.998000Z. Enable-ack-to-disable14.975s, bounded
operation30.480s; not exact service-side exposure. VM/32/defaultDeny only.
Full stable ACR exact baseline restoration/readback passed; admin off/exports
off/private/default/rules preserved. Owned Docker credentials removed.
Existing resident24bc9d1293e1ea7b59d9e75d18d43883b4d8ae758e6d7f7e8f8b012952176bcd
and employee5086b5619f0a1a9c8ae0d3aea5d6de19e1c47494182169976ea4dae63dabded0
manifests verified before/after pushes.

| Image | New index digest (sha256) | Platform digest (sha256) |
| --- | --- | --- |
| Resident | d3a3a8727b8a65305d2cf3994872477e8542b0383a47bf084fdc36ef368d849a | 6ad7c2925845c914d2d7a0cb6f5a74a364dcc22233fb63d88e8bf77a0e65b09c |
| Employee | 0bd3a9030d56ff23403ebc40cb083b3c17d42357148393578ff37ba5c0ee2ec1 | 1451d5e20a21e253acf77bcb6502c5cd88cf2a1e66f48c339e4cb12753362c27 |

Exact configs/source labels/platforms/RepoDigests bound to P01-T01 local proof.
P01 complete. P02-T01 rollout next; SQL skip unchanged.

## P02-T01 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/rollout.py` exit0.
Fresh eight-job equality and explicit no-SQL receipt guarded pair start.
Resident ca-resident-demo--res-live-20261031-023722, employee
ca-cutover-test-demo-api--emp-live-20261031-023859 both latest=ready,
Healthy/Provisioned/traffic100/ready replica, exact new index digests.
Protected full app/auth/config and existing history retained, min0,
one added revision/app. No SQL init/database read/write or retry/template job
change. No app failure, recovery or ambiguous write branch exercised.
P02 complete. P03 live cache/anonymous verification next.

## P03-T01 Complete: Curl and Final Protected Readback

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/verify.py` exit0.
Both /healthz first warm200 with retained180s/900s convergence available.
Both public shells200 and exact current-main rendered bytes, HTML
Cache-Control:no-store. All five resident and two employee public asset URLs
versioned200/source-equal with `public, max-age=31536000, immutable`.
Resident chat-widget JS/CSS, assistant/demo/css load200 and dock bytes present.
Employee /app,/api/me, versioned app/ops/widget JS/CSS401; resident /demo/view401.
No anonymous POST, sign-in or model request.
Final full protected app/auth/history equality, one added revision/app,
all eight full Manual definitions equal baseline, all four ama minima0,
full stable ACR baseline equality pass. Resident AI setting names absent/OFF.

## P03-T01 Complete: Actual Anonymous Playwright

`playwright browser_tabs list`: only about:blank, no existing owner session.
One actual `browser_run_code_unsafe` execution02:41:09.407Z-02:41:14.395Z:
fresh contexts at1365x900 and390x844, both health/public200. Versioned URLs/
network200 and exact immutable-year headers/no-store HTML independently asserted.
Resident runtime launcher/dialog and open/dock/undock/Escape states asserted.
Dock heights900/844px, widths477.75/320px; dock class/pressed/disabled-height/
hidden-launcher then inverse undock state checked, Escape closes.
Employee public shell only, protected browser302 to Entra origin without
following sign-in/query. All page request methods GET; no submission.
No horizontal overflow observed; pageerrors0 all contexts. Console errors:
resident desktop1/mobile0, employee1 per viewport. No clean-console/UI/WCAG/
screen-reader/signed-in/identity/model acceptance.

## P03-T02 Export and Pre-Review Reconciliation

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/preflight.py &&
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/export.py &&
git diff --check && git diff --name-only d20bc50c -- src infra docs` exit0.
Sanitized evidence194 actual journal records,20 completed outer commands,
one successful actual browser event/code/result binding. All retained command
stdout/stderr hashes, source archive, executor syntax/hashes and original
protected app/history/ACR/eight-job comparisons pass.
Raw config/auth/HTTP outputs remain external0600/0700. Registry raw bodies
not retained, only publisher-bound hashes; no independent raw-body rehash claim.
Failed first-window restoration retained separately; actual successful window
restores baseline before any app mutation. No live compensation was triggered.

P01/P02/P03-T01 complete; P03-T02 export complete, one independent Review and
local commit pending. AC1-6 pass within explicit anonymous/public scope.
Employee protected widget live200/cache headers and signed-in acceptance remain
unproven; no auth weakening. Resident AI stays OFF. SQL intentionally not run.
No source/dependency/test change or proxy-test claim. Complete local publication
gate, exact-head/hosted/human approval and push/PR/merge not run or claimed.
One original critique retained; no operational blockers or remaining live writes.

## Single Independent Review and Parent Dispositions

Exactly one Review executed Complete / Residual work, original preserved.
Independent retained comparison:426 archive/source files, two35-file image
receipts,194 journal records/358 output hashes,20 actual outer command
bindings,86 proof JSON hashes, nine current/eight original executors and
one actual browser receipt/code/event chain. No cloud/build/browser rerun.
Original protected app/auth/history/eight-job/ACR and raw curl comparisons pass.
No operational defect found; exact cache deployment/preservation proven.

RV-001 Medium accepted: protected employee widget200/cache and live signed-in
acceptance remain unproven. Owner-run distinct acceptance, no bypass.
RV-002 Low accepted: local administrative evidence commit pending; active
parent persistence next, not a second Review or closure assessment.
RV-003 Low accepted: console counts have no cause/source diagnosis. Distinct
optional anonymous diagnostic follow-up; no clean-console or defect claim.
AI activation remains a separate owner decision; keep OFF.

`git status --short && git diff --stat && gh api user --jq '{id,login}' &&
test -s .gitignore && git diff --check &&
git diff --name-only d20bc50c -- src infra docs` exit0: exactly eight dated
evidence paths, no source changes, fresh authenticated identity resolved.
Git-commit skill referenced instruction file absent and get_changed_files
unavailable. Apply higher repository exact-path staging and explicit diff/
readback/privacy-safe identity/Refs/trailer safeguards, not broad staging.
No full publication gate, push, PR, merge, amend or history rewrite.

## Local Evidence Persistence and Closeout

`chmod 600 ROOT/commit.py && PYTHONDONTWRITEBYTECODE=1
python3 ROOT/commit.py` exit0. Eight original dated artifacts, including the
single Review, locally committed as ae9d26da04e7289e5daf1ddaf56f7c1ef607b971,
`chore(ops): redeploy immutable asset cache on both demos`.
Fresh gh api user-derived repository-local noreply author/committer, explicit
eight-path staging, JSON/sensitive-marker/whitespace and exact message/paths/
identity/clean-tree readback pass. Refs #568,#520,#570 and exact Copilot trailer.
Actual private local-commit-proof.json retained; no push/PR/merge/amend/rebase.

All P01/P02/P03 tasks executed; finite manual full RPI loop complete/stopped.
Review original Complete / Residual work remains unchanged. Administrative
RV-002 local persistence performed; RV-001 signed-in/widget/cache acceptance,
RV-003 optional console diagnosis and separate AI decision remain later work.
No source/operational correction, repeated Review or closure assessment.
Original export/Review pending-at-assessment statements are historical, not
altered to predeclare a commit.

This final plan/details/state/changes administrative status reconciliation
is persisted separately via `PYTHONDONTWRITEBYTECODE=1 python3 ROOT/commit.py
--closure`, with identical exact-path identity/Refs/trailer/readback safeguards.
Actual final commit proof stays external in closure-commit-proof.json/events,
not self-referentially predeclared here. No further work or push selected.

## Proven and Unproven

Exact d20bc50c cache8 images live, both health200, versioned public asset200/
source-equal with max-age31536000 AND immutable, HTML no-store. Resident
anonymous dock open/dock/undock/Escape desktop/mobile proven. Exact prior
private ACR restored after both windows; old manifests/history protected;
min0/eight full Manual definitions/AI OFF retained. SQL correctly not run.
Protected employee widget200/cache and signed-in resident/employee/identity/
model acceptance unproven. No live rollback, propagation retry or ACR-build
fallback exercised/certified. Console causes and full publication/hosted/human
approvals unproven. Raw backups/executors retained privately; no .env/secrets/
private data, new RBAC/endpoints/public SQL or RG deletion.
