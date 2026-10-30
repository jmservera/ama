<!-- markdownlint-disable-file -->
# RPI Plan Critique: loading-briefing-hax-531-review-fixes

## Metadata

* Task ID: 531-review-fixes-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md
* Critique execution status: Complete
* Assessment: exactly one independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: exactly four corrections, preserving the existing title
  fixtures, original RPI evidence and local-only persistence. No implementation,
  heavy suites, nested delegation or second critique is authorized here.
* Research considered: .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md,
  particularly C2-C8 and the accepted suffix-heuristic limitation.
* Source checks: the named core parser and statement-source tests; API dispatcher
  test and corresponding aiNotes implementation; workspace loader/recovery test;
  actual h(), startupFailed(), retryWorkspaceScript(), missingWorkspaceScripts();
  async-action.js; loading_briefing_browser_check.py; component validation guides
  and strict mypy configuration.
* Decisions and dependencies: preserve all owning tests with no removals, at most
  four new parser methods, one recovery method and two browser invocations;
  nonblocking heavy admission with explicit targeted fallback; independent
  original Review and local commits only.
* Assessment boundary: credibility of the planned correction and its evidence,
  not execution success, full accessibility acceptance, publication readiness or
  hosted/human approval. The existing planning inputs remain unchanged.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C2 / P01-T01: Edit currentTarget and submit retry | Covered | Existing dispatcher selects Edit without an event and retries buttons[1]; proposed actual currentTarget and retained submit address both defects without weakening its eight-outcome matrix. |
| C3 / P01-T02: punctuation and closing delimiters | Partial | Shared relocation/segmentation ending, nested closers, newline and unknown-reference assertions are appropriate; exact supplied golden examples are not recorded, PC-002. |
| C3-C4 / P01-T03: terminal versus medial Jr./Sr. | Partial | Explicit positive/negative source ownership and preserved Contact Jr./Sr. Jones fixtures constrain the heuristic appropriately; exact supplied golden examples are not recorded, PC-002. |
| C5 / P02-T01: callable helper and real recovery DOM | Covered | Guard matches bootstrap readiness; actual h()/startupFailed() coverage for absent, empty, non-callable and healthy helpers avoids the existing stubbed-renderer blind spot. |
| C6 / P02-T01: actual browser recovery | Partial | Native keyboard reload, bounded retries, no pre-readiness API reads and recovered sign-in/account behavior are specified, but injection replay safety is unresolved, PC-001. |
| Test ownership, removals and budget | Covered | Named canonical tests, no removals and bounded additions support table-driven subtests; neither finding requires increasing the budget. |
| C7-C8 / P03-T01: strict checks and source identity | Covered | Both component strict mypy configurations exist; Ruff lint/format, source-first targeted selectors, import identity recording and admitted full/browser checks are explicit. |
| P03-T01: exact validation limits | Covered | Busy lock means targeted/static checks and explicit unperformed full/browser outcomes, not an asserted broad pass. No wait, polling, cloud fallback or publication receipt is authorized. |
| P03-T02: persistence and independent Review | Covered | Authenticated repository-local noreply identity, trailer, dated evidence, independent Review and local commits are explicit; no push, az, force-push, merge or closing keywords. |
| Dependencies, decisions and residual risk | Covered | Shared parser surface is sequenced; helper work is independent; heuristic ambiguity and unavailable broad validation remain disclosed rather than converted into acceptance. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0, High 0, Medium 2, Low 0.
* Rationale: the four surgical corrections and locked test budget are credible.
  Resolve the browser injection's same-document replay contract and make the
  exact-example acceptance criteria reproducible before implementation.
  These are direct planning corrections, not requests to broaden scope.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Specify a replay-safe unready-helper browser injection

* Related IDs: C5-C6, P02-T01, P03-T01.
* Evidence: src/api/checks/loading_briefing_browser_check.py,
  helper_bootstrap_check() intercept() and terminal assertions;
  src/api/src/zava_forward/api/web/app.js, retryWorkspaceScript() and
  requireWorkspaceScripts(); src/api/src/zava_forward/api/web/async-action.js:3;
  .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md,
  P02-T01.
* Concern: the details require fulfillment with a declared AsyncAction = {}
  but do not specify safe repeated evaluation. A successfully evaluated
  unusable helper is fetched once initially and once by the loader in the same
  document. Mirroring the real helper's const declaration in both fulfilled
  responses raises a lexical redeclaration SyntaxError on retry. The current
  missing-global scenario avoids this because its response only contains a
  comment. The proposed no-pageerror criterion would then fail because of the
  new test fixture, independently of the handler-callability fix.
* Impact: the required browser regression can produce a false failure or tempt
  removal of the no-pageerror/retry assertions, obscuring actual recovery.
* Smallest useful change: pin an idempotent injected response, for example
  var AsyncAction = {}; for every intercepted evaluation, and explicitly retain
  the two-request terminal expectation, stable count after waiting, no API reads,
  no pageerrors and route removal before native reload. For a non-callable
  variant, use the same replay-safe initialization with a non-function handler.
  A successful full document reload must fetch the original healthy helper.
* Action owner: planning parent; implementation owner executes the fixture.
* Exact resolving evidence: revised P02-T01 names the replay-safe body and both
  evaluations before terminal state. Subsequent browser evidence shows the
  empty-object scenario reaches terminal recovery after exactly two helper
  requests without pageerrors or API reads, remains bounded and recovers through
  keyboard reload. If heavy admission is busy, retain that run as explicitly
  unperformed, not passed.
* Decision route: direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Record the exact supplied parser regression fixtures

* Related IDs: C3, P01-T02, P01-T03, exact-example acceptance criteria.
* Evidence: .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md
  calls three supplied parser inputs reproduced but records neither their
  literal inputs nor outputs; the plan promises exact supplied quoted and
  Jr./Sr. cases; phase details say "exact supplied sentence" without a literal
  or a specific retrievable finding pointer. The existing
  src/core/tests/test_ai_statement_sources.py contains title/abbreviation
  counterexamples, not those new regression examples.
* Concern: the supplied candidate evidence cannot identify exactly which quoted,
  Jr. and Sr. examples must produce the promised two dictionaries. Generalized
  fixtures may exercise the same apparent behavior but cannot demonstrate
  compliance with an exact-input acceptance criterion.
* Impact: implementation and independent Review can disagree over whether the
  original reproduced cases were actually fixed, especially citation placement,
  quote characters and punctuation preservation.
* Smallest useful change: add the three literal original inputs, source mapping
  and expected per-statement dictionaries to the phase details, transcribed from
  the parent's supplied review findings. Preserve the existing research and
  other original evidence. Distinguish those original goldens from the broader
  delimiter/suffix counterexample matrix; do not substitute invented examples.
* Action owner: planning parent holding the original supplied findings.
* Exact resolving evidence: P01-T02/P01-T03 contain the exact strings, source
  labels and expected text/citations/unresolved arrays; corresponding owning
  parser tests assert full dictionary equality for each literal. No additional
  test methods beyond the locked four-method budget are needed.
* Decision route: direct planner correction; no new product or user decision
  required. If the parent cannot recover the original literals, record that
  evidence gap rather than claim exact-example verification.

## Strengths and Residual Risk

* Test ownership, preservation and budget are adequate. Parameterized methods
  can cover the specified punctuation, delimiter, citation and suffix dimensions;
  source-string checks and count-only assertions are correctly rejected.
* Existing Contact Jr. Jones and Contact Sr. Jones fixtures are explicitly
  preserved. Ambiguous uppercase continuations remain an accepted conservative
  heuristic limitation, not a reason to require a new tokenizer.
* Real renderer coverage is required in addition to the loader VM harness,
  whose existing h()/show() stubs cannot prove error/reload rendering.
* Nonblocking heavy admission and targeted fallback are explicit validation
  boundaries. A blocked browser/full suite is not silently counted as success.
* The plan keeps native recovery, manual paths, human review and source-trust
  caveats intact and does not authorize unrelated visual work or publication.

## Questions or Blocking Evidence Gaps

* No unresolved user decision. PC-002 is an evidence-recording gap owned by the
  planning parent; PC-001 is a deterministic fixture-design correction.

## Limitations

* No implementation, tests, browser, heavy suites or external research were run
  during this critique. Historical reproduction claims were read, not rerun.
* The original review finding payloads were not part of the supplied candidate
  files; their exact parser literals cannot be independently reconstructed here.
* No complete UI-guideline or accessibility review is claimed; only the named
  runtime recovery behavior and planned validation were assessed.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: specify replay-safe helper injection and bounded request
  assertions, then record the original parser goldens for PC-002.
* User response required: no.
* Dispose both findings directly, preserve this original critique and continue
  the existing RPI parent without another critique pass.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md](.copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan.md) | Assessed canonical candidate; unchanged. |
| [.copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md](.copilot-tracking/details/2026-10-29/loading-briefing-hax-531-review-fixes-phase-details.md) | Assessed phase details; unchanged. |
| [.copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md](.copilot-tracking/research/2026-10-29/loading-briefing-hax-531-review-fixes-research.md) | Supplied original research; unchanged. |
| [.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-review-fixes-plan-critique.md) | Complete independent critique and complete actionable finding set. |

## Next Steps

The active planning parent corrects PC-001 and PC-002 directly and records their
disposition before implementation. No user action or repeat critique is required.
This critique stops here; it does not implement, commit or invoke another stage.
