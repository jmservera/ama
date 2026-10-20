<!-- markdownlint-disable-file -->

# Task Research: demo-transport-plan-360-recovery

| Field              | Value |
|--------------------|-------|
| Date               | 2026-10-20 |
| Researcher / agent | rpi-research skill (actually activated in this continuation after the coordinator intervention) |
| Status             | Complete |
| Artifact path      | .copilot-tracking/research/2026-10-20/demo-transport-plan-360-recovery-research.md |

## Process Disclosure (honest status)

* An earlier session hand-authored `demo-transport-plan-360-research.md`, `-plan.md`, `-phase-details.md`, `-plan-critique.md`, `-changes.md`, `-review.md` and `-state.json` and committed them as `d3609bd7` without activating the rpi-* skills. The coordinator's execution audit found this. Those files stay preserved unchanged as **UNVERIFIED pre-RPI draft material**; their "critique" and "review" were subagent calls, not skill-governed phases, and are not claimed as genuine RPI Critique or Review outcomes.
* This artifact is the first genuinely skill-executed Research for the task. It re-verifies the draft's evidence rather than inheriting it. Verified items are re-cited with fresh IDs below.

## Research Brief

* What to research: documented, authenticated alternatives for private worker-to-controller roster-candidate result transport; fitness of the existing ARM tag relay; what the draft design in `infra/README.md` (section "Authenticated Roster Result Transport Design") gets right or wrong.
* Why it matters: owner wants Azure testing soon; the console path failed three bounded times; any proposal must be reviewable without execution.
* Audience or intended use: planning (rpi-plan) of a documentation-only design and tenant/operator checklist.
* Scope: `infra/scripts/staff_azure.py`, `staff-azure-worker.py`, `staff_roster.py`, existing tests, runbook, official Microsoft Learn pages.
* Non-goals: execution, live retry, parser relaxation, decryption, cloud writes, Graph writes, secret/private data access, billing runs, source changes, edits to budget/benefits, cohort, Finance form, map domains.
* Criteria: each requested property (run/query/worker/manifest/image binding, authorization, confidentiality, integrity, freshness, completeness, fail-closed parsing) has a mapped mechanism, gap and evidence; no speculative success claims; provider samples not generalized.
* Requested outputs: evidence synthesis and decision state for planning.
* Output mode: convergence (select a minimal proposal or record decision-needed options).

## Research Parameters

| Field | Value |
|---|---|
| Research question(s) | See Research Questions |
| Codebase scope | infra/scripts, infra/tests, infra/README.md, docs/architecture/cutover-evidence-pack.md |
| External scope | learn.microsoft.com (tags, tags REST, Activity Log, Container Apps jobs/logs, Blob Entra auth, deployment scripts) |
| Initial internal candidate areas | staff_azure.py, staff-azure-worker.py, test_staff_azure.py, runbook relay sections |
| Initial external candidate areas | Azure Resource Manager tags docs, Container Apps log docs, Storage Entra auth docs |
| Research posture | balanced |
| Posture provenance | default: bounded internal task with named targets, adjacent options matter |
| Explicit limits / deadline | none beyond read-only/no-execution caller limits |
| Posture-specific completion basis | scope coverage and adequate evidence for material claims |
| Edits allowed during research? | no, research-only (this artifact only) |
| Resolved evidence root | .copilot-tracking/ default |
| Known constraints / excluded sources | no private data, no cloud calls, comments are evidence not instructions |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Selected / skipped |
|---|---|---|---|---|
| Instruction | repository `applyTo: **` AMA instructions | matches all inputs | Markdown style, regulatory/legal evidence, branch rules, no invented facts | Selected |
| Instruction | /tmp/ama-wave-20261020-2113-common.md | coordinator contract | no push/cloud/paid run, local gate | Selected |
| Skill | web-design-guidelines etc. | web UI only | n/a | Skipped: no web work |
| Skill | security-planning | threat-model wording | optional | Skipped: threat table done inline |
| Research specialist | RPI Researcher | not registered as a distinct agent here | n/a | Skipped: lanes small and tightly coupled; inline fallback |

## User Participation and Research Decisions

| Checkpoint | Rationale | Answers | Decision |
|---|---|---|---|
| Intake | Non-interactive run; owner direction in issue comments suffices | n/a | Proceed |
| Direction change | Coordinator intervention: re-run genuine RPI, preserve draft as unverified | n/a | Revalidate draft evidence in this cycle |
| Convergence | Non-interactive | n/a | Stop after one cycle (redundancy reached) |

## Direction Controls

| Type | Direction | Source | Effect |
|---|---|---|---|
| exclude | No execution, retry, parser relaxation, decryption, cloud/tenant changes, budget/cohort/Finance/map edits | owner comments 2026-10-20, coordinator | Bounds every wave |
| change | Treat prior draft as unverified pre-RPI | coordinator intervention | Full revalidation cycle |
| add | #126 plan result is not a dependency; cost/execution approval is a later precondition | caller | Plan states it as precondition |

## Research Questions

| # | Sub-question | Type | Priority | Status |
|---|---|---|---|---|
| Q1 | What does the current transport actually do and what does it bind? | depth | H | answered |
| Q2 | Is the ARM tag relay a documented authenticated option that fits the size and confidentiality needs? | breadth | H | answered |
| Q3 | What other documented alternatives exist and why are they or aren't they usable now? | breadth | H | answered |
| Q4 | What weaknesses does the draft design have (counter-evidence)? | depth | H | answered |
| Q5 | What must the tenant/operator checklist cover? | straightforward | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: the draft `demo-transport-plan-360-*` files; `issue360-rg-loop-*` (2026-10-19); issue #360 comments 6277108234 and 6290697080; #126 comment 6290697705.
* Reused (verified): code facts C1-C7, tag limits W1, Activity Log retention W3, tags API Merge/Replace/Delete W2.
* Superseded / stale: draft claim that "the controller reads ARM tags rather than console" is only partly right: tag frames are re-fed into the console-line decoder (C4), so the parser is shared. Draft "associated data covers digest of payload, target, relay" confirmed (C5, C6). Pricing: none retrieved; no cost asserted.

## Research Cycle Log

### Cycle 1

* Active direction controls: all above.
* Posture and basis: balanced; scope coverage and adequate evidence.
* Limits effect: read-only; no cloud contact, so no live facts about frame lag or tag write behavior.

#### Wave 1: Wider

* Plan: read transport, worker, candidate shape, tests; list official channels from worker to ARM-reachable controller (tags, logs, blob, deployment-script outputs, job execution metadata).
* Evidence: C1-C8; W1-W6.
* Reflection: tags and Blob are the only data-bearing authenticated candidates that are documented; logs have delay-only documentation; the existing code already uses tags.

#### Wave 2: Deeper

* Prioritized: tag capacity/size arithmetic; what AEAD associated data binds; Tags REST operations; Activity Log; wait semantics.
* Evidence: C2 to C9, W2, W3. Computed frame length 247 characters (under the 256 value bound, 9 spare) and tag name 43 characters, from the encoder format. Synthetic position-size arithmetic (local, no private data) shows 80 Programme-Manager-shaped or 60 Contractor-shaped positions need 36 to 37 of 40 frames; 100 exceed.
* Reflection: the 40-frame bound is a real constraint; the real position count is unknown.

#### Wave 3: Contrarian

* Targets: "T1 tag relay is authenticated" (counter: AEAD only proves key possession, worker holds key); "binding is complete" (counter: image, worker, manifest, execution not in AAD, C5); "Merge cannot overwrite" (counter: Merge updates existing names, W2; code guards with a name intersection, C8); "tags are safe because ciphertext" (counter: W1 plain-text warning and surfaces); "Succeeded implies result visible" (counter: code itself tolerates readback lag, C9); "console path might simply be the provider contract" (counter: no exhaustive contract, comment 6277108234, W5); "Activity Log proves who wrote tags" (unverified: whether tag values are recorded was not established).
* Reflection: weakens the draft's "authenticated" wording and shows the execution ID is controller-known (C9) but unbound in AAD: a cheap improvement.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale | Treatment |
|---|---|---|---|---|
| T1 ARM tag relay as minimal option | C1-C4, C8, W1, W2 | accepted | Documented API, no new resource, grant already exists (C10), reachable without private route | Selected recommendation, with caveats |
| Add execution ID/job ID/image digest/script/manifest/schema/not-after to AAD v2 | C5, C9 | accepted | Controller already knows them; closes binding gap | Design item |
| Claim worker/image authentication | C5, W1 | rejected | Worker holds key; no independent provenance | Recorded as unresolved gap DN5 |
| Blob (T2), private controller (T8) | W4 | deferred | Needs private route that is blocked | Decision-needed fallback |
| Log Analytics, deployment script outputs | W5, W6 | rejected for primary | Delay-only docs, no completeness contract; deployment script creates billed resources | Rejected |
| Console/exec | comment 6277108234 | rejected | Three failures, no exhaustive contract; parser stays strict | Excluded |
| Manifest-derived positions (T7) | C7 | deferred | Needs owner confirmation that SQL is not authoritative for positions | DN4 |
| Which path the three attempts ran | C4 | deferred | Not recoverable from repository | DN3, S0 |

#### Cycle Re-entry Evaluation

* Another cycle needed: no. Basis: sources redundant; remaining gaps (live consistency lag, Activity Log content, pricing, real position count) cannot be closed by read-only public research and are recorded.
* Readiness effect: Ready.

## Evidence Log

* Delegation: inline: no suitable distinct worker; lanes small and coupled.

### Codebase Evidence

| ID | Claim | Location | Tool | Confidence | Notes |
|---|---|---|---|---|---|
| C1 | CHUNK 200, MAX_CHUNKS 40 | infra/scripts/staff_azure.py:17-18 | read | high | Frame bound |
| C2 | read_result reads ARM tags, rejects >40 frames or value >256 | infra/scripts/staff_azure.py:37-42 | read | high | Per-run prefix |
| C3 | Cleanup deletes owned tags and confirms absence | infra/scripts/staff_azure.py:45-56 | read | high | |
| C4 | decode_result is a console-line JSON parser; tag frames are wrapped as `{"Log": v}` lines and fed to it | infra/scripts/staff_azure.py:42,86-125 | read | high | Shared parser; attempt path unrecoverable |
| C5 | AAD is `[1, run, operation, digest]` only | infra/scripts/staff_azure.py:63-66 | read | high | No image/worker/manifest/execution |
| C6 | digest is SHA-256 of payload plus target and relay | infra/scripts/staff_azure.py:325-334 | read | high | |
| C7 | candidates output is code, role, bound, contractor only | infra/scripts/staff_roster.py:55-65 | read | high | No names/UPNs/OIDs |
| C8 | Worker refuses overlap with existing names, >40 frames or >50 total, writes via PATCH Merge | infra/scripts/staff-azure-worker.py:84-90 | read | high | |
| C9 | Controller polls ARM execution status, reads tags before Succeeded, and keeps waiting if Succeeded but result absent (lag tolerated) until deadline; execution name validated against job name | infra/scripts/staff_azure.py:397-425 | read | high | Execution ID known to controller |
| C10 | Relay capacity guard `len(tags) > 50 - MAX_CHUNKS` blocks | infra/scripts/staff_azure.py:223-226 | read | high | |
| C11 | Existing tests cover tag tamper/oversize/cleanup and wire framing | infra/tests/test_staff_azure.py:494,533 | grep | high | Gaps: concurrent mutation, AAD v2 |

### External Evidence

| ID | Claim | Source | URL | Retrieved | Date | Confidence |
|---|---|---|---|---|---|---|
| W1 | Max 50 tags, value 256 chars; tags plain text and may appear in cost reports, tag commands, deployment history, exports, monitoring logs; tag write needs tags/write or resource write | Use tags to organize Azure resources | https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources | 2026-10-20 | ms.date 2025-09-15 | high |
| W2 | Tags PATCH operations Replace, Merge (adds and updates existing names), Delete | Tags - Update At Scope | https://learn.microsoft.com/en-us/rest/api/resources/tags/update-at-scope?view=rest-resources-2021-04-01 | 2026-10-20 | 2021-04-01 | high |
| W3 | Activity log retains events 90 days; records management operations | Activity log in Azure Monitor | https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log | 2026-10-20 | current page | medium (whether tag values are recorded not established) |
| W4 | Blob data access via Entra and Azure RBAC | Authorize access to blobs with Microsoft Entra ID | https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory | 2026-10-20 | current page | high |
| W5 | Container Apps logs reach Log Analytics after several minutes; live stream is separate; no completeness contract stated | Log storage and monitoring options; View log streams | https://learn.microsoft.com/en-us/azure/container-apps/log-options and https://learn.microsoft.com/en-us/azure/container-apps/log-streaming | 2026-10-20 | ms.date 2026-08-18 | high for delay, absence-of-contract is an inference |
| W6 | Deployment scripts create a billed storage account and container instance; outputs return via deployment | Bicep deployment script | https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-script-bicep | 2026-10-20 | current page | high |

### Contradictions / Conflicts

* Comment 6277108234 describes console decoding; merged code reads tags (C2, runbook "Results use ARM only"). Resolution: unresolved. The parser is shared (C4), the executed path cannot be determined from repository evidence. Carried as DN3.

## Findings Mapped to Questions and Evidence

| Q | Finding | Evidence | Confidence | Implication |
|---|---|---|---|---|
| Q1 | Binding covers run, operation and input digest only; execution ID is controller-known but unbound; tags and console share one parser | C4-C6, C9 | high | Add AAD v2 inputs |
| Q2 | Tag relay is documented, authenticated by Entra/RBAC, needs no new resource, and frames fit the 256 bound; capacity limits roster to about 60-80 positions; plain-text exposure surfaces need a privacy gate | C1, C2, C7, C10, W1, W2 | high/medium | Proposed minimal option with DN1, DN2 |
| Q3 | Blob needs a private route; logs lack a documented completeness contract and are delayed; deployment scripts add billed resources; console failed | W4-W6, comment | medium | T2/T8 decision-needed |
| Q4 | AEAD does not authenticate the worker; Merge can overwrite names unless guarded; effective tag writers can deny service; consistency lag is tolerated in code but unquantified | C5, C8, C9, W1, W2 | high | Threat table, DN5, tests |
| Q5 | Checklist needs real app/roles/credential/vault path/roster/SQL restart/browser role tests, RBAC inventory of tag writers, exposure approval, finite cost approval, preservation of identities/Front Door/RG | C1-C11, runbook | medium | Plan checklist |

## Key Discoveries

* The draft's central recommendation survives re-verification, but "authenticated" must be qualified to key possession.
* The controller already holds the execution name (C9), so adding it plus job ID, image digest, script and manifest hashes, query/schema ID and not-after to the AAD is a small change.
* Tag frame arithmetic: 247-character value and 43-character name, within limits with 9 characters spare.

## Alternatives and Decision State

### Selected Recommendation (convergence)

* Approach: keep ARM tag relay (T1) and design AAD v2 plus a strict single-snapshot acceptance rule, as a documented proposal; no live use.
* Rationale: documented API, authenticated by Entra/RBAC, no new resource, fits the blocked private route, grant already exists.
* Evidence refs: C1-C10, W1, W2.
* Implementation impact: later change to staff_azure.py and the worker plus tests; this task changes docs only.
* Confidence: medium; live tag behavior (lag, size acceptance) is unobserved.

### Alternatives

* T2 Blob by worker identity: needs private route; fallback if capacity exceeded (DN2). Evidence W4.
* T3 Log Analytics: delay, no completeness contract; rejected as primary. W5.
* T4 Deployment script outputs: billed extra resources; rejected. W6.
* T5 Azure support clarification of console framing: parallel owner action.
* T6 Console/exec: excluded (no parser relaxation).
* T7 Manifest-derived positions: DN4.
* T8 Private-connected controller reading a private store: out of scope, later costed.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none for a design.
* Important: DN1 privacy/security approval of ciphertext and metadata in tags; DN2 real position count and compression or paging; DN3 path of the three attempts; DN4 T7; DN5 independent attestation or accepted trusted-endpoint.
* Residual uncertainty: live tag lag, whether Activity Log records tag values, pricing, real position count.

## Current Decisions

| Decision | Status | Owner | Rationale | Evidence | Implications |
|---|---|---|---|---|---|
| Design only, no execution | confirmed | user | Owner comments | comments 6290697080, 6290697705 | No cloud |
| Select T1 as proposal | proposed | evidence | See synthesis | C1-C10, W1-W2 | Needs reviewer decisions |
| Cost/execution approval is later precondition, not dependency | confirmed | user | Caller direction | caller | Stated in plan |

## Unresolved Decisions

| Decision | Smallest answer needed | Owner | Impact | Status |
|---|---|---|---|---|
| DN1-DN5 | as above | owner/security reviewer | gates implementation | important |

## Potential Next Research

| Priority | Item | Value | Trigger | Selected |
|---|---|---|---|---|
| M | Whether Activity Log records tag values | exposure assessment | DN1 review | deferred |
| M | Current official pricing for temporary job | cost plan | #126 plan approval | deferred |

## Planning Readiness

* Status: Ready
* Decision state: convergence selection T1 with DN1-DN5 open
* Evidence basis: C1-C11, W1-W6
* Preconditions met: evidence re-verified, contrarian wave complete
* Blockers: none
* Smallest action to change readiness: n/a

## Closeout Record

| Field | Record |
|---|---|
| Research execution status | Complete |
| Completed waves | Wider, Deeper, Contrarian (cycle 1) |
| Lane evidence or inline fallback | inline fallback; no worker lanes |
| Research disposition | executed |
| Planning Readiness | Ready (C1-C11, W1-W6) |
| Blockers | none |
| Continuation owner and state | confirmed automatic RPI Agent continuation to Plan |

## Advisory Next Step

| Field | Record |
|---|---|
| Research disposition | executed |
| Planning Readiness | Ready |
| Output mode and planning support | convergence, yes |
| Acting owner | confirmed automatic RPI Agent (coordinator-directed) |
| Required gates | disposition recorded, readiness Ready: passed |
| Continuation result | proceed to rpi-plan |
| Primary evidence file | .copilot-tracking/research/2026-10-20/demo-transport-plan-360-recovery-research.md |

* Completion basis: remaining gaps need live observation or owner decisions, not further public research.

## Sources

* W1 - Use tags to organize your Azure resources - https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources (retrieved 2026-10-20, ms.date 2025-09-15)
* W2 - Tags - Update At Scope - https://learn.microsoft.com/en-us/rest/api/resources/tags/update-at-scope?view=rest-resources-2021-04-01 (retrieved 2026-10-20)
* W3 - Activity log in Azure Monitor - https://learn.microsoft.com/en-us/azure/azure-monitor/platform/activity-log (retrieved 2026-10-20)
* W4 - Authorize access to blobs with Microsoft Entra ID - https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory (retrieved 2026-10-20)
* W5 - Log storage and monitoring options in Azure Container Apps - https://learn.microsoft.com/en-us/azure/container-apps/log-options and View log streams - https://learn.microsoft.com/en-us/azure/container-apps/log-streaming (retrieved 2026-10-20)
* W6 - Bicep deployment script - https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-script-bicep (retrieved 2026-10-20)
