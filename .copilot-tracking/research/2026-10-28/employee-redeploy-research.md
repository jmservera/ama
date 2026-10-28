<!-- markdownlint-disable-file -->
---
title: Employee redeploy research
description: Focused evidence for one owner-authorized employee app redeploy
ms.date: 2026-10-28
---

# Task Research: employee-redeploy

| Field | Value |
|---|---|
| Date | 2026-10-28 |
| Researcher | RPI Agent, inline |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-28/employee-redeploy-research.md |

## Research Brief

* Research exact AI settings, existing employee configuration, image route and rollback.
* Audience: owner/operator; output mode: convergence, preparing planning.
* Scope: `infra/README.md`, Foundry/Container Apps Bicep, merged #515,
  current `ca-cutover-test-demo-api` and `crcutovertestrzsrg` metadata.
* Non-goals: code changes, resident app, jobs, resource creation, roles,
  inference, private data, secrets, `.env`, broad infrastructure deployment.
* Criteria: one image build/push and one app update; preserved unrelated
  settings; exact ACR policy restoration; healthy revision or rollback.

## Research Parameters

* Posture: focused (default for caller's bounded operational request).
* Evidence root: `.copilot-tracking/`.
* External sources: approved PR and read-only Azure management metadata only.
* Explicit limits: no extra resources, minimum replicas zero; nonblocking
  `/tmp/ama-rpi-heavy.lock` during Docker build; no secret values.
* Prior knowledge: #515 handover verified against merged PR body. Clean topic
  branch `ops/employee-redeploy-20261028` matches caller; no existing PR.
* Intake: full-loop execution explicitly requested; no routine question needed.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
|---|---|---|
| Instruction | Repository instructions, `src/README.md` | Selected: branch, identity, complete publication gate, secret boundaries |
| Skill | rpi-research | Selected: inline wider/deeper/contrarian cycle |
| Skill | Web/design/security audit skills | Skipped: deploy existing unchanged code, no UI/source audit requested |
| Specialist | Independent critique and final reviewer | Deferred to Plan/Review, bounded independent judgments required |

## Direction Controls and Questions

| ID | Question/control | State |
|---|---|---|
| Q1 | Exact AI values and current deployed prerequisite? | Answered C2/W1/W3 |
| Q2 | Preserve config and restore ACR policy without secrets? | Answered W3/W4 |
| Q3 | One revision, anonymous probe/log/assets and rollback feasibility? | Answered C3/C4/W3; authenticated live assets remain conditional |
| D1 | One employee update only; ACR exception restored afterwards | Active caller boundary |
| D2 | No `.env`, listSecrets, data, inference, resident/job/role changes | Active caller boundary |

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Read runbook, merged #515 and Bicep outputs. Verified #514/#515/#516 merged,
clean matching branch at `bb6df04cef68cc3694a97238d002c732c3406d81`.
Inline because this is one coupled operational trace.
Reflection: one `standard` GPT-4.1 nano deployment already succeeds; no model,
role or Bicep deployment is needed.

#### Wave 2: Deeper

Read only app/registry/model metadata, CLI mutation help, Dockerfile and HTTP
route contract. Employee is Single revision, Healthy/ScaledToZero, revision
`ca-cutover-test-demo-api--0000006`, minimum zero/maximum four. Existing image:
`sha256:0769b52dddc5d6b350c74d6711ae53eda45d3e903ee27fac6b5a6c1d6b8b6e7e`.
Twenty-seven existing env entries and one Key Vault secret reference must
remain; no secret values were requested. Reflection: use additive
`--set-env-vars`, not replacement, with explicit container and min zero.

#### Wave 3: Contrarian

Challenged assumptions: ACR public access is Disabled, exports disabled, bypass
None, default Allow and empty rules. Merely adding an IP rule cannot allow
pushes while public access stays Disabled. The approved temporary ACR route
therefore needs public Enabled/default Deny plus only this VM's `/32`, followed
by exact original restoration, including the otherwise unusual default Allow.
Protected app/static routes cannot prove authenticated live asset serving
anonymously; do not forge identity headers or weaken authentication. Verify
packaged image order and available anonymous HTTP independently and disclose
the authenticated boundary. No paid inference or data endpoints.
Reflection: health/log/config failures trigger previous-revision rollback;
expected authentication challenges do not. Complete local publication gate is
required, even though no runtime source files change; upstream #515's disclosed
exception is not inherited permission to bypass it.

#### Parent Synthesis and Disposition

Accept exact three-variable additive update, digest pinning, baseline comparison,
nonblocking build lock, private-first ACR restoration and bounded verification.
Reject broad Bicep, new resources, inference, auth bypass and unapproved gate
exceptions. Defer authenticated employee UX/task-release/model acceptance.
No further research cycle: material bounded contracts covered; actual operation
results belong to Implement.

## Evidence Log

| ID | Claim | Source | Confidence |
|---|---|---|---|
| W1 | #515 supplies endpoint and both names, one existing nano model and role; no employee redeploy | https://github.com/jmservera/ama/pull/515, retrieved 2026-10-28 | High |
| W2 | #514/#515/#516 merged; clean HEAD equals fetched main | `gh pr view`, `git fetch` and `git rev-parse`, 2026-10-28 | High |
| C1 | Publication requires complete external exact-head gate for deployments | `src/README.md:74` | High |
| C2 | Endpoint and single-model standard/capable mapping | `infra/modules/foundry.bicep:120`, `infra/modules/containerapps.bicep:167`, `infra/README.md:1472` | High |
| C3 | Source image builds installed distributions from `src/` and UID10001 | `src/api/Dockerfile:1` | High |
| C4 | `/healthz` reflects store readiness; `/app` and JS require authentication | `src/api/src/zava_forward/api/server.py:220`, `src/api/src/zava_forward/api/web/index.html:35` | High |
| W3 | Existing app, ACR policy and one model readbacks above | Azure CLI GETs on named existing resources, 2026-10-28 | High |
| W4 | `--set-env-vars` preserves existing variables; registry flags and revision activation exist | Installed `az containerapp update`, `az acr update`, revision help, 2026-10-28 | High |

## Findings, Alternatives and Decision State

Selected approach: safe external baseline, one local source-image build and ACR
push, restore ACR before rollout, one additive digest-pinned update. Exact AI:

| Variable | Value |
|---|---|
| AI_ENDPOINT | https://aif-cutover-test-rzsrg.openai.azure.com/ |
| AI_DEPLOYMENT | standard |
| AI_DEPLOYMENT_STRONG | standard |

Preserve `AZURE_CLIENT_ID=1b1fe44e-f4cf-4aae-98d0-b30c7927a5e3`.
Caller authorizes these three AI entries only, not the two extra version entries
listed in #515's handover. This is deployment/config evidence, not inference,
quality, release binding or human acceptance.

## Risks and Self-check

* Authenticated live JS cannot be inspected without an authorized session;
  image/anonymous observations must be labelled separately.
* Single-mode revision activation rollback must be verified by actual traffic/
  readiness readback; use app-scoped configuration traffic changes only if needed,
  never a second image revision.
* Foreign heavy-lock ownership blocks build/gate immediately, without queueing.
* Secret values, `.env` and private datasets remain excluded; backup contains
  only configuration values and secret-reference metadata.
* Evidence/source review complete; no delegated research or source edits.

## Planning Readiness

Ready (C1-C4/W1-W4). Research disposition: executed, complete.
Parent next action: Plan, with independent one-pass critique.

Subsequent planning evidence supersedes initial readiness for execution:
foreign heavy-lock ownership, denied current cost evidence and unestablished
Single-mode/no-second-revision rollback block mutation. Original research
disposition remains executed; see plan Critique Disposition PC-001..005 and
changes record. Official revision docs consulted2026-10-28:
https://learn.microsoft.com/en-us/azure/container-apps/revisions and
https://learn.microsoft.com/en-us/azure/container-apps/revisions-manage.
