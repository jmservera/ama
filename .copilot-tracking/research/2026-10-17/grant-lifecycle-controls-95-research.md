<!-- markdownlint-disable-file -->
# Task Research: grant-lifecycle-controls-95

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher | RPI parent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md |

## Research Brief

Audit issue #95 existing delivery before changing working features. This audit
prepares planning for the exact criteria: no dashboard misrepresents opportunity
as award/cash; only designated human financial authority submits, certifies or
records receipt. Keep opportunity, application, award, claimable, claim submission
and cash evidence distinct. GBP 40 million is unverified case opportunity.
Audience: issue coordinator and independent reviewer. Output mode: audit.

## Research Parameters

Focused posture selected from the bounded caller scope. Internal candidates:
finance ledger, registered actors, API write authorization, dashboard projections,
financial requirements, finance journey synthesis and component guides.
External scope: fresh issue #95 and prerequisite PR #383 via gh, no legal research.
Evidence root: .copilot-tracking/. No source edits during Research.
No private datasets/rosters, Azure writes, paid inference, banking/payment
execution, real commitments or inferred real human delegation. Preserve #94.

## Extension Registry and Provenance

| Kind | Candidate | Disposition and authority |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Selected repository conventions; explicit caller branch/base preserved |
| Skill | rpi-research | Selected evidence and three-wave protocol |
| Specialist | Housing Finance and Grants Lead | Skipped: cannot establish actual authority and continuous trace fits parent |
| Web skills | Web/design/accessibility | Deferred unless web edits become necessary |

## User Participation and Research Decisions

Explicit automatic instruction supplies scope, sequencing and stop condition;
no routine confirmation needed. Fresh gh confirms #383 merged and current clean
topic starts at that exact merge. #93 is hierarchy, not a dependency.

## Direction Controls

Audit first; minimal evidenced corrections only. Source in src, never mvp.
Preserve original case, finance dual-control/record-only guards and append-only log.
Use tiny fictional fixtures. Local SQL required only for changed persistence behavior.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Do records/projections preserve source, currency and six lifecycle states? | depth | Answered, currency gap |
| Q2 | Do writes revalidate current registered designated human identity? | depth | Answered, concrete gap |
| Q3 | Are documentation claims supported by meaningful negative probes? | straightforward | Answered, claims only partly supported |

## Prior Knowledge Gate

Read original case, addendum baseline and KB index/memory. Existing #94 delivery
is a starting claim, not assumed acceptance. Issue requirement numbering will be
checked against linked text. Owner memory is context, not evidence.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspect current guides, requirements, financial synthesis and execution surfaces.
Existing grant state machine, source/second approver history and independent
funding/application object exist. No grant monetary dashboard aggregate or
hard-coded GBP 40 million was found in the current dashboard surfaces.
Reflection: do not replace these working features. Trace grant authorization,
legacy funding writes and transaction-time validation next.

#### Wave 2: Deeper

Grant writes use supplied role before locking; no registered identity lookup.
Approval compares email only, unlike #94 email/code/OID independence. Legacy
application funding_step also trusts supplied role and records submission and
confirmation without designation. Grant amount is nominal pounds but a supplied
USD currency is silently ignored. History lacks explicit email/identity and
currency. #94 supplies a reusable complete write/rollback boundary and SQL
validation hook. Reflection: exact authority criterion is not met by role labels.

#### Wave 3: Contrarian

Executed temporary JSON and SQLite probes with installed src distributions.
Both stores accepted an entirely unregistered supplied Programme Manager
opening a grant, role-only approval, and an approver alias sharing the
preparer's staff code. Both accepted currency USD while storing an unqualified
amount. Actual output captured in the session command on 2026-10-17 at 18:27Z.
Contrarian result disproves "existing second approver implies designated human
authority." No private data or network financial action occurred.

#### Parent Synthesis and Disposition

Accept existing ordered state history and separate application/funding object;
reject rewriting the ledger or implementing full PRD pack workflows. Accept
current identity, explicit designation and currency/refusal gaps for a minimal
fix, including the existing application write path. Retain current finance
guards and reuse its operation/independence/SQL machinery.

#### Cycle Re-entry Evaluation

No further complete research cycle needed: all exact criteria have traced
sources and concrete probes; broader live grants/forms/payment work is excluded.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| W1 | Fresh issue text reports delivered with source and second approver; exact two criteria remain unchecked | https://github.com/jmservera/ama/issues/95 retrieved 2026-10-17 | High |
| W2 | #383 merged at 18:24:53Z, merge d400eb8d1d0d6567445b0fc11803260eab897a65; current topic HEAD matches | https://github.com/jmservera/ama/pull/383 retrieved 2026-10-17; git log | High |
| C1 | Original case says finance submits, agent drafts; GBP 40 million is business-case opportunity not receipt evidence | docs/case_study_48_original.md:28; docs/case_study_48_original.md:48 | High |
| C2 | Exercise baseline explicitly separates fictional grant states, no live submission/payment and human signatures | docs/case_study_48_addendum.md:127 | High |
| C3 | Linked BRD FR-019 is now capacity; grant rules are FR-023/024 and RULE-009/010, BG-007 | docs/brds/agentic-retrofit-programme-brd.md:1448-1451; docs/prds/zava-forward-retrofit-programme-demonstrator.md (FR-019, AC-022/050) | High |
| C4 | Existing grant flow/history is real, but role and email-only checks trust input | src/core/src/zava_forward/core/grants.py:23-65 | High, fail-before JSON and SQLite |
| C5 | Application records are already separate; submission/confirmation trust supplied Finance role | src/core/src/zava_forward/core/store.py:891-921 | High |
| C6 | #94 captures registered identities, repeats validation under SQL writer lock and recovers case/audit | src/core/src/zava_forward/core/finance.py:31-173; src/core/src/zava_forward/core/sqlstore.py:539-651 | High |
| C7 | Dashboard stats show case/funding counts, not awarded/cash totals; grant panel renders each history state independently | src/core/src/zava_forward/core/insights.py; src/api/src/zava_forward/api/web/panels.js (grantPanel); src/api/src/zava_forward/api/web/app.js (overviewView/fundingView) | High, static trace; browser not run |
| C8 | Current actor helper checks persisted SQL staff, email/code/name/role/OID rather than role alone | src/core/src/zava_forward/core/change_provenance.py:15-35 | High |

## Findings, Alternatives and Decisions

Audit-only is insufficient (C4/C5). The planning scope is the root authority fix,
strict GBP handling and retained identity/evidence on grant events. Existing
funding/application records stay separate; full pack/version/export work in
PRD FR-019/042 remains beyond these two issue criteria. No new dashboard or web
assets are needed. No automatic real delegation or designation backfill.

## Open Questions and Risks

Actual real-world delegation and human acceptance remain unverified; synthetic
engineering tests cannot establish either. No new regulatory currentness claim.

## Planning Readiness

Ready. Research disposition: executed. C3-C8 and the fail-before probes establish
bounded implementation inputs. Plan must critique the shared finance refactor,
transaction-time designation revocation, safe rollback and compatibility.
Self-check: questions answered, all three waves executed in order, alternatives
and exclusions explicit, synthetic evidence distinguished from live authority.
