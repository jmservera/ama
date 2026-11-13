---
title: Independent exact-head prepublication assessment, #74 home building applicability display
ms.date: 2026-11-13
---

Verdict: Pass (FOCUSED tier), with two non-blocking Revise-optional observations. Refs #74 only. No AC tick, closure, human/AT/WCAG acceptance or publication decision is made here.

## Identity

* Candidate `f50c5c7fdd179e4d3c187130afbdf1e369983992`, tree `65e39a2821c95f13a9a5375ab5bea633688273ef`, base `15bfee2d7f6ae9b73d24c51d3dbbea7c7b78f626` (one commit, nine files, +137/-3). Reviewer branch `review/demo-home-scope-74-0506` started clean at the candidate. Author worktree not touched.

## Reading boundary

Read: full diff and all nine changed files (app.js, home_case_browser_check.py, README hunk, research, plan, details, changes, review, state JSON). Also read for context: `app.js` `buildingView` (1375-1381), `home_case.py` view() payload, the check's data builder and first assertions, and the cutover evidence pack references to this check. Not read: private datasets, `.env`, raw SQL, `rpi-149-final-ai-0104.log`. No tests were run or re-run by this reviewer.

## web-design-guidelines (current source, fetched 2026-11-13)

Fresh retrieval of `https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md` returned 8055 characters and was read in full (rules, anti-patterns, output format). The author's disclosed retrieval was the first 8000 characters, so the author's partial-fetch disclosure stands as recorded; the missing ~55 characters are the closing output-format example, which does not contain rules. Findings by file:

## src/api/src/zava_forward/api/web/app.js

src/api/src/zava_forward/api/web/app.js:1331 - pass: `scope()` keeps null=Unknown, []=None, list=IDs; `ids.join(", ") || "None"` is safe for [] only (a list never yields an empty string for non-empty IDs).
src/api/src/zava_forward/api/web/app.js:1334 - pass: `x.case_ids !== undefined` leaves systems rows unchanged (empty-state/absent handled); text via `h()` children, no innerHTML, so IDs are not interpreted as markup.
src/api/src/zava_forward/api/web/app.js:1334 - minor (content/i18n): identifiers (ZF-2, PKG-SHARED) lack `translate="no"`; consistent with the rest of the file, not introduced as a new pattern. Not blocking.
src/api/src/zava_forward/api/web/app.js:1334 - minor (long content): very long ID lists render inline in an `li`; wrapping depends on existing CSS, not asserted at 320 px for long values. Not blocking.
src/api/src/zava_forward/api/web/app.js:1358 - pass: `muted` plain `p`, native semantics, no colour-only signal, no new controls, links, focus or motion. Wording is plain, active, and informative non-eligibility ("do not establish eligibility, approval or coverage").

src/api/src/zava_forward/api/web/app.js:1334 vs 1381 - observation: home view says "Homes: ..." while the full building screen says "Affected homes: ...". The details file planned "Affected homes". The shorter label is a deliberate plain-language choice and is not wrong, but the two screens now name the same field differently. Non-blocking; owner may prefer one label.

## src/api/checks/home_case_browser_check.py

src/api/checks/home_case_browser_check.py:49-57 - pass: seeds null/[] , []/null and a multi-ID row on top of the existing DEP-1 so each meaning is exercised.
src/api/checks/home_case_browser_check.py:117-132 - pass: assertions read rendered DOM text of the building region and the home region, not source strings. They would fail on base (author reports red on base).
src/api/checks/home_case_browser_check.py:132 - minor: the assertion `"Homes: " not in home_text` and the SYS-1 `"Homes:"` check are negative proxies; adequate for separation, and SYS-1 already has a pre-existing exact-text check.
src/api/checks/home_case_browser_check.py:52 - observation: WORK-M lists sibling case id ZF-3 on ZF-2's screen. The payload already carried it (`home_case.py` embeds `buildings.view`, staff-only), the screen is staff-only, and no sibling evidence text is shown, so this is display of an existing identifier, not new exposure. Worth owner awareness; not a defect.

## src/api/README.md

src/api/README.md:4424-4426 - pass on meaning; cosmetic: one line now exceeds the surrounding wrap width (author review noted this). Plain ASCII, no em dash. README states axe is conditional on `ZF_AXE_JS`, matching the executed skip.

## Source contract and meanings

* `null` = unknown, `[]` = explicitly none, list = explicit scope, as recorded in `buildings.py` `_scope` and `buildings.blockers` (per research, matched by `buildingView`). The candidate reproduces those meanings exactly and adds no filtering, computation, approval or eligibility derivation. API, core, domain, schema and persistence are unchanged (diff confirms only app.js, the check and docs/tracking).
* Systems and costs carry no scope fields and render without a scope line (asserted).
* Home versus building separation preserved: scope text only in the shared-building region; asserted.
* Fluent 2 / plain-language / native `ul`/`li`/`p` semantics unchanged; no styles, controls, colour or motion added.
* Scenario-manifest/recipe binding: the changed check has no manifest or recipe identity in its source (grep of the file found none) and is referenced only as a named focused check. I found no binding requirement for this script in this delta. The cutover evidence pack records an earlier 24-PASS run of the base check; that historical count is not this candidate's result and must not be reused for it.

## Evidence qualification

* Supported by retained text only (author report in the changes file, not independently re-run): node syntax, ruff, format, mypy on the check, six `test_home_case_api` tests (run with PYTHONPATH pointed at this worktree), browser red on base and green on candidate under nonqueued heavy lock, no JS errors or non-safe requests.
* Adverse evidence preserved: the initial editable-install run hit the wrong source (`/home/azureuser/source/ama`), giving one unrelated 404 and an invalid red result. Both were discarded and must not count as baseline failure or as evidence. Only the PYTHONPATH rerun supports the tests claim.
* Axe SKIPPED (`ZF_AXE_JS` unset): no automated accessibility result exists for the candidate. For this small text-only delta that is not blocking the FOCUSED tier but must stay disclosed; it is not accessibility conformance, and manual keyboard/screen-reader/WCAG review remains open.
* Process drift (non-blocking, record-keeping): the plan marks Phase 2 "[x]" including `test_home_case_api.py` regressions, but the changes file states no unit test was added, per critique C1; the details file's Phase 2 unit test and "Affected homes" wording differ from what was built. The changes file is the accurate record. State JSON has `session_status: null` and `critique` pointing at the changes file; acceptable.
* The author's critique and Review are self-reported subagent results and are not re-verified here; they stay as recorded and are not replaced.

## Classification check

The research file classifies this as one INITIAL additive read-only display increment, not a correction cycle, with the historical #74 correction pool UNKNOWN. The diff is consistent: additive display, no fix of a rejected head, no rule or API change. I found nothing in the candidate contradicting that classification. It is an author/coordinator admission; I cannot verify the historical count, and no correction cycle was renewed. G5 remains optional and unproven by literal criterion 2.

## Publication blockers

None for the FOCUSED tier. Remaining gates, unaffected by this assessment: hosted CI on the exact head (not observed), actual public readiness review, human keyboard/screen-reader/WCAG acceptance, owner confirmation of the G5 display and label wording. No full gate is required by the stated tier because the delta has no schema, SQL, security, infrastructure or deployment behavior; if any owner reclassifies it, the full tier would apply.
