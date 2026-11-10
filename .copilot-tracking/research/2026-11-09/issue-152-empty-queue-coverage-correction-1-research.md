<!-- markdownlint-disable-file -->

# Task Research: issue-152-empty-queue-coverage-correction-1

| Field | Value |
|---|---|
| Date | 2026-11-09 (written from 04:52 UTC, prospectively, before any source edit) |
| Researcher / agent | RPI Agent via rpi-research (inline; no delegated lanes) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-09/issue-152-empty-queue-coverage-correction-1-research.md |
| Parent task | issue-152-empty-queue-coverage (original artifacts and original Residual work review are preserved unchanged) |

## Research Brief

* Topic: first correction of the partial C5 slice of #152 (`Refs #152`, not whole-issue delivery). An independent preliminary finding says `trustedCoverage` in `src/api/src/zava_forward/api/web/app.js` accepts a "declared-unrepresented" claim whose `fixture_version` and `source` are only non-empty strings, with no binding to an independent current fixture or provenance.
* Purpose: decide the narrowest change that restores the original fail-closed requirement: absent, stale, mismatched, unavailable or untrusted coverage metadata yields unknown.
* Scope: `app.js` empty-queue helpers, `src/api/tests/test_queue_empty_state.py`, the `src/api/README.md` empty-queue paragraph. Non-goals: a metadata producer, server schema, SQL, data, identity, permissions, deployment, AC-034/043 completion, supported devices, accessibility acceptance, real users, live deployment.
* Start: `c934312eed90487eda92d1e692c6e2b23a2f8f02` (tree `534f67ae1a9d4ab94d44c5ba0a0d9af3cad7821c`), base `b46a9ad9a9619db535368d1b2cbbddec8110e122`; target `main` unchanged.
* Tier: focused (client copy, unit test, documentation only).

## Research Parameters

| Field | Value |
|---|---|
| Research posture | focused (bounded internal defect, named source targets) |
| Posture provenance | caller brief "narrowly"; default for bounded internal task |
| Explicit limits | no heavy gates, Playwright, SQL, Docker; no push/PR; no private data |
| Output mode | convergence |
| Resolved evidence root | .copilot-tracking/ default |

## Extension Registry and Provenance

| Kind | Candidate | Provenance | Decision |
|---|---|---|---|
| Instruction | AMA repository instructions | applyTo `**` | selected (tier, evidence, web guidance) |
| Skill | rpi-research | caller-required phase | selected |
| Skill | web-design-guidelines | required before web edits and before review | deferred to Implement and Review |
| Specialist | RPI Researcher | no independent lane needed | skipped, inline fallback |

## Questions

* Q1: Is the finding real in current source?
* Q2: Is any independent authoritative current fixture/provenance available to bind to?
* Q3: What is the simplest safe change?
* Q4: What existing behaviour and documentation must be preserved or corrected?

## Wave 1 (Wider)

* C1 `src/api/src/zava_forward/api/web/app.js:464-473`: `trustedCoverage` compares `contract`, `as_of`, `policy_version`, `perspective` to page/session values and only tests `text(fixture_version)` and `text(source)`. These values arrive in the same `/api/me` payload as the declaration, so equality only shows internal consistency of one payload.
* C2 `src/api/src/zava_forward/api/web/app.js:474-486`: `queueEmptyExplanation` returns `declared-unrepresented` text quoting `fixture_version`, `source` and `as_of` as if verified.
* C3 `src/core/src/zava_forward/core/taskqueues.py:59-70` (`contract`): no `coverage` key; `src/api/src/zava_forward/api/server.py:557-560`: `/api/me` attaches `taskqueues.contract(ranking.CURRENT)` only. No producer exists, so the defect is latent, not an observed live misstatement.
* C4 `src/api/checks/workbench-manifest.json:2`: static test manifest `version` `152-ia-v1`. It is test evidence, not runtime provenance, and the brief forbids inferring authority from static test manifests, role, source text, timestamps or queue emptiness.
* C5 `src/api/tests/test_queue_empty_state.py:50-58,104-113,115-139`: tests treat `fixture_version: "152-ia-v1"` and `source: "dataset declaration"` as valid and assert the declared state; the stale-variant test omits a stale or unrelated `fixture_version`/`source` case.
* C6 `src/api/README.md:3869-3878`: documents the optional `work_queues.coverage` declaration and the declared-gap state as active client behaviour.

## Wave 2 (Deeper)

* Q1 answered: confirmed by reading C1/C2; a declaration with matching context, `fixture_version` `stale-or-unrelated-fixture` and `source` `unverified declaration` satisfies every check and yields the declared state. The implementation phase reproduces this in a regression that must fail before the change.
* Q2 answered: no independent authoritative source exists in the repository for the current runtime fixture or its provenance. Candidates rejected as authority: the manifest (C4, static test data), the declaration's own fields (self-asserted), `as_of` and policy (timestamps and versions, already bound but not about fixture provenance), role (C1), queue emptiness.
* Q3: without a trusted anchor, any client-side check of `fixture_version`/`source` is theatre: the client would compare a self-asserted value with another value from the same untrusted payload, or with an invented constant. Producing an anchor means a producer or schema, which is out of scope and a possible full-tier trigger.
* Q4: preserve no-match wording, unknown wording, populated-queue null, all-cases wording, and the wiring test of the list view. Correct README and test descriptions so they say the declared branch is not active.

## Wave 3 (Contrarian)

* Alternative A: bind `fixture_version` to the manifest or a client constant. Rejected: invents a trusted source and ties production code to a test manifest, which the brief forbids.
* Alternative B: keep the branch but label the copy "unverified declaration". Rejected: still advertises a declared gap on untrusted input and contradicts "unknown unless trustworthy version-bound metadata supports it".
* Alternative C: add a server-signed or dataset-owned declaration. Rejected here: it is a metadata producer, schema and possibly data/identity change; reserved for an owner decision (original follow-up F1).
* Alternative D (selected): defer and remove the declared branch. The empty own-queue state is always `coverage-unknown`. Counter-evidence considered: removing the code loses the future-ready path; accepted, since git history and the original artifacts preserve it and a future trusted producer needs its own design and authority binding.
* Risk: tests that exercised the declared state must change; the coverage argument disappears from the helper and list view call. No other consumer exists (grep of `src`, `tools`, `docs` found only app.js, the test and README).

## Parent Synthesis

| Item | Disposition | Evidence |
|---|---|---|
| Remove `trustedCoverage` and the declared branch; always unknown for empty unfiltered own queue | accepted | C1, C2, C3, Alt D |
| Ignore any `work_queues.coverage` payload even if present | accepted | no trusted anchor (Q2) |
| Add regression reproducing stale/unrelated/unverified provenance with matching context, asserting unknown | accepted | Q1 |
| Keep no-match, unknown, populated, all-cases tests | accepted | Q4 |
| README: state declared state is deferred; client ignores any `coverage` field | accepted | C6 |
| Bind to manifest or constant; label as unverified; add producer/schema | rejected | Alt A, B, C |
| Runtime producer with owner decision | deferred (original follow-up F1) | brief non-goals |

## Decisions and Risks

* Tier stays focused: client copy, unit test and documentation only; no auth, SQL, deployment, security-sensitive processing, schema or data change.
* Risk: Playwright/browser, `--changed`, independent review and hosted CI are not run in this task; the coordinator owns them.
* Risk: the helper signature changes; the wiring test must be updated to match.

## Closeout Record

* Research disposition: executed (one complete wider/deeper/contrarian cycle; evidence saturated for this bounded defect).
* Planning Readiness: Ready.
* Selected approach: Alternative D.
* Further research: none required.
