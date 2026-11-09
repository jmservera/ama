---
title: Infrastructure integration topic 136 research
description: Research for the planning-only kickoff of the issue 136 Bicep and platform parent integration topic
ms.date: 2026-11-08
---

## Identity and method

Task `infrastructure-integration-136`. Planning-only parent integration topic kickoff for the open epic 136, not delivery of the epic. Worktree `/home/azureuser/source/ama-wt/issue-136-integration`, branch `feat/infrastructure-integration-136`, declared PR target `main`, session `dc0efcb1-4795-4cd2-b25c-2a66564530b3`. Local only: no push, PR, merge, issue write or checkbox.

Posture: inline, single agent, reads only (git, gh read, file views). No test, build, install, SQL, Docker, browser, lock, scanner, Azure or model call, and no private dataset or `support/` read. Research disposition: `executed`. The `rpi-research` phase is the first of one loop.

## Fresh pins (observed this session)

* Start HEAD `0f05e9aae70768def8d1d9c300215f9ee2f11638`, tree `577947cb2d94de5b79f24d38b6f459ebb0aa13a8`; ignored-inclusive status 0 lines at start; `git fetch origin main` exit 0 and `origin/main` equals HEAD (commit time 2026-11-08T08:14:36+01:00). The branch is the start commit with no topic commits yet.
* Blobs at HEAD: ADR 0001 `d42fa5c4615f4107cee83e07555dba6985c1f53e` (ms.date 2026-10-24, Status Proposed); ADR 0002 `cbe21530043ff15432cc6dce1086d080f5eb15b4` (ms.date 2026-10-24, Status Proposed, with one owner-accepted staff-identity decision of 2026-10-24); ADR 0003 `d60645397b20fb70ac3d1dc47c7a6c8671201306` (ms.date 2026-10-29, accepted with owner amendment 2026-10-15, reconciled 2026-10-18); ADR 0006 `956da1a3b804c803041fe2e8a312bd9f400273ae` (ms.date 2026-10-27, accepted 2026-10-15); `infra/README.md` `7988be37fab8e467c7973f018d9f4a6f733cda3b`; `infra/main.bicep` `20ef78d888fdad6568d039ea1c898628468ed310`; case study original `0aec2d8070117a647574b1fadc8cfbdd2af68598`; addendum `888d9ff7d0190799308618dc7f153c00adabd6f6`; reference index `1f5f310d40b87019c18c20bc2f9c0a446d6c701a`; memory `e1268db9a452b5db1ca0796f32ccae00b0b418dd`. Proposed is not approval. This record approves no ADR.
* gh identity resolved: id 8036360, login jmservera; repository-local `user.email` already equals `8036360+jmservera@users.noreply.github.com`.

## Live issue observations (gh read-only, this session)

| Item | State and observation |
| --- | --- |
| 136 | Open epic "Bicep infrastructure as code and deployment pipeline"; last updated 2026-10-23T12:25:19Z; one comment (2026-10-14, jmservera) warning that epic 195 changes the container build context and the token-store job path. All four acceptance criteria and the #440 criterion are unticked. Dependencies line: "Relates to #113 and #118" |
| Sub-issues of 136 (API) | 137 open, 138 open, 139 closed, 140 open, 141 closed, 142 open, 143 open, 144 open, 145 open, 146 open, 147 closed, 148 open |
| 136 references (search) | Also mentioned by 195 (restructure epic, open), 197 (closed) and 201 (cut-over gate, open); these are mentions, not hierarchy |
| 144 | Open, `status:partially-delivered`, parent 136, body "Depends on #107 and #118"; the issue dependency API lists no blocked-by edge (body text only). Body names local candidate `6496f61f0361c27c297b97b12a5c46e374cd6a5f` and says reviewed publication "will use that stack" under 136 |
| 107 | Open epic-level feature, parent 104, partially delivered; RAI release admission criteria are unticked: persisted release record, authoritative serving-version attestation, independent SQL race and restart tests, and delivered-build acceptance under CON-009 and AC-057. Several others are ticked |
| 118 | Open, parent 113, partially delivered; four of five criteria ticked; "Azure Policy and Defender plans decided" unticked |
| 440 | Open; scoped stabilization checkpoint issue; first-checkpoint criteria ticked, triage and artifact-delivery criteria unticked. 136 requires a scoped checkpoint under 440 before closure |
| PR 1141 | Open, not draft, base `main`, head `feat/slice-144` at `1a9616d4e9ab89d93a72204d82ee26c70baee06c`, title "feat(agents): Azure Queue adapter for the task queue port (Refs #144)"; listed checks pass at that head. `origin/main..origin/feat/slice-144` is 8 commits. This record does not retarget, push or comment on it |
| Local 144 branch | `feat/slice-144` at `ea7f36c030e7a6fbac740d382fafa54f2de2dbf4` ("fix(core): enforce the dispatch start window before provider calls") in worktree `/home/azureuser/source/ama-wt/issue-144-queue-recovery`, 0 uncommitted lines; 25 commits ahead of `origin/main`'s merge base `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`, 23 commits of current `origin/main` not contained, diff 105 files. `ea7f36c0` is not an ancestor of `origin/feat/slice-144`. The supplied original `0bd489d3` is not a valid object in this repository object database, so it is unverified here |

## Document and source contracts (static reading at HEAD, no execution)

* Entry template `infra/main.bicep` (691 lines, `targetScope = 'resourceGroup'`) wires modules guard, identity, network, monitoring, keyvault, storage, registry, sql, foundry and iotHub unconditionally; apps when `deployApplications` or `deployEnvironmentOnly`; edge only when `enablePublicEdge` (default false); authTokenStore only when `enableEntraTokenStore` (default false); operationalMonitoring; four metric alerts and two scheduled-query rules in main; and a budget. `infra/governance.bicep` (policy assignment, locks, Defender plans) is not referenced from `main.bicep`, so it is a separate deployment unit.
* Module files observed in `infra/modules/`: authTokenStore, containerapps, edge-existing-auth, edge-existing-guard, edge, envDns, foundry, guard, identity, iothub-scope-guard, iothub, keyvault, monitoring, network, operationalMonitoring, privateEndpoint, registry, sql, staff-initializer-guard, storage. Top-level units also exist: governance, iot-hub-live, live-simulator-job, private-proof-publisher, public-edge-existing, resident-assistant, resident-demo, staff-initializer-rbac. Parameter sets: main, main.test, main.pilot.example (non-deployable). Workflows: `infra-plan.yml` (what-if), `src-deploy.yml` (manual release and deploy), `src-ci.yml`. Infra tests exist under `infra/tests/` for identity, governance, monitoring, IoT, edge, container contract, pipeline, SQL tier and secret lifecycle (existence observed; none run).
* The README section "Resource coverage register (issue 136, 2026-11-04)" is the current module register: a documentation record, not machine-checked and not live Azure evidence. Its manual rows (Entra registration, contractor B2B policy, Microsoft 365 grants, GitHub environments and OIDC, Azure subscription and group) name the repository owner as owner "unless a human role is named", and its unmet list says criterion 2 still needs owner confirmation.
* `infra/defender-decision.json` (2026-11-01, owner Juan Manuel Servera): Policy audit only (`DoNotEnforce`), deny stance an open owner decision; Defender deferred, `enableDefenderPlans` false, cost approval status pending, no approvedOn.
* The README hosting completeness section for 144 (2026-11-01) records worker images, live hardening, Azure rollout, a load test at declared scale and an Azure restore proof as unmet or local-only; its rebuild section dates the only from-empty observation to 2026-10-12.
* ADR 0001 and 0002 are Proposed; ADR 0003 decision 6 (IoT Hub) is an accepted owner decision that is not evidence of deployment, cost or credential authority; ADR 0006 accepts the `src/` layout and cut-over policy and sets the build context.

## Contradictions and drift to flag (not resolved here)

* C1: The 136 issue body "Existing delivery and status" says IoT Hub, parameter sets beyond dev, deployment pipeline, policy and edge are not delivered. Current files show `modules/iothub.bicep`, `main.test.bicepparam`, `main.pilot.example.bicepparam`, `infra-plan.yml`, `src-deploy.yml`, `governance.bicep` and `modules/edge.bicep`. The paragraph is outdated for authoring and is not a statement about live acceptance. Current files take precedence for authored status; none of them is Azure observed.
* C2: The 138 body says there is no deployment, what-if or release workflow; `infra-plan.yml` and `src-deploy.yml` exist. All six 138 criteria are unticked, so existence is not acceptance.
* C3: The README register unmet list names open children 137, 138, 140, 142, 143, 144, 145, 146 and 148; 139, 141 and 147 are now closed. The list matches the live open set; the register is silent on the closed three, and closure of a child is not by itself acceptance of its epic criterion.
* C4: Issue 118 leaves "Azure Policy and Defender plans decided" unticked while `defender-decision.json` records a deferral with pending cost approval. Both are consistent only if "decided" means the activation decision, which stays with the named human owner.
* C5: The 144 body names local candidate `6496f61f`; the coordinator now reports local `ea7f36c0` with original `0bd489d3`, and the published PR head is `1a9616d4`. Observed ancestry: `6496f61f` is an ancestor of `ea7f36c0` (so the local head continues the body's candidate), and `6496f61f` is not an ancestor of the published `origin/feat/slice-144`. `ea7f36c0` is not an ancestor of the published head. `0bd489d3` is not resolvable here. The issue body is therefore stale about the local head, and the published and local lines have diverged.
* C6: The 144 issue says the dependency lives in body text; the API shows no blocked-by edge for 107 or 118, so the dependency is documented but not machine-enforced.
* C7: 136 criterion 4 (from-empty deployment) cites an observation dated 2026-10-12, before the `src/` cut-over of 2026-10-27 (ADR 0006), so reproducibility from the current repository is not re-proven; the 136 comment of 2026-10-14 already flagged the build-context change.
* C8: ADR 0001 and 0002 remain Proposed while infra work cites them as source references. Neither this record nor the planned topic changes their status.

## Source prerequisites for 144 (verified here only as status, not as engineering readiness)

* 107: RAI release admission criteria unticked (see above); the issue body says the planning baseline is not implementation acceptance. Whether the prerequisites that 144 engineering needs are present in the 144 base is a 144 verification step and is not decided here.
* 118: only the Policy and Defender decision is unticked, and it is a named human decision, not a code prerequisite for the Queue adapter. 118's scanning, hardened Dockerfile and Bicep application criteria are ticked on the issue, not re-observed here.
* The 136 topic does not wait for whole-issue closure of 107 or 118; per owner direction, 144 engineering must verify them first.

## Classification

* Delivered code (static reading): Bicep modules and templates above, `governance.bicep`, workflows, parameter sets and infra tests exist at HEAD.
* Observed local: git, gh and file reads of this session only.
* Authorized Azure observed: none in this session. Historical Azure observations are carried only as dated README claims (2026-10-12 rebuild, 2026-11-04 live deploys) and are not re-observed.
* Planned: the integration-topic record, the 144 stacking path and the verification steps.
* Unknown: hosted check state of main after 08:14, owner confirmation of manual-row ownership, Defender cost approval, the identity of `0bd489d3`, whether any 107 or 118 source needed by 144 is absent in its base.

## Evidence tier and limits

Tier FOCUSED. The only output is Markdown and JSON tracking records, so validation is Markdown, link and Git diff review, then independent exact-head assessment and fresh selected CI before any publication, per the owner's CI-first direction of 2026-11-08 08:15. No tool or gate is run here.

## Contrarian wave

* A published topic could be misread as "144 is unblocked". It clears only the stacking topology blocker; child source prerequisites and human or live acceptance are separate.
* A coverage table could be read as acceptance of 136 criterion 2. It is a status record with owners and unknowns, not a tick.
* Reading the stale 136 paragraph as truth would understate delivered authoring; reading file existence as acceptance would overstate it.
* If `origin/main` moves before publication, the base pins here become stale and the topic must be re-planned, not silently merged or rebased.

## Findings and routing

* No defect is established. Eight contradictions or drift items are routed to the coordinator and the owner as review items, not edited here.
* No new issue, epic or scope is proposed.

## Planning Readiness

Ready. Carried into the plan: the exact record contents, the 144 stacking rule, owner and unknown columns, the no-tick rule, the currency check on `origin/main`, and the CI-first validation boundary.
