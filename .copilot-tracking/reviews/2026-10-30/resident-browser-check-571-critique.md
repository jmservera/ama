---
title: Resident browser check 571 independent plan critique
description: Single final-candidate assessment of the bounded resident check correction
ms.date: 2026-10-30
---

## Metadata

* Task ID: 571.
* Critique date: 2026-10-30.
* Plan: .copilot-tracking/plans/2026-10-30/resident-browser-check-571-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-browser-check-571-phase-details.md
* Critique execution status: Complete.
* This is the single final-candidate independent plan critique. Plan, details,
  research and executable sources were not changed.

## Inputs and Criterion Boundary

* Caller requirements: ordered full RPI; actual local browser reproduction;
  correct the stale check without weakening plain language, honest AI/rules
  labels or resident authority limits; resident units, browser check, Ruff and
  mypy; full API units only under the caller's exact serialization command;
  local Refs-only commit; no push, Azure, deployment, live sign-in or credentials.
* Assessment inputs: the exact supplied plan, phase details and research;
  src/api/checks/resident_assistant_browser_check.py;
  src/api/tests/test_resident_chat_api.py;
  src/api/src/zava_forward/api/resident_demo/chat.py;
  src/api/README.md:960-1062;
  docs/reference/research/ux/content-standard.md:21-48; and the supplied C1
  review at
  .copilot-tracking/reviews/logs/2026-10-30/employee-chat-dismissal-correction-review.md:102-110.
* Project context: docs/case_study_48_original.md,
  docs/case_study_48_addendum.md, docs/reference/README.md,
  docs/reference/memory.md and
  docs/reference/method/tracking-retention-policy.md. Memory is context, not
  acceptance evidence.
* Locked decisions: product unchanged; no coverage removals; at most one typed
  browser submission helper and two focused unit methods; retain existing
  positive document test where sufficient; one critique and one independent
  Review; no publication gate claimed for local-only delivery.
* Assessment boundary: credibility and implementability of this candidate,
  including its positive and adversarial validation design. This assessment
  does not implement, rerun browser/tests, assess deployed behavior or establish
  human content, accessibility, actual-model or live-service acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered research, plan, implementation, Review | Covered | Research records investigation before this candidate; P01 precedes P02; implementation remains pending. |
| C1/C2/C8, AC1: baseline failure | Partial | C1 preserves independent baseline provenance; C2 matches the current stale check. C8 is a reported browser execution whose original log was not inspected; PC-001 addresses executable paths and evidence handoff. |
| C3/C5, FR1/G2: supported versus refused inputs | Covered | Full-message document/form patterns accept the proposed complete questions. Existing mixed-request rejection is intentionally retained. |
| C4/C7, FR3: facts, sources, labels and authority | Covered | Existing HTTP document test establishes the expected facts; plan retains these, rules labeling, isolation and no-send/not-a-decision limits. |
| FR2/G3, P01-T01, AC3: fresh assistant replies | Covered | Assistant article count must increase before assertions; geometry and other-resident assertions bind to their own replies rather than whole history. |
| FR4, P01-T02: obsolete-input refusals | Covered | Existing assert_host_routes checks exact answer, sources and rules label plus no advisor, accounting, token, transport or provider use; unknown answer includes housing-officer help. |
| P01-T03, AC2/AC3: positive browser and mutation rejection | Covered | Full actual fixture/Chromium run retained; second document answer is deliberately refused after earlier facts exist; expected assertion and adverse output must be recorded. |
| P01-T03, AC4: executable validation prerequisites | Partial | Required selectors and static checks are specified, but forbidden output/runtime paths and default temporary storage need PC-001 correction. |
| Coverage lock and documentation | Covered | Three canonical targets, no runtime changes, no removals and bounded helper/test additions; directly related API rationale only. |
| P02-T01, AC5: independent Review and limitations | Covered | One independent Review retains original outcomes, assesses semantic/regression evidence and routes residual work; human/live acceptance remains unchecked. |
| P02-T02, AC5: local delivery | Covered | Privacy-safe local identity, Copilot trailer, Refs-only commit, no push/PR/deployment and no publication-gate claim. |

## Verdict

* Verdict: Revise.
* Rationale: the technical correction is credible and properly bounded.
  However, its prescribed validation procedure cannot be followed under the
  active no-temporary-directory file-operation restriction. Correct that
  procedure directly before implementation; do not broaden product behavior or
  run another critique.
* Severity totals: 0 Critical, 1 High, 0 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Validation paths violate the active file-operation boundary

* Related IDs: P01-T03, P02-T01/P02-T02, AC1, AC2, AC4, AC5, research C8.
* Evidence: phase details P01-T03 prescribes a virtual environment, axe input
  and browser output under /tmp. The plan's Sources and research C8 also point
  to the original baseline log there. Active execution instructions prohibit
  file operations in /tmp, /var/tmp or temporary directories and require new
  files to be project-relative. Additionally,
  src/api/checks/resident_assistant_browser_check.py:650-687 uses Python
  tempfile for the default output and agenda, while
  src/api/tests/test_resident_chat_api.py:205-210 creates a TemporaryDirectory.
  Merely changing --out will not relocate those fixture files.
* Concern: the candidate describes these commands as ready to execute, without
  a compliant project-owned runtime/output configuration or a path-safe
  handoff for its original baseline evidence. The optional full-suite lock
  also names /tmp, so it cannot be executed in this context despite being the
  caller's required lock for any such run.
* Impact: following the plan would breach the execution boundary; omitting
  fixtures or axe instead would weaken the required real-browser validation.
  A local evidence commit must not imply that an inaccessible original log was
  independently inspected or preserved with that commit.
* Smallest useful change: revise P01-T03 and its handoff to use explicit
  project-relative, task-owned non-temporary runtime and evidence locations.
  Configure inherited temporary-file environment variables to that approved
  project-owned runtime directory before running existing fixtures, and
  verify the effective tempfile/browser output locations without changing
  product code. Use an already available compliant environment and
  digest-checked axe input, or record the missing prerequisite as blocked.
  Record the reported original baseline log's provenance and present
  accessibility honestly in dated evidence; preserve existing adverse records
  without reading, moving or deleting forbidden-path files. If independent
  verification of that raw log is unavailable, retain C1's independently
  recorded baseline finding as such and obtain any needed new unmodified
  reproduction only through compliant paths. Do not run the optional full API
  suite in this context: record it as Not run, retain the exact caller lock
  requirement for future authorized execution and do not substitute another
  lock. Keep required resident/browser/static validation and the one-critique
  limit unchanged.
* Action owner: planning parent for the procedure correction; implementer for
  effective-path verification and validation evidence.
* Exact resolving evidence: corrected P01-T03 commands and prerequisite
  disposition; dated command/results records showing project-owned runtime
  and output locations, digest-checked axe, successful positive browser,
  expected negative-browser assertion, resident units, Ruff and mypy; explicit
  baseline-log accessibility/provenance; optional full API suite marked Not run
  unless it can legally use the exact required lock. Preserve original
  research and critique outcomes rather than rewriting them.
* Decision route: direct planner correction. No significant or divergent user
  decision is needed; the full API suite is explicitly optional and no change
  to its serialization condition is authorized.

## Strengths and Residual Risk

* The supplied routing patterns and actual HTTP test support fixing the stale
  harness rather than loosening complete-message admission.
* Fresh assistant-article assertions and the later-refusal browser mutation
  specifically address the observed whole-history false-positive risk.
* Existing assert_host_routes supplies meaningful no-model/no-side-effect
  rejection coverage without a new framework or duplicated prompt registry.
* Scope, test additions and document expectations are locked. Plain-language
  questions and rules labels preserve the stated acceptance meaning; changing
  unrelated AI label conventions is not justified by this correction.
* Synthetic checks do not approve resident wording or establish WCAG, human,
  actual-model or live-service acceptance. The candidate explicitly retains
  those gates and does not claim whole-issue closure.

## Questions or Blocking Evidence Gaps

* No unresolved product or user-choice question.
* Execution depends on the compliant runtime/axe locations and evidence
  disposition in PC-001. Missing prerequisites must be reported, not bypassed.

## Limitations

* The original C8 raw browser log and its environment were not accessed.
  Research execution claims are distinguished from independently read source
  and the preserved C1 review.
* No browser, test, static checker, account lookup or remote operation was
  performed for this read-only critique.
* This assessment is confined to the supplied candidate and relevant evidence,
  not an open-ended repository or UI audit.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly correct validation paths and optional-suite
  disposition, record the critique disposition, then hand the bounded plan to
  implementation if prerequisites are available.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/resident-browser-check-571-plan.md](.copilot-tracking/plans/2026-10-30/resident-browser-check-571-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/resident-browser-check-571-phase-details.md](.copilot-tracking/details/2026-10-30/resident-browser-check-571-phase-details.md) | Assessed implementation and validation procedure |
| [.copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md](.copilot-tracking/research/2026-10-30/resident-browser-check-571-research.md) | Supplied research and reported browser reproduction |
| [.copilot-tracking/reviews/2026-10-30/resident-browser-check-571-critique.md](.copilot-tracking/reviews/2026-10-30/resident-browser-check-571-critique.md) | Original single independent critique |

## Next Steps

The active planning parent should disposition PC-001 directly and continue only
after the compliant validation prerequisites are resolved. No second critique,
user response, implementation by this reviewer, commit or remote write is
authorized by this handoff.
