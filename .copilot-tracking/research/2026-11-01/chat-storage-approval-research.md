<!-- markdownlint-disable-file -->
# RPI Research: Chat storage approval (synthetic-data demo)

* Task slug: chat-storage-approval
* Date: 2026-11-01
* Research disposition: executed
* Planning Readiness: Ready

## Owner decision

2026-11-01T17:46Z, Juan Manuel Servera (DPO/Legal/Compliance owner): "Approve all needed to enable storage." Scope is the synthetic-data demo only; production and real data need separate approval (#163 criteria 2 and 5 deferred).

## Findings

* `ChatPrivacy.decision()` (`src/core/src/zava_forward/core/chat_privacy.py`) reads `CHAT_DPIA_REF`, `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF` from the process environment (trimmed); storage is approved only when all three are non-empty. Retention is set only when `CHAT_RETENTION_REF` is non-empty and `CHAT_RETENTION_DAYS` is a positive integer. `regulatory_privacy.py` reads the retention pair; `regulatory_chat.py` reads the three refs.
* The employee UI (`web/chat.js`) shows "Chat storage is not approved yet" when `admission.storage_approved` is false; `server.py` maps `ChatNotApproved` to a refusal.
* Employee API image (`ca-cutover-test-demo-api`, the live employee demo site; also module `ca-cutover-test-api`) is the only workload that imports ChatPrivacy. The resident demo (`src/api/.../resident_demo`) and the agents app have no ChatPrivacy or thread storage; they read no CHAT_* settings. Settings on them are inert.
* Existing docs: `docs/reference/research/chat-memory-dpia.md` (draft DPIA, decision pack D1-D8 blank, from #727); #739 decisions record; none held a lawful basis, notice or retention reference.
* Deploy path: `infra/modules/containerapps.bicep` (api env, via `main.bicep`; `main.test.bicepparam` holds the cutover-test values) and `infra/resident-demo.bicep` deployed by `infra/scripts/resident_demo_deploy.py` (what-if guard, exact resource allow-list).
* Live (az, RG ama): apps `ca-cutover-test-api`, `ca-cutover-test-demo-api`, `ca-cutover-test-agents`, `ca-resident-demo`, all min replicas 0; eight jobs, all Manual.

## Decisions

* Retention 30 days (demo; rationale in the decision record).
* Refs are repo paths with anchors in `chat-demo-storage-approval-2026-11-01.md`.
* Infra: five scalar parameters (default empty keeps refusal); env added only when all four refs are set. Resident template defaults hold the demo values. Agents app unchanged (no chat storage).

## Follow-ups

* Real-resident and production approval (DPO/Legal), D2, D6, D8.
* Resident demo has no chat storage; "resident chat stores a thread" cannot hold.
