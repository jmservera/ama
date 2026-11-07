---
title: R10 queue dispatch design checkpoint 440 research
description: Research for the seventeenth documentation-only checkpoint that records the 144 R10 design as an independently assessed, unapproved proposal
ms.date: 2026-11-06
---

## Identity and method

Task `440-r10-design-checkpoint`, a new material-design checkpoint increment, not a further correction of the r58, correction 1, correction 2, post-integration batch or batch correction 1 records. Start HEAD `c582e44b199a60baa6145accd0d3fa786b9360a6`, tree `797a91423995b880ba22b6b6f98d2e054586ed27`, ignored-inclusive status 0 lines. The `rpi-research` skill body was loaded through the skill tool before this record. Posture focused, three inline waves, no worker. Documentation and design observation only: no test, SQL, browser, container, install, scanner or provider call.

Fresh pins (fetch of `main` and the governance branch exit 0, 2026-11-06 about 14:05Z): governance `origin/feat/discovery-assurance-integration-123` `119828353ccc1d678c1a4e9c1c67b621b0d263a0`; main `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f`.

Inputs read: both supplied root assessments (`440-c1-root-assessment-r66.md`, `144-r10-root-design-assessment-r66.md`) and the whole R10 design plus its critique and Review through pinned Git objects of `/home/azureuser/source/ama-wt/issue-144-queue-recovery`.

## Pinned R10 identities (observed with git)

| Item | Identity |
| --- | --- |
| R10 final commit | `1e19209985d93e053dd449e873e792f214dd110c`, tree `7c6126374cbd6e5f5c2e62479cbee1dea98d75e3` |
| Design file | `.copilot-tracking/design/2026-11-06/issue-144-r10-dispatch-protocol-design.md`, 15360 bytes, blob `de776799aafc925c372c6c1c85e0c72ecc75b389` (supplied; to be re-resolved in the checkpoint) |
| Planning commit used as the design source pin | `3b1f51849d4108581fcbe7fc5059ce61fb448c80`, tree `99ef99e47550dd5a8a62dd6eb0be28e91af30272`, parent `323abba2e6f392e54c4ac27b427e00d05a3e6782` (the R9 design) |
| Merge base of the source pin with main | `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` |
| `src` difference of pin against main | 12 files, +1241/-18 (the unmerged queue slice; identical size to the earlier candidate `4c878d664`) |
| Other R10 records (8, same date) | research, plan, details, critique, changes, review, state JSON and a log entry in the 144 worktree |

## Finding 1: source facts split into main and candidate-only (observed)

Static `git grep` at the pin against main:

* On main and at the pin: `EVENT_FIELDS` and `meter-evidence-invalid` in `ai_consumption.py`, `FINANCE_ROLES` in `controls.py`, the SERIALIZABLE and BEGIN IMMEDIATE transaction in `assistants.py` (line 449 to 450 at the pin).
* Pin only (absent on main): `queue_azure.py` (`MAX_DELIVERIES` 5, `visibilitytimeout` set to the lease, `release` with `visibilitytimeout` 0, HTTP timeout), the worker, the `_worker_complete` route and the service-caller wiring in `server.py`.

So the R10 design's "established code facts" mix merged-main code (ledger, roles, transaction) with unmerged candidate code (queue, worker, completion route). The checkpoint must label each. These are implemented-unverified observations from reads, not runtime evidence.

## Finding 2: document trace in the design is partly mis-cited (new, documentation only)

The design's "Evidence gaps" section cites "ADR 0002 decision 6, PRD PR-005 and NFR-002". Reading the documents at governance and main (identical blobs):

* ADR 0002 "decision 6" appears in the status table as "Dockerfile and CI (decision 6)" and in the Dockerfile area, not in a dispatch or consumption decision. The fourteenth checkpoint already recorded this mis-citation for the candidate.
* PRD `PR-005` (line 487 of the PRD) is "load and operate over the whole stock of about 60,000 homes" with server-side paging; it is unrelated to queued AI dispatch.
* The matching requirements already traced in the fourteenth checkpoint are PRD FR-061 and NFR-017 with AC-107 to AC-110, joined to BRD FR-052, NFR-012, AC-100 to AC-103 and OD-51.

This is a non-blocking trace error in the supplied design, not a contract defect. The new checkpoint records the correct document-qualified trace and says the design's citation is not carried forward.

## Finding 3: topology of `feat/infra-hosting-integration-136` (observed, differs from the supplied brief)

* `git rev-parse --verify refs/heads/feat/infra-hosting-integration-136` returned `bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f` (exit 0) in this repository. Its reflog first entry reads "branch: Created from origin/main". So a LOCAL ref exists and equals main.
* `git ls-remote --heads origin feat/infra-hosting-integration-136` returned 0 lines; `git fetch origin feat/infra-hosting-integration-136` failed with "couldn't find remote ref" (exit 128); `gh pr list --state all --head feat/infra-hosting-integration-136` returned `[]`.
* The supplied brief says no local or remote ref exists. That statement is not supported for the local ref in this worktree's repository as observed now; it is supported for the remote and PRs. The local ref is an unpublished label equal to main, not a verified published parent and not evidence of ancestry or approval.

Decision: record the local ref at `bb3a3b03` as observed, remote absent, no PR, and the eventual code parent as UNKNOWN until a deliberate resolution. The R10 design's "parent 136 at bb3" is equal to main only; main is the only verified pin. No branch is created, retargeted or published here.

## Finding 4: independent technical assessment of the design (read, not tested)

Wave one (wider), two (deeper) and three (contrarian) over the design sections A to H and the 14 critique findings:

* Each of PC-001 to PC-014 has a stated proposed contract in the design (rollback or committed-denial per permit step; DB-time revalidation after the row lock; queued provenance event; marker-bound settlement; closed-without-permit ordering; evidence-gated `unused` reconciliation; identity check before eligibility; `conflict_key` dedupe; held null amounts and report cutoff; `request_plan` with deployment and temperature; optional `dispatch_check_request`; one monotonic deadline; backoff and authentication hold; the ledger `reconciled` event as durable audit). That is design coverage, not behavioral closure.
* Contrarian items, none establishing a new blocking design flaw:
  * `unused` reconciliation relies on free-text evidence naming a provider record; code cannot verify it. The design keeps the hold when evidence is missing, but conclusive provider evidence stays Finance-owned and unobserved (U4). Risk recorded, owner Finance.
  * The marker only binds callers that use the single permit route; a worker that skips the permit is out of API scope (design says so).
  * 40 s stale-liability window versus the 35 s nominal timing leaves 5 s margin; real Azure timing is unobserved (U3).
  * Queue mode requires `Limits.lease >= 45` and visibility equal to the lease; the candidate visibility is configured per queue object, so a startup validation test is required. Proposed, not present.
  * ADR 0003 decision 1 ("no new service, queue, store or network path") tension recorded in the fourteenth checkpoint remains unresolved; no ADR change is made.
  * The design supersedes the preliminary R10 Research, Plan and Details where inconsistent (optional digest method, strict reconciled field set). The Research "closed" wording means design coverage only.
* Process observations carried from the root assessment (not repeated as mine): the critique ran once (13:50:29 to 13:51:53 per root), Review followed checks; R9 qualifications are preserved.

Root assessment independence: I agree with the root conclusion that no new blocking design finding exists, with one addition (Finding 2, trace mis-citation) and one correction of the supplied topology (Finding 3, local ref present). I did not run tests, so runtime behavior, SQL races (U6), Azure poison and delayed visibility (U3), provider evidence format (U4) and hosted configuration equality (U7) remain unobserved.

## Document identities (resolved now, not guessed)

At `HEAD`, governance and main the blobs are identical: BRD 0.21.0 draft `34d88395de861e9799eb9e24121a21c92c7a5adc`; PRD 0.21.0 in-review `c788b917bafaede215f326f0efc71e071a687f1c`; ADR 0001 `d42fa5c4615f4107cee83e07555dba6985c1f53e`; ADR 0002 `cbe21530043ff15432cc6dce1086d080f5eb15b4`; ADR 0003 `d60645397b20fb70ac3d1dc47c7a6c8671201306`; ADR 0006 `956da1a3b804c803041fe2e8a312bd9f400273ae`. Draft and in-review are not approval. Statuses for ADR 0001, 0002 (Proposed), 0003 (accepted with owner amendment) and 0006 (accepted) are as recorded in the fourteenth checkpoint and not re-derived here.

## Owners and exclusions

Owners: #107 (core ledger, engine, reconcile route), #144 (permit route, worker), #118 (queue visibility and Foundry settings), #122 (identity, no new grants). Both owner CODE decisions (issue 144 comments `6681120797` and `6685915140`) stay resolved and are code-role authority only: no live grant, spend, deployment, financial waiver or ADR acceptance. Excluded: runtime test, SQL, browser, container, scanner, implementation, new issue, branch creation, publication, closure, ticks.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for a documentation-only seventeenth checkpoint. Recommendation to carry: CONTINUE a bounded tests-first runtime correction only after coordinator acceptance of this checkpoint, with FULL, real SQL, independent exact-head and hosted gates before publication; HOLD worker enablement, spend, live acceptance, main and whole-issue closure. Original High 1 and High 2 stay OPEN. No confirmed new runtime defect. Resume: coordinator consumption, then an independent genuine full RPI for the code slice.

## Smallest remaining unknowns

* The next pack heading number (the pack currently ends at the Sixteenth checkpoint plus a provenance subsection; the plan must allocate the Seventeenth after rereading the headings).
* Whether the design blob re-resolves to `de776799` (to be re-read from the pinned object in implementation).
