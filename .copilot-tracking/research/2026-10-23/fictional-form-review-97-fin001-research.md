<!-- markdownlint-disable-file -->

# Task Research: fictional-form-review-97-fin001

| Field | Value |
| --- | --- |
| Date | 2026-10-23 |
| Researcher / agent | rpi-research skill, invoked in session 8fe80adc-6a17-41ed-8337-e921375d1cc6 on 2026-10-23 |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-23/fictional-form-review-97-fin001-research.md |
| Parent task | 97 / fictional-form-review-97-recovery (original research, plan, critique, Review and two corrections preserved unchanged) |

## Brief

* Topic: independent full-diff review finding FIN-001 on exact head b22d863992f04ad5115c27ae7579e17a3704a8c0 (base 140d8f494482c78e84d15f3d46b9223d3c487af0). Review file: session b9cc4727 `pr424-b22d8639-review-20261023/review.md`.
* Purpose: establish exactly which documentation claims are false and which directly coupled claims share the defect. Output mode: convergence on a documentation-only correction.
* Authority: the owner explicitly authorized ONE additional ordered correction cycle after two recorded corrections (registry integration, certifi). Not a waiver or blanket retry. Admission: HEAD, origin/main and clean tracked, untracked and ignored state verified before research.
* Non-goals: no runtime or validation change, no fixture authority change, no invented reviewer, no unrelated inherited issues, no full gate, no Docker, Azure or private data.
* Posture: focused (bounded internal task with named source targets and supplied failure evidence). Provenance: caller brief plus review finding.
* Extensions: applicable repository instructions (Markdown style, knowledge base conventions, problem specification conventions) selected; web guidance skipped because no web file changes; company agents and cohort skipped.

## Evidence

| ID | Finding | Location |
| --- | --- | --- |
| C1 | The guide says the schema block "registers unchanged through the existing path". | docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md:28-29 |
| C2 | The core guide says the pack "registers through this path as `Unapproved`". | src/core/README.md:935-936 |
| C3 | The public fixture reviewer is the placeholder `REGISTERED-REVIEWER-SUBSTITUTED-BY-TEST`. | src/core/evals/fictional_form_review_pack.json:38 |
| C4 | `register_schema` refuses a reviewer that is not an existing registered person with "Choose an existing registered reviewer; this records no approval." | src/core/src/zava_forward/core/forms.py:131-133 |
| C5 | The test asserts the unmodified public schema raises `ValueError`, then registers a derived copy differing only in `reviewer`, which stays `Unapproved`. | src/core/tests/test_form_review_pack.py:41-50 |
| C6 | The guide's limits section already states the placeholder is refused and a derived copy is registered. The false claim at lines 28-29 contradicts it. | docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md:63-67 |
| C7 | The fixture says the placeholder exists because public payloads may not hold email addresses and the reviewer must be an existing registered staff member. | src/core/evals/fictional_form_review_pack.json:358 |
| C8 | Fixture statement "Registering its schema records Unapproved status" is conditional on a derived registration and is true; fixture authority is not to be altered. | src/core/evals/fictional_form_review_pack.json:13 |

## Waves (single complete cycle, inline; no delegation needed for a bounded lane)

* Wider: searched the guide, dictionary, KB index, provenance register, eval registry, fixture, core README, KB log and prior tracking for "regist" and "unchanged" claims about the pack.
* Deeper: read `register_schema` validation (C4), the focused test (C5), and the fixture statements (C7, C8).
* Contrarian: tested whether other "registers" wording is also false. Dictionary line 328 and index row 283 say "registered as `DS-FICT-FORM-REVIEW-PACK`", meaning the provenance register, which is true. The 2026-10-20 KB log entry says "registered fictional versioned form/template pack", also the provenance meaning and true; log entries are append-only anyway. The alternative of weakening validation or inserting a real reviewer is rejected: it contradicts the brief, C4 and the placeholder rationale C7.

## Synthesis

* Accepted: exactly two false claims, C1 and C2, share the defect. The correction is wording only: the public fixture is intentionally refused; only a derived copy with a registered reviewer substituted registers, and it stays `Unapproved` with no approval implied.
* Rejected: any runtime, test, fixture or reviewer change (C4, C7, brief).
* Deferred: the provenance-register "registered" wording, which is accurate. Index row 283 and dictionary line 328 stay unchanged, so no index description change is needed. A focused KB log entry is still appended because the guide synthesis changes.
* Residual: fixture statement C8 is conditional and true; noted, not edited.

## Decisions and Readiness

* Research disposition: executed.
* Planning Readiness: Ready.
* Unresolved human items: Finance FD-01..FD-14, real template, authority, binding and OQ-015; criterion 1 unmet, criterion 2 delivered by PR 377.
* Limits: no full gate run; the earlier b22d8639 gate is historical after edits.
