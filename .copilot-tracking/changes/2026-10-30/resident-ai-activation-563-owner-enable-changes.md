---
title: Resident AI 563 owner-enabled commands and results
ms.date: 2026-10-30
---

## Execution Boundary

Full continuation plan, task563-owner-enable-20261030T1710Z.
Prior seven resident-ai-activation-563 artifacts preserved unchanged.
Owner decision 2026-10-30T17:10Z, verbatim:
"Enable AI, I will take care of checking the cost and will warn you if there's a problem".
Live ledger pre-read waived. Owner monitors actual cost; configured USD20
ceiling, exclusive 2026-11-01 expiry and runtime fail-closed admission unchanged.
Redeploy authority through2026-11-15. Only resident app, no push, Refs #563.
One critique Complete/Revise; PC-001 applied, PC-002 rejected with parent
boundary rationale in plan. No repeated critique.

## Research and Planning Commands

All source/evidence reads used view/rg/glob, covering the previous research,
plan, details, critique, changes (including gate result), Review and state;
original/addendum, reference index opening/memory/sector primer; current
API guide, advisor, host routing, chat guidance, SQL definitions, existing
scripted browser and actual live acceptance source, gate guide/lock implementation.
No credential file, private dataset or live SQL was read.

* `git status --short && git branch --show-current &&
  git --no-pager log -3 --oneline &&
  gh pr list --head ops/resident-ai-activation-563 --json number,state,baseRefName &&
  find .copilot-tracking -type f -path '*2026-10-30*' -name '*resident-ai-activation-563*'`:
  exit0, clean requested topic, HEAD4f61a9cb, no open head PR, seven originals.
* `wc -l <original artifacts>; cat <original state>; git remote -v;
  gh issue view 563 --json title,body,state`: exit0, original automatic
  completed safe-stop state, issueOPEN; no criteria altered.
* Batched `cat` of all originals: exit0,74.1KB output truncated by tool;
  individual view reads then covered complete originals.
* `az containerapp show -g ama -n ca-resident-demo --query <safe projection>
  --only-show-errors -o json`: exit0, expected image59d5bfd6, original
  res-live-20261030-152028, Single mode, no assistant vars, min0/max1,
  existing SQL msi/client and attached id-resident-demo.
* `az cognitiveservices account show -g ama -n aoai-resident-469 --query
  '{id:id,endpoint:properties.endpoint,disableLocalAuth:properties.disableLocalAuth}'
  --only-show-errors -o json`: exit0, expected endpoint, local keys disabled.
* `az cognitiveservices account deployment list -g ama -n aoai-resident-469
  --query '[].{name:name,model:properties.model,sku:sku}'
  --only-show-errors -o json`: exit0, resident-mini/gpt-4.1-mini2025-04-14,
  Standard capacity1.
* `az containerapp job list -g ama --query
  '[].{name:name,trigger:properties.configuration.triggerType}'
  --only-show-errors -o json`: exit0, eight Manual.
* `az role assignment list --assignee-object-id
  ab308885-7010-41b8-8b70-9ef5eabe40d0 --scope
  /subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aoai-resident-469
  --query '[].{role:roleDefinitionName,scope:scope}'
  --only-show-errors -o json`: exit0, existing account-only OpenAI User.
* `command -v az; python3 -c <importlib availability>;
  ls -d .venv src/api/.venv; git ls-files <resident check patterns>`:
  final exit0; no project venv found, system Playwright unavailable,
  mssql_python/azure.identity available. No SQL access attempted.
* `az containerapp update --help | grep <env/suffix>;
  az containerapp revision activate --help;
  az containerapp revision copy --help; python3 -m pip show playwright`:
  final exit1 due missing Playwright; surgical env/revision commands confirmed.
* `rg <flock/SQL/group patterns> tools/rpi-checks.py`: source inspection,
  existing native shared lock and600s default; no gate executed yet.
* Independent critique: one bounded agent; original Revise with PC-001/002.
  No Azure, browser or model action by agent.

## P01-T01: Tooling and Backup

External private root:
/home/azureuser/.copilot/session-state/c7443ccc-e490-4e9d-ba2f-e853675ecf68/files/resident-owner-enable.
Raw responses/helpers stay external; safe command/result annex will be linked
here. No secret values requested. No lock for Azure or live browser work.

`umask 077; mkdir -p <private-root>; python3 -m venv
<private-root>/browser-runtime; <private-root>/browser-runtime/bin/pip --quiet
install playwright==1.64.0; <venv-python> -c <launch/close Chromium>`:
exit0, Chromium156.0.8078.4 responsive. Installed only after actual missing
package failure; no manifests or shared runtime changed.
`az containerapp list -g ama --query '[].name' --only-show-errors -o json &&
git diff --check`: exit0, resident plus ca-cutover-test-api/agents/demo-api.
Employee APIs are read only for preservation hashes, never modified.
Read tracking-retention policy; generated heavy/raw output stays external.

External activate.py created with apply_patch, then
`chmod700 <private-root>; chmod600 <private-root>/activate.py;
<venv-python> -c <ast.parse script>; PYTHONDONTWRITEBYTECODE=1
<venv-python> <private-root>/activate.py`: syntax valid; execution in progress.
Automation persists sanitized command argv/time/exit and raw-output SHA256
before/after each command, keeps raw stdout/stderr protected externally.
Backup capture precedes mutation, persistent login-attempt counter before
submit, no debug/recordings, fields masked/cleared, core dumps disabled.
Exception details withheld except fixed internal failure codes.
Runtime uses no heavy lock. Any changed-candidate failure invokes restoration.

The script holds the same browser session across rollout; a genuinely generated
answer pauses for executor claim/source assessment, never auto-accepting merely
known labels. No additional inference is used for that content assessment.

## P01-T02: Baseline Passed; First Rollout Check Failed

Original activate.py exit2. One real form sign-in returned200, masked/cleared,
no recordings. Health200; anonymous403; client no-consent produced no assistant
request; server use_record=false400. Consented disabled pest request200,
label "Summary by rules - AI is not enabled", repair guidance/manual route and
collapsed sources. No actual-model request was submitted in this first run.
Six before captures and six enabled captures all exit0; hashes/argv in private
sanitized-results.json. Two-var CLI update exit0.

Strict env comparison failed before model verification. Diagnostic projected
only differing field names/Boolean checks: CLI serialization adds value=""
alongside the two unchanged secretRefs. No secret value changed or was read.
Other template/config/identity/auth/jobs/employee/min0 checks all passed.
Automatic removal of both variables exit0. Immediate original-revision activate
exit1, RevisionAlreadyInRequestedState. This was not restoration success.

Additional recovery/diagnostic commands, with raw config kept private:

* Safe Python sanitized-result/command summary plus config-diff paths:
  exit0; failure confined to effective-env shape.
* `az containerapp show <safe revision/assistant/min projection>` and
  `az containerapp revision list <safe health/traffic projection>`: exit0;
  assistant vars removed, original still serving while rollback activating.
* Python env-shape/Boolean comparison: exit0; exact same secretRefs and
  empty-string-only additional values. No secret data emitted.
* `az containerapp ingress traffic set --help` and revision help: exit0.
* `python3 <private-root>/restore_exact.py`: exit1; ARM2024-03-01 rejects
  SDK response-only imageType. No template mutation applied.
* `az provider show -n Microsoft.App --query
  'resourceTypes[?resourceType==`containerApps`].apiVersions'`: exit0;
  supported2026-07-01 available.
* `python3 <private-root>/template_patch.py restore`: exit1; current schema
  also rejects response-only imageType.
* `python3 <private-root>/template_patch.py restore writable`: exit1;
  after omitting imageType, rejects SDK-only null customMetricsSettings.
* Python template field/type summary: exit0; identifies SDK-only null fields.
* `python3 <private-root>/template_patch.py restore normalized`: exit0
  acceptance with empty response, not completion. Subsequent management query
  reports provisioningFailed attempting reused suffix; original failure retained.
* Python parse of empty PATCH response: exit1 JSONDecodeError; no values emitted.
* `az containerapp revision activate -g ama -n ca-resident-demo --revision
  ca-resident-demo--res-live-20261030-152028 --only-show-errors -o none`:
  exit0 once old revision inactive; does not change traffic.
* `az containerapp ingress traffic set -g ama -n ca-resident-demo
  --revision-weight ca-resident-demo--res-live-20261030-152028=100
  --only-show-errors -o none`: exit1, Single mode prohibits traffic targeting.
  No mode change attempted.
* Repeated safe app/revision projections and `date -u`: exit0; disabled
  rollback revision healthy100%, original baseline not current traffic.
* `git diff --stat; git diff --check; gh api user --jq '{id,login}';
  git status --short; lslocks <heavy-lock filter>`: exit0; requested evidence
  only, privacy-safe identity available; foreign lock processes untouched.

## Immediate P01-T03 Execution Refinement

Ordinary evidence-check/rollback refinement, no new owner decision or critique:
normalize only inert value="" when a secretRef is present; never ignore actual
reference/value changes. Require latestRevision==latestReadyRevision and
Succeeded provisioning before live proof. Single-mode rollback must restore
exact effective baseline in a fresh ready revision100%, not target old traffic.
No mode, image, secret, identity, network or job change is authorized.
The first failed attempt and all rejected ARM payload/results are preserved.

retry_verified_rollout.py imports the unchanged original helper and overrides
only effective-env comparison, wait-for-readiness and supported rollback.
Fresh attempt2 private backups/results; persistent login counter starts at1,
allowing only the second and final submission. Still zero paid requests so far.
P01-T01/T02 baseline completion is supported; activation remains Unmet pending
the second bounded run. Full original config bytes remain preserved.

## P01-T03: Final Bounded Run and Verified Rollback

`PYTHONDONTWRITEBYTECODE=1 <private-root>/browser-runtime/bin/python
<private-root>/retry_verified_rollout.py`: exit2,17:29:01-17:35:05UTC.
Second and final login submission200; no more credentials/sign-ins permitted.
Fresh baseline health200/anonymous403, client no-consent no-request,
server no-consent400, disabled pest200 with correct label/manual route.
Two-var update succeeded; seven readiness queries, then latest==ready with
Succeeded provisioning. Health200. Enabled full configuration invariants passed.

Post-deploy enabled_live timed out (Playwright TimeoutError) before any
enabled assistant response/label could be observed. Exact browser substep
unavailable because protected exception details were withheld and the script
used one coarse enabled_live stage. Do not diagnose SQL failure, model failure
or session invalidation from this timeout. Unknown whether an enabled assistant
request was dispatched: request timestamps were in memory, not persisted.
No paid request completion or spend is proven. No blind inference retry.
Enabled out-of-scope and actual-AI/thin-label/grounding checks Not proven.

Mandatory rollback removed exactly both variables, waited four readiness
queries, then captured all configuration and health. All effective environment,
template, config, MI, auth, jobs, employee and scale checks passed.
Fresh ready ca-resident-demo--owner-safe-173404 serves100%; health200,
anonymous403. Original immutable image retained, min0/max1, eight Manual jobs.
No new secret, role, SQL/network/endpoint/group/job/employee change.
No destructive deletion or RG mutation. Browser contexts closed, no recordings.
Owner monitors cost; cap/expiry code/settings not altered.

### Complete Automated Command/Result Annex

Every automated command's full argv, UTC time, exit and protected stdout/stderr
SHA256 are retained in the following immutable external sanitized receipts;
these are the detailed annex to this changes artifact, not passing gate receipts.

| Private result file | SHA256 |
| --- | --- |
| sanitized-results.json | ea049deb101fc2015694939d4e39750a36f06aa1bd59c05657574e86a2460a33 |
| attempt2/sanitized-results.json | 4273681cbbb2d2afab1d17170111309a7bad03296766c6b374206a24328ae2e4 |

For each capture prefix, exact commands are:

```bash
az containerapp show -g ama -n ca-resident-demo --only-show-errors -o json
az containerapp revision list -g ama -n ca-resident-demo --only-show-errors -o json
az containerapp auth show -g ama -n ca-resident-demo --only-show-errors -o json
az containerapp job list -g ama --only-show-errors -o json
az containerapp show -g ama -n ca-cutover-test-api --only-show-errors -o json
az containerapp show -g ama -n ca-cutover-test-demo-api --only-show-errors -o json
```

Original run: before and enabled prefixes,12 reads exit0; enable exit0;
rollback-remove-vars exit0; rollback-activate exit1 as recorded above.
Second run: before/enabled/rollback prefixes,18 reads exit0;
enable exit0; enable-ready-1 through7 (resident show above) exit0;
rollback-remove-vars exit0; rollback-remove-vars-ready-1 through4 exit0.
No missing/failed capture is represented as passing.

Exact mutation argv (all also in receipt):

```bash
az containerapp update -g ama -n ca-resident-demo --set-env-vars ZF_DEMO_ASSISTANT_ENABLED=true ZF_DEMO_ASSISTANT_ENDPOINT=https://aoai-resident-469.openai.azure.com --revision-suffix owner-ai-172421 --only-show-errors -o json
az containerapp update -g ama -n ca-resident-demo --remove-env-vars ZF_DEMO_ASSISTANT_ENABLED ZF_DEMO_ASSISTANT_ENDPOINT --revision-suffix owner-rollback-172455 --only-show-errors -o json
```

Second run uses the same surgical mutation argv with enable suffix
owner-ai-172922 and rollback suffix owner-safe-173404. Supplementary failed
REST argv/body-file hashes live in exact-restore/commands.json and the
restore[-writable/-normalized]-exact-command.json files; payloads are private,
not command lines with secret values. The rejected schema attempts and async
reused-suffix failure did not establish restoration.

### Exact Original Backups and Executed Helpers

All raw config files0600, enclosing root0700, outside repository.

| Original file | SHA256 |
| --- | --- |
| before-app.json | 507793cfe93842c16fcbe6ae660a2e117360aab634188330d7e8b39d9cd9be12 |
| before-auth.json | ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356 |
| before-jobs.json | 667087d6c57f40e5049e1c59774bc55a109269fb236d763c79aa8f161e709b3d |
| before-revisions.json | a6fd48fe1dbd3220848c5665be6abd97409062cc502bb7a355e9a4cc0cfcb8ca |
| before-ca-cutover-test-api.json | e81297cf7308fbc9484c34bd2b24d6bebb1bde45c4cabec6b25521ff7e0d8562 |
| before-ca-cutover-test-demo-api.json | 326f30ebcb5f1426e598459892524f9a3b968a6169ab6260b4e1d1d8506f063e |

Exact original activate.py executed hash:
3d25178578372860b644654c84b484c9588890b4675ece670e3c289ebe099809.
Executed wrapper hash:
a58fcc3bcfc09be34f5321cb5c31639129118550ea06474fd860d3a9be7b7ee4.
restore_exact.py hash6286fa9c2991cbad2ee19acb8573c09d5651a3aacd69edc36a91241aaf78b1c1.
Final template_patch.py hash220a3356b05414ff24fe1bd1237a213f321b1b3c7a30231fe9e0b4783c07fe05;
its early failed bodies remain separate, not claimed as that final helper's
exact earlier source. No backup/secret material is committed.

## P02-T01: Original-to-Final Reconciliation

Read-only Python comparison of original before files against attempt2 rollback
files: exit0, original effective template (ignoring revisionSuffix and only the
inert empty value beside an unchanged secretRef), full shared configuration,
identity, auth and jobs all equal. Employees template/config/identity unchanged
through both attempts. No source/UI edits. Activation Unmet; restoration proven.
Live matrix: disabled/consent/denied passed; enabled actual AI/grounding/label/
out-of-scope Not proven. Human content/WCAG acceptance not performed.
The prior SQL47073 pre-read blocker is resolved by owner direction, not revived.
Current blocker is exhausted2/2 sign-ins and unproven post-deploy browser flow.

## P02-T02: Original Independent Review and Local Closeout

Exactly one independent Review Complete / Not accepted, preserved at
.copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-owner-enable-review.md.
RV-001 High: activation and actual-model acceptance unmet; timeout dispatch/
spend unknown. Route later rpi-research, not another sign-in/fix/Review here.
RV-002 Low: scheduled local persistence/gate closeout owned by parent.
Review verified safe helper/result hashes, not raw configs or fresh Azure state.
No application defect diagnosed; no human/hosted/content acceptance.

`git fetch origin main --quiet; git rev-parse origin/main;
gh api user --jq '{id,login}'; git status --short;
python3 <safe exact second-mutation argv extraction>`: exit0, fetched
main5634f9a077d175a931c15e3400114665d8c071ee; only seven new RPI artifacts.
No original evidence rewritten; no source/infra/doc change.

Authorized local closeout commands below are recorded before execution.
Their actual result belongs to external local-closeout.log/gate output and
the later explicit outcome section, not an assumed pass:

```bash
git config --local user.name jmservera
git config --local user.email 8036360+jmservera@users.noreply.github.com
git add -- <seven continuation RPI artifacts only>
git commit -m "docs(ops): record resident AI activation rollback (Refs #563)" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 600 --base 5634f9a077d175a931c15e3400114665d8c071ee --out /home/azureuser/.copilot/session-state/c7443ccc-e490-4e9d-ba2f-e853675ecf68/files/resident-owner-enable/full-gate
```

The existing runner implements the same bounded600s flock admission natively
on /tmp/ama-rpi-heavy.lock; no outer double-lock, alternate lock or tool patch.
No lock was used for Azure/browser operations. Never interrupt foreign holders.
After gate, inspect actual external receipt and run verify-receipt if present.
No receipt copy or raw command output is committed; no push is authorized.
Any evidence-only follow-on commit makes an earlier receipt historical.

## Remaining Work

P01 and P02-T01 operations complete via mandatory rollback, Review executed
Not accepted. Local commit/full-gate closeout pending. Future finer browser
diagnostics/sign-in allowance remain separate; no child or additional login.
Activation/issue criteria remain unmet; owner monitors any possible cost.
