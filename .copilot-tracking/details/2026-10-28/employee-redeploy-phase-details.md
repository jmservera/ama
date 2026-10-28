---
title: Employee redeploy phase details
description: Task-level preservation and verification contracts
ms.date: 2026-10-28
---

## Metadata

* Task ID: employee-redeploy-20261028
* Plan: .copilot-tracking/plans/2026-10-28/employee-redeploy-plan.md
* Research: .copilot-tracking/research/2026-10-28/employee-redeploy-research.md
* Status: critique Complete / Revise, compatible corrections applied.
* Current execution: read-only backup/evidence permitted; build/cloud blocked.
* Backup result: `/tmp/ama-employee-redeploy-20261028.nbVE6l`, directory0700/
  JSON0600. Complete safe app/config/template, revision and ACR GETs captured.
  Final app/ACR semantic equality passed;27 original env entries, one Key Vault
  reference, min0/max4 and old revision/digest unchanged; AI entries absent.
* Completion markers: P01-T01 partial, P01-T02/P02 blocked; P03-T01 complete
  with independent Review Complete / Not accepted. No build/push/update/rollback.
* Full publication gate not admitted because foreign heavy-lock ownership
  blocks without queueing or polling. No verified receipt, no push/PR.

<!-- rpi:phase id=P01 -->
## P01: Preserve and publish image

<!-- rpi:task id=P01-T01 -->
### P01-T01: Capture baseline and build once

Safe ARM/CLI GET projection: identity, complete configuration excluding secret
values (only name/keyVaultUrl/identity), complete template, revision status and
digest. Current env values are noncredential configuration; never invoke
listSecrets, Key Vault secret retrieval or inspect `.env`. Auth config GET
stores only public configuration/reference metadata if included, never secret
values. Baseline retained outside git, mode0600 under owned `/tmp` directory.
Record baseline hash and old revision/digest, not complete config in git.
Source `bb6df04cef68cc3694a97238d002c732c3406d81`; build context has zero
untracked/ignored files. Build one image under `flock -n`.
If later re-admitted, construct exactly `{"cases":[],"staff":[]}` in an owned
external data directory; Store uses these required keys and supplies defaults.
Make data readable and state writable to UID10001. Run exact built image ID
with only these mounts and password auth plus a constructed explicit synthetic
password to suppress generated-password printing. Publish8088 only to a random
127.0.0.1 port, no cloud settings/credentials/network URLs. Bound readiness to
60seconds, request `/healthz`, `/app`, `/ops.js`, `/app.js` and require all200.
Parse served HTML script elements: `/ops.js` index strictly less than `/app.js`;
record indices/statuses/SHA256s, not response bodies. Bind built image ID to
subsequently pushed manifest. Finally remove only this exact owned container
and known constructed local fixture files. This is a runtime command recipe,
not a new tracked test. Currently NOT RUN: foreign heavy lock blocks build.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Push digest and restore ACR

Initial ACR: public Disabled, default Allow, IP/VNet arrays empty, bypass None,
export disabled, admin false. Save exact policy JSON externally. VM egress
observed `4.225.218.160`, recheck just before rule creation and require IPv4.
Add owned `/32` while public remains Disabled. Enable exports using
`az acr update --allow-exports true`; enable public only with default Deny.
Use `az acr login --expose-token` captured in memory, Docker `--password-stdin`,
temporary mode0700 DOCKER_CONFIG and no shell tracing. Push unique source tag;
read manifest digest, compare local pushed RepoDigest and remote manifest.
Finally disable public first, remove only owned rule, restore other original
policy fields and assert exact JSON equality. Clean exact owned Docker auth
file and empty config directory. Any exception prevents app update.
PC-003: all cloud writes additionally blocked pending current sanitized all-in
headroom (accrued, remaining liabilities, reserve, currency/lag/exclusions and
bounded redeploy exposure). One cost query429 and one stable-API alternative
RBAC denial cannot satisfy it. Do not grant roles or alter shared login.
PC-005 bounds if re-admitted:600seconds total exception,60seconds each policy/
rule/token/login/digest operation,420seconds push, private-first restoration
on handled error/timeout/interruption in finally,120seconds restoration readback.
Unconfirmed cleanup is an explicit recovery blocker, never a success.

<!-- rpi:phase id=P02 -->
## P02: Update and verify once

<!-- rpi:task id=P02-T01 -->
### P02-T01: One additive revision update and bounded checks

Compare current safe projection to baseline immediately before write. Single
command `az containerapp update -g ama -n ca-cutover-test-demo-api
--container-name api --image <registry>/zava-forward-api@sha256:<digest>
--set-env-vars AI_ENDPOINT=https://aif-cutover-test-rzsrg.openai.azure.com/
AI_DEPLOYMENT=standard AI_DEPLOYMENT_STRONG=standard --min-replicas 0
--revision-suffix emp-20261028-<unique>`, `-o none`.
Never retry that mutation if ambiguous: read actual revision list/status.
Bound convergence to ten minutes, GET-only retries. Compare full app config/
identity and normalized template with only intended differences.
Anonymous GETs only `/healthz`, `/app`, `/ops.js`, `/app.js` and optionally `/`;
no data endpoints, sign-in or model call. HTTP401/302 sign-in protects assets;
do not bypass it. Record HTTP status and artifact hashes/order without content.
Require positive timestamped new-revision Provisioned/Healthy state and
successful startup/readiness or ready replica fields, not just401 or absent
error text. If min0 yields no observed startup within600seconds, runtime is
unverified/blocked, not healthy-by-inference. Do not change scale to force it.
Console/system log bounded query: parse in memory, retain only startup/error
counts and safe event reasons, never raw request/customer or credential text.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Rollback or final success readback

Previous revision `ca-cutover-test-demo-api--0000006`, digest
`sha256:0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e`.
Official docs https://learn.microsoft.com/en-us/azure/container-apps/revisions
and /revisions-manage retrieved2026-10-28 describe failed-rollout old-traffic
retention, activation and multiple-mode routing, but do not establish exact
Single-mode rollback after successful cutover without a new revision. Therefore
PC-001 is resolved by fail-closed planning: block mutation until a compliant
route is established. No automatic mode/traffic divergence is authorized.
With zero app writes, confirm previous revision/config remain unchanged;
rollback is not needed or executed. Never copy/update image a second time.

<!-- rpi:phase id=P03 -->
## P03: Review and publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: Evidence and independent Review

Record actual operations/exits, revision/digest, exact policy restoration,
preservation equality, probe/log/asset boundaries and rollback disposition.
One independent reviewer assesses plan, implementation evidence and actual
readbacks; leaves human acceptance unchecked. No review-driven second rollout.
Executed once, original record:
.copilot-tracking/reviews/logs/2026-10-28/employee-redeploy-review.md.
Outcome Not accepted; reviewer assessed supplied operation records, did not
independently access external backup bytes. Parent's direct equality assertions
remain distinct original execution evidence. RV-001..005 remain routed.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Commit, full gate, conditional PR

Git identity from `gh api user`: local `{id}+{login}@users.noreply.github.com`
for author/committer; coauthor exactly as requested. No `.tmp`/config/token
files staged. Full gate command: `python3 tools/rpi-checks.py --all --jobs 3
--lock-timeout 0 --base <fetched-main-sha> --out <new-external-directory>`.
No gate success/PR claim unless receipt verification and independent exact-head
assessment pass. Push only requested topic, no force/amend/merge. PR body uses
Refs #514, #515, #516 only, with revision/digest/restored policy and all limits.
Gate failure is a publication blocker, not an app rollback trigger after an
otherwise healthy rollout; code-gate failure is not runtime failure.
