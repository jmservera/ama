---
title: Resident chat 520 final-candidate plan critique
description: One bounded assessment of the resident chat plan and phase details
ms.date: 2026-10-28
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 520.
* Critique date: 2026-10-28.
* Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-plan.md.
* Phase details: .copilot-tracking/details/2026-10-28/resident-chat-520-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one final-candidate assessment. No implementation, tests, heavy commands or further agents.

## Inputs and Criterion Boundary

* Primary inputs: .copilot-tracking/research/2026-10-28/resident-chat-520-research.md, .copilot-tracking/plans/2026-10-28/resident-chat-520-plan.md and .copilot-tracking/details/2026-10-28/resident-chat-520-phase-details.md.
* Caller requirements: ordered Research, Plan, independent critique, implementation and independent Review; Fluent 2/WCAG/plain language; bottom-right help throughout the resident site; own-record grounding; explicit data-use and booking consent; dated regulatory explanations without legal conclusions; first suitable real free slots, 1..3 proposals, confirmation, cancellation and a manual route; preserved Azure route and labelled offline operation; synthetic-only local work; tests outside packages; units/Node/real HTTP/Playwright/axe; nonblocking heavy admission; complete exact-head publication gate and PR Refs #520.
* Supplied evidence pointers checked: issue #520 and linked #469/#164; src/README.md local RPI gate; the named resident demo assistant route, Azure advisor, host-owned assistant answers and showcase projection; the existing assistant browser harness; the selected Safety and Quality Standard snapshot; regulatory register; WCAG and content standards. Mandatory project orientation used the original case study, resident-service section of its addendum, knowledge-base index/memory and sector primer. No new regulatory research or live service inspection was undertaken.
* Decisions assessed: local explicitly configured persistent SQLite callback agenda rather than writes to the read-only SQL showcase or reuse of works agreements; host-owned bounded answers; no model booking authority; unknown absent consent records; human/AT and live-model acceptance deferred.
* Dependencies and acceptance criteria assessed: every P01-T01 through P03-T04 task, stated inter-task dependencies, AC1 through AC6, test ownership/change budget, RPI order and publication prerequisites.
* Boundary: assess implementation readiness and truthful synthetic-demo claims, not source correctness, operational feasibility, legal currentness, live approval or accessibility conformance. The supplied plan has no numbered functional requirements; findings identify its named requirement sections and task/AC IDs.
* Workspace inspection found the expected feat/resident-chat-520 topic tracking origin/main, no matching PR, and four pre-existing untracked RPI inputs/state files. They were not changed, moved or committed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Ordered RPI; P01/P02/P03 dependencies | Partial | Research and one critique are ordered correctly; final exact-head independent assessment needs an explicit position and stop condition, PC-006. |
| AC1; P02-T01; shared launcher | Covered | One mount outside hidden personal content; anonymous/error states; native button, visible Chat label, keyboard dismissal, focus return and session-generation teardown are specified. |
| Fluent 2, WCAG, content; AC1/AC6; P03-T02 | Partial | Tokens, 44px targets, reflow, focus, reduced motion and announcements are planned; text-resize/zoom evidence is absent, PC-005. |
| AC2; P01-T02; own-record/data-use boundary | Partial | Own-case projection, no free text to the model, reauthorization and cross-owner tests are credible; retained personal topic route is not covered by the new consent condition, PC-001. |
| AC3; C8/W5; regulatory explanations | Covered within the stated limit | Local source/provision/source date/retrieval date, refusal and unverified-currentness warning are specified. A failed official-source check is not currentness evidence. |
| Safety and manual human help; P01-T02/P02-T02 | Covered as a manual handoff only | Immediate human/emergency guidance and an explicit not-sent statement are appropriate for this bounded demo. No staff receipt, hazard case or response may be claimed. |
| AC4; C4/C5; callback agenda choice | Partial | Persistent real local inventory is preferable to fabricated slots or works authority; resident-facing scope and acceptance claims need explicit qualification, PC-003. |
| AC4; P01-T01/P02-T02/P03-T01 | Partial | Transactions, uniqueness, short-lived case-bound offers, explicit confirmation, idempotency, expiry, revocation and race tests are planned. Person-assisted cancellation and precise time ordering/filter semantics remain incomplete, PC-002/PC-004. |
| AC5; C1/C2/C3; preserved Azure route | Covered | Existing approved topics and host-owned prose remain; existing response labels include AI suggestion, not approved and Summary by rules. Preserve those labels in the new presentation and test the offline branch without real model calls. |
| Synthetic-only; package/test boundaries | Covered | No default agenda data, explicit configuration, constructed fixtures, tests outside source packages, no SQL write expansion or new model provider. |
| AC6; P03-T01/P03-T02 | Partial | Focused/API units, Node, lint/types, actual HTTP, Chromium and pinned axe reuse are planned; PC-005 completes the stated visual-accessibility evidence boundary. No AT/resident pass is inferred. |
| Heavy admission and exact-head publication; P03-T04 | Partial | Nonqueued admission, complete gate, authenticated noreply identity, trailer and Refs #520 are retained; PC-006 makes the final assessment and invalidation sequence executable. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 4 Medium, 0 Low.
* Rationale: the bounded architecture is credible and does not need a framework overhaul. Six substantive gaps need direct planning corrections before implementation/publication readiness can be asserted.
* Callback scope assessment: #520 does not specify that the appointment must be works installation. An explicitly configured, persistent, operator-seeded synthetic officer-callback agenda can honestly demonstrate its free-slot search/proposal/confirmation mechanism. It does not establish integration with an operational agenda, officer availability, works consent, a live service, current-law knowledge or complete historical appointment/consent records. Scope qualification must be visible to residents and in acceptance/PR evidence, not only in developer documentation. Refs #520 is appropriate; whole-issue closure or live-service acceptance is not established.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: The retained personal topic route can bypass the proposed data-use consent

* Related IDs: explicit record-use requirement; AC2; P01-T02; P02-T01; P03-T01.
* Evidence: the plan limits the consent condition to "new personal chat/agenda lookups"; phase details require the boolean only for an "Additional bounded question request" while retaining the existing endpoint. In src/api/src/zava_forward/api/resident_demo/app.py, _assistant accepts only {"topic"} and resolves the personal case/provider response without a record-use consent field or equivalent grant.
* Concern: sign-in, a familiar question selector or preserving an old endpoint is not the explicit assistant data-use permission required by #520. Merely protecting the new request shape leaves the retained personal status/model path outside that boundary.
* Impact: the launcher could access own-case information or invoke the approved model path before the resident has agreed to this use, despite the new checkbox.
* Smallest useful change: explicitly apply the consent precondition to every personal assistant and agenda request, including retained fixed-topic requests. Specify a server-checked request condition or session-bound permission, its reset/revocation behavior, and refusal before personal lookup/model invocation. Preserve approved topics/provider limits rather than silently preserving an unconsented request contract. Anonymous generic help remains independent.
* Action owner: planning parent; implementation owner executes the corrected contract.
* Exact resolving evidence: P01-T02/P02-T01 and AC2 explicitly include the legacy personal endpoint; P03-T01 names direct HTTP tests for absent/false consent on old and new request shapes with zero personal response/model calls, explicit-consent success, and clearing/rejection after session change or permission withdrawal. Later implementation evidence must show those tests passing.
* Decision route: direct planner correction. Current user direction already requires explicit data-use permission; no new user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Resident cancellation is specified, but person-assisted cancellation has no supported path

* Related IDs: issue #520 appointment scope; AC4; P01-T01; P02-T02; P03-T01/P03-T03.
* Evidence: #520 says "A person or the resident can always cancel." The plan specifies only own-booking cancellation. The details similarly say "cancel only own booking"; the visible human route is described as book/call help, without a way for that person to cancel the new SQLite booking.
* Concern: an officer cannot be assumed to have authority or tooling over this newly introduced agenda. A generic contact instruction alone does not demonstrate assisted cancellation, particularly after a resident loses the session.
* Impact: a persistent local booking can remain reserved with no defined assisted release mechanism, and AC4 could be reported as satisfied on resident-only evidence.
* Smallest useful change: define one bounded, explicit synthetic operator-assisted cancellation procedure for the same agenda, without adding a staff portal or reusing works approval. State the required booking reference/verification, authorization boundary and resident-visible manual instructions. If person-assisted cancellation is deliberately deferred, mark that portion of #520 unmet rather than claiming full cancellation coverage.
* Action owner: planning parent, with implementation owner responsible for the local operator procedure.
* Exact resolving evidence: P01-T01/P02-T02 identify the assisted procedure and resident instructions; P03-T03 documents its actual local command/workflow; P03-T01 covers resident and authorized assisted cancellation, unauthorized refusal, repeated cancellation and correct inventory release. Acceptance evidence explicitly distinguishes both routes.
* Decision route: direct planner correction within the requested demonstrator. A new live staff identity/service integration would be a significant expansion, but is not required or recommended.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Synthetic callback limitations are not required in the resident booking states or acceptance claims

* Related IDs: callback scope decision; C4/C5; AC2/AC4; P02-T02; P03-T03.
* Evidence: the executive summary and README task call this a local synthetic callback agenda and reject works authority. P02-T02 nevertheless requires generic requested/proposed/booked messages without explicitly requiring the callback-only, synthetic/no-live-service qualification in those states. The showcase projection contains neither actual appointment history nor works-consent records.
* Concern: correct local persistence can still be presented as a real officer appointment or as evidence that the assistant knows all the resident's appointments/consents. "Booked" alone does not explain the authority of this new data source.
* Impact: the implementation could pass the planned booking checks while misleading the resident or PR reviewer about delivery of #520 and about whether anyone will actually call.
* Smallest useful change: require plain-language synthetic callback-only/no-live-contact wording at proposal, confirmation and booking receipt, plus unavailable/cancel/manual states as applicable. Identify local callback records separately from unavailable operational appointments and unknown works consent. Add a scoped acceptance/PR matrix: local search/booking demonstrated; operational connector, live officer service, absent record types and unverified regulatory currentness not established. Do not equate callback confirmation with works consent or legal compliance.
* Action owner: planning parent, then implementation/documentation owner.
* Exact resolving evidence: revised P02-T02 and AC4 require visible qualified receipts; browser assertions cover the proposal and booked views with no promised live contact; P03-T03 requires README and PR Refs #520 to reproduce the acceptance limitations and preserve pending human/AT/#164 gates.
* Decision route: direct planner correction. The bounded callback choice itself is compatible with a synthetic demonstration. Claiming a live agenda or works booking instead would require a significant user decision and new evidence, not wording alone.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: First-suitable ordering and time-zone semantics are not defined

* Related IDs: first suitable 1..3 free slots; AC4; P01-T01; P02-T02; P03-T01.
* Evidence: the plan says future slots filtered by earliest date and morning/afternoon/any, up to three; the details mention first three and Intl display. Neither defines the ordering key, filtering/display time zone or treatment of offsets and date boundaries.
* Concern: three free rows are not necessarily the first suitable slots. Browser-local formatting can disagree with server-local filtering about the date or morning/afternoon; a slot can also cease to be future between proposal and confirmation.
* Impact: residents can confirm a different local time than intended, receive non-earliest results, or book a past slot despite a valid offer token.
* Smallest useful change: define aware stored instants, deterministic ascending ordering with a tie-breaker, a single explicit resident-facing demo time zone used for filters and display, and fresh future/free checks at confirmation. Use the same rule for chat and manual controls; do not infer household suitability.
* Action owner: planning parent; agenda/UI implementation owner.
* Exact resolving evidence: P01-T01/P02-T02 specify the shared time/order contract; P03-T01 names unsorted seed, 0/1/2/3/>3 matches, date and morning/afternoon boundaries, differing browser zone, DST-offset display and slot-becomes-past confirmation fixtures. The future gate remains distinct from token expiry.
* Decision route: direct planner correction. An explicit UK demo zone is an implementation assumption to document, not a request for a new scheduling platform.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Medium]: Viewport tests do not cover the baseline's text-resize and zoom requirements

* Related IDs: Fluent/WCAG/content requirement; AC1/AC6; P02-T01/P02-T02; P03-T02.
* Evidence: docs/reference/research/ux/wcag-conformance-baseline.md names 200% text resizing and 400% zoom where applicable, alongside 320/390/1280 CSS-pixel viewports. P03-T02 names only those widths, reduced motion, keyboard and session/error states.
* Concern: narrow-width tests and axe do not establish that enlarged text preserves the floating window, confirmation/cancel controls, manual path, focus visibility and access to background content.
* Impact: a persistent bottom-right control can obscure or clip essential actions for residents who enlarge text even when ordinary-width checks pass.
* Smallest useful change: add a bounded local rendered-browser text-resize/zoom check for the launcher, open chat and appointment form/receipt, including keyboard access and no loss/obscuring of focused controls. Describe the method and its limits rather than treating device scale as text resizing. Keep human and AT acceptance Not run.
* Action owner: planning parent; browser-check implementation owner.
* Exact resolving evidence: P03-T02/AC1 explicitly require the two baseline conditions; the existing browser harness records the effective CSS viewport/text sizing, assertions and retained evidence for readable/reachable controls and focus. No second harness or framework change is required.
* Decision route: direct planner correction.

<!-- rpi:critique id=PC-006 -->
### PC-006 [High]: The independent exact-head assessment is mentioned but not placed after receipt verification

* Related IDs: full ordered RPI; P03-T03/P03-T04; complete gate/publication requirement.
* Evidence: P03-T03 schedules the independent Review before commit. P03-T04 then says verify "immediately before push/independent exact-head assessment", but assigns no distinct post-gate assessment step, expected result or stop condition. src/README.md distinguishes the original Review from exact-head verification/independent assessment and invalidates receipts on later commit, base or relevant input changes.
* Concern: the pre-commit Review cannot by itself attest to the committed, fully gated HEAD. The slash wording can permit pushing before independent exact-head assessment, and the task lacks an explicit fresh fetch before final verification.
* Impact: one push/PR could publish a different or insufficiently assessed candidate despite a complete receipt existing for an earlier boundary.
* Smallest useful change: explicitly order original independent Review and correction/disposition, commit implementation plus dated original evidence, capture fetched reviewed-main SHA, complete --all gate under nonblocking admission to a new external directory, fetch main again, verify the external full receipt against current origin/main and exact HEAD, obtain independent exact-head assessment, then verify as necessary immediately before push and create the Refs #520 PR. State how any assessment requiring a correction blocks push and invalidates the old receipt; preserve original adverse outcomes. Do not commit the authoritative receipt or require a new commit solely to record the final external assessment.
* Action owner: planning parent and publication coordinator.
* Exact resolving evidence: P03-T04 names the post-gate assessment owner, its exact commit/base/receipt inputs and acceptable outcome, the second fetch, and mandatory stop/rerun conditions for changed HEAD/base/dirty or relevant tool/image inputs. Final external evidence must bind the same HEAD/base as the verified receipt and pushed branch. Busy lock or missing SQL/browser/scanner prerequisites must stop publication without queueing, skips or cloud fallback.
* Decision route: direct planner correction. No permission to bypass or weaken gates is implied; a correction/reassessment is not a request for another plan critique.

## Strengths and Residual Risk

* Read-only SQL and works-confirmation authority are correctly kept separate from callback inventory. Persistent seeded free slots and transactional reservations can be genuine local agenda behavior, not invented suggestions.
* Existing fixed-topic Azure/provider boundaries, host-owned text, usage controls and labelled rules fallback are retained. The plan does not authorize actual paid calls or satisfy outstanding #164 enablement/human-effectiveness gates.
* Own-case reauthorization, strict schemas, CSRF/same-origin checks, no-store, expiring case-bound proposals, delayed-response isolation and no chat browser storage are appropriate safeguards.
* Shared launcher placement, anonymous help, optional AI, an independent manual path and human/AT acceptance limitations are explicit.
* Regulatory explanations may be demonstrated using the dated local regulatory standard with the unverified-currentness warning. The recorded 404 is a limitation, not permission to claim "current rules" or satisfaction of a duty. No legal conclusion or operational rule activation is accepted.
* Local callbacks cannot guarantee an officer, a works appointment, adjustments or a response time. Generic human contact guidance is a manual handoff, not proof that a safety report was sent. Keep that distinction visible, including when chat/agenda is unavailable.
* The supplied plan does not establish approved production wording, full regulatory coverage, live identity/representative workflows, operational scheduling or whole-product accessibility. Those remain outside this candidate; no additional framework or provider is recommended.

## Questions or Blocking Evidence Gaps

* No decision-critical user question is required for the scoped synthetic candidate. All six findings have a direct planner route under existing direction.
* If the parent instead intends whole-issue/live-service acceptance, a real appointment/consent source, currentness evidence and appropriate human approvals are missing. That is a significant scope/authority decision; do not silently make it.

## Limitations

* This is one plan critique, not an implementation review. No source was changed, no test was run and no live model, Azure, SQL service, private dataset or secret was accessed.
* Evidence inspection was bounded to the supplied artifacts, named dependencies and evidence pointers. No open-ended research, official-source refresh or fresh complete web-guidelines review was claimed.
* The research's successful-read assertions and future validations are not independently observed test passes. Source inspection corroborates the legacy route and read-only projection boundaries, not all proposed runtime behavior.
* The three primary inputs and pre-existing state remain unchanged. Only this critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: extend the consent contract to retained personal-topic requests, then resolve PC-002 through PC-006 directly in the plan/details and record their dispositions.
* User response required: no for the bounded synthetic callback candidate.
* Do not request another plan critique. Finalize the corrected planning handoff while preserving this original Complete / Revise outcome.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/resident-chat-520-research.md](.copilot-tracking/research/2026-10-28/resident-chat-520-research.md) | Supplied focused research and evidence pointers. |
| [.copilot-tracking/plans/2026-10-28/resident-chat-520-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-520-plan.md) | Assessed final-candidate plan, unchanged. |
| [.copilot-tracking/details/2026-10-28/resident-chat-520-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-520-phase-details.md) | Assessed task contracts and dependencies, unchanged. |
| [.copilot-tracking/plans/2026-10-28/resident-chat-520-critique.md](.copilot-tracking/plans/2026-10-28/resident-chat-520-critique.md) | Original single-pass Complete / Revise critique. |

## Next Steps

The active planning parent should resolve PC-001 through PC-006 directly, record exact dispositions and finalize without another critique. No user action is required unless the parent seeks live-service or works-booking scope beyond the bounded synthetic callback demonstration. Implementation and heavy validation were not started by this critique.
