---
title: Current-main routing two-site redeployment changes
ms.date: 2026-10-31
---

## Execution Boundary

Task439ddfed-247a-4d5a-85ce-c60e9b939be3; demo-sites-redeploy-routing.
Owner requested finite full RPI loop; manual full-loop progression authorized.
Clean chore/ops-redeploy-routing at84035ae9, no open PR; fetched main includes
#611 at9ecb159bd843411c2e17dc2785ab59f5e837040f and fast-forwarded cleanly.
Original #596 and latest cache8 evidence/procedures reused; read required context.
Research Complete / Ready. One critique Complete / Revise, PC001-003 applied
directly: timeout-only inner/outer branches do not compensate; independent
employee identity prerequisite; protected signed-in cache/source proof.
No repeat critique. Standing deployment/short IP-only ACR window authority
accepted through2026-11-15. Resident AI OFF.

## Intake Commands and Results

`git status --short && git branch --show-current && git log -1 &&
git fetch origin main --quiet && git show origin/main:<#596 changes path>` exit0:
clean matching topic; previous original redeploy evidence retrieved.
`git rev-parse HEAD origin/main && gh pr list --head chore/ops-redeploy-routing
--json number,state,baseRefName && git log -8 origin/main &&
git diff --name-only 4cb5964f origin/main -- infra src` exit0:
fresh main9ecb159b ahead of initial84035ae9, no open PR.
`git merge --ff-only origin/main && git diff 4cb5964f HEAD -- <SQL-related paths>
&& az account show --query '{subscription:id,state:state}' -o json &&
docker info --format '{{.ServerVersion}}'` exit0, Enabled expected subscription,
Docker29.9.0. `git diff --name-only 4cb5964f HEAD -- '*.sql'` empty, but persisted
SQL SELECT and SQL job transport source changed; caller SQL-touch condition holds.
Python Playwright import succeeds. No credentials or .env read during research.

## P01-T01 Preparation

Private executor/backups/output root:
/home/azureuser/.copilot/session-state/439ddfed-247a-4d5a-85ce-c60e9b939be3/files/redeploy.
Raw config/auth/history and outputs remain external0700/0600.
Source9ecb159b; distinct main-20261031-9ecb159bd843-routing9 release.
Original retained helpers unchanged; adapters hash-bound before cloud mutation.
SQL init will reuse narrow #596 counts-only procedure, not deploy changed staff
transport or broaden schema/permissions. P01 in progress.

`chmod700 ROOT && chmod600 ROOT/*.py && python3 ROOT/preflight.py &&
python3 ROOT/ops.py && flock -n -E75 /tmp/ama-rpi-heavy.lock ...build.py &&
python3 ROOT/verify.py --images` exited75 at lock admission. Fresh backups
complete, both min0/eight Manual/private ACR/AI settings absent passed.
No build or cloud mutation. `lslocks` confirmed another process owns shared
heavy lock; no process killed, bypass or unowned cleanup. Wait/retry admission
while preparing independent bounded browser automation.

## P03-T01 Independent Preparation

Credential preflight first returned blocked format (zero attempts). Metadata-only
format inspection found resident two-line and employee password-only formats;
reused existing live-azure-verification.py format/directory procedure.
Corrected preflight exit0: both credential formats usable, independent employee
directory attestation denied/unavailable. No values printed or signed-in
submissions. Employee checks blocked before sign-in, actual attempts0.
Resident remains eligible with fresh maximum2 budget. Current capture-free
browser executor asserts actual own-case Summary by rules and unknown examples;
no screenshots/traces/storage state/body exports. Failure of acceptance alone
does not compensate live deployment.

## P01-T01 Complete

First bounded20 admission attempts ended75; immediate retry75. Extended
nonblocking admission acquired after six occupied attempts; both builds and
`verify.py --images` exit0. Same shared lock, no queue bypass/process interference.
`adapter_check.py && preflight.py` exit0: constructed offline converge/finish/
pair deadline branches never call recovery, zero cloud/browser/SQL calls.
Source archive SHA256ba27db75ca17909f3623cad3e901fe6b31389fcf6bb78ef14f21836091dc1697;
src tree2c8b5f6217460360862194759b18be70d823527c.
Local resident config6c864062d849cc3d5c6414171ff92943aa7cbdf8349132d425cd7cd513570925;
employee configaf405343983d3a4585758d065ab188b5e37bdcece3c6b33faab3c3e37b54d9a9.
Both packaged web receipts match concrete archived source subdirectories.
Local proof passed before any ACR write; publication next.

## P01-T02 First Window Failure and Reconciliation

`preflight.py && flock -n -E75 ... publish.py` exit1 at resident Docker push.
Publisher finally restored exact private ACR before returning failure.
Fresh readback confirms full stable ACR equality and both full apps unchanged.
Public enable acknowledged17:58:21.077998Z; Disabled confirmed17:58:54.269282Z;
exact restoration17:58:59.764423Z, acknowledged interval33.191284s,
bounded operation47.995s. Actual service-side exposure is not asserted.
No verified new manifest receipt; remote push completion is not assumed.
Safe private log categorization identifies firewall/public-network category,
not timeout/auth/disk. Raw outputs remain private. Token/login/old manifest GET
succeeded, so public access is not established impossible; propagation remains
an unproven possibility.

Immediately relevant publisher adapter: retain original guarded window/finally
and cache8 token acquisition. Before every Docker push, read remote exact tag;
404 admits publication, existing exact config skips repeat, differing/unclassified
tag blocks. A failed push must be reclassified by GET before at most two retries
with3s backoff; never blindly repeat a potentially completed manifest write.
No source/policy/authority change or repeat critique. If unavailable after this
classified attempt, assess owner-authorized az acr build from restored private
baseline. Preserve first-window receipt and executor before new window.

## P01-T02 Complete

`archive selected first-window receipts with copy/hash readback && preflight.py &&
flock -n -E75 ... publish.py` exit0. Second window public-enable acknowledged
18:01:06.351044Z; Disabled confirmed18:01:22.869562Z; exact restore18:01:28.467612Z.
Acknowledged interval16.518518s; bounded operation32.358s, not exact service-side
exposure. VM/32/defaultDeny only, full prior private/default/rules/admin/export
config restored/read back. Both current image configs/source labels/platforms/
RepoDigests verified; old live manifests preserved before/after. Token and owned
Docker credentials never printed; owned config removed by retained finally.
Both target tags confirmed absent404 before successful push, no same-window
retry or az acr build fallback needed/exercised.

| Image | New index digest (sha256) | Platform digest (sha256) |
| --- | --- | --- |
| Resident | 5fa6d9d83ecad5b06bce42beab27f4c53d0ebc162a9ddff5624195ce88b75300 | de0cee0ee5445bcb4a60c5ddc92b7d7b18961e19eb0a6965173e482358c244f9 |
| Employee | 04538b7606e4f924e94e7d10bb394877ffead5072938e7e8e7e144338241165c | 29077cacbbb96ab77cfe426c7d406bc88f362efbff4e36c9db25a87cdc035bb7 |

P01 complete. Narrow existing init next because SQL-touch condition holds.

## P02-T01 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 ROOT/sql_init.py` exit0.
Exactly one in-VNet execution job-cutover-test-init-k04xk8d Succeeded, one
replica, retry0. Post-COMMIT worker/input SHA256 marker verified.
Six sensor table counts before/after0; allowlist/view/valid sensor JSON counts522.
Narrow resident principal, exact17 projection columns and existing four hidden
ledger metadata columns/table verified. Applied view batch hash unchanged:
86747aa207f64341ec341910396b91fc57454bb8c1d58644c4710f7f3860ef70.
No row content, authority-window, grant/accounting or new DDL applied.
Retry restored1; all eight full job definitions equal original baseline/Manual.
Existing initializer transport reused, no new staff transport/RBAC deployed.
P02-T02 pair rollout next.

## P02-T02 Complete

`preflight.py && rollout.py` exit0. Resident res-live-20261031-180318 and employee
emp-live-20261031-180457 latest=ready/Healthy/Provisioned/100% traffic/ready replica,
exact new published index digests. One added revision/app, all original history/
protected full config/auth retained, min0. Pair proof persisted. No live
recovery, timeout or ambiguous forward branch exercised; constructed offline
timeout proofs are distinct, not live failure certification. P02 complete.

## P03-T01 Curl Complete and Browser Preparation Correction

`verify.py && browser.py` curl verifier exit0, browser exit1 before sign-in.
Curl both first-warm health200; both public shells200/source-equal/no-store.
Every versioned public asset200/source-equal with exact
`public, max-age=31536000, immutable`; resident widget/assistant/demo/dock
bytes present. Employee app/api/widget/app/ops protected401; resident view401.
Full protected config/auth/history/eight Manual definitions/private ACR and all
four ama minima0 passed. No live compensation.
Actual browser dock button locator timed out because its size-details disclosure
was collapsed; this is an automation error, not absent live dock bytes.
No sign-in started, actual resident0/employee0. Original browser/executor/
manifest/attempt receipts copied and readback-hash verified privately.
Current adapter opens size details before the dock action, as retained original
live procedure does. Resume only from verified zero-slot pre-sign-in state;
no credential retry, reset or cloud mutation. Original failure retained.

Corrected browser invocation failed a second anonymous assertion after resident
desktop passed: employee public logo is an img URL, omitted by script/stylesheet
DOM selector. Current selector includes img[src], matching the retained curl
source URL set. Original second executor/partial browser receipt archived and
hash verified. Both actual sign-in counts still0. No deployment change or
compensation; exact route/source/cache assertions are retained, not weakened.

Third invocation: all four anonymous desktop/mobile browser observations pass.
Resident signed-in automation failed AssertionError after consuming one slot;
employee blocked with zero slots. Original receipt retains unclassified failure
(exception/body details withheld), not a live login or routing defect claim.
Current source inspection identifies direct own-case GET missing the mandatory
X-Resident-Session header (app explicitly returns409 for that request); canonical
UI sends it. Adapter now uses login's session_id only in memory for that GET,
records fixed stage/status before assertions and preserves original attempt.
One remaining resident slot under original at-most-two budget is used for the
corrected bounded exercise. Completed anonymous checks are reused, not rerun;
no employee attempt, budget reset, auth bypass or deployment compensation.

## P03-T01 Final Actual Playwright Results

`preflight.py && browser.py --resident-remaining-slot` exit0. Corrected resident
bounded acceptance18:10:36.448993Z-18:10:55.680061Z:
sign-in200, session-bound own-case view200; both "How's my case going" and
"Is my case blocked?" return200 with Summary by rules, exact case
progress/closed/next-step answer equality and Where things are/What happens
next sources, actual rendered answer/label equality. Unknown input returns200
but refuses, includes example questions and Assistant task limits source.
Two actual resident sign-in submissions total (one prior unclassified automation
failure, one successful corrected exercise), zero employee. No further slots
or sign-ins attempted. Record consent only, no works/callback/AI authority.
Resident AI remains OFF, no actual model request.

Four completed anonymous Playwright observations at1365x900 and390x844:
both health/public200, source-bound versioned asset200/immutable-year headers,
HTML no-store, resident open/dock/undock/Escape poststates and full-height
dock900/844px. No horizontal overflow; GET-only page request methods.
Employee public shell only and browser protected302 Entra origin; curl401
preserved. Pageerrors0 in all contexts; console error counts retained, not a
clean-console/accessibility diagnosis.
Employee independent directory attestation remains unavailable: signed-in
chat/capacity and protected widget200/source/cache are BLOCKED/unproven.
This is bounded synthetic resident acceptance, not real resident identity,
full employee/map/case, model, human/safety/legal/operational acceptance.
P03-T01 partial against whole signed-in request; deployment remains healthy,
no compensation for acceptance/tool errors.

## P03-T02 Export and Pre-Review Reconciliation

`preflight.py && final_readback.py && export.py && git diff --check &&
git diff --name-only 9ecb159b -- src infra docs` exit0. Post-browser fresh full
protected app/auth/history/eight complete Manual job/ACR baseline comparisons
pass; all four minima0, resident AI settings absent/OFF. No source/infra/docs
change. Sanitized evidence255 journal commands and38 outer event-bound command/
read results, all stdout/stderr retained hashes verified. Current/transitive
helpers compile/hash-bound; source archive equals exact tracked source.
First failed window, three prior browser executor/attempt receipts retained
and hash-bound; registry raw response bodies not retained, only actual
publisher-bound hashes (no independent raw-body rehash claim).

Implementation partial against full signed-in request: P01/P02 and anonymous/
resident scope proven; employee attestation/chat/capacity/protected cache
unproven. P03-T02 export complete, one independent Review/local commit pending.
No further operational correction or cloud/browser replay planned. Original
critique unchanged; plan/details/state/current evidence reconciled.
Push/PR blocked by explicit no-push direction versus final PR request.
Complete exact-head local publication gate, hosted/human approval not performed
or claimed; no skip token/cloud fallback/protection change.

## Single Independent Review and Parent Dispositions

Exactly one Review executed Complete / Residual work, implementation Partial
against the complete signed-in/publication request. Original preserved unchanged.
Independent read-only reconciliation:255 journals/456 output hashes/38 actual
event-bound results;30 current/transitive executor entries;431 archived source
files/70 packaged resource hashes; two protected apps/auth and41 retained
revision templates; eight full Manual jobs/four minima0;16 curl responses/
four anonymous observations/three actual resident answer receipts.
No cloud/browser/build/SQL/scanner rerun during Review.

RV-001 High accepted: employee independent identity/signed-in chat/capacity/
protected cache unproven, later rpi-research with owner/admin attestation.
RV-002 Medium accepted: no-push/PR authority conflict and complete exact-head/
hosted/human gates outstanding, distinct publication follow-up; keep blocked.
RV-003 Low accepted: local administrative persistence pending, active parent
exact-path commit next. No repeat Review, operational fix or closure assessment.
Resident AI activation remains separately owned and OFF.
Review preserves registry raw-body limitation, reconstructed first wrapper,
original unclassified third browser failure and unexercised live recovery.

## Local Persistence Admission

`git status --short && git diff --check &&
git diff --name-only 9ecb159b -- src infra docs && gh api user --jq '{id,login}'`
exit0: exactly eight dated evidence artifacts, no source/infra/docs changes,
fresh authenticated account resolved. Referenced git-commit instruction file
unavailable and get_changed_files tool absent; higher repository exact-path
staging/staged diff/privacy-safe identity/Refs/trailer safeguards apply.
No private/global email change, broad staging, push, PR, merge or rewrite.
Original eight-artifact local commit next; actual receipt remains private.
