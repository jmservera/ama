---
title: Current-main two-site redeployment changes
ms.date: 2026-10-31
---

## Execution Boundary

Task 975bbf93-de84-47b4-ad5d-b55583f970c9; demo-sites-redeploy-1031.
Full plan declared by owner, manual full-loop progression authorized.
Clean chore/ops-redeploy-1031 at intake, no PR lifecycle; fetched source
4cb5964f7acce89668a37b5a56c3e125e26f6d21=HEAD=origin/main.
Research Complete / Ready; one critique Complete / Revise, dispositions
PC001 rejected unsupported restriction, PC002/003/005/006 applied,
PC004 planning prose reconciled to actual original procedure. No repeat.
Standing deployment/short IP-only ACR window authority accepted through
2026-11-15. Resident AI stays OFF. No push or source repair authorized.

## Initial Commands and Results

`git status --short && git branch --show-current && git log -1 &&
git remote -v && gh pr list --head chore/ops-redeploy-1031` exit0:
clean matching topic, expected origin, no existing PR.
`git fetch origin main && git rev-parse HEAD origin/main &&
az account show --query '{subscription:id,state:state}' -o json &&
docker info --format '{{.ServerVersion}}'` exit0: exact current source,
expected Enabled subscription and Docker29.9.0.
Required project context and original/latest redeployment records read.
Exact retained operational functions inspected, no raw secrets printed.

## P01 Preservation, Build and Publish

P01-T01 Complete. Private root:
/home/azureuser/.copilot/session-state/975bbf93-de84-47b4-ad5d-b55583f970c9/files/redeploy.
Original transitive executors and current adapters hash-bound before cloud
mutation. Raw full config/auth/history/job/ACR backups and command outputs
remain external0700/0600; sanitized results only are committed.

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/preflight.py &&
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/ops.py && flock -n -E75
/tmp/ama-rpi-heavy.lock env PYTHONDONTWRITEBYTECODE=1 python3 ROOT/build.py`
exit0. All selected dependencies/adapters compile and hash-bound. Fresh full
backups pass: eight Manual, both min0, ACR private/admin off/exports off,
resident assistant settings absent (names only). Both tracked-main builds
complete under shared lock. Source archive SHA256
59fe779ea52e07d265b9cdd427efb570a5b2b9c910f2f6ab0ee12ec6bc4e6b56,
src tree d9691825f1580b1f926361d7ad5799805ef2bd54.
Release prefix main-20261031-4cb5964f7acc; resident/employee suffixes.
Local config SHA256 resident85b80b0cb55fbbf9cd6ad302c784d743703e2e91d886cbdffa3ba14e63fda3ca,
employee08074fdda6ff19477d518ee0595b1624668acfc3f85f55b931df602d175b59e8.
No cloud write yet. P01-T02 publication next.

P01-T02 Complete. `flock -n -E75 /tmp/ama-rpi-heavy.lock env
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/publish.py` exit0.
Original guarded publisher used unchanged. Public enable acknowledged
01:07:45.448684Z; Disabled confirmed01:08:02.288363Z; exact restoration
01:08:09.380293Z. Enable-ack to disable-confirm16.840s, not exact
service-side exposure; bounded operation34.016s. VM/32/defaultDeny only.
Exact stable ACR baseline restored (private/admin off/exports off/no rules,
original default), readback passed; old remote manifests verified before/after.
New resident index24bc9d1293e1ea7b59d9e75d18d43883b4d8ae758e6d7f7e8f8b012952176bcd,
employee5086b5619f0a1a9c8ae0d3aea5d6de19e1c47494182169976ea4dae63dabded0.
Platform/config/source labels verified. Owned Docker credentials removed.
No fallback or restoration failure branch needed. P01 complete; P02 next.

## P02-T01 Preparation Amendment

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/sql_init.py` exit1 in local prepare(),
before retry PATCH or execution. Current main adds an authority-renewal batch,
so historical fixed GO index2 selected a constraint batch, correctly refused.
No SQL job or database write occurred. Current-state adapter selects the unique
exact v_resident_case CREATE OR ALTER VIEW batch instead of numeric position,
with explicit guards excluding authority placeholder/ALTER TABLE/grants/denies/
transaction statements. No authority constraint or accounting change applied.
Original failed preparation and original executor remain preserved; safe
corrected invocation is not a repeated or ambiguous SQL execution.

P02-T01 Complete. `PYTHONDONTWRITEBYTECODE=1 python3 ROOT/preflight.py &&
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/sql_init.py` exit0.
One execution job-cutover-test-init-2fe7yoj Succeeded, one replica/retry0,
hash-bound post-COMMIT receipt. Six sensor counts before/after0, allowlist/
view/valid projected sensor arrays522, narrow resident principal and exact17
columns/ledger metadata verified. View batch hash equals prior successful batch:
86747aa207f64341ec341910396b91fc57454bb8c1d58644c4710f7f3860ef70.
Retry restored1 and all eight full job definitions equal baseline/Manual.
No authority-window/grant/accounting/data changes. P02-T02 pair rollout next.

P02-T02 Complete. `PYTHONDONTWRITEBYTECODE=1 python3 ROOT/rollout.py` exit0.
Resident ca-resident-demo--res-live-20261031-011026, employee
ca-cutover-test-demo-api--emp-live-20261031-011208 both latest=ready,
Healthy/Provisioned/traffic100 with ready replicas, exact new immutable digests.
One added revision each, all prior history retained, protected full config/
auth equality passes, min0. Pair proof persisted. No failure/recovery or
ambiguous forward write occurred. P02 complete; warm anonymous verification next.

## P03 Local Proof Failure, Actual Recovery and Corrected Attempt

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/preflight.py &&
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/verify.py` exit1. Read-only local
Docker image proof failed: namespace importlib resource root is MultiplexedPath,
so relative_to(root) raises TypeError. This was an adapter defect, not live
startup or asset failure. The handler was too broad and actually compensated
both healthy deployments to original digests. Preserve this undesired but
verified recovery, not an unexercised-rollback claim.
Resident recover-20261031-011425 and employee recover-20261031-011532
both Healthy/Provisioned/100%/ready/min0 with original config/auth/history.
No lost digest, SQL rollback or ACR change.

Immediate current-state amendment: compute image file paths relative to each
concrete resource subdirectory. Local image-proof errors are outside the live
operational compensation block; genuine live HTTP/control failures remain
guarded. Corrected image proof must pass before any further forward mutation.
Preserve/readback-hash the complete first attempt proof/adapter/journal snapshot
outside Git; verify recovered exact targets and take fresh baseline backups.
Then one distinct corrected pair rollout from the confirmed recovered baseline
under continuing owner redeployment authority. This is not a blind retry of
an ambiguous PATCH and does not repeat SQL, push, build, critique or Review.

## Corrected Deployment and Final Verification

`PYTHONDONTWRITEBYTECODE=1 python3 -c '<import verify; image_assets()>' &&
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/resume_after_recovery.py` exit0.
Both images' entire packaged web-file hashes match archive. First attempt
proof/adapter/journal snapshot copied and full readback verified under
ROOT/attempt1. Both recovered originals verified before new fresh backups.
Corrected targets resident res-live-20261031-011743 and employee
emp-live-20261031-011847 Healthy/Provisioned/100%/ready/min0, same published
new digests. No second init/build/push. Full initial and recovered baselines
retained; total3 added revisions/app since intake, not only final-attempt1.

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/verify.py` exit0.
Both /healthz first warm attempt200; both public shells200 and exact current-main
rendered bytes. Every public shell asset URL versioned and200/source-equal;
resident shared widget JS/CSS/assistant/demo/dock bytes verified.
HTML Cache-Control no-store. Versioned assets no-cache,must-revalidate
(employee header order differs), no max-age: long-lived caching UNMET.
Employee /app,/api/me,versioned app/ops/widget JS/CSS401; resident /demo/view401.
No anonymous POST/sign-in. Full protected config/auth/history passed;
all four ama minima0, all eight complete Manual job definitions equal baseline,
full stable ACR baseline equality passed. Resident AI settings absent/OFF.

Actual Playwright first attempt failed on overly narrow employee401 assertion:
browser-style anonymous GET/app returns302 to Entra, not curl401. This is
authentication, not access drift; no sign-in or live repair occurred.
Corrected fresh browser receipt01:20:45.077Z-01:20:49.402Z:
both health/public200 at1365x900 and390x844, versioned URLs/network200.
Resident launcher/dialog/runtime present, open/dock/undock/Escape verified,
full-height dock900/844px and desktop477.75/mobile320px width. No submission.
Employee public shell only, protected302 Entra origin retained without query.
Resident console errors0, employee1 per viewport; page errors0.
No horizontal overflow observed, no full UI/WCAG/signed-in/model acceptance.

## Export and Review Readiness

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/preflight.py &&
PYTHONDONTWRITEBYTECODE=1 python3 ROOT/export.py && git diff --check &&
git diff --name-only 4cb5964f -- src infra docs` exit0.
Sanitized evidence380 actual journal records,16 completed outer shell command
bindings, one actual browser receipt and one failed browser attempt/code/event
binding. All raw output hashes, first-attempt archive files, original/current
executor hashes and archived current-main source equality verified.
Original intake protected app/auth/history/ACR/eight jobs independently compared:
three added revisions/app and all prior revisions retained. Raw config backups/
worker logs stay external0600/0700; no secret output or .env/private dataset.

Implementation operationally complete, AC6 requested cache/employee-widget200
unmet, AC8 local commit pending; ready for one independent Review.
Actual recovery exercised successfully but its initial trigger was a local
tool defect; fallback, cleanup retries and ambiguous SQL/forward paths not
exercised/certified. No source/dependency/application-test change or proxy
test claim. Full local publication gate, exact-head/hosted/human approval,
push/PR/merge not run or claimed. Existing original critique unchanged.

## Single Independent Review and Parent Dispositions

Review executed Complete; outcome Not accepted against whole original request,
while exact-main deployment/preservation/SQL/anonymous scope is verified.
One Review only, original retained unchanged. Independent reconciliation:
380 journal records/732 raw output hashes,20 executor entries/120 proof hashes/
110 archive hashes,16 tool bindings and successful/failed browser provenance,
426 source/archive files, both35-file image receipts and complete protected
original/recovered/final app/auth/history/jobs/ACR/SQL/HTTP comparisons.
No repeated cloud/build/browser or implementation fixes after Review.

RV-001 High accepted: long-lived versioned caching is not delivered by main.
Distinct source-policy follow-up, no waiver or whole acceptance.
RV-002 Medium accepted: employee widget200 and signed-in acceptance remain
unproven; owner-run separate exercise, authentication unchanged.
RV-003 Low accepted: undock button was clicked but post-click state was not
asserted; only open/dock/Escape state is proven. Later bounded rpi-research
reconciliation, no current browser rerun or closure assessment.

Review also qualifies attempt1 archive: it is the verified pre-second-rollout
snapshot taken after the helper correction, not a pristine faulty helper copy.
Original faulty verifier remains reconstructable in the actual retained
apply_patch events, SHA25607fc72e9ac7002d51dee257441c40c35efc08121be7b817366d7201bf277ea01;
corrected archive verifier4480cd044ac8201eaee88c8ae353d77f0486353ff04d169ec9dfcc43a67110dc.
Registry raw response bodies were not retained, only actual publisher-bound
hash receipts; no independent raw-body rehash or fresh registry read is claimed.

P03-T02 original evidence/local commit pending. `git status --short &&
git diff --stat && gh api user --jq '{id,login}' && test -s .gitignore &&
git diff --check && git diff --name-only 4cb5964f -- src infra docs` exit0:
exact eight evidence paths, no source changes, authenticated identity resolved.
Git-commit skill's additional instruction file absent and get_changed_files
tool unavailable; higher repository explicit-path safety/staged diff and
privacy-safe identity/Refs/trailer readback apply instead.
No push/PR/merge/amend/rebase planned or authorized.

## Known Acceptance Limits

Exact current main versions rendered asset URLs but returns no-cache,
must-revalidate for assets and no-store for HTML. Long-lived versioned caching
is not expected to pass; verify actual headers, report unmet.
Employee /app/shared widgets require sign-in; anonymous401 is preserved, not
employee widget200 or signed-in acceptance. No auth/cache source edits inferred.
