---
title: Current-main demo redeployment changes
ms.date: 2026-10-30
---

## Execution Boundary

Task870037be-e9ad-4240-8734-fa056bea01df; demo-sites-redeploy-1030b.
Declared scope: full plan, partial execution explicitly blocked at P02.
Manual full sequence authorized by current request; no ongoing automatic loop.
Source a72cb268e11f2fc744d299b2b72bdcb1e05b5d6f=origin/main after fetch,
clean matching chore/ops-redeploy-1030b at intake; no existing PR lifecycle.
Owner standing redeployment authority and USD337.19/700 admission acknowledged.
No new cost query or broader approval inferred.

## Research and Plan

Both prior redeploy changes read; final admitted executors inspected. Original
initial blocked evidence and later successful correction/Review remain unchanged.
One three-wave focused Research complete. One critique Complete/Revise:
PC-001 claims a nonexistent parent /tmp prohibition; rejected with exact shared
lock prior art, not silently rewritten. No repeat critique.

## Pre-implementation Commands and Results

| Command | Actual result |
| --- | --- |
| git status --short; git branch --show-current; git log -1 | Clean expected topic and a72cb268 |
| gh pr list --head chore/ops-redeploy-1030b --state all --json number,state,baseRefName | exit0, no PR |
| git fetch origin main; git rev-parse HEAD origin/main | exit0, both exact expected source |
| command -v az; docker info --format '{{.ServerVersion}}' | exit0, az present, Docker29.9.0 |
| gh api user --jq '{id,login}' | exit0, privacy-safe identity resolved |
| getent ahostsv4 crcutovertestrzsrg.azurecr.io | exit0, public51.143.208.11 |
| curl --silent --show-error --connect-timeout15 --max-time40 --output /dev/null --write-out 'ACR HTTP %{http_code}' https://crcutovertestrzsrg.azurecr.io/v2/ | exit0, HTTP403 |
| az account show --query '{state:state,id:id}' -o json --only-show-errors | exit0, expected enabled subscription |
| az containerapp show -g ama -n ca-resident-demo --query '{settings:properties.template.containers[0].env[].name,minReplicas:properties.template.scale.minReplicas,image:properties.template.containers[0].image}' -o json --only-show-errors | exit0, min0, previous live image; names-only settings |
| az network private-endpoint list -g ama --query '[].{name:name,subnet:subnet.id,dns:customDnsConfigs}' -o json --only-show-errors; ip -4 route | exit0, existing endpoints; host172.16.0.4 outside cutover VNet |
| curl --resolve crcutovertestrzsrg.azurecr.io:443:10.40.4.20 --connect-timeout10 --max-time20 ... /v2/ | exit28, TCP timeout; historical address subsequently confirmed as data endpoint, not login |
| az network private-endpoint show -g ama -n pe-crcutovertestrzsrg --query 'networkInterfaces[].id'; az network private-dns record-set a list -g ama -z privatelink.azurecr.io --query '[].{name:name,ips:aRecords[].ipv4Address}' | exit0, login10.40.4.21/data10.40.4.20 |
| curl --silent --show-error --connect-timeout15 --max-time30 --resolve crcutovertestrzsrg.azurecr.io:443:10.40.4.21 --output /dev/null --write-out ... https://crcutovertestrzsrg.azurecr.io/v2/ | exit28 after15s, confirmed private-login TCP timeout |

Literal argv and result hashes for implementation are exported from the private
journal. Pre-implementation tool commands above retain original tool transcript;
spacing elisions in this human table are not executable replacement commands.

## Active Implementation

Private evidence root:
/home/azureuser/.copilot/session-state/870037be-e9ad-4240-8734-fa056bea01df/files/redeploy.
Fresh full private backups complete; both app minima0, eight jobsManual, ACR
private/exportDisabled/adminDisabled/no IP rules. Separate auth/history retained.
`PYTHONDONTWRITEBYTECODE=1 python3 <root>/ops.py && flock -n -E 75
/tmp/ama-rpi-heavy.lock env PYTHONDONTWRITEBYTECODE=1 python3 <root>/build.py`
exit0. Exact original build() AST reused with fresh root/currentSHA, two builds
held under shared lock. Tracked src archive SHA256
badf877b48f1ccb741a1621ab993115f3e7cd1f92b0de8b61bb37da4a7af8496;
src tree e767a88b8c153baa6777351d2c40e1d6c34ff345.

| Image | Local image ID | Actual config SHA256 |
| --- | --- | --- |
| resident | 00abe43d90ac9708ba7b250869611251eb27bfed1f5c96fffadbeb470b4ff38b | 654e42dabf89641b2f135f9c16f7bbfc007dee15a356c0f38b4c355fa27cd628 |
| employee | 2aabba75cea68274378bf445d3ef0974971f7671e0f383729d296e824e4fa686 | 2712e66541405f6be0810f56fed0f9b77f55acb2133bff89b3fce6422c404e16 |

OCI source labels/config bytes verified; unique main-20261030-a72cb268e11f tags
are LOCAL ONLY. Scratch saved-image tars removed by exact owned filenames.
No ACR token/policy/network mutation,
SQL job, rollout, AI activation, model call, .env or private dataset read.

## Blockers and Remaining Work

P02 blocked: exact previous publisher changes public network, forbidden now;
confirmed private-login route inaccessible. No alternative/new execution host,
role, endpoint or exception invented. No rollback is needed without owned
forward deployment. Keep eightManual/min0/config/ACR unchanged.

Resident optional prerequisite names present: ZF_SQL_AUTH, ZF_SQL_CLIENT_ID.
Names absent: ZF_DEMO_ASSISTANT_ENABLED, ZF_DEMO_ASSISTANT_ENDPOINT.
No setting values disclosed. AI remains off. Owner must confirm generated-prose
activation is within the older sentence-selector pilot, and separately authorize
any missing accounting SQL migration/exact EXECUTEs; verify remaining lifetime
allowance and existing MI access first. No additional inference/cost, role or
secret approval is assumed. The tariff still expires2026-11-01T00:00:00Z.
Live SQL accounting and authenticated-model quality remain unverified, not
diagnosed absent from environment names.

## P03-T01: Current Live Verification

`PYTHONDONTWRITEBYTECODE=1 python3 <root>/verify.py` exit0. Curl warmed both
/healthz with180s per attempt and bounded900s retry loop; each first attempt200,
no app cold-start timeout in this run. TCP registry timeouts above are separate.

| Route/boundary | Actual result |
| --- | --- |
| Both /healthz and public / | 200 |
| Resident /chat-widget.js,/chat-widget.css,/demo.js,/assistant.js | 200 |
| Resident /demo/view | 401 |
| Resident anonymous POST /demo/assistant, no credentials/origin/session | 403, no model |
| Employee /app,/app.js,/ops.js,/api/me,/chat-widget.js,/chat-widget.css | 401 |

Both public shells and resident shared widget/demo.js are current-main byte
equal. Resident assistant.js is NOT current-main byte equal, consistent with
undeployed PR564; it is not labelled a successful new-source check. Existing
resident/employee targets remain res-live-20261030-085634 and
emp-live-20261030-091952, Healthy/Provisioned/traffic100. Zero added/removed
revisions. Full protected app, separate auth and revision templates equal fresh
baseline. Eight exact complete job definitions unchanged/Manual; all four app
minima0; stable full ACR exact equality. No remote old-manifest presence claimed.

Real Playwright in fresh anonymous contexts: both public pages200 at1365x900
and390x844, no horizontal overflow; health200. Resident shared script1/dialog1;
initial probe used wrong `.zf-chat-launcher` selector and returned0, not proof
of absence. Correct repository `.chat-widget-launcher` probe returned1 visible
at both widths; opening it expands one visible dialog without submission or
credentials. Both actual raw tool results retained, original not overwritten.
Employee public sign-in link present; /app reaches login.microsoftonline.com,
only final origin/path retained. No password/session import/model invocation.
Initial resident console has one resource404 with no attributed response;
employee image CSP error at both widths. No clean-console or WCAG claim.

Direct browser command/result provenance will be recovered from this session's
actual tool events, not reconstructed DOM literals. No screenshots were needed
or claimed; two direct browser result receipts are the retained evidence.

## Export and Review Handoff

`PYTHONDONTWRITEBYTECODE=1 python3 <root>/export.py && git diff --check &&
git diff --name-only a72cb268 -- src infra docs` exit0; source/infra/docs diff
empty. Sanitized evidence JSON contains67 child commands with actual exit/time/
argv and134 raw-output hashes,12 completed outer shell commands with tool-event
bindings and two actual browser results/code/event/hash bindings. Private raw
backups and proof/executor hashes retained externally. Every nonzero command is
preserved, including expected resident auth absence and both private TCP probes.
Export/administrative closeout commands remain in the durable session transcript.
No private dataset/.env, secret output or model call; no registry/app/SQL/job/
role/network/policy write. No application tests necessary for evidence-only
changes; actual two builds and required live verification executed. No full
local publication gate or remote/human approval claimed. P01/P03-T01 complete,
P02 blocked, P03-T02 pending. Full deployment remains Partial/Blocked.

## Original Independent Review

Exactly one Review executed Complete; outcome Not accepted for full deployment.
Original canonical Review retained unchanged after completion. Independent
read-only lens matched all67 journal/134 output hashes,4 executor/38 proof
hashes,12 outer tool bindings, exact archive/413 source files, actual local
image/config labels and both raw browser receipts. Full app/auth/history/
eight-job/ACR preservation independently corroborated; no unauthorized mutation
or executed source defect found. No cloud/build/browser replay by reviewer.

RV-001 High: full deployment undelivered; later owner-approved publishing path/
network decision, then fresh source/drift and rollout gates.
RV-002 Medium: generated-prose authority/accounting/access/allowance unestablished;
keep AI off; later owner decision and bounded prerequisite verification.
RV-003 Low: authenticated resident/employee and actual-model acceptance remain
separate; public console residuals need separate attribution. No issue closure.
Findings routed once, no post-Review implementation or repeated Review.

## Local Persistence Boundary

Original eight dated task artifacts committed locally as
baef7d8f33970cddd8af7250736ec9bd7caf00f2 with fresh authenticated privacy-safe
author/committer identity, Refs only and exact Copilot trailer. `test -s .gitignore`,
whitespace/status checks, fresh `gh api user`, repo-local name/email config,
exact eight-path stage equality, JSON/sensitive-marker checks, staged diff check,
`git commit -F -`, author/committer/trailer readback and clean-tree check all
succeeded. No push, PR, merge, amend or publication receipt.
The requested full RPI sequence is complete, but redeployment is NOT complete.
P02 remains blocked. This final parent-status/marker update is administrative,
persisted separately without modifying original critique/Review/machine evidence
or performing post-Review implementation. Private backups, local images and
raw receipts retained. Owner needs an authorized publishing path before a
fresh admitted rollout; the existing sites and AI default-off state are unchanged.

## Owner-selected Publishing Continuation (13:10Z Update)

The original blocked execution and Review above are unchanged historical records.
Owner now explicitly authorises the short VM-IP ACR window and selects RV-001
continuation in this same worktree. Child demo-sites-redeploy-1030b-publish
preserves one critique/Review per task rather than repeating the original
assessment. Dated research/plan/details/changes/machine evidence use that slug.
Child changes:
.copilot-tracking/changes/2026-10-30/demo-sites-redeploy-1030b-publish-changes.md.
Both current-main images now published, initializer Succeeded, both exact new
revisions healthy/ready/traffic100, ACR exact private restoration, min0/eight
Manual preserved. New-source curl/browser anonymous checks complete; child
independent Review/local persistence follows. AI remains off; original RV-002
activation and RV-003 authenticated/model acceptance boundaries are not closed.
