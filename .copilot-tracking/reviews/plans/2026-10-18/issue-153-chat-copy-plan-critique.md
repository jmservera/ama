<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-153-chat-copy

## Metadata

* Task ID: 153
* Task slug: issue-153-chat-copy
* Critique date: 2026-10-18
* Plan: .copilot-tracking/plans/2026-10-18/issue-153-chat-copy-plan.md
* Phase details: .copilot-tracking/details/2026-10-18/issue-153-chat-copy-phase-details.md
* Research: .copilot-tracking/research/2026-10-18/issue-153-chat-copy-research.md
* Critique execution status: Complete
* Verified branch: fix/chat-copy-audit-153
* Verified exact base and current HEAD: 2ca6d1c48bb95b65e6c349fe508e99c00a74efbe
* This is the one independent final-candidate critique. No implementation or repeat critique was performed.

## Inputs and Criterion Boundary

The full three canonical caller artifacts were read. Source inspection covered
src/api/tests/test_content_standard.py, src/api/src/zava_forward/api/web/chat.js,
the relevant app.js and assistants.js rendering paths,
src/api/checks/regulatory_ux_check.py,
src/api/tests/test_regulatory_ux_check.py,
src/api/tests/test_chat_panel.py,
src/api/tests/test_regulatory_chat_api.py,
src/core/tests/regulatory_fixture.py,
docs/reference/research/ux/content-standard.md, the relevant component-guide
commands, src/api/pyproject.toml and .github/workflows/src-ci.yml.
Repository context was read from the original case study, the addendum's
exercise-baseline sections, the KB index and owner memory.

The criterion is implementation credibility for this bounded partial #153
delivery, not whole-issue acceptance, resident approval, operational readiness
or a redesign. Assessment includes all three phases, locked test ownership,
the four chat literals and three coupled time labels, the six vocabulary
families, raw technical and dynamic-content exclusions, mutation proof,
actual local Chromium, immutable adverse records, correction limits and
publication. The owner's ordered-loop authorization resolves phase prompting;
no new authorization question is introduced.

Existing untracked canonical planning/research/state artifacts were present.
They were left unchanged. No private datasets, support files, environment
secrets, external inference, Azure or production resources were accessed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| C1-C2; P01-T01; six vocabulary families | Covered | Extend the existing seven-target lexical audit with snapshot/envelope singular/plural; retain gate/hold/provenance/trace coverage. No parser or new framework is required. |
| C3-C4; P01-T01; seven application-owned literals | Covered | Four chat strings and three app time labels are named. Recorded/as-of wording must not change timestamps or suggest currentness. |
| C3-C5; source/user/model/identifier boundary | Partial | Exclusions and no dynamic rewrite are explicit, but the plan makes the adversarial source-quote proof conditional; PC-002. |
| P01-T01; test ownership lock and mutation | Covered | Existing four unit methods stay; no removals; at most four additions in test_content_standard.py; existing browser owner only. In-memory restoration of each observed chat string must fail the actual guard. |
| C2-C3; safety semantics and AI boundaries | Covered | Authorised-human restart decision, panel inability to restart, independent hazard service, exact AI label and proposal-only/manual routes are retained. No new authority decision is needed. |
| C6; P02-T01; actual local Chromium | Partial | Existing harness really launches Chromium against loopback HTTP/SQLite and blocks inference/external browser resources. Its inherited workspace constraint needs an explicit execution control; PC-003. |
| P01-T02; public KB scope/history | Covered | Existing standard/glossary extended, index updated, log append-only, named human review and comprehension gaps remain unmet. No issue criteria are checked off. |
| P02-T01; candidate freeze | Covered | Exact tree plus SHA-256 manifest before original Review; public documentation remains unchanged afterward unless a separate source-correction receipt is necessary. |
| P03-T01; independent original Review and corrections | Covered | One fresh original Review, immutable adverse verdict and critique, at most two separate correction receipts; no repeated independent pass. |
| P03-T02; validation/publication disposition | Partial | Branch/base/head and restricted PR operations are explicit, but transition from adverse or incomplete evidence to publication is not fail-closed; PC-001. |
| SQL/Docker, human acceptance and external limits | Covered | SQL parity correctly inapplicable to a string-only change; Docker availability reported honestly; human/WCAG/live gates not promoted to acceptance. |

## Verdict

* Verdict: Revise
* Execution: Complete
* Severity summary: 0 Critical, 0 High, 3 Medium, 0 Low.
* Rationale: The copy approach and safety interpretation are credible. Three
  concrete execution/evidence gaps should be corrected directly before
  implementation. None requires changing the agreed slice or obtaining a
  significant or divergent owner decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Define the disposition gate before publication

* Related IDs: acceptance criteria; P02-T01; P03-T01; P03-T02.
* Evidence: The plan accepts checks that "pass or explicitly report actual
  failures." Phase details make P03-T02 depend on "Review/corrections," but do
  not state what happens when a required scoped check is unavailable/failing,
  a Review finding remains unresolved, or two correction receipts are
  exhausted. Recording the result is not the same as resolving its impact.
* Concern: An implementer can satisfy the written sequence by reporting an
  adverse result and proceeding to ordinary publication without an explicit
  disposition. The plan does correctly prohibit rewriting the original
  Review or self-awarding an independent pass; preserve those protections.
* Impact: The PR could be presented as a completed validated slice despite an
  unresolved scoped defect or missing required Chromium evidence.
* Smallest useful change: Add an explicit transition rule: implementation-caused
  scoped failures and unresolved actionable scoped findings prevent a
  ready/validated publication claim; correct within the two-receipt limit or
  stop and return the exact unresolved evidence to the coordinator. Distinguish
  those failures from demonstrated inherited failures, optional axe/Docker
  unavailability and intentionally unmet human/whole-issue gates. If a
  blocked/draft evidence handoff is published, label it unaccepted and retain
  the unresolved items; do not silently treat publication as passing. Stop
  immediately for a newly discovered semantic/authority choice.
* Action owner: Planning parent.
* Exact resolving evidence: P02/P03 exit criteria explicitly distinguish
  validated publication from blocked/unaccepted handoff, state the
  correction-budget exhaustion outcome, and preserve the original adverse
  verdict alongside any separate correction evidence. The eventual changes
  record and PR must use that same disposition.
* Decision route: Direct planner correction. No owner response is needed to
  preserve honest status or the already specified authority boundaries.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Make the prohibited-word source-preservation canary mandatory

* Related IDs: C3-C5; P01-T01; test ownership lock; exact visible-text boundary.
* Evidence: The plan's browser-owner paragraph requires a synthetic source
  quote containing prohibited words only "if supported by the fixture."
  Phase details instead say the harness proves original source text.
  src/core/tests/regulatory_fixture.py defines source(..., text=QUOTE);
  src/api/checks/regulatory_ux_check.py already renders a real cited answer
  and restores it after reload. Its existing source assertion checks only
  "Synthetic hazard reports go to a human reviewer," not an exact
  prohibited-word canary.
* Concern: The conditional clause permits the differentiating boundary proof
  to be omitted even though source text is controllable locally. An ordinary
  quote without banned vocabulary cannot show that application-label banning
  leaves banned words in quoted evidence untouched.
* Impact: A blanket visible-text ban or source sanitization could appear to
  satisfy the copy audit while corrupting evidence, or a reviewer could
  receive only non-adversarial preservation evidence.
* Smallest useful change: Remove the conditional clause. Require a
  harness-local constructed quote containing all six term families and assert
  its complete exact text in the rendered source block before and after
  history restoration. Seed it through a consistent synthetic source/version
  fixture; do not edit shared canonical source fixtures or introduce a
  provider call. Keep the canary assertion scoped to quoted content, not a
  page-wide absence test. Use the already locked identifier-exception method
  to prove a permitted identifier/raw-payload token does not exempt an
  adjacent application-owned bad label on the same line.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 and its locked test contract unconditionally
  name the exact source canary and pre/post-restore equality assertions.
  Subsequent Chromium evidence shows those assertions passed against the
  actual local app; the four-method unit budget includes the mixed
  exception/visible-label negative case. Production dynamic source, user,
  model, fact and identifier expressions remain unchanged.
* Decision route: Direct planner correction; the owner already prohibited
  rewriting these content classes.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Pin workspace-local temporary storage for existing validation fixtures

* Related IDs: C6; P02-T01; local-only and no-temporary-directory constraints.
* Evidence: Phase details prescribe the existing harness and its teardown but
  no workspace-local temporary-storage configuration.
  src/api/tests/test_regulatory_chat_api.py:29 uses
  tempfile.TemporaryDirectory() with no directory argument, inherited by
  src/api/checks/regulatory_ux_check.py through RegulatoryApi.setUp().
  src/api/tests/test_regulatory_ux_check.py also uses TemporaryDirectory()
  without a location. The supplied execution constraint forbids file
  operations in /tmp and /var/tmp; several historical component-guide example
  commands explicitly use /tmp and cannot be copied as written.
* Concern: An otherwise compliant real-app or focused-test invocation can
  create synthetic databases, blobs or axe-test files outside the permitted
  workspace before any browser assertion runs.
* Impact: Validation either violates the execution boundary or fails for
  infrastructure reasons, leaving required local Chromium proof incomplete.
* Smallest useful change: Specify a task-local scratch/cache directory under
  the worktree and set TMPDIR, TMP and TEMP for fresh validation processes,
  including the harness/fixture and Chromium launch. Keep any axe input,
  generated JSON, browser artifacts and output paths in the worktree as
  well. Record the effective temporary-directory resolution, clean up scratch
  data, and exclude it from the commit while retaining intended changes/
  evidence. No shared fixture or production-code change is needed. Use the
  actual workflow's separate isolated lint/format commands for the changed
  browser harness, since ordinary API Ruff settings exempt checks/*.py.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 contains concrete workspace-local
  environment/output instructions and the isolated harness check commands.
  Subsequent command receipts demonstrate that the fresh Python process
  resolves tempfile.gettempdir() inside the worktree, actual Chromium ran,
  and no scratch files were staged.
* Decision route: Direct planner correction. No new spending, toolchain or
  fixture-ownership decision is required.

## Strengths and Residual Risk

* The approved safety glossary is used instead of finance "pause payment"
  wording. Retrofit restart and hazard-service closure remain independent;
  completion does not become safety assurance.
* The production scope is string values only. Source quotations, user/model
  replies, facts, stored keys and raw technical JSON are distinct from
  application-owned labels even when their words appear visibly.
* The lexical scanner is correctly described as conservative regression
  evidence, not a JS visibility parser or a universal semantic guarantee.
  Seven named audit targets, six vocabulary families, narrow exceptions and
  four in-memory chat mutations form a proportionate bounded contract.
* The existing real-app harness is the correct browser owner. It already
  covers roles, unknown sources, source changes, retained risk, disabled chat,
  supplier denial, keyboard operation and reflow; extend rather than replace it.
* The exact AI label remains "AI suggestion, not approved"; manual workflow,
  meaningful human decisions and proposal-only operation are not relaxed.
* Named human resident-wording review and comprehension remain absent and
  explicitly unmet. This is an accepted limitation of synthetic engineering
  delivery, not permission for resident use.
* No redesign, backend/schema migration, production SQL parity or whole-issue
  acceptance is required by this critique.

## Questions or Blocking Evidence Gaps

None requiring an owner response. The three findings are planner-owned
corrections. A material new semantic or authority conflict during implementation
must still stop for human resolution; the critique does not pre-authorize one.

## Limitations

This assesses a pre-implementation plan, not implemented behavior or fresh
test results. No tests, mutations, browser run or image build were executed
for the critique. Current Web Interface Guidelines were not re-fetched:
this was not a changed-web-file UI review, and the supplied W1 retrieval is
research evidence rather than a new complete review. The single original
implementation Review must perform the planned fresh retrieval. Historical
component results and supplied dependency status were not promoted into new
execution or acceptance claims.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Correct the publication disposition, mandatory canary
  and workspace-local validation instructions in the canonical plan/details;
  record dispositions without editing this completed critique.
* User response required: No.
* Critique stop: This one complete finding set closes the independent
  critique. Do not repeat it after planner corrections.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue-153-chat-copy-research.md](.copilot-tracking/research/2026-10-18/issue-153-chat-copy-research.md) | Supplied bounded research and evidence log |
| [.copilot-tracking/plans/2026-10-18/issue-153-chat-copy-plan.md](.copilot-tracking/plans/2026-10-18/issue-153-chat-copy-plan.md) | Assessed final-candidate plan, unchanged by critique |
| [.copilot-tracking/details/2026-10-18/issue-153-chat-copy-phase-details.md](.copilot-tracking/details/2026-10-18/issue-153-chat-copy-phase-details.md) | Assessed execution details, unchanged by critique |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-153-chat-copy-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-153-chat-copy-plan-critique.md) | Immutable original independent critique |

## Next Steps

The active planning parent should directly disposition PC-001 through PC-003,
then continue the owner-authorized ordered loop once its gates are satisfied.
No user action or additional critique is required. This critique performs no
implementation or publication.
