<!-- markdownlint-disable-file -->
# Review: aftercare hooks final correction (issue 133, C5)

Single post-implementation author review of the working tree on C4 HEAD 9efdeb0149a2945780dcc8e58208833000d10327. This is an author review, not the independent reviewer's C5 assessment and not human, assistive-technology, WCAG, deployment or model acceptance. Refs #133, #89, #134 only; whole-issue criteria remain unproven. C1 to C5 spent; no automatic C6.

Review execution: executed once. Outcome: conformant for the three C4 findings under the targeted tier, with the residual items below routed to later work. No second Review in this task.

## Finding disposition

* F1 (High) fixed: `aftercare_store.py` classifies and restores inside the lock that performed the save; outer lock-exit failure reacquires first and reads second; mutator once. RED/GREEN: `red_f1_test.log` then `core_store2.log`; SQLite and MSSQL (36 tests, 0 skipped) commit-ambiguity, reload, CAS and two-writer tests retained and passing.
* F2 (High) fixed: `web/aftercare.js:321-326, 376-381`. The submit continuation always persists draft, request id and outcome and renders or focuses only while `me` is the same session object, the view token is current and the form is mounted. A real 401 leaves sign-in in place; same-actor sign-in restores the original request id and the retry saves once; a late reply after a safe hash change leaves the page unchanged. `api()` unchanged.
* F3 (Medium) fixed: `web/aftercare.js:264-276`. One once-installed `beforeunload` guard warns while edited or unresolved, including after a safe hash change; none for pristine drafts or after a confirmed receipt; sign-out discards. No browser storage. Real tab-close dialog observed.
* Typing: four C4 `ignore_errors` entries removed; adapter and both new test modules now checked (Core 286 files, API 214 files). The two new test modules carry only a narrow `disallow_untyped_calls = false` for the existing untyped Store, SqlStore, MssqlStore and App constructors, disclosed in the changes artifact.

## Web interface guidelines (fresh fetch, HTTP 200, 8055 bytes, sha256 d246b026f4f29b58...)

Source copy: root `web-guidelines-133-c5-review-fetch-1110.md`. Applicable findings on changed web files (`aftercare.js`):

* `aftercare.js:267-276`: guard prevents data loss on navigation; compliant with the unsaved-changes intent and avoids replacing native browser UI.
* `aftercare.js:376-381`: focus is moved only when the view is still owned, so focus is not stolen from the sign-in form; compliant.
* No new colour, typography, animation or markup was added; existing linked field errors, native controls and non-colour status are unchanged.
* The guideline preference for Title Case headings conflicts with the repository plain-language sentence-case standard; the owner standard is kept and no heading changed.
* Retrieval succeeded; no partial retrieval.

## Residual items routed to later work (not repeated in this task)

* A second Store instance on the same JSON file is still unprotected by design; cross-instance protection is SQL only.
* The draft is held in memory only by design, so a discarded unresolved draft cannot be recovered after a document reload that the user confirms.
* Out-of-scope baseline failures reproduced unchanged: `test_simulator_admin` expired fixtures (PR1377), `employee_workspace_browser_check` missing ops exhaustion, `workspace_scripts_browser_check` request count. Current-main integration is coordinated by the root after the clock repair.
* Independent exact-head review, human approvals and hosted CI remain required before publication.
