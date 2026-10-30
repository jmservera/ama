---
title: Fresh main two-site redeployment changes
ms.date: 2026-10-30
---

## Execution Boundary

Task fc881d21-3ba8-4071-a186-c2dba4fa081e; declared scope full plan.
Source252a498e2001193b0142b4f4ac031096dd6cc2b7=HEAD=fetched origin/main,
PR #568 included. Clean expected branch at intake; no prior PR lifecycle.
Owner standing redeploy/cost authority and narrow ACR public window accepted.
Research Complete/Ready; one critique Complete/Revise, PC001/003 applied,
PC002 rejected unsupported /tmp prohibition; no repeat.
Earlier records preserved. External private root:
/home/azureuser/.copilot/session-state/fc881d21-3ba8-4071-a186-c2dba4fa081e/files/redeploy.

## Initial Commands and Results

`git status --short && git branch --show-current && git log -3 --oneline &&
git rev-parse HEAD && git remote -v` exit0: clean expected branch/pin/origin.
`git fetch origin main --quiet && git rev-parse origin/main &&
gh pr list --head chore/ops-redeploy-1030c --state all --json
number,state,baseRefName && az account show --query '{state:state,name:name}'
-o json && docker info --format '{{.ServerVersion}}'` exit0:
same source, no PR, Enabled expected subscription, Docker29.9.0.
No .env, private dataset, secret or model read/call.

## P01-T01 Active

Execution copies reuse original functions/commands by pinned executor hashes
with current ops SHA/root/build-proof origin and pair coordinator adaptation.
Fresh resource/auth/history/jobs/ACR backups precede builds and all writes.
Literal subprocess argv, exit/time/output hashes are retained privately and
will be exported sanitized; raw backups never committed.

## P01-T01 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 <root>/ops.py && flock -n -E 75
/tmp/ama-rpi-heavy.lock env PYTHONDONTWRITEBYTECODE=1 python3 <root>/build.py`
exit0. Complete fresh backups, min0/eight Manual/private ACR confirmed.
Present optional names: ZF_SQL_AUTH, ZF_SQL_CLIENT_ID. Absent names:
ZF_DEMO_ASSISTANT_ENABLED, ZF_DEMO_ASSISTANT_ENDPOINT. Values never printed.
Both fresh builds hold shared heavy lock; exact original build() reused.
Archive SHA2567f8fe62c6d970dcfbcda67dc53d84b7291903d1bf7f553857d43dc2b7b5899d5,
src tree1bc3b21e0ddcc7d89b31ffcb901928df165066e6.
Tags main-20261030-252a498e2001-resident/employee, actual OCI config hashes
80146216a36c2e6a44031cd507bb6a6944f5f22eee6046848e063d33e81e0419 and
53696080a1217083dbef87ac5124daefadaee574056dab6470e88e5f208455ac.
Source labels/config bytes verified. Scratch image-save tars removed exactly.
No cloud mutation yet; publisher is next.

## P01-T02 Complete

`flock -n -E 75 /tmp/ama-rpi-heavy.lock env PYTHONDONTWRITEBYTECODE=1
python3 <root>/publish.py` exit0. Prior publisher unmodified; current builds
rehashed before push. VM/32/defaultDeny only. Public enable acknowledged
15:18:26.902Z; Disabled confirmed15:18:43.473Z; full exact restoration
15:18:49.824Z. Acknowledged-enabled to confirmed-disabled16.571s, not an
exact service-side exposure duration. Full bounded operation32.687s.
ACR readback equals full stable baseline: public Disabled, admin disabled,
exports disabled, empty IP rules and original default restored.
Both old manifests verified before/after. New index/platform/config/OCI chains
verified; new resident59d5bfd6722a214e4de2c2fe3b1995ce5b7f9ea85eae415c20551d7de6b2304a,
employee dab5e300f2c05deaaf5b9112b756a4b2dc9ed4dbf26e3a8d78c00125f4443311.
Owned Docker credentials removed. No fallback build or cleanup error needed.
P01 complete; P02 private initializer now admitted.

## P02-T01 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 <root>/sql_init.py` exit0.
Single execution job-cutover-test-init-fnjgiv9 Succeeded, one replica/retry0,
post-COMMIT worker/input-bound receipt. Six sensor counts before/after0;
allowlist/view/valid sensor JSON counts522. Existing narrow principal,
17-column projection and hidden ledger columns verified. Current pinned view
source hash625c141707c5bc983c19f81f3c2c7daafc27feb0318896a40af1659d478be939.
Original initializer and standalone decoder function reused unchanged.
Retry restored1, all eight complete job definitions equal baseline/Manual.
No rows/private dataset, model, secret, grant or AI accounting migration.

## P02-T02 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 <root>/rollout.py` exit0.
Resident ca-resident-demo--res-live-20261030-152028 and employee
ca-cutover-test-demo-api--emp-live-20261030-152210 latest=ready,
Healthy/Provisioned/traffic100/ready replica, verified new digests.
One added revision each, all historical revisions retained, protected full
configuration/auth equality and min0. Pair coordinator persisted both outcomes.
No actual failure/recovery/ambiguous-write or cold-timeout path was needed.
P02 complete, warm anonymous verification next.

## P03-T01 Complete

`PYTHONDONTWRITEBYTECODE=1 python3 <root>/verify.py` exit0.
Both warm /healthz first-attempt200, both public shells200 exact-source equal.
Resident /chat-widget.js,/chat-widget.css,/demo.js,/assistant.js200 exact-source
equal. Resident /demo/view401 and anonymous POST/demo/assistant403.
Employee /app,/app.js,/ops.js,/api/me,/chat-widget.js,/chat-widget.css401.
Exact digest targets reverified ready/healthy/traffic100; full protected config/
auth/history retained, one new revision each. All eight complete job definitions
equal/Manual, all four ama app minima0, ACR full stable baseline equality.

Actual Playwright15:23:49.640Z-15:23:53.401Z, fresh anonymous contexts:
both health200/public200 at1365x900 and390x844, no horizontal overflow.
Resident shared script/launcher/dialog present; launcher click opens dialog,
Escape closes, no submit/password. Employee public sign-in link and /app Entra
redirect, query withheld. Resident one unattributed resource404 console error;
employee one image CSP console error; zero page errors. No clean-console,
WCAG, authenticated, actual-model or human acceptance claim.

`git show --format=fuller --stat 252a498e && git show 252a498e -- <selected
web assets> | head -180` exit0 clarified actual PR568 change is employee app.js,
not shared widget. Research/details amended explicitly, no scope change.
`PYTHONDONTWRITEBYTECODE=1 python3 <root>/asset_proof.py && git diff --check
&& git diff --name-only 252a498e -- src infra docs` first exit1, private helper
SyntaxError before any subprocess/cloud action. Missing comprehension closure
fixed; exact command rerun exit0, no source/infra/docs diff. Both published/
deployed image chains contain app.js hash87e53560258cb5f6ee600eab61dbc78309a6645b572069caf33ccb075d1a66d0
and widget hasha3ae12e567df405ff7bcf9394d2f74e2d06367480e560e6d0b9f5078d38bd849,
exact pinned bytes. Docker read-only/no-network/removed containers only.
Employee actual live app.js remains401; this is deployment provenance, not
signed-in Enter/Send behavior acceptance.

## Resident AI Decision

Set names only: ZF_SQL_AUTH, ZF_SQL_CLIENT_ID.
Absent names only: ZF_DEMO_ASSISTANT_ENABLED, ZF_DEMO_ASSISTANT_ENDPOINT.
All existing env values preserved, never printed. AI remains off because older
Oct27 approved-sentence pilot does not establish generated-prose authority.

Owner must decide:

* Authorize generated own-case prose rather than only approved sentence
  selection, or keep off.
* Authorize the two absent assistant settings within existing USD20 ceiling
  and2026-11-01T00:00:00Z tariff expiry, after existing SQL reserve/complete
  procedures/exact EXECUTEs, remaining lifetime/hour allowance and existing
  managed-identity model access are verified.
* If prerequisites require changes, separately authorize bounded accounting
  SQL/exact grants or any new role/secret/cost/expiry change. None is inferred.

Live accounting/allowance/model access was not established and is not diagnosed
missing merely from names. Sensor initializer is not AI accounting evidence.
No model call/activation/new approval performed.

## Export and Review Handoff

`python3 <inline event-schema inspection>` exit0, names/keys only, identifies
actual browser tool event for provenance. `PYTHONDONTWRITEBYTECODE=1 python3
<root>/export.py && git diff --check && git diff --name-only 252a498e --
src infra docs` exit0. Sanitized machine evidence contains205 actual journal
entries with argv/time/exit/output hashes,16 completed outer command-event
bindings including delegated critique shell inspection, one actual browser
code/result/event/hash receipt, original/current executor hashes, full private
backup/proof hashes. Fresh archive matches original exact tracked src archive.
Token-bearing outputs held only in memory and withheld, no token hashes/raw.
Raw resource/auth/history/config backups and outputs retained0700/0600 external.

P01/P02/P03-T01 complete. P03-T02 one independent Review/local commit pending.
No operational blocker; generated-prose authority/accounting/access/allowance,
signed-in employee chat behavior, resident/model/human acceptance and console
attribution are separate later work. No source/tests/dependency changes, so no
application test run needed or claimed; actual cloud/SQL/HTTP/browser checks
performed. No fallback/recovery/failure cleanup retry exercised; no certification
of those branches. No .env/private dataset/model/RBAC/private endpoint/RG
deletion or network exposure outside bounded ACR exception. No full local
publication gate, independent exact-head publication, hosted/human approval
or push is claimed for this local-only operational evidence commit.

## Single Independent Review and Dispositions

Review executed Complete; original outcome Residual work because P03-T02
local persistence was pending at assessment. No implementation defects,
unaccepted operational decisions or material provenance gaps established.
All AC1..7 operational evidence passes; AC8 administrative commit remains.
Independent read-only lens verified205 journal/382 raw hashes,10 current/
7 original executor/105 proof hashes,16 outer command events and one actual
browser event/code/result binding,414 archived source files/symlinks,57 full
resource responses and40 full job comparisons. No cloud/build/browser replay.

RV-001 Low local persistence: parent next action, not an implementation defect.
RV-002 Medium authenticated/model/human acceptance: later owner-selected
exercise; no issue closure. RV-003 Medium generated-prose authority/prerequisites:
later owner decision, preserve off. RV-004 Low disclosed console errors:
later attribution, no current source/policy repair inferred. Original Review
unchanged; no second Review or post-Review implementation.

`git status --short && git diff --stat && gh api user --jq '{id,login}'`
exit0: exact expected nine-path evidence set, authenticated privacy-safe identity
resolved. Git-commit skill's additional instruction file was absent and its
get_changed_files tool unavailable; repository-required explicit staging,
Git diff checks and identity/Refs/trailer readback are used instead.
Local commit proof will be recorded after execution, not presumed here.

## Local Persistence and Task Closeout

`PYTHONDONTWRITEBYTECODE=1 python3 <root>/commit.py` exit0:
nine explicit evidence paths committed as8507e31cdfd16d00dddd34e7def9b0d510f75588,
`chore(ops): redeploy both demo sites from main 252a498e`.
Every helper subprocess check=True: nonempty .gitignore, correct branch,
initial empty index/exact nine changed paths, JSON/sensitive-marker/whitespace
checks, fresh gh api user, computed repository-local privacy-safe identity for
author/committer, explicit staging/exact staged set, commit via STDIN and exact
message/email/trailer/clean-tree readback. Refs #563/#550/#568 only and required
Copilot trailer verified. Actual local-commit-proof.json remains external.
No push/PR/merge/amend/rebase/history rewrite.

Original Review Complete / Residual work preserved, not reclassified or
repeated. Its RV001 administrative local-persistence action handled here.
All P01/P02/P03 complete. RV002 signed-in/model/human acceptance, RV003 AI
activation/prerequisites and RV004 console attribution remain distinct later
owner-selected work; no current operational blocker or inferred acceptance.
Full requested manual RPI sequence complete; session stops with AI off.

This final four-file plan/details/state/changes administrative reconciliation
is persisted by `PYTHONDONTWRITEBYTECODE=1 python3 <root>/commit.py --closure`
with the same fresh identity, exact paths, Refs/trailer and clean-tree checks.
Its actual commit/result is retained externally in closure-commit-proof.json
and session events rather than predeclared successful here. No cloud/source
change or second Review follows. No publication receipt/human approval claimed.
