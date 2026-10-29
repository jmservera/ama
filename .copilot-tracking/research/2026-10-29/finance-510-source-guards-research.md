<!-- markdownlint-disable-file -->

# Task Research: finance-510-source-guards

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/finance-510-source-guards-research.md |

## Research Brief

* What to research: RV-001 missing-byte disclosure through retained history and diagnostics; RV-002 unusable alternatives counted as conflicts.
* Why it matters: working reviews must not expose unavailable evidence or imply choices that cannot be accepted.
* Audience or intended use: maintainers preparing the bounded PR #510 correction.
* Scope: form_review.py, its external tests, storage contracts and directly related documentation.
* Non-goals: financial authority, staged-history deletion, Azure, pushing, rubric-score edits and unrelated branch changes.
* Criteria: source availability independent of schema/current field; non-mutating reads; report-local read reuse; missing versus service failure distinction; review-equivalent alternative freshness/policy.
* Requested outputs: evidence-backed recommendation, then user-requested full RPI loop and local commit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which disclosures need availability checks? Which alternatives can the review path accept? |
| Codebase scope | src/core/src/zava_forward/core, src/core/tests, src/core/README.md |
| External scope | PR #510 lifecycle metadata only |
| Initial internal candidate areas | form_review.py, forms.py, documents.py, test_form_review.py, change_provenance.py |
| Initial external candidate areas | None; no external technical research needed |
| Research posture | focused |
| Posture provenance | Default for named, bounded defects and supplied failure evidence |
| Explicit limits / deadline | No push, no Azure, no hand-edited rubric scores; tests outside package |
| Posture-specific completion basis | Focused scope coverage and materiality |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No private datasets or live services |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide guidance supplied in context | Topic branch, local validation, evidence and publication gate | Selected |
| Skill | rpi-research | RPI lifecycle | Three-wave evidence synthesis | Selected |
| Specialist | hve-core-all:rpi-researcher | Host-visible research agent | Independent research lane only | Skipped: a single tightly coupled trace is best handled inline |
| Skill | Web/design skills | Backend-only task | No applicable web surface | Skipped |

## User Participation and Research Decisions

* Intake: explicit complete task, constraints and commands supplied; no clarification needed.
* Full loop is explicitly requested, without entering an open-ended automatic follow-up session.

## Scope and Success Criteria

* Preserve stored history and diagnostics, existing authority holds, scan/policy denials and staged records.
* Every finding maps to code evidence and a regression.
* Tests must distinguish absent bytes, stale metadata and storage outage.

## Task Research Requests

* RV-001 and RV-002 are user-supplied findings to verify against current source.
* Run requested unittest discovery, Ruff lint/format and mypy from src/core.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | Two form-review findings | User request | No unrelated fixes |
| exclude | Push, Azure, rubric score edits | User request | Local-only delivery |
| add | Full RPI and local commit | User request | Dated evidence and independent critique/Review |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How can history and diagnostic snapshots escape byte availability checks? | depth | H | answered |
| Q2 | How can alternative eligibility reuse review freshness and policy checks without mutating staging? | depth | H | answered |
| Q3 | What cache lifetime and exception behavior preserve existing contracts? | straightforward | H | answered |

## Prior Knowledge Gate

* Read the previous issue-96-pr-510-fix-cycle-1 state: its completed work introduced exact-source report-local freshness caching and required history protection.
* Cross-session branch lookup returned no matching sessions within seven days; repository evidence remains authoritative.
* Treat prior review outcome as historical, not proof against these newly supplied cases.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

* Inline inspection of form_review.py identifies separate metadata preflight, current-field freshness and a weak staging-alternative filter.
* Reflection: byte checks are short-circuited by schema staleness and metadata mismatch; history preflight currently checks only metadata and policy. Prioritize storage exception and test contracts next.

#### Wave 2: Deeper

* Local and blob storage both map missing bytes to KeyError, while service failures use DocumentStoreError (C3).
* JSON and SQLite controlled actions restore failed work; read-only view never needs a save or scan (C4).
* Existing two-field cache tests spy on exact source freshness and one read per report, including diagnose (C5).
* Reflection: share a report/action-local document digest cache across historical preflight and current-source freshness, retaining tuple-keyed freshness results.

#### Wave 3: Contrarian

* Challenge: checking only current fields still misses rejected/replaced evidence; schema staleness short-circuits freshness; diagnostic snapshots can independently retain earlier source references.
* Challenge: historical version mismatch must not block retained history when bytes remain available. Availability is independent of historical freshness.
* Challenge: suppressing all storage exceptions would hide outages. Convert only missing-source KeyError to DocumentUnavailable; propagate DocumentStoreError.
* Challenge: unavailable unreviewed alternatives need exclusion rather than whole-draft denial, because their values are not returned; history/snapshots require fail-closed denial.
* Reflection: traverse fields, prior/new history evidence and diagnostic fields/history/attachments. Deduplicate byte reads by document ID; cache freshness separately by exact source tuple.

#### Parent Synthesis and Disposition

* Accepted C1-C6. Retained evidence gets availability and existing clean/policy checks regardless of schema freshness.
* Alternative qualification uses the same source-policy helper and _current as candidate review; matching case/schema and non-human-only field checks apply before counting raw values.
* No further cycle: storage, rollback, persistence and cache constraints are now evidence-backed; regressions belong to implementation.

## Evidence Log

* Delegation: inline; tightly coupled trace does not justify isolated research workers.

| ID | Claim / finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Metadata preflight never reads bytes; freshness is schema/current-field gated | src/core/src/zava_forward/core/form_review.py:98 | read | High |
| C2 | Conflict filter checks matching schema and clean document ID, not freshness/policy | src/core/src/zava_forward/core/form_review.py:225 | read | High |
| C3 | Missing bytes raise KeyError; backend failures raise DocumentStoreError | src/core/src/zava_forward/core/documents.py:76,176 | read | High |
| C4 | Controlled JSON/SQLite actions recover errors; source clean checks do not scan | src/core/src/zava_forward/core/change_provenance.py:108; src/core/src/zava_forward/core/doc_controls.py:150 | read | High |
| C5 | External JSON/SQLite tests enforce exact tuple freshness and one read for shared fields on view/diagnose | src/core/tests/test_form_review.py:98,137 | read | High |
| C6 | Candidate review checks current kind against field policy, then exact metadata/bytes | src/core/src/zava_forward/core/form_review.py:119,151 | read | High |

## Findings Mapped to Questions and Evidence

* Q1: C1/C3/C4 prove RV-001. All returned retained-source surfaces need independent availability checks without rescan or source writes.
* Q2: C2/C6 prove RV-002. Stage records must remain untouched while unusable alternatives are excluded.
* Q3: C3/C5 require missing/service distinction, per-report byte-digest reuse and exact-tuple freshness caching.

## Alternatives and Decision State

* Selected: report/action-local digest cache plus existing exact-tuple freshness cache; explicit traversal of known report-shaped retained surfaces; one shared field-policy guard for candidate and alternative review.
* Rejected: only checking current fields or returning stale history after a missing blob, because C1 proves disclosure bypasses.
* Rejected: deleting staging/history or swallowing service failures, because C3/C4 and caller requirements preserve these contracts.
* Rejected: global caches or ID-only freshness keys, because C5 requires fresh requests and distinct version/hash/kind identities.

## Open Questions, Risks, and Residual Uncertainty

* No unresolved design questions. Missing validation executables on PATH will be handled only after the actual command failure.
* The full publication gate is separate: no push/publication is requested; no Azure fallback is permitted.

## Planning Readiness

* Research disposition: executed, complete.
* Planning Readiness: Ready.
* Self-check: questions mapped to C1-C6, all three waves and alternatives recorded; no external technical claims, no source changes, no private data.
* Continuation: user-requested parent advances to Plan; no independent automatic session is started.
