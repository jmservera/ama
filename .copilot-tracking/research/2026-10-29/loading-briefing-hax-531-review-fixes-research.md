<!-- markdownlint-disable-file -->

# Task Research: loading-briefing-hax-531-review-fixes

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md |

## Research Brief

* What to research: four supplied Copilot findings on PR #538, refs #531:
  Edit event harness, quoted/bracketed sentence boundaries, terminal Jr./Sr.
  citation ownership, and defined-but-unready AsyncAction startup recovery.
* Why it matters: prevent false citation ownership and restore reliable error
  recovery and review-dispatch regression coverage.
* Audience or intended use: local correction implementation and independent review.
* Scope: named core/API source, their tests, browser check and directly related docs.
* Non-goals: redesign, new features, cloud use, publication, historical evidence edits.
* Criteria: reproduce supplied failures; preserve medial abbreviations, manual
  recovery and human review boundaries; run requested strict/static/unit/browser checks.
* Requested outputs: evidence-backed surgical correction plan.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which contracts fail, which existing fixtures cover them, and what negative cases prevent regressions? |
| Codebase scope | src/core, src/api, relevant tracking evidence and scenario manifests |
| External scope | Required current Web Interface Guidelines only |
| Initial internal candidate areas | ai_tasks.py, test_case_journey.py, app.js, recovery/browser tests, component guides |
| Initial external candidate areas | vercel-labs/web-interface-guidelines main/command.md |
| Research posture | focused |
| Posture provenance | Default for four named defects with supplied reproductions |
| Explicit limits / deadline | Local commits only; no push, az or force-push; nonblocking shared lock for heavy checks |
| Posture-specific completion basis | Complete three-wave coverage of named defects and their counterexamples |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | .copilot-tracking/research/2026-10-29/ |
| Known constraints / excluded sources | No private data, cloud calls, or change to original RPI evidence |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | Repository instructions | Supplied applyTo ** | Branch, src layout, typing, evidence and local gates | Selected |
| Skill | rpi-research | RPI lifecycle | Three-wave evidence and readiness | Selected |
| Skill | web-design-guidelines | app.js behavior correction | Fresh source before edits and review | Selected |
| Research specialist | hve-core-all:rpi-researcher | Registered internal research lane | Bounded independent research | Skipped: small tightly coupled trace handled inline |
| Skill | redesign-existing-projects | Visual redesign | Preserve existing design | Skipped: no styling or redesign |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit complete local RPI round, concrete fixes and validation supplied | No missing scope | New bounded automatic full-loop task, stop after local commits as requested |

## Scope and Success Criteria

* Validate all four findings on the rebased branch and retain original evidence.
* Assert exact per-statement references, including uncited statements.
* Exercise actual recovery DOM for an object-valued but unusable helper.
* Keep source in src; update manifest pins only for changed pinned files.

## Task Research Requests

* Run full Research, Plan, Implement and Review; commit dated evidence locally.
* Run mypy, Ruff lint/format in API/core, unit tests and relevant browser check.
* Full suites require flock -n /tmp/ama-rpi-heavy.lock; targeted fallback if busy.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | Four supplied review findings on existing feat/loading-briefing-hax-531 / open PR #538 | User intake | Reuse branch; no unrelated fixes |
| exclude | Push, az, force-push, closing keywords | User intake | Local-only persistence |
| add | Rebase first, strict typing and relevant browser recovery check | User intake | Pull completed cleanly before research |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | How do Edit and retry test handlers map to current DOM controls? | straightforward | H | answered |
| Q2 | How can citation normalization and segmentation share closing-delimiter handling? | depth | H | answered |
| Q3 | How can terminal suffixes split without breaking medial suffixes? | depth | H | answered |
| Q4 | How should unavailable and defined-but-unready helpers render recovery? | straightforward | H | answered |
| Q5 | Which validation, pin and publication boundaries apply? | straightforward | H | answered |

## Prior Knowledge Gate

* Existing correction state reviewed: previous 2026-10-29 correction round is
  completed/stopped; its original critique/Review remain unchanged.
* Supplied reproductions are hypotheses to verify against current source.
* Clean branch rebase completed, HEAD 81ab4a0e76e1ab86ce0d7174c630c809d8487064.
* PR #538 is OPEN, targets main and matches this workstream.

## Research Cycle Log

### Cycle 1

* Active direction controls: all intake boundaries above.
* Posture: focused; named defect coverage and counterexamples.
* Wider: read named source and harness; inventoried component validation guides,
  statement-source tests and recovery suites. Confirmed all four supplied failure
  paths exist: bare Edit invocation, punctuation-only boundary regexes, unconditional
  Jr./Sr. shielding, and object-existence-only listener wrapping.
* Wider reflection: exact fixes are local; inspect existing negative fixtures and
  browser injection mechanics before selecting shared boundary rules.
* Deeper: reproduced the exact Node harness TypeError before review dispatch;
  reproduced combined quoted statements and Jr./Sr. citation leakage. Existing
  core fixtures require "Contact Jr. Jones" and "Contact Sr. Jones" to remain
  intact. Loading browser check already injects missing helper globals, but
  never a defined unusable object. Startup recovery uses the real h() factory.
* Deeper reflection: use one closing-delimiter boundary pattern for relocation
  and splitting; distinguish suffixes using preceding name context and following
  lowercase continuation. Keep the existing medial title fixtures.
* Contrarian: existing four statement-source tests pass while supplied inputs
  fail. Title fixtures include Jr./Sr. Jones, so blindly treating every suffix
  before a capital as terminal breaks existing behavior. Preserve title use
  and lowercase medial continuations, conservatively split after a preceding
  capitalized name pair before a capitalized new claim. Cover punctuation
  followed by nested closers, both citation placements and uncited first text.
  Existing browser recovery checks missing globals and healthy scripts, never
  object-valued unready helpers. Test the actual h()/startupFailed() path rather
  than a stubbed renderer alone.
* Contrarian reflection: no new dependency or language model is warranted.
  Deterministic heuristics must state their ambiguity, not imply NLP certainty.

#### Parent Synthesis and Disposition

| Material / claim | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Edit harness and history retry are stale | C2 | accepted | Exact TypeError reproduced; use actual Edit currentTarget and submit retry |
| Quoted/bracketed end handling must be shared | C3 | accepted | Relocation and split currently disagree with closing delimiters |
| Jr./Sr. need contextual treatment | C3, C4 | accepted | Terminal reproduction fails while medial/title fixtures pass |
| Readiness must guard listener wrapping | C5, C6 | accepted | Factory otherwise throws while constructing terminal recovery |
| Add a broad sentence tokenizer | C3, C4 | rejected | Unnecessary dependency/scope; bounded conservative heuristic suffices |

#### Cycle Re-entry Evaluation

* Another cycle needed: no; all named questions answered with exact source and
  fixture contracts. Remaining validation is implementation evidence, not research.
* Readiness: Ready.

## Evidence Log

* Delegation: inline; no separate research context needed.

### Codebase Evidence

| ID | Claim / finding | Location | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | Prior round is completed/stopped with full/browser checks previously blocked | .copilot-tracking/rpi-sessions/2026-10-29/loading-briefing-hax-531-corrections-state.json:1 | read | high | Historical only, not current validation |
| C2 | Bare Edit invocation throws at currentTarget; history retry targets wrong choice | src/api/tests/test_case_journey.py:1472 | read, Node unittest | high | Exact supplied regression reproduced |
| C3 | End regexes accept punctuation only; suffix shielding merges terminal Jr./Sr. | src/core/src/zava_forward/core/ai_tasks.py:154 | read, direct parser reproduction | high | All three supplied parser inputs combine claims |
| C4 | Existing title/medial contracts must remain intact | src/core/tests/test_ai_statement_sources.py:48 | read, unittest | high | Four existing tests pass |
| C5 | h() wraps any defined AsyncAction; readiness separately requires callable handler | src/api/src/zava_forward/api/web/app.js:20 | read | high | startupFailed uses h at line 1536 |
| C6 | Existing browser injects absent globals but not defined unready helper | src/api/checks/loading_briefing_browser_check.py:66 | read | high | Extend existing synthetic loopback scenario |
| C7 | Manifest pins four unrelated fixture inputs | docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:46 | read | high | None planned for edits; no hash churn required |
| C8 | Strict checks and owned loopback browser entry points are established | src/README.md:44; src/api/README.md:83 | read | high | Requested /tmp/mv tools present; editables currently point at another worktree |

### External Evidence

| ID | Claim / finding | URL | Retrieved | Confidence |
| --- | --- | --- | --- | --- |
| W1 | Preserve native button semantics, focus and explicit recoverable errors | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | 2026-10-29 | high |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Readiness implication |
| --- | --- | --- | --- | --- |
| Q1 | Pass actual Edit event; retry submit, not index 1 | C2 | high | Ready |
| Q2 | Share punctuation-plus-closers boundary pattern | C3, C4 | high | Ready |
| Q3 | Contextual suffix exception plus positive/negative ownership fixtures | C3, C4 | high | Ready |
| Q4 | Guard callable handler; actual DOM and browser unready-object scenario | C5, C6, W1 | high | Ready |
| Q5 | Existing strict checks, source-first paths, nonblocking heavy admission | C7, C8 | high | Ready |

## Alternatives and Decision State

Select surgical existing-parser and h() corrections. Reject replacing the parser,
redesigning recovery, or accepting only a source-string assertion. Preserve all
existing title, newline, unknown-reference and readiness retry-budget behavior.

## Open Questions, Risks, and Residual Uncertainty

* Shared lock was unheld at inspection; admission is authoritative at command start.
* Requested /tmp/mv has pinned mypy/Ruff/Playwright but editables point at issue-532.
  Reinstall required current-worktree packages under the shared lock and force
  current-worktree source-first PYTHONPATH. If admission is busy, use source-first
  targeted checks and report the full/browser work unperformed.
* Name-suffix grammar remains heuristic; uppercase continuation is ambiguous.
  No semantic truth, human accessibility acceptance, hosted or publication claim.

## Planning Readiness

Ready. Research disposition: executed. Focused wider/deeper/contrarian cycle
complete; all findings linked to evidence. Self-check: no source edits during
research; original historical evidence unchanged; no unresolved planning decision.

## Sources

Code locations C1-C8 and current required guidelines W1 above.

## Continuation

Active RPI parent advances to Plan under explicit full-loop user direction.
