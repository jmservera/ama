<!-- markdownlint-disable-file -->

# Task Research: demo-transport-blob-360

| Field              | Value                                                                   |
|--------------------|-------------------------------------------------------------------------|
| Date               | 2026-10-22                                                              |
| Researcher / agent | rpi-research skill (RPI Agent, automatic mode), continuing #360 / PR #423 |
| Status             | Complete                                                                |
| Artifact path      | .copilot-tracking/research/2026-10-22/demo-transport-blob-360-research.md |

Parent lineage: `demo-transport-plan-360` and `demo-transport-plan-360-recovery` (2026-10-20). Their artifacts, critique and review are preserved unchanged. This task supersedes only the tag-relay proposal (T1) under owner decisions DN1 to DN5 of 2026-10-22.

## Research Brief

* What to research: the smallest private-connected path to return SQL staff-job results through a private Blob container with managed identity, based on actual infra, and the precise remaining live prerequisites.
* Why it matters: the console path failed three times and the tag relay was rejected by the owner (DN1).
* Audience: coordinator, independent reviewers, later live operator.
* Scope: `infra/scripts/staff_azure.py`, `staff-azure-worker.py`, `staff_roster.py`, `setup-entra.py` consumer, `infra/modules/storage.bicep`, `infra/staff-initializer-rbac.bicep`, `infra/main.bicep`, tests, `infra/README.md`, cutover evidence pack, KB index and log.
* Non-goals: Azure charges, deployment, tenant change, role grants, live jobs, Front Door or resource deletion, private dataset or roster reading, parser relaxation, web or visual work.
* Criteria: no public Blob, SAS, shared key, tags or console fallback; strict schema, run binding, expiry, count and size; explicit errors; claims limited to evidence.
* Requested outputs: design revision, offline implementation, tests, live prerequisites.
* Output mode: convergence.

## Research Parameters

| Field | Value |
|---|---|
| Research posture | balanced |
| Posture provenance | default; bounded internal task with named sources and owner decisions |
| Explicit limits | caller: no new Azure charges or tenant mutation; offline fakes only |
| Edits allowed during research | no, research-only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Disposition |
|---|---|---|---|
| Instruction | AMA repository instructions | applyTo `**` | Selected: RPI gate, branch, KB, regulatory boundaries |
| Instruction | Web guidance | web files only | Skipped: no web files change |
| Skill | rpi-research, rpi-plan, rpi-implement, rpi-review | caller direction | Selected, one per phase |
| Specialist | explore / RPI Researcher | single continuous trace | Skipped; waves inline |

## User Participation and Research Decisions

| Checkpoint | Rationale | Decision |
|---|---|---|
| Intake | Non-interactive; owner decisions DN1 to DN5 supplied | Adopted as active controls |

## Direction Controls

| Control | Boundary | Source | Effect |
|---|---|---|---|
| change | DN1 private Blob with managed identity, no tags, backing services private | owner 2026-10-22 | T1 superseded, T8 promoted |
| add | DN2 complete results, measure size, bounded paging, no silent truncation | owner | paging, not compression or reduction |
| add | DN3 three old failures remain unknown historical transport failures; retire old demo code paths; no Azure resource or Front Door deletion | owner | tag and console code removed from demo path |
| add | DN4 production roles manual; demo may match from available evidence else random; admin-prefixed stays ProgrammeManager; no directory roles; app roles stay authorization | owner | design text; existing behaviour verified |
| add | DN5 controlled demo worker checks; independent signed attestation unverified and deferred | owner | trust statement |
| exclude | charges, deployment, tenant mutation, grants until coordinator release | owner | offline only |

## Research Questions

| # | Sub-question | Priority | Status |
|---|---|---|---|
| Q1 | Which tag and console code and tests must be retired and who consumes them? | H | answered |
| Q2 | What storage, network and RBAC exist for a private Blob result? | H | answered |
| Q3 | What is the smallest controller path that can read a private Blob? | H | answered |
| Q4 | What guarantees strict schema, binding, expiry, count, size and completeness? | H | answered |
| Q5 | How large is a result and is paging needed? | M | answered (synthetic) |
| Q6 | What does DN4 require of existing role code? | M | answered |
| Q7 | Which live prerequisites remain? | H | answered |

## Prior Knowledge Gate

* Reviewed: all `*-360-*` tracking artifacts (research, plans, details, changes, critiques, reviews, state), the 2026-10-20 design, `infra/README.md` in-VNet staff and transport sections.
* Reused (verified): AEAD envelope, per-run key, input digest and job lifecycle guards (C1, C2). Preserved negative evidence: three temporary-job recovery attempts failed at console decoding; no tag value was ever written live.
* Superseded: T1 tag relay, relay-tag capacity gate, reviewer-pending DN1 to DN5 status.

## Research Cycle Log

### Cycle 1

* Active controls: all above. Posture balanced. No limit effect.

#### Wave 1: Wider

* Inline lanes: code consumers, infra storage/network/RBAC, official Azure docs, role-assignment code.
* Reflection: tag/console code is localized to `staff_azure.py`, the worker and `test_staff_azure.py`; infra already has a private Entra-only storage account with private endpoint; the open item is the controller route.

#### Wave 2: Deeper

* Prioritized: Q2, Q3, Q4.
* Findings: the account is private (public Disabled, shared key off, anonymous blob off, OAuth default) with versioning and 30-day soft delete; no `staff-results` container exists; the initializer identity has no Blob role; `setup-entra.py` runs on an operator host with no VNet route.
* Reflection: worker-to-Blob is fully private in-VNet; only the controller read lacks a route.

#### Wave 3: Contrarian

* Challenges: (a) keep tags? Plaintext metadata, 50 x 256 limits, frame cap blocks complete results (W3, DN2). (b) Controller job reads Blob and returns via ARM? Its output still has to egress, recreating the failed problem. (c) Allow operator IP on the storage firewall? Mutates network and violates DN1. (d) SAS or shared key? Excluded by DN1 and by `allowSharedKeyAccess: false`.
* Reflection: the smallest compliant path is a private-connected operator host, the same host class already required for read-only setup modes; no new resource if one exists, otherwise a precise live blocker.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
|---|---|---|---|
| Worker writes AEAD pages to private Blob via MI | C3, C4, W1 | accepted | In-VNet, no secret, container-scoped role |
| Controller reads via Entra from a private-connected host; unreachable is an explicit refusal | C3, W2 | accepted | No route from an ARM-only laptop; no fallback |
| Dedicated container `staff-results` plus prefix lifecycle expiry | C3, W1 | accepted | Container scope is the narrowest role boundary |
| Keep AEAD inside Blob | C1 | accepted | Defence in depth; versions and soft delete retain ciphertext 30 days |
| Controller deletes blobs | C3 | rejected | Needs Contributor for the operator; expiry plus reader-enforced not-after instead |
| Paging with total, size, digest | C1, C5 | accepted | DN2 |
| Tag relay | C1 | retired from demo path | DN1, DN3 |
| Signed attestation | n/a | deferred, unverified | DN5 |

Re-entry decision: no further cycle; remaining gaps are live-only.

## Evidence Log

| ID | Evidence |
|---|---|
| C1 | `infra/scripts/staff_azure.py:22-135` tag and chunk encode/decode and `aad`; `:306-489` `execute` reads and clears tags; `MAX_CHUNKS = 40` at `:17` |
| C2 | `infra/scripts/staff_azure.py:140-300` `discover` binds API, SQL, identity, image; relay capacity gate at `:214-219` |
| C3 | `infra/modules/storage.bicep:20-62` private account properties, versioning, soft delete; `:63-67` container list; `infra/main.bicep:213-235` role list; `infra/modules/containerapps.bicep:154` `ZF_BLOB_ACCOUNT_URL` |
| C4 | `infra/staff-initializer-rbac.bicep` result-tag custom role; `infra/scripts/staff-azure-worker.py:57-110` tag publisher and ARM adapter |
| C5 | `infra/scripts/staff_roster.py:55-65` `staff_candidates` row shape |
| C6 | `infra/scripts/setup-entra.py:1101-1103` consumer of `staff_azure.execute`; `infra/tests/test_staff_azure.py:118-284` fake ARM relay |
| C7 | `src/api/requirements.txt` pins azure-identity 1.26.0, azure-storage-blob 12.31.0, cryptography 50.0.2 |
| W1 | https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview (retrieved 2026-10-22): prefix filters; up to 24 hours before changes take effect |
| W2 | https://learn.microsoft.com/en-us/azure/storage/common/storage-private-endpoints (retrieved 2026-10-22): private endpoint clients are on the VNet or VPN/ExpressRoute-connected networks |
| W3 | https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources (ms.date 2025-09-15; retrieved 2026-10-20): tags are plain text, 50 names, 256-character values |

## Findings by Question

* Q1: retire `result_prefix`, `tags_url`, `result_tags`, `read_result`, `clear_result`, chunk encode/decode, `TAG_VERSION`, `MAX_CHUNKS`, the relay tag capacity gate, the worker tag publisher, the tag role in the RBAC Bicep and their tests (C1, C2, C4, C6). Keep ARM `Management.call` for the verified restart.
* Q2: needed: container `staff-results`, a prefix lifecycle rule, initializer identity Storage Blob Data Contributor at that container only, operator Storage Blob Data Reader at that container only, and a network route for the reader.
* Q3: ARM control (create, start, stop, delete job) works anywhere; the Blob read needs line of sight (W2). If unreachable the run reports outcome unverified and cleanup still happens. The per-run key exists only in the job secret and controller memory, so left-behind blobs cannot be decrypted later (critique PC-001, corrected after critique). Recovery is a new, separately authorized run from a private-connected host, never a hidden retry; the controller should therefore preflight the Blob route (list the container) before creating any job.
* Q4: envelope v2 binds version, run, operation, input digest, schema, page index and count, item and byte totals, image digest, created and not-after through AEAD associated data; strict blob names; one listing snapshot; exact page set; bounded sizes; unknown fields refused.
* Q5: synthetic rows are tens of bytes of JSON; paging at 64 KiB keeps complete results without reduction. Real position count unknown and not read.
* Q6: no code assigns directory roles; admin-prefixed ProgrammeManager behaviour exists since #363. Design text only, plus a regression check where cheap. No names, UPNs or object IDs are collected.
* Q7: listed in the README design section.

## Alternatives

| Alt | Verdict |
|---|---|
| A Worker MI writes private Blob; controller on private host reads (selected) | Recommended |
| B ARM tags (T1) | Superseded by DN1 |
| C Controller job relays to operator | Rejected: same egress problem |
| D Operator-IP firewall exception, SAS or shared key | Rejected by DN1 |
| E Log Analytics or console | Rejected |

## Risks and Open Items

* Controller route and Entra data-plane roles unproven live.
* Versioning and soft delete retain deleted ciphertext 30 days; per-run key limits exposure; privacy review needed.
* Lifecycle expiry can take 24 hours or more (W1); expiry is enforced by not-after in the reader.
* No write-only built-in role; the worker identity could overwrite within its own container; exact-set validation and AEAD detect it, residual risk documented.
* Image and run identity checks are controlled-demo checks only (DN5).

## Planning Readiness

* Research disposition: executed (inline; lanes tightly coupled).
* Planning Readiness: Ready. Selected Alternative A.
* Self-check: C# have path:line, W# have URL and date; no secrets, names, UPNs, object IDs or roster contents read.
