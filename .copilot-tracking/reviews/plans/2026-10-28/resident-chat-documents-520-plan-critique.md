---
title: Resident chat document correction plan critique
description: Independent final-candidate assessment for task 520-documents-correction
ms.date: 2026-10-28
---

## Metadata

* Task ID: 520-documents-correction
* Task slug: resident-chat-documents-520
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-documents-520-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-documents-520-phase-details.md
* Critique execution status: Complete
* Assessment: single independent final-candidate critique; no implementation or heavy checks.

## Inputs and Criterion Boundary

* Owner direction: correct PR #525 on feat/resident-chat-520 for own-case missing
  documents, provision instructions and all recorded resident-facing warnings/errors.
  Answers must be plain, grounded and cited, preserve the same rules facts with AI
  off, make no acceptance/compliance claim and refer uncertain decisions to staff.
* Supplied research:
  .copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md,
  C1-C6, W1, Q1-Q3 and the recorded alternatives.
* Source evidence: infra/sql/resident-showcase.sql;
  src/core/src/zava_forward/core/resident_showcase_sql.py;
  src/core/src/zava_forward/core/resident_showcase.py;
  src/core/src/zava_forward/core/resident_assistant.py;
  src/core/src/zava_forward/core/store.py;
  src/core/src/zava_forward/core/doc_controls.py;
  src/core/tests/test_resident_showcase_sql.py;
  src/api/src/zava_forward/api/resident_demo/app.py;
  src/api/src/zava_forward/api/resident_demo/chat.py;
  src/api/src/zava_forward/api/resident_demo/aoai.py;
  src/api/checks/resident_assistant_browser_check.py;
  src/README.md; tools/rpi-checks.py.
* Repository context: docs/case_study_48_original.md; relevant opening context in
  docs/case_study_48_addendum.md and docs/reference/README.md; owner preferences in
  docs/reference/memory.md. No legal-currentness conclusion is assessed.
* Read-only GitHub inspection confirmed open PR #525, head feat/resident-chat-520,
  base main, and issue #520's added document-answer acceptance criterion.
* Decisions and dependencies assessed: additive own-case view/typed snapshot,
  explicit request and resident-visible issue fields, deterministic mandatory
  answer, guidance-ID-only AI, preserved consent/revocation, source-only view
  application, existing pinned dependencies and local full-gate publication.
* Locked test contract is retained: core owns parsing/explanation/SQL; API owns
  HTTP/advisor/browser; no test removals; at most two new files and 24 new methods.
  Findings can be resolved through existing files and table-driven subtests
  without increasing those limits or adding dependencies.
* Scope excludes implementation, source edits, live deployment, Azure operations,
  secrets, .env, private datasets, whole-issue approval and human/AT acceptance.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Own-case missing documents and provision; C1-C4; P01-T01 | Covered | Explicit resident requests, nongenerated kind matching, no staff-checklist inference, manual secure route. |
| All recorded issues and plain explanations; C3; P01-T01/P02-T01 | Partial | Resident warning/error lists are covered; canonical infected/mismatch scan explanations are not explicitly assigned or tested: PC-002. |
| Strict bounds, malformed input, null versus empty; C2; P01-T01/P02-T01 | Partial | Parser tests are planned, but source-through-view preservation of invalidity is not an explicit SQL acceptance condition: PC-001. |
| Own-case authorization, citations, consent and revocation; C4 | Covered | Per-item references, fresh authorization, two-case HTTP fixtures and post-inference revocation are specified. |
| Identical rules facts with AI off; C5 | Covered | Mandatory host-owned answer and sources are retained under guidance selection and fallback. |
| Typed explanation routing; P01-T01 | Covered | Document explanations precede generic status/action refusal while preserving safety, injection and other-resident refusals. |
| Browser and accessibility engineering; C6; P02-T01 | Covered | Actual typed/selected questions, citations/issues, session isolation and long-answer reflow are specified; human/AT acceptance remains pending. |
| Test ownership, removals and bounds; P02-T01 | Covered | Ownership and numerical limits are explicit and need not change. |
| Component documentation and deployment boundary; P02-T01 | Covered | Unknowns, manual/no-upload path and separately authorized view application are documented. |
| Independent evidence and exact-head publication; P03-T01 | Partial | Original outcomes, nonblocking shared lock and normal push are preserved; required reviewed-base argument is absent: PC-003. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: The approach is credible and appropriately bounded, but the locked
  validation contract must prove malformed source data survives SQL projection as
  invalid rather than becoming apparently valid facts. It must also enumerate
  the existing scan failure states and make the required gate base explicit.
  These are direct planner corrections, not unresolved design decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Prove strictness before SQL projection can erase source invalidity

* Related IDs: C2; P01-T01; P02-T01; strict bounded shapes and null/empty acceptance.
* Evidence: Plan lines 67-69 require explicit fail-closed behavior without
  truncation, while lines 81-82 assign SQL integration only named-field privacy,
  own-case filtering and grants. Phase details lines 20-23 specify
  OPENJSON/FOR JSON projection; lines 44-48 assign strict shape tests to the core
  parser but do not require malformed canonical case JSON through the real view.
  infra/sql/resident-showcase.sql already uses scalar JSON_VALUE and JSON_QUERY
  extraction; src/core/src/zava_forward/core/resident_showcase_sql.py parses
  only the projected row. src/core/tests/test_resident_showcase_sql.py provides
  the existing disposable-loopback SQL harness.
* Concern: Strict parsing after projection does not prove strictness of the
  original record. SQL scalar extraction or typed OPENJSON columns can coerce
  non-string values; bounded SQL string types can truncate before Python checks
  length; lax container extraction can collapse a wrong-type value into null.
  OPENJSON also needs an explicit array-versus-object distinction. The plan
  does not specify preservation or validation of these distinctions at the
  source-to-view boundary. This is a missing proof obligation, not a claim that
  the unwritten implementation already contains these defects.
* Impact: Malformed data could become a valid-looking request, a misleading
  known-empty/unknown document list, or shortened instructions/issues, defeating
  the required completeness and fail-closed guarantees despite passing parser
  unit tests.
* Smallest useful change: Add source-through-real-view acceptance cases to
  P01-T01/P02-T01. Require container/type/length validation before lossy
  projection, or an explicit invalid marker that the reader rejects. Preserve
  unknown versus empty; do not solve this by projecting raw private metadata.
* Action owner: Planning parent; implementation ownership remains core/SQL.
* Exact resolving evidence: Revised plan/details require disposable-local-SQL
  subtests inserting absent/null/empty and wrong-type request/document/issue
  containers, numeric values where strings are required, and over-limit text
  and collection lengths into constructed dbo.cases bodies. Assertions exercise
  the actual view and ShowcaseReader, prove valid boundary values survive
  unchanged, and prove malformed values fail explicitly rather than normalize,
  truncate or disappear. Existing privacy/grant assertions remain required.
* Decision route: Direct planner correction; no user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Lock explanations and tests for both canonical scan failure states

* Related IDs: C3; P01-T01; P02-T01; every recorded issue acceptance.
* Evidence: src/core/src/zava_forward/core/doc_controls.py, Scanner.scan,
  _scan_result and require_clean, defines clean, pending, infected and mismatch.
  The plan requires all known scan issues at lines 58-59 but its explicit scan
  acceptance matrix at lines 75-77 names pending/unknown/clean only. Details
  lines 44-46 name resident warnings/errors and unknown codes, without naming
  either canonical failure status or its distinct plain explanation.
* Concern: The proposed warning/error fixtures can satisfy the new
  resident_issues contract while leaving infected and mismatch untested or
  lumped into an unknown scan response. Those are known recorded codes, not
  unknowns. Their established meaning can be explained without scanner detail,
  bytes, model interpretation or a claim that the file is accepted.
* Impact: The correction can still miss a document's actual recorded error or
  explain a type mismatch as a different problem, leaving the owner's added
  criterion unproven.
* Smallest useful change: Enumerate the deterministic scan mapping and add
  infected/mismatch to the locked core test matrix. Explain the recorded malware
  flag or file-type mismatch in neutral plain wording, with document citation
  and staff referral; never infer a duty is met or tell the resident to upload
  in chat. Retain pending/clean/unknown distinctions.
* Action owner: Planning parent; core owns mapping/tests and API owns parity.
* Exact resolving evidence: Revised P01/P02 details explicitly require
  table-driven constructed records for all four canonical statuses plus an
  unknown code, asserting distinct grounded explanations, per-document sources,
  no scanner detail and no acceptance claim. Require the existing fake-advisor
  parity assertion to preserve those rules facts/sources. State that fixtures
  do not prove live persistence: normal upload rejects infected/mismatch and
  rescan normally removes such documents.
* Decision route: Direct planner correction; no new producer, historical-event
  retrieval, scanner execution or user decision is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Pin the required reviewed main base in gate and receipt verification

* Related IDs: P03-T01; exact-head publication acceptance.
* Evidence: Details lines 68-71 instruct
  tools/rpi-checks.py --all --lock-timeout 0 with an external output directory,
  but do not name a reviewed base or pass --base to either gate operation.
  tools/rpi-checks.py:2199 makes --base mandatory, and clean_identity rejects
  a base that differs from origin/main or is not the candidate's ancestor.
  src/README.md, Local RPI gate, explicitly captures origin/main after fetch
  and uses that SHA for both the run and receipt verification.
* Concern: As written, the named gate command fails argument parsing. More
  importantly, publication identity is not explicitly bound to a reviewed main
  SHA, although the plan correctly recognizes that a changed base invalidates
  the receipt.
* Impact: The implementer must invent an omitted publication prerequisite, or
  cannot execute the planned full gate. A different fetched main before push
  needs an explicit stop/reconciliation rule rather than reuse of old evidence.
* Smallest useful change: Specify fetching main, recording the reviewed
  origin/main SHA and passing --base <reviewed-main-sha> with --all,
  --lock-timeout 0 and --out <new-external-directory>. Require receipt
  verification against freshly fetched current origin/main immediately before
  exact-head assessment/push. If main moved, reconcile and rerun the gate.
* Action owner: Planning parent; publication executor follows P03-T01.
* Exact resolving evidence: Plan/details contain the complete argument contract
  for run and --verify-receipt, identify the captured base, and explicitly block
  publication on base/receipt mismatch. Keep the existing nonqueued runner-owned
  shared lock, clean-candidate rule and external immutable receipt.
* Decision route: Direct planner correction; no user decision, gate execution
  or change to the authorized normal-push/rebase direction is required here.

## Strengths and Residual Risk

* Explicit resident requests avoid inventing obligations from the staff evidence
  checklist. Unknown data is not treated as "nothing needed".
* Generated placeholders cannot establish presentation; receipt and clean scan
  cannot establish acceptance or compliance.
* The deterministic answer remains authoritative under AI selection/fallback.
  Large valid answers may exceed the existing 4096-byte AI payload allowance;
  the existing advisor then returns the unchanged rules base. Do not silently
  enlarge model/accounting limits or truncate mandatory facts to avoid fallback.
* Consent, own-session selection, fresh revocation checks, inert quoted record
  text and manual staff routes remain explicit.
* Source-only view changes do not prove deployment. Human/resident/AT and
  real-model acceptance remain pending, as the plan already records.
* Requested rebase and normal push are owner-authorized; no branch change,
  force-push, merge, or whole-issue closing claim is recommended.

## Questions or Blocking Evidence Gaps

* No significant/divergent user decision is needed. Supplied evidence supports
  this critique; the three findings are plan corrections rather than requests
  for further open-ended research.

## Limitations

* This is plan credibility assessment, not an implementation review, successful
  test run, legal opinion, accessibility-conformance assessment or publication
  approval. No SQL server, browser, model, scanner or full gate was run.
* Branch and PR lifecycle were checked read-only. The pre-existing untracked
  plan, details, research and state artifacts were not edited or committed.
* Only this requested critique artifact was written. No source, original Review,
  research, plan, phase details or session-state record was changed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Add the canonical-source-through-SQL strictness proof
  to the existing owned test matrix, then dispose PC-002 and PC-003 directly.
* User response required: No.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/resident-chat-documents-520-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-documents-520-plan.md) | Assessed final-candidate plan. |
| [.copilot-tracking/details/2026-10-28/resident-chat-documents-520-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-documents-520-phase-details.md) | Assessed phase execution contract. |
| [.copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md](.copilot-tracking/research/2026-10-28/resident-chat-documents-520-research.md) | Supplied internal evidence and decisions. |
| [.copilot-tracking/reviews/plans/2026-10-28/resident-chat-documents-520-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/resident-chat-documents-520-plan-critique.md) | Complete independent critique; Revise. |

## Next Steps

Return to the active planning parent to revise and record dispositions for
PC-001 through PC-003, preserving this original finding set, test ownership,
no-removal rule and numerical bounds. Finalize without another critique.
No user action is required. This critique stops here; it does not implement,
run publication checks or invoke another stage.
