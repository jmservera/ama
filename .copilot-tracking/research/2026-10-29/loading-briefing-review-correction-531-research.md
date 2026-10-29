<!-- markdownlint-disable-file -->

# Task Research: loading-briefing-review-correction-531

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/loading-briefing-review-correction-531-research.md |

## Research Brief

* What to research: all AsyncAction consumers and page dependencies, and the complete statement_sources punctuation path.
* Why it matters: correct both Copilot findings on PR #538 without leaving sibling failures.
* Audience or intended use: correction implementation and independent review.
* Scope: src API web/scripts, core citation parser, tests, browser checks and directly related documentation.
* Non-goals: redesign, Azure, paid inference, push, merge, issue closure.
* Criteria: native helper-failure recovery on every consumer; complete cited statement objects for trailing punctuation runs; existing behavior retained.
* Requested outputs: dated full RPI evidence and local commits.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which pages depend on AsyncAction? How do all punctuation boundaries attach citations? |
| Codebase scope | src/, tools/, matching existing evidence and manifests |
| External scope | Current Web Interface Guidelines only |
| Initial internal candidate areas | app.js, law.js, async-action.js, HTML loaders, ai_tasks.py, tests and browser check |
| Initial external candidate areas | vercel-labs/web-interface-guidelines |
| Research posture | focused |
| Posture provenance | Default for named correction targets with explicit sibling audit |
| Explicit limits / deadline | No push, az or force-push; nonblocking shared lock for heavy suites |
| Posture-specific completion basis | Complete dependency and punctuation scope, regression evidence |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No private dataset; source in src/, not mvp/ |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | Repository instructions | All files | Branch, evidence, validation and retention | Selected |
| Skill | rpi-research | RPI request | Three-wave evidence | Selected |
| Skill | web-design-guidelines | Changed web code | Fresh rules for scoped edits/review | Selected |
| Research specialist | None | Small coupled audit | Inline evidence | Skipped; no independent lane warrants delegation |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision |
| --- | --- | --- | --- |
| Intake | Explicit user request supplies all scope and phase advancement | Full loop and local commits requested | Execute all four phases; stop locally |

## Scope and Success Criteria

Both named findings plus sibling dependency and punctuation cases. Confirm supplied failures against actual current source. Full object assertions, browser helper blocking, strict package checks and explicit validation gaps are required.

## Task Research Requests

Audit before source edits. Pull with rebase first. Keep the existing branch and PR; no closing keywords. Update SHA-256 pins if pinned files change.

## Direction Controls

| Control type | Direction or boundary | Source / checkpoint | Effect |
| --- | --- | --- | --- |
| narrow | Two findings and their complete sibling surfaces | User intake | No unrelated fixes |
| exclude | No push, Azure or force-push | User intake | Local-only delivery |

## Research Questions

| # | Sub-question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | All AsyncAction scripts/pages and helper failure paths? | depth | H | answered |
| Q2 | All citation punctuation boundaries and consumers? | depth | H | answered |
| Q3 | Required regressions, pins and validation commands? | straightforward | H | answered |

## Prior Knowledge Gate

* Read original case study, addendum, knowledge-base index, owner memory, sector primer and src gate guidance.
* Clean worktree; branch feat/loading-briefing-hax-531; PR #538 open against main.
* `git pull --rebase`: Already up to date.
* Supplied review findings are starting claims to verify.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline repository search found exactly two direct production consumers, app.js
and law.js, and exactly two HTML helper loaders, index.html and law.html.
The helper exports handler, run and feedback. Indirect workspace scripts use
h/api from app.js, not their own AsyncAction dependency. No other page needs
a new bootstrap. Parser ownership is core ai_tasks.py; API AI-task tests and
the briefing renderer consume its statement objects.

Reflection: law has no readiness gate; app has a gate but checks handler only.

#### Wave 2: Deeper

Read every direct helper call and bootstrap path, helper implementation, both
HTML loaders, loader tests, browser check, full parser and complete parser
tests. law binds handlers before its initial read and throws if the helper is
absent. Workspace bootstrap gates account listeners, start, routes and every
direct consumer, but a handler-only object passes while feedback/run fail.
Both citation relocation and splitting share STATEMENT_END; its single
punctuation character allows a relocation to match only the final character.

Reflection: gate each consumer's required methods before any binding/read;
reuse the punctuation pattern rather than adding a second parser.

#### Wave 3: Contrarian

Actual source reproduction confirms ellipses and ?! split into uncited text
plus cited punctuation-only objects, including closing quotes/brackets.
Unicode ellipsis instead merges adjacent statements and both citations.
Existing tests cover plain terminators, closers, newline citations, titles,
abbreviations and name/street suffixes but omit punctuation runs. No new
sentence tokenizer is justified; preserve conservative abbreviation rules.
Native reload avoids unsafe lexical helper reinjection in the standalone
viewer. Check missing, empty, null and partial/non-callable helper interfaces,
not only network failure; no service read or binding should precede readiness.

Reflection: accept complete terminator runs including Unicode ellipsis,
extend clean-text whitespace normalization for that terminator, and expand
full-object matrix coverage. Keep the existing app bounded recovery.

### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| law native terminal recovery | C1-C3 | accepted | No dependency on broken helper |
| Complete workspace interface gate | C1-C4 | accepted | Handler-only stubs otherwise pass bootstrap |
| Shared punctuation run | C5-C6 | accepted | Correct both regex consumers and Unicode sibling |
| General tokenizer or shared loader extraction | C1-C6 | rejected | Unnecessary risk and abstraction for two bounded corrections |

### Cycle Re-entry Evaluation

No material unanswered scoped question remains. One complete inline cycle
covers the requested surfaces; further broad discovery would be redundant.

## Evidence Log

| ID | Location | Evidence |
| --- | --- | --- |
| C1 | src/api/src/zava_forward/api/web/async-action.js:3 | Exports run, handler, feedback |
| C2 | src/api/src/zava_forward/api/web/law.js:22 | All five handler bindings and initial run are unguarded |
| C3 | src/api/src/zava_forward/api/web/law.html:26; src/api/src/zava_forward/api/web/index.html:41 | Only two HTML helper inclusions |
| C4 | src/api/src/zava_forward/api/web/app.js:49,227,704,709,712,1495,1523,1630 | Feedback, route filters/search, import, account and map dependencies; bootstrap gates actual work but only checks handler |
| C5 | src/core/src/zava_forward/core/ai_tasks.py:31,135,140,155,183,289 | Shared terminator, normalization, relocation, split and finish ownership |
| C6 | src/core/tests/test_ai_statement_sources.py:8; src/api/tests/test_ai_tasks.py:46 | Full-object boundary matrix and task/store integration |
| C7 | src/api/checks/loading_briefing_browser_check.py:66,503 | Existing helper failure cases apply only to app; law healthy/read-error flow exists |
| C8 | docs/reference/research/retrofit-synthetic-data/scenario-manifest.json:45 | Four pinned source paths; none is proposed for editing |
| W1 | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md | Retrieved 2026-10-29; native controls, live error text, focus, actionable recovery; repository ASCII/content rules take precedence |

## Findings Mapped to Questions and Evidence

Q1: C1-C4 establish complete consumer inventory and partial-interface sibling.
Q2: C5-C6 and direct reproduction establish exact punctuation failures.
Q3: C7-C8 and package READMEs identify the regression harness and pin boundary.

## Alternatives and Decision State

Select native law error/reload before any helper use and strengthen app readiness
to all three required methods. Select shared complete punctuation runs and
full-object matrices across before/after/uncited, whitespace and closers.
Reject helper fallback emulation and a general tokenizer as unnecessary.

## Open Questions, Risks, and Residual Uncertainty

Shared heavy-lock availability is unknown. If busy, user explicitly authorizes
targeted tests with full/browser suites reported unmet. No direct human,
hosted, live or accessibility conformance acceptance is established.

## Planning Readiness

Ready. Research disposition: executed. Explicit caller full-loop request owns
advancement to Plan. Self-check: all questions mapped, three waves completed,
complete dependency inventory and parser source read before source edits.
