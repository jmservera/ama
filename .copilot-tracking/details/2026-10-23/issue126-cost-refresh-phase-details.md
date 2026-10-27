<!-- markdownlint-disable-file -->
# RPI Phase Details: issue126-cost-refresh

## Metadata

* Task ID: 126
* Task slug: issue126-cost-refresh
* Related plan: .copilot-tracking/plans/2026-10-23/issue126-cost-refresh-plan.md
* Evidence: .copilot-tracking/research/2026-10-23/issue126-cost-refresh-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Scoped evidence and minimum proposal | Complete | P01-T01, P01-T02 |
| P02 | Validation and conditional publication | P02-T01 complete; P02-T02 pending | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Refresh supported cost synthesis

Current proposal lives in docs/case_study_48_addendum.md. Preserve dated
2026-10-20/22 history and add a current subsection before superseded history;
update the existing introduction to point to it. No Azure operation is part
of implementation.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Current scoped cost evidence

Include exact API bodies semantically (ActualCost, Custom, daily Sum PreTaxCost,
1-23 October; forecast23-31 with includeActualCost/includeFreshPartialCost),
sanitized scope, timestamps, no-nextLink, totals and lag/source caveats.
Include enough daily values to reproduce arithmetic, or exact aggregate terms
and separately identified partial actual. Service-derived provisional RG total
does not satisfy the complete-post-change-day rule. All-in actual/forecast and
headroom remain Unknown, not USD700 less scoped actual or scoped forecast.

Targets: existing addendum only. Dependencies: Research W2-W6. Validation:
Decimal recomputation, one partial-actual inclusion, no saving deducted,
USD700 not additional. Completion: changed subsection and source references.
Unresolved: inaccessible subscription cost and other charges, not a docs blocker.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Finite minimum demo and knowledge navigation

Dependencies: P01-T01. Keep at most a two-hour attended envelope ending before
2026-10-25T16:02Z, six-hour approval/cleanup margin (latest start08:02Z on25Oct).
First public welcome checks independent of SQL/tenant/AI; then one real
synthetic owner sign-in/role and minimal SQL persistence/restart verification;
one private result object (at most10MiB/10writes/30reads); one real AI draft,
one attempt/no retries, at most2000 total input and256 output tokens including
overhead or refuse. Reuse existing resource and model only when its identity,
capability, quota and rate are verified; otherwise exact model/bootstrap
pricing is a separate blocker, not permission to deploy.

Existing SQL remains authority; no reseed or private data read. Later approved
synthetic SQL evidence must use isolated owned records and preserve histories.
Private Blob path/managed-identity permissions must be verified by an authorized
operator, not inferred from a private endpoint. Do not add a VM/Front Door,
environment, database or photo-token-store merely to show welcome.

Incremental prices must come from current effective agreement meters or dated
official region/currency/model rates for API/SQL/Blob/PE/logging/AI and retained
liabilities; prior allowances are not quotes. Total remains Unknown if any
required rate/usage term is unbounded. Separate owner approval must identify
exact mutations, rollback, resulting E/L, reserve and stop conditions.

PC-002 resolution: use the existing works-resident-coordination draft capability,
POST /api/assistants/works-resident-coordination/invoke and the protected
Assistant proposals queue (src/api/src/zava_forward/api/server.py; roles and
allowances in src/agents/README.md). Propose one explicitly fictional
coordination case with a pending handoff; no sending, scheduling, consent or
acceptance action. Evidence chain: authenticated app200 and expected permitted
role, approved synthetic case/run reference, one actual provider attempt with
usage, draft visible to owner, same proposal/reference persisted across API
restart in SQL, and one private synthetic result object associated with that
run. If current image/path/capability/token reservation cannot support these
bounds, stop at that exact readiness blocker; do not widen limits silently.
No human study, accepted-outcome denominator or new feedback subsystem.

PC-003 resolution: separately authorized operator owns proposed terminal
closeout within the two-hour window: no further AI attempts/jobs; restore only
separately approved temporary config to the approved baseline; disposition
only the owned result object subject to approved retention; preserve SQL
histories, identities and retained estate. Record terminal timestamp/status,
retained object/version/soft-delete liabilities and their priced lifetime.
Unknown cleanup cost or absent operator blocks activation. Six-hour margin
is not extra execution time; no deletion or mutation is authorized here.

Targets: addendum, existing KB index row, log EOF. Validation: no historical log
rewrite, links resolve, no internal tracking links in canonical docs.
Completion: bounded proposal and exact owner export blocker with no activation.

<!-- rpi:phase id=P02 -->
## P02: Validate and hand off exact candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Documentation validation and original Review

Dependencies: P01. Run git diff --check; review changed Markdown structure,
relative paths/anchors, arithmetic, scope/privacy and historical preservation.
No repo-wide doc linter exists per guidance; do not invent a passed command.
Activate rpi-review once after implementation. Route findings to later
coordinator work; do not repeat Review or treat unknowns as compliant.
PC-001 resolution: explicitly disposition every Review finding before
publication. Out-of-scope activation/issue-acceptance blockers may stay disclosed.
An unresolved material defect in this candidate's accuracy, privacy or authority
boundary stops publication and routes to later coordinator correction, without
returning to Implement or repeating Review in this task. Preserve original
Review; any later corrected commit needs its own full exact-head gate.
Completion: changes record and one original dated Review artifact.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Exact candidate gate and conditional publication

Dependencies: P02-T01. Resolve gh api user, configure only privacy-safe local
author/committer email, Conventional Commit with required Copilot trailer.
Keep tracking paths out of subject/body. Fetch main and report exact base;
no rebase/force-push. Inspect shared lock/processes without disturbing an active
gate; do not duplicate. Use one unique external output directory and preserve
all receipt/environment files. Run python3 tools/rpi-checks.py --all --base
CURRENT --out UNIQUE; official --verify-receipt against freshly fetched base
immediately before any push. Any failure stops publication; do not install or
repair shared tooling speculatively or use a cloud fallback. Report retained
receipt/hash if present. Do not claim a receipt if preflight produced none.

If passing, push normally and open DRAFT to main with Refs #126, explicit unmet
criteria and evidence/validation. Independent coordinator assessment and hosted
approval remain outstanding. This is a publication task, not issue acceptance.
Gate success is necessary, not sufficient: the P02-T01 Review disposition
prerequisite also governs publication.
Post-commit run results stay external to avoid receipt self-invalidation; final
response carries their exact paths and outcome.
