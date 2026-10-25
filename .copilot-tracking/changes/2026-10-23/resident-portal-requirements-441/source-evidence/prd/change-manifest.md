---
title: Resident PRD draft integration and dependent-document manifest
date: 2026-10-23
status: draft
---

## Included change and sequence

Only `docs/prds/zava-forward-retrofit-programme-demonstrator.md` is targeted
by this package's `amendment.patch`. Nothing has been applied to the repository.
Use the pinned commit and exact base/candidate hashes in `validation.json`.
No local dirty content, stale detached HEAD or historical PRD alias is the
patch authority.

Parent sequence: BRD draft integration/reconciliation, this PRD draft,
then ADR commission using `adr-handoff.md`; owner/quality decisions and
implementation remain separate. Resolve BRD FR-044/AC-084 before activating
any routine exception. Re-read registries/current main at actual integration;
base drift requires deliberate rebase and fresh hashes/review, not fuzzy
application. No git operations, worktree changes or repository PR are done here.

## Dependent documents (not edited by this task)

The upstream `../brd/change-manifest.md` remains the fuller source/rationale
inventory. These rows refine its PRD/ADR dependencies without claiming they
have been delivered.

| Path | Required prospective reconciliation | Preserve |
| --- | --- | --- |
| `docs/brds/agentic-retrofit-programme-brd.md` | Integrate unsigned v0.20.0 scope and resolve FR-044/AC-084 exception wording; retain OD-52 to OD-55 and blocked gates | BRD IDs/history, unrelated inherited issues, no fabricated Govern exit |
| `docs/case_study_48_addendum.md` | Append dated owner optional-portal direction, PRD candidate mapping and proposed routine policy delta; link controlled BRD capacity model | Historical EXA-004 inclusion, old per-message finding, old exercise acceptance and budget history |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md` | Apply this surgical v0.19.0 candidate patch after exact-base verification; new ranges in `id-traceability.md` | Existing FR/AC/NFR/CON/GOAL/DD definitions, eleven staff profiles, staff/regulatory/no-send scope and false completion markers |
| `docs/reference/research/ux/customer-journeys/residents.md` | Add six constructed optional self-service jobs and assisted equivalents, household/representative/recovery negatives, grounded/human-held replies | Desk research is not direct resident validation; no required portal and no persistent resident memory |
| `docs/reference/research/ux/customer-journeys/frontline.md` | Add shared source event, no re-entry, manual connector gaps, owned exception and accepted-handoff workflow | Existing human/safety/service authority and non-digital routes |
| `docs/reference/research/ux/customer-journeys/customer-journey-atlas.md` | Link new resident projection/answer task separately from five staff assistants and prospective dispatch exception | Historical counts and hypotheses until actually amended; no broad autonomous-agent scope |
| `docs/reference/research/ux/zava-forward-prototype-profile-review.md` and `docs/reference/research/ux/content-standard.md` | Add resident AI disclosure, approved/received/reviewed/confirmed distinctions, safe-contact/help/error wording | Existing staff review observations are not evidence of a built portal |
| `docs/reference/research/ux/wcag-conformance-baseline.md` and `docs/reference/research/ux/design-system.md` | Extend engineering checks to core resident mobile sign-in/upload/appointment/help and assisted recovery | No conformance/user-validation claim; privacy/accessibility are essential demo tasks |
| `docs/adrs/0001-azure-architecture.md`, `0002-pilot-readiness-architecture.md`, `0003-journey-derived-capabilities-runtime-fit.md` | ADR specialist reads actual paths under `docs/adrs/`; compare new identity/files/events/task/service requirements after PRD | Existing accepted-build Azure/SQL/real-AI evidence and proportional topology; no new deployment permission |
| `docs/adrs/0004-per-user-agent-chat-and-memory.md` | Explicit new resident trust boundary/cross-reference in later ADR, not expansion of staff acceptance | Staff-only private chat/memory, existing authority/review |
| `docs/adrs/0005-regulatory-compliance-assistant.md` | Later ADR confirms regulatory assistant remains no-send and separate from resident-answer task | Existing no legal conclusion/rule activation and no resident communication authority |
| New ADR path chosen after current registry inspection | Commission decision/options output from `adr-handoff.md`, including service/security/agent-autonomy needs | No ADR number/status/acceptance invented here |
| `docs/architecture/zava-forward-executive-architecture.excalidraw` and `.svg` | After ADR, show proposed resident projection/trust boundary alongside dated observed staff baseline; regenerate source/export together | “No resident portal needed” remains dated history, not current prospective exclusion; accessible text equivalent |
| `docs/reference/research/retrofit-synthetic-data/README.md`, `data-dictionary.md`, `needs-inventory.json`, `scenario-manifest.json`, `provenance-register.json` | Inventory needed fictional identity/grant/household/representative/event/upload fixtures with six-script manifest | Continue generated 60,000-home/980-case history; no estate regeneration, real resident data or implied verified links |
| `docs/reference/README.md` | Route current BRD/PRD/ADR draft chain and separate namespace/counts; link unresolved routine policy | Historical snapshots and unsigned status; no approval laundering |
| `docs/reference/log.md` | Append dated amendment chain, exact source/hash, owner scope, hypothetical pitch and new IDs | Append-only historical findings/decisions/test evidence |
| `docs/capstone/README.md` and pitch/presentation assets | Present the linked 14.74-hour hypothetical capacity case and downside, not observed benefit, resident count, cash or headcount saving | Existing staff capability/demo status; no premature resident implementation claim |
| `docs/case_study_48_original.md`, `docs/reference/memory.md`, `docs/prds/proper-warm-retrofit-programme-demonstrator.md` | No rewrite; if needed, dated routing cross-link only in authorised later scope | Immutable source, owner-controlled memory and historical renamed PRD |

## Package-only artifacts

`amendment.patch`, `amendment.md`, `id-traceability.md`, `adr-handoff.md`,
`change-manifest.md`, `quality-review.md`, `validation.json`, `state.json`
`reviewer-findings.yaml`, `reviewer-report.yaml`, `.markdownlint.json`
and `validate-package.py` are session authoring/evidence artifacts, not a new
canonical repository tracking tree or approved PRD copy. The validator prints
to stdout and reconstructs candidate bytes in memory only.

State is deliberately located here rather than in
`.copilot-tracking/prd-sessions/`, under the user's write restriction.
There is no copied replacement PRD, repository code or implementation plan.
