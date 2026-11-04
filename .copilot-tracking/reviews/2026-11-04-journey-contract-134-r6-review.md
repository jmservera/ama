# RPI #134 slice 2 (R6): AC-034 to AC-043 acceptance register

Date: 2026-11-04. Branch feat/issue-134-r6 (requested name feat/agent-chat-skills-530 not present in this worktree). Tier: focused (no security, infrastructure, SQL or deployment change; gate not run).

## Research

* Merged PRs for #134: #872 only (slice 1, same-home journey trace). #103 manifest and #76 queues are delivered separately.
* Prior review routed RV-001 (store journey test), RV-002 (AC-034..043 register), RV-003 (screens and accessibility).
* PRD acceptance table lists AC-034..043 all `Not run`. Manifest 0.2.1 lists 11 profiles and 9 workflows, all `unavailable`.
* Existing evidence by module: resident_decisions (AC-037), procurement (AC-039/042), quality (AC-042), exception_queue (AC-040), workbench browser check (AC-034).
* Contradiction flagged: module headers cite AC numbers (quality AC-039, procurement AC-042) that differ from the PRD criterion text; the register follows the PRD wording.
* Planning readiness: Ready. Smallest coherent slice that is locally testable: RV-002 register. Needs live browser/owner: perspective screens, announcements (not implementable here).

## Plan (slice 2 of 4)

* [x] Add `journey_acceptance.py`: pure register plus `check(root)`.
* [x] Tests: full coverage, no pass claim, reason and evidence required, broken evidence.
* [x] README section; log entry.
* [x] Focused validation.

Critique (single pass, author): never record `pass` without executed evidence (applied: status limited to partial or deferred); verify evidence paths exist (applied); no approval or user-validation claim (applied: notice). No AI feature, no screen, no consent or approval action.

## Details

Files: src/core/src/zava_forward/core/journey_acceptance.py, src/core/tests/test_journey_acceptance.py, src/core/README.md, docs/reference/log.md.

## Changes and validation

* Added the two source files; README section; log entry.
* Run (PYTHONDONTWRITEBYTECODE=1, package from a temporary target dir): `tests.test_journey_acceptance` and `tests.test_journey_trace` 14 pass; ruff check and format pass; mypy --cache-dir=/tmp/mypy-530 pass on the new files.
* Not run: gate, benchmarks, full suites, SQL Server, browser, assistive technology.

## Review (single pass, author; independent exact-head review still required)

Outcome: residual work, no defect found.

* Eleven perspective walkthroughs: UNMET.
* AC-034..043 pass or deferred with reason: PARTIAL (6 partial, 4 deferred with reasons; none passes).
* Same-home journey: PARTIAL (unchanged; store journey test still open, RV-001).
* Sibling and building negative controls: PARTIAL (unchanged).
* Text state, keyboard and announcements: UNMET.
* Constructed-fixture labelling: MET for register notice.

Follow-ups: RV-001 store journey test (slice 3), RV-003 perspective screens and accessibility evidence (slice 4). Use Refs #134.
