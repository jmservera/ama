# Issue 74 current-main acceptance audit: plan

Date: 2026-11-10. Research: [research](../research/2026-11-10-issue-74-main-acceptance-audit-research.md). Details: [details](../details/2026-11-10-issue-74-main-acceptance-audit-details.md).

## Objective

Produce a source-bound acceptance matrix, for current main `c66370042eb08f07839d054433f4483078703cf2`, of whether each field of the unmet #74 criterion is independently rendered and sourced for the existing staff roles, with no same-building evidence or approval transfer. Audit only; no source, test, fixture, criterion, issue, shared pack, push or PR change.

## Decisions carried from Root and research

* Constructed local fixture behaviour is reported separately from real customer, human, AT or live acceptance.
* A missing maintained assertion is reported as an exact gap, never repaired.
* Closure or tick is only suggested when the literal criterion and its dependency evidence hold; Root decides after independent review.

## Phases

* [x] Phase 1: pin and prepare. Re-confirm HEAD, tree, blobs and `origin/main`; create own venv with `/tmp/ama-74-venv-1110`, installing declared manifests (`src/core`, `src/agents`, `src/api[dev]`) only because `playwright` and the local distributions are absent; record the install and imports log.
* [x] Phase 2: core and API targeted checks. From `src/api`, run `python -m unittest` for `test_home_case_api` with `PYTHONPATH=../core/tests:../agents/tests`, and from `src/core` run `test_home_case`. Record command, exit, counts and skips; stop that check on failure and capture failure evidence.
* [x] Phase 3: browser check. Inspect runner cwd assumptions (done in research), then run `python -m checks.home_case_browser_check` from `src/api` under non-queued `flock -n /tmp/ama-rpi-heavy.lock`, with an owned short `ZF_BROWSER_SCRATCH` outside the checkout and no `ZF_DATA`. If the lock is busy or a profile or socket error occurs, record it as environment evidence and stop that check without weakening assertions. Axe only if the pinned file with the matching hash is already available in an owned location; otherwise record axe as skipped.
* [x] Phase 4: field and role matrix. For each criterion field (shared systems, dependencies, holds, works, costs; home evidence, decision, cost allocation, outcome) and each role (Retrofit Programme Manager, Resident Liaison Officer, Contractor, anonymous) classify as local-observed, implemented-unverified, blocked or unknown, with evidence pointer and exact remaining action. Combine run output with the pinned static source read only to explain how the field is sourced and rendered.
* [x] Phase 5: focused UI review. Load `web-design-guidelines`, fetch its current source, review only `homeCaseView` and the pinned screen component with `file:line` findings, preserving Fluent 2, local WCAG baseline, plain-language and ASCII precedence. No whole-site sweep; no automated result is claimed as conformance.
* [x] Phase 6: write the changes record and acceptance matrix, then the single review, then the Root handoff.

## Validation tier

Focused tier (non-gate, documentation-only candidate that touches no source, workflow, dependency manifest or image): planned local API, core and browser checks with raw evidence, diff review, and link review. No full local gate, no SQL, image, cloud, provider, model or real-account work. Independent exact-head review, hosted CI and human approvals remain required later and are not claimed.

## Constraints

* Own environment only; no shared installs, no full discovery, no new agents.
* No private or default dataset; the fixture is `home_case_data()` and the unit-test fixtures.
* Witness: strict state validation succeeds before each marker; prospective changes file exists before `implement-start`; the commit claim uses the literal 40 hex HEAD.

## Follow-ups

Carried from research.
