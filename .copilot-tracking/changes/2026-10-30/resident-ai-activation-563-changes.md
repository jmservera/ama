---
title: Resident AI activation 563 changes and commands
ms.date: 2026-10-30
---

## Execution Boundary

Task563 / resident-ai-activation-563, full safe-stop plan.
Owner activation approved2026-10-30T16:31Z, USD20 ceiling, exclusive
2026-11-01T00:00:00Z AI expiry, redeploy authority through November15.
Live activation is blocked, not delivered. No push or issue closure.
Research and one critique precede implementation; original critique Revise
preserved, PC-001 disposition in plan.

## Research Commands and Results

All commands below are read-only. Source reads via view/rg/glob covered the
original/addendum, reference index/memory/sector primer, API/infra guides,
resident aoai/assistant modules, SQL accounting schema/helper, browser examples,
existing rollout evidence, RPI references/templates and src local gate guide.
No private dataset or resident credential file was opened.

* `git status --short && git branch --show-current &&
  git log -1 --format='%h %s' &&
  gh pr list --head ops/resident-ai-activation-563 --json number,state,baseRefName &&
  gh issue view 563 --json title,body,state && command -v az`: exit0;
  clean named branch, HEADa0670b58, no open head PR, issue OPEN, az installed.
* `az account show --query '{subscription:id,state:state}' -o json`: exit0,
  expected enabled subscription.
* `az containerapp show -g ama -n ca-resident-demo --query <identity/revision/
  fqdn/scale/image/env-name/secret-name projection> -o json`: exit0; resident
  identity attached, latest=ready res-live-20261030-152028, min0/max1,
  two optional assistant names absent, existing two secret names only.
* `az cognitiveservices account show -g ama -n aoai-resident-469 --query
  '{id:id,kind:kind,endpoint:properties.endpoint,publicNetworkAccess:properties.publicNetworkAccess,disableLocalAuth:properties.disableLocalAuth}'
  -o json`: exit0, expected endpoint, local keys disabled.
* `az cognitiveservices account deployment list -g ama -n aoai-resident-469
  --query '[].{name:name,model:properties.model,sku:sku}' -o json`: exit0;
  resident-mini, gpt-4.1-mini2025-04-14, Standard capacity1.
* `az containerapp job list -g ama --query
  '[].{name:name,trigger:properties.configuration.triggerType}' -o json`:
  exit0, all eight Manual.
* `az role assignment list --assignee-object-id
  ab308885-7010-41b8-8b70-9ef5eabe40d0 --scope
  /subscriptions/e51ebc89-79d0-4a52-a82b-01a292eefd5b/resourceGroups/ama/providers/Microsoft.CognitiveServices/accounts/aoai-resident-469
  --query '[].{role:roleDefinitionName,scope:scope}' -o json`: exit0,
  Cognitive Services OpenAI User already assigned on that account only.
* `az containerapp show -g ama -n ca-resident-demo --query
  'properties.template.containers[0].env[?name==`ZF_SQL_SERVER` ||
  name==`ZF_SQL_DATABASE` || name==`ZF_SQL_AUTH` || name==`ZF_SQL_CLIENT_ID` ||
  name==`ZF_DEMO_EXPIRES_AT`]' -o json`: exit0; msi/existing client,
  sql-cutover-test-rzsrg/retrofit; portal expiry2026-12-31T23:59:00Z is
  separate from model expiry.
* `python3 -c <importlib availability probe for playwright, pyodbc,
  azure.identity, zava_forward.api>`: exit1, zava_forward not installed.
  Corrected availability probe for playwright/mssql_python/azure.identity
  exit0: False/True/True. No package install needed for safe-stop checks.
* `az sql server show -g ama -n sql-cutover-test-rzsrg --query
  '{publicNetworkAccess:publicNetworkAccess,fullyQualifiedDomainName:fullyQualifiedDomainName}'
  -o json`: exit0, public access Disabled.
* `az containerapp exec --help | head -65`: exit0, interactive execution
  options inspected only; no exec session was opened.
* `git show -s --format='%h %s' 4aa1b33 2>/dev/null`: optional historical
  lookup failed (unknown abbreviated object); no change.
  `gh pr view 564 --json mergeCommit,mergedAt,files`: exit0, merged
  a72cb268, source fixes and activation documentation confirmed.
* `getent ahostsv4 sql-cutover-test-rzsrg.database.windows.net | head -3`
  and Python socket.create_connection port1433/timeout10: exit0, public DNS
  and TCP reachable; this does not establish database authorization.
* `az acr manifest show-metadata -r crcutovertestrzsrg -n
  zava-resident-demo@sha256:59d5bfd6722a214e4de2c2fe3b1995ce5b7f9ea85eae415c20551d7de6b2304a
  --query '{digest:digest,createdTime:createdTime,tags:tags}' -o json`: exit1,
  private registry firewall denial. No firewall opening attempted.
* `az vm list -g ama --query '[].{name:name,powerState:powerState}' -o json`:
  exit0, empty. No existing VM route identified.
* `az containerapp revision list -g ama -n ca-resident-demo --query
  '[].{name:name,active:properties.active,traffic:properties.trafficWeight}'
  -o json`: exit0, sole current revision active/traffic100.
* `gh api user --jq '{id,login}'`: exit0; privacy-safe local identity available.
* Session-history read-only query, seven-day repository scope for563/469:
  zero rows; no prior evidence substituted.
* `PYTHONDONTWRITEBYTECODE=1 python3
  /home/azureuser/.copilot/session-state/83552de8-08ca-41d8-9731-98a1baa7b2b9/files/resident_sql_preflight.py`:
  exit2, SQL47073 public interface disabled. Script internally used
  `az account get-access-token --resource https://database.windows.net/
  --query accessToken -o tsv` captured in memory only, then an encrypted
  read-only connection attempt with15s timeout. Raw driver error and token
  withheld. Connection failed before any SELECT, permission test or write.

## Implementation Controls and Current State

P01-T01 starting: private exact backup. External evidence root:
/home/azureuser/.copilot/session-state/83552de8-08ca-41d8-9731-98a1baa7b2b9/files/resident-activation-backup.
No Azure writes admitted. Future exact settings (not applied):
ZF_DEMO_ASSISTANT_ENABLED=true and
ZF_DEMO_ASSISTANT_ENDPOINT=https://aoai-resident-469.openai.azure.com.
Existing MSI SQL settings would be reused. No new secretrefs or credentials.

## Blocker and Required Unblock Evidence

B1: obtain an authorized private SQL execution route and sanitized receipt
verifying resident principal SID/narrow rights, actual reserve/complete
definitions, 2000-cent lifetime row and remaining headroom/rate allowance,
one-cent permanent reservation before HTTP and exclusive November1 SQL UTC
expiry. If accounting objects are absent or wrong, separately approve the
existing infra/sql/resident-assistant.sql migration; preserve every reservation.
Do not assume the migration is absent merely because it cannot be inspected.
No network opening, job mutation, key or unmetered developer inference is an
authorized substitute.

## P01-T01: Private Backup Complete

`PYTHONDONTWRITEBYTECODE=1 python3
/home/azureuser/.copilot/session-state/83552de8-08ca-41d8-9731-98a1baa7b2b9/files/resident_safe_stop.py`:
exit1 only at final overly strict revision equality assertion. All eight Azure
reads succeeded; before/after exact app/auth/job JSON equality established.
Raw responses stayed external, directory0700/files0600. No secrets retrieved.

Actual repeated commands, each with `--only-show-errors -o json`, exit0:

```bash
az containerapp show -g ama -n ca-resident-demo --only-show-errors -o json
az containerapp revision list -g ama -n ca-resident-demo --only-show-errors -o json
az containerapp auth show -g ama -n ca-resident-demo --only-show-errors -o json
az containerapp job list -g ama --only-show-errors -o json
```

Before reads began16:38:31Z; after reads began16:39:09Z.
Exact original backup hashes:

| Private filename | SHA256 |
| --- | --- |
| before-app.json | 507793cfe93842c16fcbe6ae660a2e117360aab634188330d7e8b39d9cd9be12 |
| before-auth.json | ca3d163bab055381827226140568f3bef7eaac187cebd76878e0b63e9e442356 |
| before-jobs.json | 667087d6c57f40e5049e1c59774bc55a109269fb236d763c79aa8f161e709b3d |
| before-revisions.json | a6fd48fe1dbd3220848c5665be6abd97409062cc502bb7a355e9a4cc0cfcb8ca |

These are exact returned configurations, not a backup of secret material
omitted by the management API. Existing secret references were never changed.

## P01-T02 and P02-T01: Read-Only Verification Complete

Initial helper warmed health and checked anonymous assistant denial with180s
timeouts. A subsequent inline Python comparison printed only differing JSON
paths, never values: revisions/0/properties/runningState and replicas.
This is expected scale-from-zero warming, not a configuration change.
Original failed assertion preserved rather than rewritten as a pass.

`PYTHONDONTWRITEBYTECODE=1 python3
/home/azureuser/.copilot/session-state/83552de8-08ca-41d8-9731-98a1baa7b2b9/files/resident_finalize.py &&
git diff --check && git status --short`: exit0.
Finalizer reads original backups, compares full app/auth/jobs and compares
revision configuration with only runtime replicas/runningState excluded.
It repeats GET /healthz and anonymous POST /demo/assistant (synthetic rat
question, record-use false and matching Origin), each timeout180s.

Results: health200; anonymous assistant403; app/auth/jobs exact equality;
same sole revision/configuration. Runtime moved0 to1 replicas and
ScaledToZero to RunningAtMaxScale as health warmed it; min0/max1 unchanged.
All eight jobs Manual, assistant optional names still absent.
Private sanitized-results.json retains command argv, UTC times, exit codes,
all backup hashes and permissions. Original command-events.json hash:
05ad2b06df2d43a4ec744420c28909b5797a6552641d82bc68adfd02aaca7e3b.

No Azure configuration mutation, SQL write, model call, role creation, job
execution, key retrieval, secret read or sign-in attempt occurred.
No rollback was necessary: there was no changed candidate.
No UI/source change or unrelated cleanup was made. Private backups/helpers
are intentionally retained as original operational evidence.

## Live Acceptance Matrix

| Required proof | Result |
| --- | --- |
| Existing managed identity and account-only OpenAI User | Read-only management-plane verified |
| Existing model/deployment and min0/Manual jobs | Verified unchanged |
| Exact private app configuration backup | Complete |
| Health warm and anonymous denied path | HTTP200 / HTTP403 |
| Optional AI settings unset | Verified in exact deployed app configuration |
| Actual SQL cap/procedures/permissions/headroom | BLOCKED47073, unknown |
| Consented grounded rat/pest AI reply, AI label and collapsed sources | Not run, activation blocked |
| Live out-of-scope rules fallback under enabled AI | Not run |
| Authenticated no-consent refusal / unavailable or unset fallback | Not run |
| Resident credential file use / sign-in attempts | Not read / zero of two |
| Whole #563 acceptance / human content acceptance | Unmet / not performed |

## P02-T02: Review and Local Persistence

Independent one-pass Review executed Complete, outcome Residual work. No
safe-stop defect established. Original record:
.copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-review.md.
RV-001 Medium: private SQL evidence remains blocked, route rpi-research.
RV-002 Low: actual-model/authenticated browser proof remains a distinct later
activation task, not falsely marked complete.
RV-003 Low: parent owns scheduled local persistence/full-gate closeout;
original Review correctly precedes those actions. No repeated Review.

`git fetch origin main --quiet && git rev-parse origin/main &&
python3 --version && python3 tools/rpi-checks.py --help | head -65 &&
git diff --check && git status --short`: exit0; origin/main equals
a0670b58a171255284b005ad281b26fd50ea89c7, Python3.12.3, expected seven
evidence files only. No source/infra/docs diff.
`for tool in node docker az actionlint shellcheck trivy; do command -v
"$tool" || true; done && docker info --format '{{.ServerVersion}}' &&
git diff --stat && git diff --check`: exit0; all named tools available,
Docker29.9.0. Availability is not a gate pass.

## Local Persistence and Post-Commit Gate Handoff

The following exact local closeout commands are recorded before execution so
the committed candidate includes original Review and no receipt is committed.
Actual command exits, commit identity and final gate outcomes are retained in
the external closeout log and gate directory below; unavailable results must
not be read as success.

```bash
git config --local user.email 8036360+jmservera@users.noreply.github.com
git config --local user.name jmservera
git add -- .copilot-tracking/research/2026-10-30/resident-ai-activation-563-research.md .copilot-tracking/plans/2026-10-30/resident-ai-activation-563-plan.md .copilot-tracking/details/2026-10-30/resident-ai-activation-563-phase-details.md .copilot-tracking/changes/2026-10-30/resident-ai-activation-563-changes.md .copilot-tracking/reviews/plans/2026-10-30/resident-ai-activation-563-plan-critique.md .copilot-tracking/reviews/logs/2026-10-30/resident-ai-activation-563-review.md .copilot-tracking/rpi-sessions/2026-10-30/resident-ai-activation-563-state.json
git commit -m "docs(ops): record blocked resident AI activation (Refs #563)" -m "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
python3 tools/rpi-checks.py --all --base a0670b58a171255284b005ad281b26fd50ea89c7 --out /home/azureuser/.copilot/session-state/83552de8-08ca-41d8-9731-98a1baa7b2b9/files/resident-full-gate
```

External result locations, not tracked receipt copies:
files/local-closeout.log and files/resident-full-gate/receipt.json under
/home/azureuser/.copilot/session-state/83552de8-08ca-41d8-9731-98a1baa7b2b9/.
A receipt, if generated, must remain external and be verified using
`python3 tools/rpi-checks.py --verify-receipt
/home/azureuser/.copilot/session-state/83552de8-08ca-41d8-9731-98a1baa7b2b9/files/resident-full-gate/receipt.json
--base a0670b58a171255284b005ad281b26fd50ea89c7`.
Any gate failure remains an explicit blocker; do not install bypasses, push,
infer hosted/human approval, or change the preserved original Review outcome.
Task completion means the authorized safety-stop branch, not AI activation.
