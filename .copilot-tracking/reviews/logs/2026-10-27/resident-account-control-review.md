---
title: Resident account control independent Review
description: One post-implementation Review for issue 467, parent 466
ms.date: 2026-10-27
---

## Opening Review State

* Goal: independently assess the resident account control implementation for #467, parent #466.
* Scope: complete working-tree diff against feat/resident-interactive at 55c239d90dabec1e974eb60330e224c3a0fc6190, including the new resident_account_check.py and canonical RPI evidence.
* Evidence readiness: named artifacts and state directory are present; comparison and validation assessment pending.
* Acceptance basis: own canonical email after existing current-case authorisation, native top-right account disclosure, existing logout/isolation, long-content/reflow and keyboard/focus; approved focused checks replace the full local gate.
* First comparison boundary: canonical plan, details, original critique, changes and state against all changed source and checks.
* Read-only boundaries: only this review record may be written. No source/artifact correction, nested agents, second Review, SQL harness, Azure, private data, secrets, environment or real verifier inspection.
* Initial blockers: none identified.

## Execution Status

* Review execution: Complete.
* Exactly one independent Review completed on 2026-10-27; no nested agents, correction cycle or repeated Review.
* Implementation execution: P01-T01/T02/T03 complete. P02-T01 is satisfied by this record; P02-T02 remains deliberately pending with the parent. This is not a claim that publication or the whole delivery lifecycle is complete.

## Scope and Evidence

* Task: #467; parent #466; branch feat/resident-account-control.
* Research: .copilot-tracking/research/2026-10-27/resident-account-control-research.md.
* Plan: .copilot-tracking/plans/2026-10-27/resident-account-control-plan.md.
* Details: .copilot-tracking/details/2026-10-27/resident-account-control-phase-details.md.
* Original critique: .copilot-tracking/plans/2026-10-27/resident-account-control-critique.md, preserved Complete / Revise, PC-001 Medium.
* Changes: .copilot-tracking/changes/2026-10-27/resident-account-control-changes.md.
* State: .copilot-tracking/rpi-sessions/2026-10-27/resident-account-control-state.json, automatic parent context, active Review, no blockers or follow-ups.
* Complete tracked diff reviewed against origin/feat/resident-interactive at 55c239d90dabec1e974eb60330e224c3a0fc6190: src/api/README.md; src/api/checks/resident_demo_browser_check.py; src/api/src/zava_forward/api/resident_demo/app.py; src/api/src/zava_forward/api/resident_demo/web/demo.js; src/api/src/zava_forward/api/resident_demo/web/index.html; src/api/src/zava_forward/api/resident_demo/web/demo.css; src/api/tests/test_resident_demo_api.py.
* New untracked source reviewed in full: src/api/checks/resident_account_check.py. The new canonical RPI artifacts listed above were also compared; they are not silently excluded because git diff omits untracked files.
* Supporting context: docs/case_study_48_original.md; docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md; docs/reference/research/sector/housing-association-primer.md; docs/reference/research/ux/design-system.md; docs/reference/research/ux/wcag-conformance-baseline.md; docs/reference/research/ux/content-standard.md; existing employee account markup/styles and resident HTTP tests.
* Current web rules: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md, freshly retrieved in full for this Review on 2026-10-27. No retrieval failure or partial-rule limitation.
* No source, plan, critique, changes, research or state edits made by this reviewer. No SQL harness, Azure access, private datasets, secrets, environment files, real verifier files or MAX_MAPPINGS changes.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Current-state reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 | Authorised account projection and native header disclosure | Reconciled | view_for adds only canonical account.email after token verification, case lookup and existing current-row authorisation; session/login contracts unchanged. |
| P01-T01 | Interaction, privacy and focus | Reconciled | textContent rendering; Escape closes and focuses summary; outside click dismisses; hidden, denied, failed and successful-logout states clear account text and close disclosure. Existing logout endpoint and recovery remain. |
| P01-T02 | Two added API methods, amended positive allowlist, new browser check | Reconciled | Within four-method/one-file ceilings; no test removal, core change, new dependency or generated target. Existing denial, expiry, email-change, forged-token and replay tests retained. |
| P01-T02/P01-T03 | Four existing SQL browser harness interactions adapted | Reconciled | Each now opens the disclosure before logout access. Static coverage expanded to this fourth Python file; SQL execution remains excluded. |
| P01-T03 | README and focused/full API validation evidence | Reconciled | Documents intentional own-email disclosure and limitations; pass/fail history is distinguished and full-suite optional skips are explicit. |
| P02-T01 | Independent Review pending at handoff | Reconciled | This one independent record supplies the requested Review; no retroactive evidence edits. |
| P02-T02 | Stacked publication pending | Reconciled | Intentionally deferred until Review; no premature completion, push, merge, issue closure or hosted acceptance claimed. |
| Follow-Up Items | None established | Reconciled | Formal human accessibility acceptance remains outside this small slice and is not converted into active work. |

## Completed Work Assessment

| Marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01 | app.py | The new projection uses identity.email_for(case_id), not submitted text, query parameters, headers or browser storage. The same canonical email participates in existing authorisation before disclosure. No email added to anonymous/session responses. |
| P01-T01 | web/index.html, web/demo.js, web/demo.css | Account is initially hidden in the top header. Native details/summary and a real button match the employee interaction pattern without a custom menu. Existing tokens, visible focus, 44px target and rem sizing remain. Bounded right-anchored panel, flex wrapping/min-width and overflow-wrap handle long content. |
| P01-T02 | tests/test_resident_demo_api.py | Exact projection now allows precisely the resident's own email while continuing to exclude another email and private identifiers. Two clients, canonicalisation, query spoofing, repeated views, anonymous/session anonymity and post-revocation omission are covered. Existing lifecycle/isolation tests still pass. |
| P01-T02 | checks/resident_account_check.py | Actual loopback HTTP app, constructed FakeReader rows, runtime-only synthetic verifier and clock; no SQL/private-data setup. Covers restored identity, accessible summary name, Enter/Space, Tab to logout, Escape focus, outside dismissal, logout/replay denial, second identity, failed logout/retry, long email at 320/390/1280px, right edge, reduced motion and expiry. Context/browser/server shutdown is present. |
| P01-T02 | checks/resident_demo_browser_check.py | All four compatibility-only additions open the native disclosure before existing sign-out interactions. No infrastructure or SQL behavior changed; this harness was not run. |
| P01-T03 | README.md | Correctly distinguishes synthetic identity from real authentication; documents own-email allowlist extension, clearing and recovery, safe browser command and absence of human accessibility acceptance. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change and reason | Trigger and decision | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| P01 validation lock | Exact API/core/browser/static targets added | Original PC-001 identified unsafe selector ambiguity; owner already excluded SQL/verifier siblings | Current plan target map, details and dated commands agree | Compatible direct correction; original Revise verdict preserved, no repeat critique required. |
| P01-T02/P01-T03 | Existing SQL browser script added to compatibility/static scope | Moving logout under details makes its four old accesses hidden | Plan implementation-time update, details, changes and four-line diff agree | Directly coupled maintenance, not material architectural/scope divergence; no SQL execution authorised. |
| P01-T02/P01-T03 | Native-summary locator, namespace import and format corrections | Initial browser/format/mypy failures described in changes | Final browser source and recorded passing targets reflect the corrections | Test-harness corrections preserve native semantics and scope; no new user decision or material plan revision needed. |
| P01/P02 | Focused checks replace full local gate | Explicit owner direction, recorded in research/plan/details/state and this review request | Validation and publication wording retain hosted/human limitations | Justified owner-selected validation boundary, not a bypass inferred by the implementer. |

## Critique and Material Revision Assessment

* PC-001 is resolved by the plan's exact target map: test_resident_demo_api.py, the precise test_resident_showcase.py selector, full API discovery, named no-SQL browser file/command and changed-file static checks. Source additions remain within the locked ceilings.
* Original critique execution Complete and outcome Revise remain intact. This Review does not rewrite it as a pass.
* Recorded handoff establishes selector correction before source edits; the current artifacts and actual safe test targets support that disposition. Historical sequencing is supplied evidence, not independently reconstructed commit history.
* No material architectural change, unaccepted autonomy expansion, identity-policy change, dependency change or significant divergent decision found. The compatibility update is reconciled across all relevant artifacts.
* No evidence of affected work resuming under an unresolved material decision gap.

## Plan Follow-Up Assessment

| Item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| No task-specific follow-up recorded | Plan explicitly states none established | None | No unresolved plan item to route or add to implementation scope. |
| Human accessibility acceptance and wider Fluent adoption | Existing project-wide boundaries, not completion criteria of this native account slice | Existing accessibility/design work owners | Remain distinct existing acceptance work; this Review neither claims completion nor creates a duplicate defect. |

## Web Findings

Changed web code was reviewed against every category in the freshly retrieved rules, with the repository's Fluent/native-semantics, plain-language and ASCII standards taking precedence over generic title-case/typographic preferences. Findings are grouped by file; pass locations identify the assessed change, not defects.

### src/api/src/zava_forward/api/resident_demo/web/index.html

* src/api/src/zava_forward/api/resident_demo/web/index.html:19 - pass: native disclosure, named summary, text-only untranslated identity and native sign-out button; no custom menu role, icon-only action or inline navigation.

### src/api/src/zava_forward/api/resident_demo/web/demo.css

* src/api/src/zava_forward/api/resident_demo/web/demo.css:25 - pass: wrapping header, shrinkable brand and right-aligned disclosure.
* src/api/src/zava_forward/api/resident_demo/web/demo.css:28 - pass: visible inherited focus, minimum target height and hover/open feedback.
* src/api/src/zava_forward/api/resident_demo/web/demo.css:31 - pass: viewport-bounded, right-anchored panel and long-email wrapping.

### src/api/src/zava_forward/api/resident_demo/web/demo.js

* src/api/src/zava_forward/api/resident_demo/web/demo.js:88 - pass: identity from authorised view rendered with textContent.
* src/api/src/zava_forward/api/resident_demo/web/demo.js:100 - pass: hidden/error/signed-out reset clears identity and native open state.
* src/api/src/zava_forward/api/resident_demo/web/demo.js:218 - pass: Escape closes and restores summary focus; outside click dismisses without custom keyboard-role handling.

| Current rule category | Changed-scope assessment |
| --- | --- |
| Accessibility | Native summary/button supply activation semantics; existing labels, live regions, skip link and heading hierarchy preserved. No new media/icon semantics. |
| Focus | Inherited two-tone focus-visible treatment; explicit Escape focus restoration and unchanged success/error targets. Header is not sticky. |
| Forms | No new form/input, paste policy or navigation-with-unsaved-data path. Existing sign-in semantics retained. |
| Animation | No new animation or transition; existing reduced-motion token retained and covered by supplied browser execution. |
| Typography | Existing rem typography preserved. Repository ASCII and plain-language rules override generic curly punctuation/title-case advice. |
| Content handling | Canonical nonempty email, safe text rendering, explicit hidden-state clearing, min-width and wrapping; long synthetic input included in browser check. |
| Images | No new image, asset request or layout shift source. |
| Performance | No new list, external font/CDN, render-time measurement or per-keystroke work. Measurements are test-only. |
| Navigation/state | Transient native account disclosure needs no durable URL state; no navigation link replaced by scripting. Existing sign-out is not a destructive data mutation needing a new confirmation. |
| Touch/interaction | Summary has manipulation touch behavior and native keyboard equivalent; existing button target/touch behavior retained. No gesture-only control, drag or autofocus. |
| Safe areas/layout | Existing padded non-full-bleed header; CSS flex layout and bounded panel, not JS layout measurement. |
| Dark mode/theming | Existing explicitly light theme; no dark theme or native select added. |
| Locale/i18n | Identity has translate=no; no date, currency, number formatting or language-detection change. |
| Hydration | Static HTML and imperative DOM; no server/client hydration boundary. |
| Hover/states | Summary hover/open feedback and inherited button hover/focus preserved. |
| Content/copy and anti-patterns | Specific Account/Sign out labels, honest existing error recovery, no disabled zoom, div-click action, blocked paste, unlabeled control or new anti-pattern. |

No substantive changed-scope web defect identified. This is not a whole-site audit, screenshot review, screen-reader test, human acceptance or WCAG conformance claim.

## Findings

* No substantive actionable finding. Severity counts: Critical 0, High 0, Medium 0, Low 0.
* No RV-xxx defect, decision gap or evidence gap is invented for intended publication sequencing, known project-wide acceptance work or checks intentionally not rerun by this reviewer.

## Defects and Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| None | No rpi-implement, rpi-plan or rpi-research referral | Parent continues P02-T02 | No source defect, unaccepted significant decision or material evidence gap found. |

Later implementation of any separately identified issue does not require this Review to run again.

## Residual Work, Blockers and Remaining Work

* Review blockers: none.
* Implementation blockers or task-specific residual defects: none found.
* Remaining active work: parent records P02-T01 completion and performs P02-T02 using the approved stacked base feat/resident-interactive, Refs #467/Refs #466, privacy-safe author/committer identity, normal push and PR creation. No merge or issue closure is authorised.
* Hosted checks, rubric scoring, owner review and formal accessibility acceptance remain distinct pending gates. This Review is not publication permission beyond the owner's existing bounded direction and does not establish exact committed/pushed-head validation.
* The full two-hour local gate is intentionally excluded by the explicit owner direction for this task, not represented as passed.

## Validation Evidence

Commands below use the existing supplied virtualenv; no dependency installation was performed by this reviewer. Independent Python test reruns disabled bytecode writes.

| Command or evidence | Scope | Status | Result and provenance |
| --- | --- | --- | --- |
| From src/api: PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../core/tests:../agents/tests /tmp/ama-467-venv/bin/python -B -m unittest discover -s tests -p test_resident_demo_api.py -q | Focused API | Passed, independently rerun | 39 tests in 27.092s, OK. Two expected constructed RuntimeError request diagnostics did not fail the suite. |
| From src/core: PYTHONDONTWRITEBYTECODE=1 /tmp/ama-467-venv/bin/python -B -m unittest discover -s tests -p test_resident_showcase.py -q | Exact safe core selector | Passed, independently rerun | 39 tests in 2.504s, OK; no SQL/verifier sibling selector. |
| From src/api: /tmp/ama-467-venv/bin/ruff check --no-cache src/zava_forward/api/resident_demo/app.py tests/test_resident_demo_api.py checks/resident_account_check.py checks/resident_demo_browser_check.py | Four changed Python files | Passed, independently rerun | All checks passed. |
| Ruff format --check --no-cache on app.py/test_resident_demo_api.py; --check --no-cache --isolated --line-length 100 on both browser checks | Four changed Python files | Passed, independently rerun | Two source/test files and two check files already formatted. |
| node --check src/api/src/zava_forward/api/resident_demo/web/demo.js | Changed script | Passed, independently rerun | Exit 0. |
| git diff --check | Tracked working diff | Passed, independently rerun | Exit 0. New browser file was separately read in full and covered by Ruff. |
| Full API discovery | Full API suite | Passed, supplied implementation evidence | Changes and explicit caller evidence agree: 1069 tests in 577.664s, OK, skipped=308. Not rerun; optional/integration skips are not SQL passes. External raw log was not accessed. |
| Mypy on four changed Python files; compileall on both check scripts | Static type/compile checks | Passed, supplied implementation evidence | Changes records no issues in four files and passing compileall. Not independently rerun. |
| From src/api: PYTHONPATH=tests python -m checks.resident_account_check | Actual HTTP/Chromium | Passed, supplied implementation evidence | Caller and changes report health 200 and all named scenarios passed. Entire executable check inspected; not rerun here, so no fresh browser, visual or screenshot result claimed by this reviewer. |
| Existing checks/resident_demo_browser_check.py | SQL-backed compatibility harness | Not run, intentionally excluded | Only four disclosure-opening adaptations and static checks reviewed; no SQL harness execution. |
| Full local RPI gate, cloud and human/assistive-technology checks | Wider validation/acceptance | Not run | Owner substituted focused checks; cloud/SQL prohibited, and human accessibility acceptance remains outside this slice. |

## Outcome

* Outcome: Conformant.
* Rationale: completed P01 matches approved account disclosure, authorisation, isolation, native interaction, recovery and reflow requirements. The compatibility amendment is small and reconciled; PC-001 is resolved without erasing its original verdict. Independent focused tests/static checks pass and supplied full-suite/browser evidence supports the bounded acceptance basis.
* The approved focused-check substitution is a user-defined acceptance boundary, not an unexplained implementation divergence.
* Confidence boundary: code/artifact review and independently rerun focused checks, supplemented by explicitly attributed implementation-time browser/full-suite/type evidence. No live-service, human-accessibility, whole-site or publication/hosted-gate acceptance is inferred.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement referral. |
| Significant decision gap or invalid assumption | None | No rpi-plan referral. |
| Material evidence gap | None | No rpi-research referral. |
| Non-blocking task-specific residual work | None established | Existing project-wide accessibility/design work retains its owners. |
| Planned publication | Active parent, P02-T02 | Record this Review and continue approved stacked publication; no second Review. |

* Review execution: Complete.
* Outcome: Conformant.
* Substantive findings: none.
* Validation coverage: independent API 39/core 39, Ruff/format, JS syntax and diff whitespace; supplied full API 1069/308 skips, mypy/compile and actual HTTP/Chromium evidence.
* Blockers: none for the supplied Review boundary; publication and hosted/human gates remain pending.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-27/resident-account-control-research.md](.copilot-tracking/research/2026-10-27/resident-account-control-research.md) | Research and selected direction. |
| [.copilot-tracking/plans/2026-10-27/resident-account-control-plan.md](.copilot-tracking/plans/2026-10-27/resident-account-control-plan.md) | Current plan and exact validation lock. |
| [.copilot-tracking/details/2026-10-27/resident-account-control-phase-details.md](.copilot-tracking/details/2026-10-27/resident-account-control-phase-details.md) | Reconciled task details. |
| [.copilot-tracking/plans/2026-10-27/resident-account-control-critique.md](.copilot-tracking/plans/2026-10-27/resident-account-control-critique.md) | Preserved original Revise / PC-001 critique. |
| [.copilot-tracking/changes/2026-10-27/resident-account-control-changes.md](.copilot-tracking/changes/2026-10-27/resident-account-control-changes.md) | Implementation and supplied validation evidence. |
| [.copilot-tracking/rpi-sessions/2026-10-27/resident-account-control-state.json](.copilot-tracking/rpi-sessions/2026-10-27/resident-account-control-state.json) | Parent-owned automatic continuation state. |
| [.copilot-tracking/reviews/logs/2026-10-27/resident-account-control-review.md](.copilot-tracking/reviews/logs/2026-10-27/resident-account-control-review.md) | This single independent Review. |
| [src/api/checks/resident_account_check.py](src/api/checks/resident_account_check.py) | Reviewed no-SQL real-HTTP/browser check. |

## Next Steps

Return this Complete / Conformant Review to the active parent for P02-T01 recording and approved P02-T02 stacked publication. No corrective RPI command, repeat Review or user decision is required. This reviewer stops without changing source or parent-owned artifacts.
