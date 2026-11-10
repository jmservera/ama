<!-- markdownlint-disable-file -->
# Issue 184 IoT demo deployment-readiness metadata slice: plan (2026-11-10, Refs #184 #440)

Prospective plan for task `issue-184-cloud-readiness-1110`. Stage boundary: this plan is written and frozen now; the Implement phase is NOT started and waits for Root's disposition of the shared knowledge-base file ownership held by the 108 workstream. No Implement or Review marker exists or is claimed.

Research: [issue-184-cloud-readiness-1110-research.md](../../research/2026-11-10/issue-184-cloud-readiness-1110-research.md). Details: [issue-184-cloud-readiness-1110-details.md](../../details/2026-11-10/issue-184-cloud-readiness-1110-details.md). Critique: [issue-184-cloud-readiness-1110-critique.md](./issue-184-cloud-readiness-1110-critique.md).

## Objective

Record the five dated ARM configuration observations already taken (Research Part B) in the smallest existing IoT knowledge-base location, with the evidence class and limits stated, so a later live-transport or deployment admission starts from current real metadata instead of the 2026-10-29 and 2026-11-08 snapshots. No new page, no source, test, infra, runbook, workflow, issue, board or PR change, and no further Azure call.

## Fixed decisions

* Scope: existing synthesis [`docs/reference/research/iot-sensor-analytics-research-plan.md`](../../../docs/reference/research/iot-sensor-analytics-research-plan.md) (one dated subsection), the existing #110/#184 paragraph of [`docs/reference/README.md`](../../../docs/reference/README.md) (index), and one appended entry in [`docs/reference/log.md`](../../../docs/reference/log.md). The #440 sensor checkpoint in `docs/architecture/cutover-evidence-pack.md` is linked, not edited.
* Shared-file ordering: README.md and log.md are written only after Root releases the 108 ownership (merged, or an explicit no-KB-change blocked disposition). There is no functional dependency on 108, only write ordering.
* Claims allowed: dated ARM configuration observations only. Not claimed: ingestion works, runtime proven, build provenance, schedule executed, authorized budget, Azure acceptance, stream/UI/quality success. Unknown or not-found is stated with its exact scope, never as "absent everywhere" or zero.
* The whole #184, #110, #140 and #440 criteria stay OPEN; no ticking, no closing keyword.

## Phases

* [ ] Phase 1: Resume gate. Confirm Root's written release and the exact file ownership; fetch `origin/main`; if it moved, merge-tree check overlap with the three target files and re-read their anchors. Stop if not released or if the 108 change touched the same paragraph in a conflicting way.
* [ ] Phase 2: Synthesis update. Add one `###` subsection at the end of "Bounded streaming engineering (2026-10-27, Refs #110, #184)": the observation table (Q1 to Q5 results, times, exit codes), evidence class, unknowns, and the not-claimed list; link the #440 sensor checkpoint and the infra README sections it qualifies. Raise `ms.date` to the observation date if the front matter date is older.
* [ ] Phase 3: Index and log. Append two to four sentences to the existing #110/#184 README paragraph linking the new subsection; append one log entry `## [2026-11-10] update | ...` at the end of `log.md` without touching earlier entries.
* [ ] Phase 4: Validation (documentation only, focused tier): link and anchor check of every new link, Git diff review restricted to the planned files plus tracking, GUID/secret/endpoint scan of the diff, confirmation that no Azure command ran after the research stage, and the external handoff cross-check of query counts.
* [ ] Phase 5: Own-stage closeout (a later Implement stage): changes record, then an independent Review, owned by later RPI invocations. Not part of this stage.

Classification and basis: documentation-only, read-only metadata; focused tier per the repository validation policy. The full gate does not apply because there is no source, infrastructure, deployment, SQL or security-control change. Hosted CI and independent review are still required before publication.

## Dependencies and risks

| Item | Handling |
| --- | --- |
| 108 owns `README.md` and `log.md` until merged or an explicit no-KB-change disposition | Phase 1 gate; no KB edit until Root releases |
| `main` movement changes README or log anchors | Phase 1 merge-tree check; anchors re-read, not trusted |
| Observation staleness (taken 2026-11-10T17:54Z) | Text states the time; resume does not re-query unless a new explicit authorization exists |
| Overstating a configuration observation | Not-claimed list and "ARM configuration observation" wording are acceptance checks in details |
| Leak of identifiers | Scan for GUIDs, endpoints and key material before commit; the digest reference is a public image reference and is kept short |

## Follow-ups (evidence-grounded, not selected)

1. Owner-approved admission input list: device registration and certificates, receiver identity grants, SQL tables and grants, hub route and Entra receive limitation, image provenance for the digest, current usage and a renewed finite budget. Each is a separate explicit authorization. Basis: Research Part B gaps.
2. Identify the existing Manual jobs from the 2026-11-08 handoff by exact name from existing project records before any later job-level query. Basis: Q4 and Q5 not found, handoff inventory unnamed.
