<!-- markdownlint-disable-file -->
# Research: authenticated roster result transport design (#360, 2026-10-20)

Task: `demo-transport-plan-360`. Branch `docs/demo-transport-plan-360`. Research disposition: `executed`.
Scope: design and review checklist only. No cloud write, no execution, no secret/private data access.

## Authority and evidence boundaries

* Owner planning direction (issue #360 comment 6290697080) and unblock decisions (#126 comment 6290697705): documented authenticated transport alternative and tenant-administrator checklist for review. No allocation, retry, parser relaxation, decryption, deletion or paid run.
* Preserved adverse evidence (issue #360 comment 6277108234, 2026-10-19): three bounded temporary-job attempts, temporary resources confirmed removed, latest attempt refused provider console framing, original roster unchanged, no authenticated SQL projection or replacement candidate exists.
* Whole 360c/d/e remain unproved. Real sign-in, Graph authority, deployed SQL/AI remain unproved.

## Findings

| ID | Finding | Evidence |
| --- | --- | --- |
| F1 | Merged `infra/scripts/staff_azure.py` (since #375, 2026-10-17) already reads results from ARM resource tags via `Microsoft.Resources/tags/default`, not console streaming. The 2026-10-19 comment describes console decoding. Which code path the three attempts ran is not recoverable from repository evidence: flagged as an unresolved contradiction and a Phase 0 precondition | `git log -- infra/scripts/staff_azure.py`; runbook "Results use ARM only" |
| F2 | The tag relay has only had its IAM role configuration read back (2026-10-17). No tag value was ever written or read live, so it is unproven end to end | runbook "Approved existing-job relay delta" |
| F3 | Candidate output is position metadata only (`code`, `role`, `bound`, optional `contractor`); no names, UPNs or object IDs | `staff_roster.staff_candidates` |
| F4 | Synthetic size feasibility (local, no private data): 25 positions about 1.8-2.3 KB clear; 80 Programme-Manager-shaped positions about 5.4 KB (37 of 40 frames); 60 Contractor-shaped about 5.4 KB (36 of 40); 100 positions exceed the 40-frame bound. The real position count is unknown and was not read | local computation with `encode_result` arithmetic |
| F5 | Current AEAD associated data binds `[1, run, operation, input digest]`. The input digest covers payload, target app and relay. It does NOT bind worker image digest, worker script hash, manifest hash, query/projection version, result schema or a freshness deadline | `staff_azure.aad`, `execute` |
| F6 | The worker holds the result key, so an in-band image or script claim is self-asserted, not independent attestation. The controller can compare the ARM-read execution/job template image digest and its own repository file hashes against the claim | design reasoning |

## Official documented sources checked (2026-10-20)

| Topic | Source | Relevant fact |
| --- | --- | --- |
| Tag limits and warning | [Use tags to organize your Azure resources](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources), ms.date 2025-09-15 | Maximum 50 tag pairs per resource; tag value maximum 256 characters; tags are plain text and sensitive values may be exposed through cost reports, tag-returning commands, deployment histories, exported templates and monitoring logs; tag write needs `Microsoft.Resources/tags` write or write on the resource |
| Container Apps logs | [Log storage and monitoring options](https://learn.microsoft.com/en-us/azure/container-apps/log-options), ms.date 2026-08-18 | Log Analytics records are not instantly available; expect several minutes delay; live console is a separate streaming feature. This is a delay statement, not a completeness or framing contract |
| Container Apps jobs | [Jobs in Azure Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/jobs), ms.date 2026-09-16 | Jobs run to finite completion; permissions roles Jobs Contributor/Operator, Monitoring Reader optional. No documented result-payload channel |
| Blob Entra authorization | [Authorize access to blobs with Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/storage/blobs/authorize-access-azure-active-directory) | Blob data access authorized by Azure RBAC over an Entra token; needs reachability to the private endpoint |
| Deployment scripts | [Bicep deployment script](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-script-bicep) | The service creates a supporting storage account and container instance and bills them until removed; outputs return via deployment properties |
| ARM template limits | [Azure subscription and service limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits), ms.date 2026-08-04 | 64 template outputs, 4 MB template/parameter file |
| Repository posture | `infra/modules/monitoring.bicep`, `storage.bicep` | Log Analytics query access follows the private profile (Disabled); storage `allowSharedKeyAccess: false` |

Limits of this research: provider samples are not treated as exhaustive protocol guarantees. The tags API is documented as a resource-management API; consistency delay between write and read is not quantified in the sources read. Pricing was not retrieved and no cost is asserted.

## Options evaluated

| Option | Authenticated | Reachable from the operator without private route | Integrity and completeness evidence | New resource or authority | Verdict |
| --- | --- | --- | --- | --- | --- |
| T1 ARM tag relay of AEAD frames (existing, plus binding extension) | Entra and Azure RBAC over ARM | Yes, ARM is the management plane | Structured key/value records, per-run prefix, contiguous index/count, AEAD over whole ciphertext, terminal job Succeeded | None beyond the already activated tags read/write on the existing initializer job | Recommended proposal |
| T2 Blob result written by worker MI | Entra RBAC | No: private endpoint needs a private-connected controller, the same blocked route | Content-MD5, ETag, versions | New data-plane role and container or account | Decision-needed fallback if the roster exceeds T1 capacity |
| T3 Log Analytics KQL | Entra RBAC | No under production profile (query access Disabled) | Ingestion delay in minutes, no completeness contract | Reader role | Rejected as primary |
| T4 Deployment script outputs | ARM | Yes | Outputs recorded in deployment history | New storage account and ACI, charged | Rejected |
| T5 Provider/support clarification of console framing | n/a | n/a | Would give a contract for the failed path | None | Parallel owner action, does not block T1 |
| T6 Console stream or `exec` | Entra | Yes | Failed three times; no exhaustive contract | None | Excluded: no parser relaxation |
| T7 Send no candidates; derive positions from a versioned synthetic manifest | n/a | n/a | Removes return payload | None | Decision-needed: only if the owner confirms positions are not SQL-authoritative |

## Planning Readiness

Ready. Selected T1 with explicit decision-needed items DN1-DN4 in the plan. Follow-ups: engineering implementation of the binding extension and synthetic tests (later task); cost/execution plan approval (#126, later precondition).
