<!-- markdownlint-disable-file -->

# Task Research: assessment-reconciliation-controls-84

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md |

## Research Brief

* Target: exact open issue #84, stock reconciliation, separate versioned technical sign-offs, affected-only reapproval and non-vulnerability-only prioritisation with unknown flags.
* Purpose and audience: establish delivered behavior and genuine root gaps before a scoped implementation for repository reviewers.
* Scope: existing core reconciliation, assessment, sign-offs, ranking, Store and surgical API integration; constructed tiny cases only.
* Non-goals: architecture replacement, procurement/capacity #90, infrastructure/package #381, private datasets, map dataset, cohort, paid inference, cloud changes, operational safety/rank-policy/legal approval.
* Criteria: prove all four exact issue checkboxes independently; fail-before focused regressions for missing behavior; preserve independently approved sign-off authority and existing deterministic policy.
* Output mode: convergence, preparing the requested ordered Plan/Implement/Review.

## Research Parameters

| Field | Value |
| --- | --- |
| Questions | What is already delivered? Which exact criterion gaps remain? Which existing seams safely cover them? |
| Codebase scope | src/core, src/api and named requirements |
| External scope | Exact GitHub issue, parent hierarchy and adjacent backlog only |
| Initial internal candidate areas | signoffs.py, ranking.py, reconciliation tests, current Store/API and previous #84 artifacts |
| Initial external candidate areas | jmservera/ama #84, #81, #90, #381 |
| Research posture | focused |
| Posture provenance | Explicit bounded caller scope |
| Explicit limits | No private inputs, operational authority inference, broad UI or unrelated work |
| Completion basis | Four-criterion evidence coverage and contrarian boundary checks |
| Edits allowed during research | Research and workflow tracking only |
| Resolved evidence root | .copilot-tracking/ |

## Extension Registry and Provenance

| Kind | Candidate | Provenance | Authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | Repository guidance | supplied applyTo ** | Requirement reads, topic branch, privacy-safe commits and PR | selected |
| Skill | rpi-research | activated at intake | Three-wave evidence and readiness | selected |
| Specialist | RPI Researcher | registered | Independent research lanes | skipped; one tightly coupled trace is better handled inline |
| Skill | Web design/review | available | Required only if web edits become necessary | deferred; no UI assumption |

## User Participation and Research Decisions

Caller explicitly requested the entire ordered lifecycle and delivery without routine questions. Branch is the requested clean isolated topic; no existing PR. No additional intake clarification is needed.

## Direction Controls

* Exact issue first, no explicit dependencies; #81 is hierarchy only.
* Verify prior artifacts against actual current behavior, never treat historic claims as fresh evidence.
* Preserve deterministic ranking policy and separate human competence/sign-off authority.
* Avoid shared source except surgical Store/API integration; flag overlaps with #90/#381.

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | Both compared stock values and query owner visible? | depth | high | open |
| Q2 | Four separate versioned sign-offs and affected-only staleness? | depth | high | open |
| Q3 | Ranking independent of vulnerability alone, missing flags unknown? | depth | high | open |
| Q4 | Scoped integration, persistence and validation boundaries? | depth | high | open |

## Prior Knowledge Gate

Initial mandatory original, addendum, reference index and memory read. Existing dated #84 artifacts and tests discovered; claims remain unverified pending current source and execution.
Baseline source citations below refer to inspected main-derived commit adedf1f;
subsequent implementation can shift current line positions without changing
that recorded research provenance.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Exact #84 retrieved first: four checkboxes and explicit no dependencies. Parent #81 inspected as hierarchy; adjacent backlog checked. Current branch clean and correct; no existing topic PR. Existing reconciliation tests and earlier #84 artifacts warrant verification before assuming missing implementation.

Reflection: focus on actual source/test gaps, not repeating historic delivery.

#### Wave 2: Deeper

PRD FR-012/013 and BRD FR-037/AC-065/RULE-017 inspected alongside current modules.
Existing comparisons retain both values/metadata/query owner and separate terminal
events; four independent sign-offs and affected-only reassessment already exist.
Core baseline: 47 tests (stock reconciliation plus finance/sign-offs) pass.
API/ranking baseline: 18 tests pass, one opt-in browser skip. Correct component
test paths are required; initial missing-package failure was repaired with
task-owned .venv and declared editable packages only.

Reflection: do not recreate delivered controls. Verify SQL authority and rollback
under adverse conditions before planning a narrow continuation.

#### Wave 3: Contrarian

Constructed five-case fixture probe changed the SQL inspector's registered role
to Contractor without changing the case sequence. The old cached actor still
signed an assessment. A second probe injected OSError at save during a design
change: durable version stayed 1, but a success-shaped technical_design_change
audit was independently committed by outer lock cleanup.

Reflection: current happy-path coverage does not prove current sign-off authority
or failed-write integrity. Both are directly coupled to reliable versioned
sign-off/reconciliation decisions; preserve the existing policy and fix these
bounded SQL gaps, not a new stock authority or competence model.

#### Parent Synthesis and Disposition

| Claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Reimplement comparison/sign-off/ranking mechanisms | C1-C4 | rejected | Already delivered and passing focused tests |
| Fresh registered authority and atomic failed decision audit needed | C5-C7 | accepted | Actual revoked actor and failed-save probes expose genuine gaps |
| Nomination/self-referral included here | W3 | rejected | Owner explicitly assigned those routes to #130 |
| Source selection or competence approval can be inferred | C1-C4 | rejected | Synthetic mechanics do not establish these authorities |

#### Cycle Re-entry Evaluation

No further cycle needed: four criteria and tightly coupled failure paths have
current evidence. Existing fresh-actor and SQL validation/rollback patterns
provide a bounded implementation seam. No external law/model research needed.

## Evidence Log

| ID | Claim | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Exact four criteria; no dependencies; parent #81 | https://github.com/jmservera/ama/issues/84 retrieved 2026-10-17 | gh issue view | high |
| W2 | Parent safety epic, not child dependency | https://github.com/jmservera/ama/issues/81 retrieved 2026-10-17 | gh issue view | high |
| W3 | Owner routes staffed nomination/self-referral/challenge to #130 | https://github.com/jmservera/ama/issues/84#issuecomment-6180413384 retrieved via gh 2026-10-17 (comment by jmservera) | gh issue view --json comments | high |
| C1 | Both compared values/metadata, query owner and unknown authority retained | src/core/src/zava_forward/core/stock.py:75; src/core/src/zava_forward/core/store.py:421 | read and passing baseline | high |
| C2 | Four independent versioned sign-offs; selected downstream staleness | src/core/src/zava_forward/core/signoffs.py:11; src/core/tests/test_stock_reconciliation.py:173 | read and passing baseline | high |
| C3 | Missing support distinct from explicit negative; safety/wait/stage also rank | src/core/src/zava_forward/core/stock.py:13; src/core/src/zava_forward/core/ranking.py:70; src/core/tests/test_stock_reconciliation.py:497 | read and passing baseline | high |
| C4 | API exposes comparisons and contractor projection denies them | src/api/tests/test_stock_reconciliation_api.py:109 | 18-test HTTP/ranking baseline, one browser skip | high |
| C5 | Technical actor checks use cached staff; cache only initially loads | src/core/src/zava_forward/core/signoffs.py:48; src/core/src/zava_forward/core/sqlstore.py:437 | read and revoked-role probe | high |
| C6 | Generic failed save leaves pending success audit for _finish | src/core/src/zava_forward/core/sqlstore.py:499; src/core/src/zava_forward/core/sqlstore.py:579 | read and injected-OSError probe | high |
| C7 | Existing fresh actor, writer-lock revalidation and explicit discard patterns | src/core/src/zava_forward/core/change_provenance.py:15; src/core/src/zava_forward/core/change_provenance.py:39; src/core/src/zava_forward/core/forms.py:218 | read | high |

## Findings, Alternatives and Decision State

Keep all delivered criteria and deterministic policy unchanged. Use a bounded
stock/technical decision scope, reuse the existing registered-actor helper and
SQL discard mechanism, recheck under the existing writer transaction. Do not
change unrelated SQL exception/lock behavior or other domains. Surgical Store
integration overlaps the file used by #90; no procurement code changes.
#381 infrastructure/package files remain untouched.

## Open Questions, Risks and Residual Uncertainty

Sign-off authority and actual stock-source authority must not be inferred from synthetic fixtures. Local SQL parity availability is not cloud acceptance.

## Planning Readiness

Ready. Research disposition: executed. Mandatory Wider -> Deeper -> Contrarian
cycle complete inline; no workers were needed. Self-check: all questions answered
for planning, exact criteria separated from broader BRD/human acceptance, real
source/test evidence and remaining platform/authority limits retained.
