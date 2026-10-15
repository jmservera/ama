---
title: Building shared systems review for issue 75
ms.date: 2026-10-15
---

## Scope and Evidence

* Task: 75 / shared-systems-75.
* Review date: 2026-10-15.
* Scope: complete P01/P02 local synthetic model/view slice, not platform release.
* Assessed boundary: issue acceptance criteria, PRD FR-002 and separation
  intent of AC-001/002/003; accepted ADR 0006 and parity-matrix placement.
* Research: .copilot-tracking/research/2026-10-15/shared-systems-75-research.md.
* Plan: .copilot-tracking/plans/2026-10-15/shared-systems-75-plan.md.
* Details: .copilot-tracking/details/2026-10-15/shared-systems-75-phase-details.md.
* Critique: .copilot-tracking/plans/2026-10-15/shared-systems-75-critique.md.
* Changes: .copilot-tracking/changes/2026-10-15/shared-systems-75-changes.md.
* Code evidence: final core buildings module, Store/SqlStore/procurement/
  projection changes, API route and DOM rendering; core/API regressions and
  component READMEs, knowledge index/log, actual loopback browser assertions.

## Opening Review State

Implementation is reconciled and source edits finished. Assess once against
the complete supplied local boundary. Review writes only this record.
Administrative commit/push/PR follows outside source implementation. No
independent review subagent is claimed; this is the RPI parent's one Review.
One independent planning critique was already executed and dispositioned.

## Execution Status

Execution: Complete. Compared final source diff and typed new model with
requirements, all current plan markers, details, critique corrections, changes
evidence and remaining-work claims. No second Review or correction loop.

## Plan-to-Change Reconciliation

| Scope | Evidence | Reconciliation |
| --- | --- | --- |
| P01-T01 | core buildings validation, Store gates, SqlStore.DOCS, procurement issue/reissue/correction | Complete for imported read-only records; no new SQL or workload import |
| P01-T02 | Staff-only API, Finance projection, home/building/sibling DOM navigation | Complete for engineering slice; resident evidence and allocation not merged |
| P02-T01 | Core 270, api 462 (92 skipped), agents 70, orchestrator 17, importer 39; all project lint/format/mypy | Complete locally; skipped external SQL tests not counted as executed |
| P02-T02 | Component guides, index and append-only log, full command/correction record | Complete; publication is subsequent administrative delivery |
| Follow-Up Items | Live platform, governed register/owners, human acceptance | Preserved outside current local acceptance; routed below |

## Completed Work Assessment

The building record provides all five required categories. Strict allowed
fields exclude home approval/evidence payloads. Case and package IDs are
validated explicitly; unknown versus explicitly empty applicability is retained.
Home allocation is neither copied nor summed into shared costs. API
authorization rejects contractors/unknown roles before disclosure; Finance
amounts are omitted from other staff responses, not merely hidden in the UI.

Home consent/funding/technical checks continue to block independently of clear
building context and approved sibling state. Quality, closure and evidence
remain distinct. Additional shared checks block matching home advancement and
package instructions, including reissue/correction, without altering consent
or stopping hazard intake/referral. Changing free-text scope cannot alter the
exact package relationship. Unknown explicit links fail closed; absent legacy
links retain existing behavior, not evidence of building readiness.

Both local backends preserve building data on reopen. SQL checked-document
synchronization/conflict testing confirms retained provenance and no lost
update. MSSQL shares the document hooks; no added dialect-specific SQL, driver,
blob dependency or infrastructure change. This is a portability design and
local evidence, not proof of this feature against a real SQL Server.

## Implementation-Time Update and Critique Assessment

PC-001 exact case/package matching is implemented and tested across different
packages on the same home, siblings and reissue. PC-002 shared costs are
Finance-visible while allocations remain home-only, confirmed in API and DOM.
PC-003 JSON/SQLite reopen and legacy no-reseed tests are mandatory and present.
PC-004 separate resident/funding/technical negative assertions, independent
quality/closure/evidence and hazard referral are present.

Formatting/import/type-check adjustments and completed synthetic metadata are
ordinary evidence-led corrections, not a new product decision. The narrow
API shared-fixture import setting does not exempt production or new test
errors; the fixture is strictly checked in core. Plain-language UI copy
preserves the content standard; its allow-list addition covers a code key only.
Documentation/review handoff was separated from later administrative
publication in both plan and details. No new critique was needed or run.

## Findings and Routing

### RV-001 [Medium]: Actual-platform evidence is unavailable for this revision

Evidence: changes commands show local JSON/SQLite/browser checks; Docker socket
permission denied. Real SQL Server tests are among the existing API skips.
No actual model call or Azure deployment was performed, and existing AI release
controls were not bypassed.

Impact: cannot claim full exercise/platform acceptance from synthetic local
tests. Existing AI proposal paths are retained, not newly approved for live use.

Destination: distinct evidence-verification follow-up (`rpi-research` for
access/authority readiness, then authorized validation). First consume PR CI
image and disposable SQL results; retain remaining actual Azure/model checks
unticked until attributable evidence is available.

### RV-002 [Low]: Real register and governed update authority are not supplied

Evidence: source-backed building records are read-only seeded inputs; legacy
live files/databases are deliberately not overwritten by changed seed files.
Fixture identities, costs, scopes and reviewers are explicitly fictional.

Impact: this is not an operational building register or a release workflow.
No invented safety owner or allocation formula can substitute for real evidence.

Destination: distinct owner-led register/update-governance follow-up, beginning
with `rpi-plan` only after the owner supplies authoritative sources and rights.

### RV-003 [Low]: Browser engineering checks are not direct human acceptance

Evidence: actual DOM navigation, focus, categories, amounts and server projection
were checked, but no resident/staff task study, assistive-technology exercise
or full WCAG evaluation was performed.

Impact: do not tick wider PRD AC-043 or accessibility/user acceptance.

Destination: distinct human acceptance/accessibility evidence follow-up.

## Defects

No known implementation defect established within the assessed local boundary.
The residual findings above remain open; they are not silently treated as
passed criteria or remediated by another Review in this task.

## Validation Evidence

| Check | Status | Evidence |
| --- | --- | --- |
| Core full suite | Passed | 270 tests; pre-existing sensor file ResourceWarnings only |
| API full suite | Passed with explicit skips | 462 tests, 92 skipped; final changed fixture additionally passed focused 3-test HTTP suite |
| Agents/orchestrator/importer | Passed | 70 / 17 / 39 tests |
| Ruff, format, mypy | Passed | All five projects; new core module and tests strictly checked |
| JavaScript syntax | Passed | node --check src/zava_forward/api/web/app.js |
| Rename regressions | Passed | 25 tests after pip restoration of existing tool requirements |
| Local app/browser | Passed | Final two-home SQLite navigation, six headings, focus and Finance/non-Finance isolation; zero final console errors |
| Docker | Unavailable | Socket permission denied, no local image evidence |
| Final source diff / forbidden paths | Passed | git diff --check; no changed mvp, .env, .vscode or github-issues paths |
| Actual model / Azure / SQL Server | Not run for this revision | Must not infer completion from mocks, SQLite or historical deployment |

## Outcome

Outcome: Residual work. The three issue model criteria have local synthetic
implementation evidence; release/human/platform acceptance remains unaccepted
where evidence is absent. No material user decision was guessed. PR must use
Refs #75 and list the unticked evidence, not automatically close the issue.

## Closeout Routing Record

Execution Complete; outcome Residual work. P01/P02 complete. No source
implementation is resumed after Review. Parent may perform authorized topic
publication, then report CI status and the three distinct follow-ups above.
