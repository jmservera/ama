---
title: Resident chat 520 original independent Review
description: Independent post-implementation assessment and remaining acceptance boundaries
ms.date: 2026-10-28
---

## Assessment identity and verdict

* Task: issue #520, resident-chat-520.
* Assessment: the one original independent post-implementation Review, not a
  second plan critique or the subsequent independent exact-head assessment.
* Branch: `feat/resident-chat-520`.
* Observed HEAD: `413ccaf253fce4566e855bae9d0a924b2a82b506`.
  The implementation and original evidence were uncommitted at assessment.
  This Review therefore assesses the observed working candidate, not an
  immutable committed/published head.
* Execution: Partial. Artifact, diff, source/test and fresh web-guideline
  comparisons are complete. Raw external validation files were not independently
  inspected: the supplied browser report and stdout are under `/tmp`, outside
  this assessor's permitted file-operation boundary. Their outcomes below are
  implementation-reported evidence, not independently reproduced results.
* Outcome: Residual work. No high-confidence material runtime defect was found
  in the inspected implementation. One Low evidence-consistency finding remains.
  Neither whole-issue acceptance, complete Fluent adoption, accessibility
  conformance nor publication readiness is established.
* Findings: 0 Critical, 0 High, 0 Medium, 1 Low.
* This original outcome must be preserved. Route corrections to later work;
  do not replace this record with a second original Review.

## Compared artifacts and scope

The complete task artifact set was resolved and compared:

* `.copilot-tracking/research/2026-10-28/resident-chat-520-research.md`
* `.copilot-tracking/plans/2026-10-28/resident-chat-520-plan.md`
* `.copilot-tracking/plans/2026-10-28/resident-chat-520-critique.md`
* `.copilot-tracking/details/2026-10-28/resident-chat-520-phase-details.md`
* `.copilot-tracking/changes/2026-10-28/resident-chat-520-changes.md`

Issue #520's current title/body were retrieved with `gh issue view`. Git
status, branch, tracked diff and newly added source/tests were inspected.
Existing dirty files were assessment inputs, not permission to modify them.
Only this Review record was written.

Implementation files compared:

* `src/api/src/zava_forward/api/resident_demo/app.py`
* `src/api/src/zava_forward/api/resident_demo/__main__.py`
* `src/api/src/zava_forward/api/resident_demo/agenda.py`
* `src/api/src/zava_forward/api/resident_demo/chat.py`
* `src/api/src/zava_forward/api/resident_demo/web/assistant.js`
* `src/api/src/zava_forward/api/resident_demo/web/demo.js`
* `src/api/src/zava_forward/api/resident_demo/web/demo.css`
* `src/api/src/zava_forward/api/resident_demo/web/index.html`
* `src/api/tests/test_resident_chat_agenda.py`
* `src/api/tests/test_resident_chat_api.py`
* `src/api/tests/test_resident_assistant_api.py`
* `src/api/checks/resident_assistant_browser_check.py`
* `src/api/README.md`

Context compared: `docs/case_study_48_original.md`, the resident proposal and
relevant governance context in `docs/case_study_48_addendum.md`,
`docs/reference/README.md`, `docs/reference/memory.md`,
`docs/reference/research/ux/design-system.md`,
`docs/reference/research/ux/wcag-conformance-baseline.md`,
`docs/reference/research/ux/content-standard.md`,
`docs/reference/regulatory/README.md`, the cited
`docs/reference/regulatory/social-housing-regulation/social-housing-safety-and-quality-standard-2024.md`
provisions, and `src/README.md`'s local RPI gate.

## Requirements and implementation assessment

| Requirement | Assessment and exact evidence |
| --- | --- |
| Shared accessible launcher on resident states | `web/demo.js:16` mounts once on the body; `web/assistant.js:193-209,278-300,364-377` provide native launcher/close, named nonmodal dialog, opening focus, Escape, focus return and session reset. `web/demo.css:80-85` provides fixed bottom-right placement, safe-area spacing and contained scrolling. Anonymous, signed-in and error states are represented in the browser harness. |
| Own-case access and explicit record use | `app.py:328-338` rejects absent/nonboolean permission and unexpected assistant fields before personal lookup, including retained topics. `app.py:412-450` applies the agenda contract before lookup/mutation. Session-derived case keys, not client selectors, identify ownership. `test_resident_chat_api.py:39-85,121-160` covers permission-before-lookup, cross-resident disclosures, proposal use and cancellation. |
| Preserved bounded Azure path and labelled AI-off mode | `app.py:361-368` retains the advisor/provider only for existing `Topic` values. Raw typed messages are host-routed in `chat.py:36-72`; other answers carry workflow-only/no-AI labels at `chat.py:112`. Existing advisor/isolation/refusal tests remain, with the intentional record-use schema correction rather than removed contracts. Real-model effectiveness and activation are not evidenced. |
| Dated regulatory explanation, no legal conclusion | `chat.py:10-27,100-101` supplies local path, provision, source/retrieval dates, selected official-comparison date and explicit refusal of legal/safety/compliance conclusions. Local sections 2.3.1..2.3.3 support the bounded summary. This is not knowledge of every current applicable rule. |
| Safety human route without invented receipt | `chat.py:28-33,38-39` prioritizes recognized safety terms and states no report/alert was sent. `web/assistant.js:273-274` keeps person/emergency directions available independently of a successful answer. This is referral, not an integrated hazard intake or delivery receipt. |
| Actual free synthetic inventory, first 1..3 matching slots | `agenda.py:99-147` filters stored free future rows, UK date/period and stable chronological ordering, with expiring own-case offers. A configured empty result is distinct from an unavailable agenda (`app.py:451-453`). Chat initiates the same manual search at `web/assistant.js:179-184,338-340`; the independent form remains usable without AI. |
| Explicit confirmation, race protection and cancellation | `app.py:429-438` requires the exact boolean confirmation. `agenda.py:74-79,158-200` supplies transactional uniqueness, owner binding, idempotency, admission recheck and a fresh future-time check. `agenda.py:202-226,249-253` supports own and file-authorized assisted cancellation. Resident UI requires separate booking/cancel confirmation. |
| Synthetic and unknown boundaries | `agenda.py:14-20`, `chat.py:87-99`, `web/assistant.js:38-41,125-127,145-160` and `README.md:81-146` explicitly distinguish synthetic callbacks, no live contact, absent operational appointments and unknown works consent. No operational officer availability, works authority, real identity verification or invented contact number is claimed. |
| Accessibility/content acceptance | Native controls, labels, live regions, reduced motion, narrow reflow and enlarged-text checks are present. Human/resident wording and actual AT acceptance remain Not run. Fluent-derived tokens are retained; actual Fluent component adoption or owner acceptance of a native-only substitute is not established by this candidate. |

## Original critique dispositions

| Finding | Disposition against the implementation |
| --- | --- |
| PC-001 | Addressed in the inspected code/test contract: legacy and new assistant shapes and agenda actions all require exact `use_record:true` before lookup. Negative tests assert zero personal lookup/model selection. Session/withdrawal generation guards clear answers or suppress stale presentation. |
| PC-002 | Addressed for the synthetic boundary: assisted cancellation uses the explicit local CLI, reference and verification flag, not a new unauthenticated staff HTTP authority. Resident instructions and README describe that boundary. Direct agenda tests cover repeated assisted cancellation and unknown references; a real operational officer workflow is not evidenced. |
| PC-003 | Addressed for the bounded demonstration: visible proposal/confirmation/receipt wording and README distinguish callbacks from live appointments/works consent. The wider absent-record/live-service acceptance remains residual rather than inferred from SQLite success. |
| PC-004 | Addressed by UTC instants, Europe/London filtering/display, chronological first-three ordering, expiry/race tests and the final post-authorization future-time refinement. Test fixtures cover summer offset/noon separation and the slot becoming past while confirming. This does not establish household/professional suitability. |
| PC-005 | Addressed as scoped engineering evidence, not full accessibility acceptance: the existing harness exercises root text at 200% and 320/390/1280 CSS widths, asserts overflow/panel/close-focus conditions and scans chat/manual states. The 320px case is explicitly 400%-equivalent reflow from 1280px, not native browser zoom; native zoom and AT remain unperformed. |
| PC-006 | Planning correction is present, execution is pending: the plan now distinguishes original Review, commit, fetched base/full gate, fresh receipt verification, independent exact-head assessment and pre-push verification. This Review cannot close that finding's publication evidence or attest to a later committed head. |

## Evidence assessment and amendments

The changes record reports:

* Original full API discovery: 1160 tests, OK, 314 opt-in/general-discovery
  skips. Skipped SQL selectors are not SQL integration evidence.
* Final focused five-module run: 45 tests, OK.
* Final full API Ruff/format and mypy over 94 source files, both Node syntax
  checks and diff whitespace check: passed.
* Actual local HTTP Chromium 156.0.8078.4 with pinned axe 4.10.3: 16 scanned
  states, zero violations; synthetic constructed fixtures only.
  Reported raw receipt: `/tmp/ama-520-browser-reviewed/report.json`.

The harness source verifies the pinned axe digest when supplied and contains
the reported interaction/state assertions. Its scans are scoped to chat,
launcher and callback surfaces, not whole-product accessibility. Its request
and page-error assertions do not establish an independent audit of every
browser console message. The raw report/screenshots/stdout were not reopened
under this assessor's file boundary; no fresh browser or test run is claimed.
`git diff --check` was independently run and passed. No heavy tests, SQL,
models, private datasets, secrets, environment inspection or deployment ran
as part of this Review.

The final confirmation-clock refinement is a justified implementation
amendment: `agenda.py:196-199` rechecks future time after admission within the
reservation transaction, and `test_resident_chat_agenda.py:105-112` covers
rollback at the boundary. Full discovery predates that refinement; final
focused/browser results are reported afterward. Do not relabel the earlier
full discovery as an exact-final-head run.

The corrected official URL/provision comparison is recorded in research,
code and README without erasing the original failed URL. This bounded update
does not validate the wider legal corpus. RV-001 concerns only the stale
summary of that evidence.

## Findings

### RV-001 [Low] - Remaining-work summary retains the superseded currentness explanation

* Evidence: `.copilot-tracking/changes/2026-10-28/resident-chat-520-changes.md:98`
  says regulatory currentness is unverified because the official attempted URL
  returned 404. Lines 49-52 of that same record describe the successful corrected
  official publication retrieval and selected-provision comparison. Research
  W6, `chat.py:15-26` and `src/api/README.md:74-79` make the narrower distinction.
* Impact: the handoff summary can leave a later reader unable to distinguish
  the preserved failed first attempt from the successful bounded comparison
  and the still-unverified wider rules. This is an evidence-consistency defect,
  not evidence of an unsafe legal conclusion or a failed official comparison.
* Required disposition: in a later implementation/documentation correction,
  reconcile the remaining-work summary with the already recorded success;
  retain the historical 404 and the wider-currentness limitation. Do not
  rewrite the original critique or this Review.
* Owner/route: implementation parent, later Implement documentation amendment.
  No new research cycle, second critique or second original Review is needed.
* Resolving evidence: a subsequent dated correction clearly separates the two
  retrieval outcomes and preserves the limited claim; any commit after a gate
  requires a new candidate/gate as applicable.

## Fresh changed-web guideline review

The `web-design-guidelines` skill was loaded. The current complete rule source,
`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`,
was successfully fetched on 2026-10-28; the tool returned its full plain text.
All four changed web files were read against its accessibility, focus, forms,
motion, typography, content handling, image, performance, navigation/state,
touch, safe-area, theme, locale, hydration, interaction and copy rules.

Local ASCII punctuation and sentence-case standards take precedence over the
external curly-quote/ellipsis/title-case preferences. Transient personal chat
is intentionally not URL-persisted or guarded as an unsaved durable draft.
Media, hydration and large-list guidance do not introduce new applicable
changed-surface requirements here. This is source inspection, not AT acceptance
or a fresh runtime accessibility scan.

### src/api/src/zava_forward/api/resident_demo/web/assistant.js

Pass within changed scope; no high-confidence material guideline finding.

### src/api/src/zava_forward/api/resident_demo/web/demo.js

Pass within changed scope; no high-confidence material guideline finding.

### src/api/src/zava_forward/api/resident_demo/web/demo.css

Pass within changed scope; no high-confidence material guideline finding.

### src/api/src/zava_forward/api/resident_demo/web/index.html

Pass within changed scope; no high-confidence material guideline finding.

## Remaining work, acceptance and publication routing

| Remaining item | Route and acceptance boundary |
| --- | --- |
| RV-001 evidence summary | Later Implement/documentation correction; preserve original outcomes. |
| Independent inspection of raw reported validation evidence | Publication coordinator/exact-head assessor must inspect the relevant accessible evidence, not infer an independently verified browser pass from this Review. This is a Review execution limitation, not an assertion that the reported run failed. |
| Complete local gate and final independent exact-head assessment | Post-Review publication work, not a request for another original Review. Commit implementation and dated original evidence; fetch main and capture the reviewed base; run the required complete `--all` gate under nonblocking admission to a fresh permitted external directory; fetch again and verify the external receipt against current main and exact HEAD; obtain independent exact-head assessment binding commit/base/receipt; verify immediately before push. Changed source, commit, base, dirty/ignored/untracked inputs or relevant tool/image identity invalidates the old candidate. Missing SQL/browser/scanner prerequisites or busy lock blocks without queueing, skips or cloud fallback. |
| Fluent implementation acceptance | Distinct design-system follow-up or explicit owner acceptance of the native-only substitute; `docs/reference/research/ux/design-system.md:27-32` says tokens/native styling alone do not complete the selected adoption. Do not silently authorize a framework swap through this Review. |
| Resident/content, human and assistive-technology acceptance | Distinct human acceptance work. Browser assertions/axe and partial Fluent foundations do not satisfy these gates or WCAG conformance. |
| Operational agenda, appointment/consent records and wider current rules | Distinct future research/plan/integration and qualified human review. Local callbacks are not an operational service or a complete personal record, and the selected regulatory comparison is not universal current-law knowledge. |
| Real-model #164 evaluation/activation | Distinct evaluated and approved task/provider work; preserved code and mocked transport tests are not paid-inference, effectiveness or live-enablement evidence. |
| Hosted checks and merge | Only publish after the required local/exact-head gates permit; PR references #520 without closing it. Hosted checks and the human merge decision remain separate. No deployment or permission expansion is authorized. |

The synthetic callback choice, bounded host routing, explicit unknowns and
preserved Azure path maintain the intended safety/authority limits. These are
credible scoped engineering results, not permission to claim all #520
acceptance criteria or the complete publication gate satisfied.
