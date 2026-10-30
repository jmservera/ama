<!-- markdownlint-disable-file -->
# Task Research: employee-chat-dismissal-correction

| Field | Value |
| --- | --- |
| Date | 2026-10-30 |
| Researcher / agent | RPI parent, rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-30/employee-chat-dismissal-correction-research.md |

## Research Brief

* What to research: RV-001 delayed-render dismissal focus ownership and RV-002 missing full API evidence.
* Why it matters: a deliberately dismissed chat must not redirect focus or reopen; all 12 original send combinations must remain valid.
* Audience or intended use: correction-cycle planning and independent local review.
* Scope: employee app show/route lifecycle, focused/shared browser checks, API validation commands, original review.
* Non-goals: live warming, Azure, deployment, paid inference, private data, remote writes, issue closure, unrelated visual changes.
* Criteria: exact connected outside/launcher focus retained after delayed render, normal workspace focus retained when appropriate, failing-before browser assertion, complete requested local validation.
* Requested outputs: dated research, plan, critique, implementation and independent Review evidence, local Refs-only commit.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Q1 safe focus boundary; Q2 actual regression surface; Q3 required validation |
| Codebase scope | src/api and existing employee-chat-closes-on-send RPI artifacts |
| External scope | Current Web Interface Guidelines only |
| Initial internal candidate areas | app.js show/route, chat-widget.js, chat_submit_browser_check.py, chat_widget_browser_check.py, project guides |
| Initial external candidate areas | vercel-labs/web-interface-guidelines command.md |
| Research posture | focused |
| Posture provenance | Default for named review findings and bounded correction |
| Explicit limits / deadline | Local commit only; lock wait <=600 seconds; no live/Azure/credentials |
| Posture-specific completion basis | Focused scope and materiality |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No private dataset or live application |

## Extension Registry and Provenance

* Precedence: host safety, owner scope, repository guidance, research contract, domain guidance.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | Repository copilot guidance | All files | Existing topic, privacy-safe commit, preserve original evidence | Selected |
| Skill | rpi-research | Bounded correction investigation | Three ordered inline waves | Selected |
| Skill | web-design-guidelines | Changed web focus behavior | Fresh source before edits and review | Selected, source retrieved |
| Skill | redesign-existing-projects | Existing app design improvement | Visual design | Skipped: behavioral correction, no redesign |
| Research specialist | hve-core-all:rpi-researcher | Host-visible independent-lane worker | Read-only lane evidence | Skipped: one tightly coupled low-volume trace |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Owner gave findings, stages, branch, command and safety limits | Explicit full correction loop | Continue selected child loop in inherited automatic mode |

## Scope and Success Criteria

Preserve original adverse review/critique and parent state. Verify behavior using actual loopback synthetic applications, not live systems or a DOM-only proxy.

## Task Research Requests

Owner explicitly requires RV-001 red-before-green browser coverage, RV-002 full API discovery under flock -w 600, ruff check/format, mypy and browser checks, all 12 send combinations.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | RV-001 / RV-002 correction only | Owner | No unrelated UI or auth refactoring |
| exclude | Push, Azure, live warming, credentials, closing keywords | Owner | Local Refs-only delivery |
| change | Wait for shared lock up to 600 seconds | Owner | Authorized queued full-unit admission in this cycle |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How can show retain connected deliberate focus without suppressing ordinary navigation focus? | depth | H | Answered |
| Q2 | Which existing browser assertions must fail before correction? | straightforward | H | Answered |
| Q3 | Which local tools/checks supply missing package and browser evidence? | straightforward | H | Answered |

## Prior Knowledge Gate

Original Review and parent Changes/state read. HEAD 366ca4a2 matches owner direction and worktree was clean. Original review's opposite delayed-dismissal assertion is visible in current check; prior full suite remains unrun. Cross-session search found no additional matching session. Project original/addendum, reference index, memory and sector primer read; none authorizes live work.

## Research Cycle Log

### Cycle 1

Active posture: focused. All waves inline because the scope is one continuous focus lifecycle.

#### Wave 1: Wider

Original review locates a coupled implementation/test gap: show unconditionally focuses app whenever chat is no longer visible; the delayed-dismissal check asserts that wrong target. API guide documents outside focus should not redirect. Existing source tools are /tmp/mv; no installation indicated.

Reflection: prioritize exact route completion semantics, native focus connectivity and ordinary navigation counterexamples before selecting correction.

#### Wave 2: Deeper

route() updates displayedHash before asynchronous reads, so displayedHash alone cannot distinguish the previously rendered workspace. show() replaces only #app; nav, account and launcher remain outside it. Native Escape/Close return to launcher and external focus hides without cancelling requests. The focused browser already holds the real case read and captures renderFocus.

Reflection: retain a last-rendered session/path context in show(), preserving connected outside-app focus only within that context; retain existing visible-chat preservation independently.

#### Wave 3: Contrarian

Challenged unconditional connected-focus preservation: it would leave focus in persistent nav after genuine navigation. Challenged global no-focus: it loses normal workspace landing when the old focused descendant is removed. Challenged dismissal flags/events: unnecessary coupling to shared resident widget, plus never-cleared state risks. Auth resets change me reference and remove chat; successful equal rechecks preserve me reference.

Reflection: guard preservation by last-rendered authenticated session and route path (query-only refresh remains same workspace). Exclude body/document root and replaced app descendants; require target connectivity after replacement. Test real destination navigation, replaced input, removed external node, no-chat and changed-session cases as counterexamples.

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Same-context connected external/launcher preservation | C2/C3/C5/C6 | accepted | Meets RV-001 without reopening or refocusing |
| Suppress all workspace autofocus | C5 | rejected | Breaks destination/replaced-control landing |
| Shared-widget dismissal flag | C6 | rejected | Existing native focus + render context suffice |
| Full API discovery under authorized waiting lock | C4/C7 | accepted | Direct RV-002 evidence, not targeted proxy |

#### Cycle Re-entry Evaluation

No further cycle required: focused trace, examples and counterexamples covered. No material source uncertainty remains; runtime red/green proof belongs to Implement.

## Evidence Log

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Original Review reports RV-001 and RV-002 | .copilot-tracking/reviews/logs/2026-10-30/employee-chat-closes-on-send-review.md:159 | view | High | Original preserved |
| C2 | show focuses app when chat does not own focus | src/api/src/zava_forward/api/web/app.js:92 | view | High | Baseline source |
| C3 | Delayed-dismissal regression explicitly expects app focus | src/api/checks/chat_submit_browser_check.py:117 | view | High | Baseline opposite contract |
| C4 | Required full/static/browser commands exist | src/api/README.md:125; src/api/pyproject.toml:29 | view | High | Existing /tmp/mv tools found |
| C5 | route updates displayedHash before reads and resets chat on destination-path changes | src/api/src/zava_forward/api/web/app.js:283 | view | High | Preserve normal navigation landing |
| C6 | Escape/Close focus launcher; external focus hides without redirect | src/api/src/zava_forward/api/web/chat-widget.js:61; src/api/src/zava_forward/api/web/chat-widget.js:117 | view | High | No widget changes needed |
| C7 | Browser server sanitizes env, constructs data and health-checks owned loopback | src/api/checks/design_system_browser_check.py:227 | view | High | No live warming or credentials |
| C8 | Shared check invokes focused employee regression plus existing employee/resident/axe boundaries | src/api/checks/chat_widget_browser_check.py:958 | view | High | Standalone focused also covers actual resident replies |

### External Evidence

| ID | Claim / finding | Source | URL | Retrieved | Version/date | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| W1 | Native semantics and visible unobscured focus; avoid unjustified autofocus | Web Interface Guidelines | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-30 | Current retrieval | High |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Confidence | Readiness implication |
| --- | --- | --- | --- | --- |
| Q1 | Preserve connected outside-app focus only in identical rendered session/path; visible chat retains prior behavior | C2/C5/C6 | High | Ready for bounded implementation |
| Q2 | Replace opposite expectation with exact renderFocus equality after Escape, Close and external dismissal; check hidden/expanded state | C3/C6 | High | Actual browser red-before-green |
| Q3 | Existing /tmp/mv API tools and loopback checks provide requested evidence | C4/C7/C8 | High | No new tooling or live service needed |

## Alternatives and Decision State

Selected recommendation: minimal show-local last-rendered session/path context plus current native connected focus. No shared-widget/auth change. Regression extends existing focused check, still integrated in shared check. Alternatives and rejection evidence are above.

## Open Questions, Risks, and Residual Uncertainty

* No research blocker. Full-suite pass is not yet known and must be measured.
* Local browser checks cannot establish live-site or human accessibility acceptance.

## Planning Readiness

Ready. Research disposition: executed. All three waves complete inline; evidence IDs and paths self-checked. Parent next action: Plan, one independent critique, then authorized correction/validation and one new Review. Original Review remains unchanged.
