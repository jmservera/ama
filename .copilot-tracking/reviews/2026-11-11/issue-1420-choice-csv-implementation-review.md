# Issue 1420 implementation review (2026-11-11)

Executed once, by the implementing author, after implementation. Not an independent review; independent exact-head review and human approval remain required.

## Outcome

Conformant with disclosed limitations. No open material finding.

## Checked

* Plan decisions Q1 to Q6 and the eight-column contract: header and label text match `resident_choice_export.FIELDS`; unknown, stale, paused, withdrawn and retained human review are stated, never as consent or readiness (serializer tests, canary exclusion test).
* Route reuses the store method and `num()`, so roles, clamps, defaults, blank, repeated and unknown query behaviour match the JSON route; denied and signed-out users get no CSV; loader or shape failures give JSON errors, not a partial attachment.
* UI link is a native anchor, outside the table region, absent on load failure and bad paging numbers.
* Scope: only admitted files changed against `a853cce`; no `LIST_EXPORTS`, core, role, schema, `ops.js` or Capacity edits.

## Findings

* Low: mypy checked only the new module; `server.py` is untyped legacy and was not widened.
* Low: the browser observation used one role (Resident Liaison Officer) and story 232; other roles are covered by HTTP tests, not by Chromium.
* Info: the shared `origin/main` ref moved to `064f42f83` (1432) after the pinned integration; it is not merged here. Re-evaluate on the PR.
* Info: `ruff format --check` has one pre-existing hunk in `role_screens_browser_check.py`.

## Web Interface Guidelines (fetched in full from the source URL on 2026-11-11, complete retrieval)

Changed web file `role-screens.js` only; `server.py`, tests and checks are not UI.

* `src/api/src/zava_forward/api/web/role-screens.js:44` pass: `<a>` for the download (navigation to a file), described by the note at `:46`; visible focus and hover come from the existing `btn alt` design-system class (axe clean in Chromium).
* `src/api/src/zava_forward/api/web/role-screens.js:47` pass: active voice, second person, specific label, empty state explained, no ellipsis or straight-quote issue.
* `src/api/src/zava_forward/api/web/role-screens.js:60` pass: link absent when the load failed, so no broken empty success.
* Not assessed: Title Case rule against the sentence-case house style (plain-language standard wins); keyboard and focus checked only by the existing harness. This is a changed-file review, not accessibility conformance.

## Disclosures

No push, PR, issue or board write. Unobserved hosted CI is not a pass. No real data, live, privacy, retention or human acceptance is claimed.
