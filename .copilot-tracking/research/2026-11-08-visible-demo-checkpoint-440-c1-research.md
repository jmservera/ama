---
title: Visible-demo integration checkpoint 440 C1 research
ms.date: 2026-11-08
---

## Scope

C1 correction of candidate `398a1b6c7b92aaf313bdaed100b1cfc2323bae9a` (tree `305b8316d701ac95ae42a105f65fb59c1dfe0081`), session `9dfa8bcc-4468-4888-be6a-d543c459c94f`. Written 2026-11-08T20:10Z, before any correction edit. Original `fcbd81e8` research, plan, critique (Revise), the original changes record and the original author Review stay unchanged; the original Review was an author review, not independent.

## Current identities

* `origin/main` fetched again: `6354b13f7abf1441a815e92f2b01dc184ce0b0ac`, unchanged. Worktree clean at start.

## Independent assessment (preserved adverse evidence)

Coordinator file `review-440-visible-398a-independent.json`, read completely: verdict request_changes, 0 Critical, 0 High, 3 Medium, 1 Low. It read the full 441-line, ten-file diff, the native log and source.

* F1 Medium (pack line 3243): "answers nothing without a model" contradicts `chat_panel.py` 455-505 (unstored rules-only, no model) and 681-688 (rules-only grounded answer after provider failure with permitted facts). Model-generated answers need the model; the model call is at most once per stored turn.
* F2 Medium (line 3278): closure of every listed issue made dependent on #184/#1288. Actual outstanding criteria: #229 accessibility (WCAG); #159 screen-reader and turn accounting; #891 per-call token, cost, privacy, retention and refusal conjunction. No blanket IoT dependency. Only sensor-grounded Quality acceptance needs its own corrected source, integration, separately admitted activation and observed journey.
* F3 Medium (lines 3267, 3229): global "no sensor input reaches any model from main" and "no live sender or receiver has occurred" exceed evidence. Supported: the `Assistants.capture` Quality allowlist at this pin (`assistants.py` 104-169, per the assessment) excludes sensor readings; no live activation was observed or verified within this checkpoint.
* F4 Low (line 3251): 19 hosted exact-head checks grouped under "Local observed". Separate hosted from local assessment.
* Additional qualification (line 3265 region): one real generic employee model answer on deployed e2ece revision 27 was observed; no real case-grounded answer or human acceptance is proven.

## Own verification of source

* `chat_panel.py` 455-470: unstored ask "calls no model". 681-688: grounded rules-only answer after fallback when case facts exist. Both read directly this session.
* `assistants.py` 104-169 allowlist: to be re-read before the edit to qualify wording (done in implementation, recorded in changes).

## Limitations

No test, SQL, browser, model or Azure action. No new defect beyond F1-F4. Ordering defect (#81) remains unverified and unlinked. Planning readiness: Ready.
