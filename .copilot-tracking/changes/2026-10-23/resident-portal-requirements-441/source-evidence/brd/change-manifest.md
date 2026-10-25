---
title: Resident portal amendment integration manifest
date: 2026-10-23
status: draft
---

## Integration boundary

The only repository-targeted file in `amendment.patch` is
`docs/brds/agentic-retrofit-programme-brd.md`. This package has changed no
repository file, branch, index, issue, delivery worktree or live system.
The remaining rows are integration instructions for the parent's isolated
native RPI topic/PR, not claims that those documents were already updated.
Do BRD, then PRD, then ADR in sequence; do not treat this as approval to implement.

Base: `140d8f494482c78e84d15f3d46b9223d3c487af0` (`origin/main` when read).
Re-read current main at integration. If changed, inspect the full identifier
registries again, resolve collisions without renumbering historical IDs, and
regenerate hashes, traceability and review evidence. No remote freshness beyond
the locally available `origin/main` ref is asserted.

## Files and required reconciliation

| File / exact source anchor at base | Required change | Treatment |
| --- | --- | --- |
| `docs/brds/agentic-retrofit-programme-brd.md:1-49,599-656,720-765,1215-1223,1339-1395,1495,1512,1538,1557,1906-1910,2046-2164,2328` | Apply surgical draft v0.20.0 patch: optional scope, contact/WIP rationale, quantified scenarios, ten FRs, two NFRs, two rules, four decisions, explicit human-approval policy proposal, updated registry/matrices/history. | Included in patch; status remains draft, existing lineage/IDs preserved. |
| `docs/case_study_48_addendum.md:61-93,118,1091` | Append dated 2026-10-23 owner direction and *proposed* scope/policy amendment. Cross-link BRD/PRD/ADR candidate chain; explain that EXA-004's no-required-portal protection survives while deferral rationale is replaced prospectively. Record scenario inputs as author judgement authorized for planning. | Do not alter historical EXA register, 2026-10-10 approval or old all-message-review finding. No fabricated new exercise acceptance. |
| `docs/prds/zava-forward-retrofit-programme-demonstrator.md:216-246,308-332,482-502,709-815,831-926,1474-1558,1604-1731,1786-1918,1946-1967,1997-2141` | Parent's PRD specialist adds resident user/representative journeys, entitlements, safe documents, scheduling requests, optional channels, case-event/queue contracts, agent grounding and gated dispatch. Reconcile staff identity and staff-only chat boundaries; declare resident memory excluded. Add exact upstream draft IDs, guardrail tests, scenario hypotheses and capacity sizing questions. | Do not silently replace existing PRD FR-061 (Tokenomics) with BRD FR-061 (bounded dispatch). Separate document namespaces and inspect entire PRD registry before allocating. No PRD/ADR written by this task. |
| `docs/reference/research/ux/customer-journeys/residents.md:23,37-95` | Retain historical EXA-004 provenance at line 23. Replace line 95's current/future interpretation with optional portal and grounded resident agent candidate, per-message review default plus proposed OD-53 exception. Add login/recovery/own-case/doc/upload/scheduling/help, shared-device, multi-occupant, representative revocation and non-digital equivalent task journeys. | Preserve research dates and hypotheses; do not relabel desk research as real resident validation. Keep unrelated delivery-engineering notes/history intact. |
| `docs/reference/research/ux/customer-journeys/frontline.md:51-63,78-103` | Add shared omnichannel event/exception workflow, assisted-capture fallback and workload accounting; retain phone/letter/visit accessibility and named human ownership. | Current channels/connectors remain unverified; do not claim existing email/telephony automation. |
| `docs/reference/research/ux/customer-journeys/customer-journey-atlas.md:46-51,169-190,207-224` | Add resident portal candidate and source-to-staff handoff map, without turning “no shared portal assumed” into a ban or erasing current research status. Update candidate counts only if actual additions change them. | Existing opportunities' human decisions remain; do not expand all autonomous-agent scope. |
| `docs/reference/research/ux/zava-forward-prototype-profile-review.md:304` and `docs/reference/research/ux/content-standard.md` | Add resident persona/task and plain-language/help/status/error/AI-label checks when PRD exists; distinguish proposal, recorded fact, offered slot, resident response and confirmed appointment. | Current staff screens, issue evidence and incomplete findings are not evidence of a resident portal. |
| `docs/reference/research/ux/wcag-conformance-baseline.md` and `docs/reference/research/ux/design-system.md` | PRD/UX specialist defines core resident task checks, recovery and assisted equivalents under EXA-011's engineering target, including mobile upload and shared-device safe contact. | No conformance assertion from this draft; baseline checks are not permission to omit basic accessible tasks from the demo. |
| `docs/adrs/0004-per-user-agent-chat-and-memory.md:9-16,75-123,175-184` | ADR specialist explicitly preserves accepted staff-only memory/chat decision; new resident service is separate scoped capability, not a silent expansion of that acceptance. Cross-reference any new ADR's exact changed boundary. | Keep historical owner acceptance and staff privacy restrictions intact. |
| `docs/adrs/0001-azure-architecture.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, `docs/adrs/0005-regulatory-compliance-assistant.md` | ADR specialist assesses resident identity/trust boundary, case authorization, files, event reconciliation, agent grounding/evaluation/dispatch, costs and observability after PRD. Reference current staff and workload identities, without assuming residents have staff Entra membership. Keep regulatory assistant no-send authority. | Evaluate managed identity choices and simple username/password UX; no identity product, topology, paid operation or implementation selected by BRD. |
| `docs/architecture/zava-forward-executive-architecture.excalidraw:623-624` and companion `.svg:4,17` | Visuals include “No resident portal needed.” Preserve as dated observed staff baseline, but add proposed resident channel/trust boundary in future-state assets after ADR. Update source and generated export together, with text alternative. | Do not relabel proposed features as observed. No `.md` companion exists at this base. |
| `docs/capstone/README.md`, process diagram/text equivalent and pitch assets | Add separate optional resident-service proposal and defensible scenario pitch; do not claim five current assistants already deliver it. Distinguish real AI exercise gate from portal implementation status. | Generated presentation assets should follow integrated PRD/ADR, not this standalone authoring task. |
| `docs/reference/README.md:310-319,341,371-377,404` | Add resident-service routing and update integrated document versions/counts/status links; point to proposed policy, quantitative assumptions and unresolved decisions. | BRD candidate totals: 62 FR, 126 AC, 14 NFR, 7 CON, 28 RULE, 13 BG, 55 OD. Update PRD totals only after its specialist finishes. |
| `docs/reference/log.md:489` and newest-entry section | Append one dated change record with owner request/follow-up, exercise-only assumptions, IDs, source SHA and artifact chain; leave old universal-human-review history unchanged. | Append-only log. Do not retroactively rewrite historical decisions or test evidence. |
| `docs/reference/research/company/agent-what-if-study.md:955,1347` and `agent-request-challenge.md` | Add dated cross-reference if these are presented as current universal authority; retain original findings and no-portal-writes-on-officer-authority restriction. State narrow resident-channel exception is only proposed/gated. | Historical desk studies are not new company approval or a mandate to re-run broad research. |
| `docs/reference/research/retrofit-synthetic-data/README.md`, `data-dictionary.md`, `needs-inventory.json`, `scenario-manifest.json`, `provenance-register.json` | Later PRD/design work inventories missing fictional identity/household/representative/channel-event/upload fixtures and provenance, preserving existing stock/programme lineage. | Do not generate private residents, overwrite fixtures, assert existing coverage or equate 60,000 homes with accounts. Changes require separately scoped delivery. |
| `docs/case_study_48_original.md`, `docs/reference/memory.md`, `docs/prds/proper-warm-retrofit-programme-demonstrator.md`, older renamed UX notes | No content rewrite. Original is immutable; memory needs separate owner request; Proper Warm PRD is a historical-name snapshot with same logical ID, not the current drafting target. Use a dated cross-link only if integration needs reader routing. | Preserve history and approvals. |

## Acceptance and sequencing checklist for parent

1. Verify base, full ID registries, exact patch and candidate hashes before integration.
2. The patch also repairs inherited FR-033 “All goals” matrix enumeration to
   include existing BG-013 and its reciprocal goal-alignment link; no requirement
   behavior or ID changes. It also escapes the literal line-initial `#58`
   reference to resolve inherited MD018 without changing its meaning.
   Reconcile BRD draft plus addendum, journey, index and append-only log statements
   in the same document chain; do not leave “later exploration only” as current scope.
3. Give the PRD specialist `draft-prd-handoff.json` with source/rationale and
   reviewer limitations, not a success-shaped signed handoff. Let it inspect its
   own registry and produce a proposed acceptance contract.
4. Give the resulting PRD to the ADR specialist. Require explicit policy delta,
   options for resident identity and document trust boundary, and reversible
   staged scope. Staff landing/auth delivery proceeds independently unless a
   proven dependency is recorded.
5. Obtain independent document review and owner exercise acceptance without
   inventing real company/DPO/legal/safety signoff. All actual operational gates
   remain distinct. Reviewers' deferred feasibility/SMART findings remain open.
6. Only later implementation work may create backlog/tasks; this bounded task
   creates no repository issues, commits, pushes, application/heavy tests or paid resources.

## Package-only artifacts

`amendment.md`, `amendment.patch`, `draft-prd-handoff.json`, this manifest,
`quality-review.md`, `validation.json`, `state.json` and `render-amendment.py`
remain session working files. The renderer deterministically derives the patch
from authored blocks and exact source bytes; `verify` applies hunks in memory.
There is no copied full BRD, second case study or new repository tracking tree.

`.lint-tools/` and `.npm-cache/` contain validation-only tool dependencies/cache
inside the authorized output boundary; do not integrate them into the repository.
The Markdown profile preserves existing long-table/H2/`br` conventions. It is
explicitly not a claim that the unmodified default rule set passes. The exact
candidate and readable artifacts pass the recorded profile; the inherited bare
issue-reference warning on the base is retained in the check record.
