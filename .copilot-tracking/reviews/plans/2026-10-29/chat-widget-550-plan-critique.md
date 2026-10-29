<!-- markdownlint-disable-file -->
# RPI Plan Critique: Shared chat widget

## Metadata

* Task ID: 550; slug: chat-widget-550.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-widget-550-phase-details.md
* Critique execution status: Complete.
* Assessment: exactly one independent final-candidate critique; one complete actionable finding set.

## Inputs and Criterion Boundary

* Caller requirements: one shared employee/resident widget, persistent session-local thread, pinned composer, Enter/Shift+Enter, bounded skills selector, disabled attach/voice reasons, thin truthful labels, collapsed sources, explicit resident record consent, honest unsupported-question handoff, 200 ms loading, visible errors, keyboard semantics and reduced motion. Preserve APIs and #503/#525/#541 boundaries.
* Primary inputs: .copilot-tracking/plans/2026-10-29/chat-widget-550-plan.md; .copilot-tracking/details/2026-10-29/chat-widget-550-phase-details.md; .copilot-tracking/research/2026-10-29/chat-widget-550-research.md.
* Issue #550 title/body were read through the read-only GitHub CLI. Its nine acceptance criteria are mapped below in their published order. No new external research was performed.
* Baseline inspected: 9b74ac8d, merged #503; branch feat/chat-widget-550 tracks origin/main. Supplied planning/research/state files were already untracked and were not altered.
* Relevant code evidence: src/api/src/zava_forward/api/web/chat.js; src/api/src/zava_forward/api/web/app.js; src/api/src/zava_forward/api/web/index.html; src/api/src/zava_forward/api/server.py; src/api/src/zava_forward/api/resident_demo/app.py; src/api/src/zava_forward/api/resident_demo/chat.py; src/api/src/zava_forward/api/resident_demo/web/assistant.js; src/api/src/zava_forward/api/resident_demo/web/demo.js.
* Validation evidence inspected: src/api/checks/employee_chat_browser_check.py; src/api/checks/resident_assistant_browser_check.py, lines 1-300; src/api/tests/test_resident_chat_api.py, lines 1-300; src/api/pyproject.toml; .github/workflows/src-ci.yml, lines 65-115.
* Repository context: original case study, addendum opening sections, reference index and owner memory. No regulatory interpretation or changes were needed.
* Decisions assessed: native dependency-free shared factory; separate API/consent adapters; no cross-identity or browser-storage persistence; conservative resident routing; manual callback action; no new model authority; synthetic local validation; no Azure, push, publication or rubric edits.
* Assessment boundary: implementation readiness, lifecycle risks and exact acceptance coverage of this candidate. This is not implementation Review, a fresh web-guidelines audit, executed test evidence, human accessibility acceptance or authorization to publish.

## Coverage Assessment

Covered means an actionable approach is present, not that implementation or acceptance has passed. Partial identifies a substantive precision gap in the planned implementation or proof.

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| AC-1: shared component, bottom-right icon launcher and popup | Partial | P01 specifies identical JS/CSS bytes and both mounts; the existing employee dependency recovery/readiness path is not accounted for. PC-002. |
| AC-2: persistent scrolling thread, newest-bottom, pinned input, remains open | Partial | Session-local retention and explicit callback action are appropriate. Pending-close abort/reopen recovery and exact geometric proof need definition. PC-001, PC-003. |
| AC-3: Enter, Shift+Enter and send button | Covered | P01 specifies textarea, native form/send and IME guard; P03 includes keyboard assertions. |
| AC-4: compact active employee agent/skill selector | Covered | General plus five API-provided employee skills, resident-only assistant, and input-area select are explicit. Preserve selected skill with the retained context. |
| AC-5: attach/voice present or disabled with reason | Covered | Both controls and visible unsupported-capability explanations are explicit; no unsupported capability is promised. |
| AC-6: thin truthful label and collapsed sources | Covered | Adapter-owned truthful AI/rules distinction, native details and text-only rendering are specified. Research explicitly rejects relabelling rules as AI. |
| AC-7: resident consent before record use | Covered | P01 prevents requests from open/consent alone, clears on withdrawal and retains existing server consent/session checks. P03 checks request counts; pending-turn fencing needs the PC-001 matrix. |
| AC-8: rat/unrelated question not home summary | Covered | P02 targets the actual broad home-token route, explicit supported home intents, unknown default, HTTP regression, no model invocation and hazard precedence. Existing incorrect policy/home expectations are explicitly eligible for correction. |
| AC-9: 200 ms loading, errors, keyboard/screen-reader semantics, reduced motion | Partial | Named nonmodal dialog/log, focus return, Escape and reduced-motion behavior are explicit. Timing, cleanup and no-trap proof are not yet concrete enough. PC-001, PC-003. |
| C1-C3, P01-T01, P02-T01: component fit, routing, resident authority | Covered | Actual DOM/API code supports the proposed architecture without endpoint changes or raw-text-to-model forwarding. |
| C4, P01-T01, P03-T01: late-result and access boundaries | Partial | Existing employee checks distinguish transport abort from successfully fulfilled obsolete promises. Candidate names those guarantees but leaves new retained-instance recovery ambiguous. PC-001. |
| C5, P03-T01: local validation | Covered | Existing unittest, ruff, mypy, Node syntax and actual local browser checks are selected. Tests/checks remain outside the package. Existing harness changes are constrained against weakened boundary assertions. |
| P03-T02: documentation, independent Review, commit and stop | Covered | Session-only limits, privacy-safe identity, original evidence retention, one independent Review and no push are explicit. An adverse Review must remain adverse; a commit is not acceptance. |
| W1-W4: requirements, web guidance, label/source rationale | Covered within supplied evidence | Research records source retrieval and limits. Source contents were not freshly fetched during this plan-only critique. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: scope, authority boundaries and the resident routing fix are credible. Before implementation, the planner should close the retained-instance lifecycle contract, integrate the new dependency with existing employee startup recovery, and make the acceptance assertions falsifiable. These are direct planner corrections, not reasons to reopen the owner's product decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Define pending-close recovery and turn-scoped cleanup for retained instances

* Related IDs: AC-2, AC-7, AC-9, C4, P01-T01, P03-T01.
* Evidence: the plan's Functional Requirements allow pending employee close to abort while settled conversation persists. Phase details say to invalidate obsolete results and clear timers on finish/disposal, but do not distinguish hiding, cancelling a turn and disposing a context. src/api/src/zava_forward/api/web/chat.js currently creates a fresh controller, skills load and thread ID inside each open and removes the entire dialog on close. src/api/checks/employee_chat_browser_check.py explicitly forces successful obsolete skills/thread/ask promises to settle and checks DOM, focus and downstream ask suppression. Resident assistant.js uses a generation guard when consent/session changes.
* Concern: the old abort-and-destroy implementation cannot simply become abort-and-hide. Closing during initial skills load can leave a retained widget permanently disabled on reopen unless setup is restarted. Closing during thread creation can admit an obsolete thread or start an ask after reopening unless the operation has its own identity. Similarly, an old catch/finally or loading timer can clear a newer turn's busy state, focus a hidden widget, or mutate the post-withdrawal conversation even when reply insertion is guarded. The candidate does not yet choose the recovery behavior or require these distinct continuations to be tested.
* Impact: a core persistence change can regress usability and the merged stale-result/consent isolation guarantees. This is a risk in the proposed refactor, not a claim that the current generation guards are defective.
* Smallest useful change: add a small lifecycle table defining hide, turn cancellation, reopen and context disposal. Specify retained settled history/draft/skill/thread, fresh controller or operation generation on retry, skills initialization recovery, guarded success/catch/finally/timer effects and no focus movement while hidden or obsolete. Include resident withdrawal followed by re-consent/new send, not only withdrawal followed by silence.
* Action owner: planning parent, revising P01-T01 and P03-T01.
* Exact resolving evidence: phase details name the expected state and recovery for pending skills/thread/ask across employee close/reopen and route/session/access disposal; resident pending answer across withdrawal, re-consent and session replacement; browser checks settle obsolete success and rejection independently of abort and prove no old log/status/draft/focus/busy/timer mutation or obsolete follow-on request. The replacement turn must remain usable and complete normally.
* Decision route: direct planner correction. Owner direction already resolves retention scope and disposal boundaries; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Integrate the shared script into employee dependency readiness and failure handling

* Related IDs: AC-1, AC-9, P01-T01, P03-T01.
* Evidence: P01 names both entry points and resident static allowlisting, but not employee workspace dependency readiness. src/api/src/zava_forward/api/web/app.js:197-266 implements bounded script retry and checks chat.js readiness using chatCasePanel and employeeChat. The route subsequently calls employeeChat.install. The proposed chat-widget.js introduces another runtime prerequisite. Existing dependency harnesses include src/api/checks/workspace_scripts_browser_check.py and src/api/checks/loading_briefing_browser_check.py.
* Concern: adding a script tag is sufficient for the happy path, but existing readiness checks can still report chat ready when only the adapter globals exist and the shared factory failed to load. Retrying chat.js without its prerequisite can also evaluate the adapter in the wrong order. The plan does not assign this dependency integration or its failure validation.
* Impact: a missing/slow shared asset can produce an uncaught error or unusable employee workspace/chat rather than the established handled loading/error path. Sharing the component should not weaken startup resilience or force changes to unrelated workflow authority.
* Smallest useful change: include app.js dependency/readiness integration in P01. Define the shared factory's readiness check and prerequisite-before-adapter order, preserving bounded retry and avoiding duplicate evaluation of lexical declarations. Define handled failure behavior, whether integrated recovery or an explicit chat-unavailable/manual-workflow state.
* Action owner: planning parent, revising P01-T01 and P03-T01.
* Exact resolving evidence: the revised task names app.js and a bounded browser scenario for blocked shared asset, successful recovery and exhaustion. Expected assertions: no uncaught ReferenceError/redeclaration error, truthful visible feedback, no retry-budget reset on navigation and ordinary authorized workflows still usable. Include the relevant existing startup harness in the validation selector.
* Decision route: direct planner correction; no new feature or user choice is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Replace umbrella browser claims with observable timing, layout and keyboard assertions

* Related IDs: AC-2, AC-3, AC-5, AC-6, AC-9, P03-T01.
* Evidence: the plan says all nine criteria map to browser assertions; phase details currently say the harness checks dimensions, delayed/errors, focus/Enter/Shift+Enter and reset boundaries. The existing employee harness checks horizontal overflow but not a pinned composer and deliberately asserts modal Tab containment; that containment expectation must change for the new nonmodal design. Neither supplied task specifies before/after timing observations or the precise pinned-composer/newest-bottom assertions.
* Concern: a delayed response test can pass with an immediate spinner, an orphan timer or loading that never appears at 200 ms. A width-only check can pass with the whole panel scrolling and the composer disappearing, reproducing the reported resident defect. Reusing the modal keyboard loop can preserve a focus trap contrary to the new nonmodal requirement. Generic mention of these categories is not an exact acceptance oracle.
* Impact: the new harness could be green while material parts of AC-2 and AC-9 remain unproven, or intentional keyboard changes could be mistaken for permission to weaken coverage.
* Smallest useful change: add a compact AC-to-assertion table to P03-T01. For loading, use a controlled clock or bounded timing observations before 200 ms and at/after the threshold, plus fast-success/error/close/disposal cleanup. For layout, overflow the thread and compare composer position/visibility while scrolling the log; verify the newest answer is reachable at the bottom and send leaves the popup open. For keyboard, prove Tab can leave the nonmodal popup, Escape returns focus, Shift+Enter inserts a newline without a request, Enter sends exactly once and composition Enter does not send. Retain positive checks for disabled reasons, collapsed details and reduced-motion static loading.
* Action owner: planning parent, revising P03-T01.
* Exact resolving evidence: phase details give those assertions and identify which existing modal assertions are replaced rather than deleted. The planned report records both applications at 320/390/1280 CSS px, held/fast/error loading cases, normal and reduced-motion modes, and the request counts for keyboard cases. Browser evidence remains engineering evidence, not actual screen-reader acceptance.
* Decision route: direct planner correction; the owner has already specified the required behavior.

## Strengths and Residual Risk

* Sharing a native factory while keeping API/session/consent logic in audience adapters is a well-supported, narrow change. Both asset trees already use native DOM and the package includes staff web assets.
* The resident home-token defect is directly evidenced. Restricting supported home intents while keeping safety first and unknown as the default is preferable to a new free-text model path.
* Explicit manual callback actions remove the current automatic chat-to-agenda transition without granting booking or works-consent authority.
* The plan correctly distinguishes rules from AI, advisory output from approval, record-use consent from works consent and browser evidence from human/live acceptance.
* Session-local persistence is explicit; reload durability is not promised. Human assistive-technology, live-site and operational acceptance remain owner activities, not automatically accepted risks or completed criteria.
* No push, Azure action, rubric edit, hosted approval or full publication-gate success is claimed or authorized.

## Questions or Blocking Evidence Gaps

* No decision-critical user question is required for these corrections.
* No additional open-ended research is needed. The supplied plan, code and issue body support a Revise decision rather than Blocked.

## Limitations

* No application, browser, linter or test execution was performed; this is a plan critique.
* Relevant code and selected harness sections were read, not the entire repository. The unprovided implementation cannot be judged correct or defective in advance.
* External guidance retrieval status is taken from the supplied research; no fresh complete web-guidelines or accessibility review is claimed.
* No files other than this requested critique artifact were written. Plan, phase details, research, existing evidence and unrelated work remain untouched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: define retained-instance hide/cancel/reopen/dispose behavior and its late-continuation matrix, then incorporate PC-002 and PC-003 into the same plan revision.
* User response required: no.
* Return this one finding set to the parent for direct disposition. Do not request another plan critique. Proceed to implementation only after the parent records compatible resolutions; later independent implementation Review remains separate.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/chat-widget-550-plan.md](.copilot-tracking/plans/2026-10-29/chat-widget-550-plan.md) | Final-candidate plan assessed, unchanged. |
| [.copilot-tracking/details/2026-10-29/chat-widget-550-phase-details.md](.copilot-tracking/details/2026-10-29/chat-widget-550-phase-details.md) | Phase details assessed, unchanged. |
| [.copilot-tracking/research/2026-10-29/chat-widget-550-research.md](.copilot-tracking/research/2026-10-29/chat-widget-550-research.md) | Supplied research and evidence boundary. |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-plan-critique.md) | This single independent critique. |

## Next Steps

Planning parent: directly resolve PC-001 through PC-003 and preserve this original outcome; finalize without another critique. No user action is required. This critique stops here without implementation or agent dispatch.
