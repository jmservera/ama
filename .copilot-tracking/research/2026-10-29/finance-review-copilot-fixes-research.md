<!-- markdownlint-disable-file -->

# Task Research: finance-review-copilot-fixes

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/finance-review-copilot-fixes-research.md |

## Research Brief

* Topic: PR #510 blank required strings and per-draft source unavailability.
* Purpose/audience: evidence for a bounded correction on docs/finance-96.
* Scope: form_review.py, external package tests, directly related contracts.
* Non-goals: financial authority, schema approval, UI changes, Azure, pushing,
  rubric score editing and unrelated PR work.
* Criteria: blanks remain recorded but cannot satisfy required inputs; numeric
  zero and boolean false remain valid; one unavailable draft cannot hide another.
* Requested outputs: dated full RPI evidence, regressions, local commit.
* Output mode: convergence.

## Research Parameters

* Questions: where is confirmed-input membership determined, and where should
  DocumentUnavailable be isolated without leaking retained values/history?
* Internal candidates: core form_review, forms, tests, API route and component
  READMEs. External candidates: PR #510 lifecycle only.
* Posture: focused (default for named defects with supplied failure evidence).
* Explicit limits: no Azure, no push, no manual rubric-score edits.
* Completion basis: focused scope coverage and material counterexamples.
* Research source edits: prohibited.
* Resolved evidence root: .copilot-tracking/research/2026-10-29/.

## Extension Registry and Provenance

| Kind | Candidate | Match/provenance | Authority / disposition |
| --- | --- | --- | --- |
| Instruction | Repository Copilot instructions | All files | Selected: branch, tests, gates, evidence |
| Skill | rpi-research | Full RPI request | Selected: three-wave evidence |
| Specialist | hve-core-all:rpi-researcher | Registered internal researcher | Skipped: one tightly coupled trace, handled inline |
| Skill | UI/security assessment skills | No UI edit or vulnerability audit requested | Skipped: outside bounded correction |

## User Participation and Research Decisions

* Intake: explicit scope and lifecycle supplied; no clarification needed.
* Caller requests entire loop, local commit only. This is a bounded explicit
  phase sequence, not consent to an indefinite automatic follow-up session.
* Initial git pull --rebase succeeded, worktree clean; current matching branch
  docs/finance-96 has open PR #510 targeting main. Reuse it.

## Scope and Success Criteria

* Regression tests live in src/core/tests, outside the installed package.
* Preserve correction history and document-visibility checks.
* Run all four caller-specified commands from src/core.
* Independent critique and post-implementation Review retain original outcomes.

## Task Research Requests and Direction Controls

* Fix only the two supplied findings and tightly coupled tests/documentation.
* Do not introduce a per-draft route if an opaque list entry can preserve the
  existing endpoint and denial boundary.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | How do required checks distinguish valid scalar values from blanks? | depth | Open |
| Q2 | How can reads isolate unavailable drafts without exposing content? | depth | Open |

## Prior Knowledge Gate

* Read original case study, addendum, reference index and owner memory.
* Verified PR lifecycle with gh pr view; supplied findings remain hypotheses
  until the code/test trace is completed.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Inline trace started at form_review.py and component gate documentation.
* Preliminary observation: _valid accepts blank strings, while view uses a
  comprehension that propagates DocumentUnavailable across the whole response.
* Reflection: inspect external tests, conditional schemas, HTTP serialization
  and existing unavailable-result conventions before selecting changes.

#### Wave 2: Deeper

* C4: external FormReview tests exercise JSON and SQLite reopen, retained
  snapshot/history surfaces, source byte reuse, outages, actor checks and writes.
* C5: HTTP GET serializes view directly; its test expects 403 for one unavailable
  draft and must change to the new explicit 200/per-entry contract.
* Reflection: keep _valid as type validation; filter blank strings at confirmed
  membership so correction and history remain intact, without false type errors.
  Catch only DocumentUnavailable inside the authorized draft loop.

#### Wave 3: Contrarian

* Challenged truthiness filtering: numeric zero and boolean false are valid;
  using `if value` would regress both and typed condition equality.
* Challenged rejecting correction: loses the caller-required recorded correction.
* Challenged partial redaction: retained snapshots, attachments and reviewer
  reasons can disclose evidence even when current fields are empty. Return only
  draft_id, status Unavailable and a fixed recovery notice for an affected draft.
* Challenged broad catch: DocumentStoreError is a service failure, not document
  unavailability; preserve error propagation. Authentication remains outside
  the per-draft exception handler.
* Reflection: existing per-report caches remain unchanged; no route or UI is
  needed. Existing tests must retain write denial and read nonmutation evidence.

#### Parent Synthesis and Disposition

* Accepted C1/C2: exclude blank strings from confirmed values, not from history.
* Accepted C3/C4/C5: return opaque per-draft unavailable entries.
* Rejected: generic falsey filtering, correction rejection, redacting only fields,
  broad exception handling, and an additional route with duplicate authorization.
* Re-entry: not needed; both bounded questions answered with direct code evidence.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | String type validity does not reject blank text | src/core/src/zava_forward/core/form_review.py:44 | High |
| C2 | Required checks use membership in confirmed | src/core/src/zava_forward/core/form_review.py:279 | High |
| C3 | Whole-list report comprehension propagates source denial | src/core/src/zava_forward/core/form_review.py:334 | High |
| C4 | Existing tests cover both stores and all retained snapshot surfaces | src/core/tests/test_form_review.py:21 | High |
| C5 | HTTP tests directly assert old 403 read contract | src/api/tests/test_form_staging_api.py:247 | High |
| C6 | Schema fixture includes required EPC and conditionally required area | src/core/tests/test_form_staging.py:20 | High |
| C7 | Component documentation defines exact typed conditions and retained history | src/core/README.md:146 | High |

No external sources used. No delegation; the trace is tightly coupled.

## Findings, Alternatives and Decision State

* Q1 answered by C1/C2/C6/C7: valid nonblank string values alone join confirmed;
  finite zero and false join it normally. Missing required inputs stay Unknown.
* Q2 answered by C3/C4/C5: isolate DocumentUnavailable for each complete report;
  discard any partial report and expose only a fixed unavailable entry.
* Selected recommendation: minimal confirmed-membership filter and authorized
  per-draft loop; regressions through public actions and reopened persistence.

## Open Questions, Risks and Further Research

* No unresolved implementation question. API test expectations and README must
  change with intentional response shape; no frontend consumes this endpoint.
* Initial validation attempt failed with exit 127: python, ruff and mypy were
  absent from PATH. Created a session-owned external venv and installed existing
  core[dev], agents and api distributions with pip successfully.
* No regulatory interpretation, real data or external model needed.

## Planning Readiness

Ready. Research disposition: executed. Artifact self-check: scope, three waves,
stable evidence IDs, alternatives, constraints and handoff all recorded.
Parent next action: Plan under the user's explicit full-loop direction.
