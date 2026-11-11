# Issue 1420 correction cycle C1 research evidence and bounded plan amendment (2026-11-11)

Additive, written before any C1 source or test edit. Original research, plan, critique, admission, the current-main amendment, adverse runs, the author Review and earlier handoffs are unchanged. The earlier valid research and plan are reused; no broad re-research.

## Grant

Root grants ONE first review-correction cycle, C1, of the standing five total (four remain after C1). The earlier integration and validation was not a source correction. No counter is reset and no other issue's grant is borrowed. Starting clean HEAD `23a26e139386b0c9d79953edca818deed6a6c4cb`, tree `53ef2d070f77ff651dc19ebc0dce130cb831a59b`; integrated main `1b169fe7d4f9b5a005123c8eb1825028ea431612`; frozen implementation `fa497143cf9653b6bf3de1d5c11bff7a922b0aaf`.

## C1 research evidence

* Independent functional report `.copilot-tracking/reviews/2026-11-11/issue-1420-fa497-independent-functional-findings-historical.json` (reviewer `e7904990-f50c-4663-95f0-bd4e4ea6096f`, copied byte-exact from the Root original, sha256 `5ec5c9bfae26c2759d64bc134f62efbf53f27993af6fd97732801b82f1c5584e`). Verdict `request_changes`, one High. It is the historical review of `fa497`; final reassessment by the same reviewer is pending and it is not relabelled Pass.
* High finding: `resident_choice_export.py` `_complete` accepts any string as `review.status`. For current Waiting, versions v1 Declined then v2 Waiting and review `{"status": "garbled", "decision_version": 1}`, completeness succeeds, `_review_version` finds no `Needs human review`, and the retained-review column writes `None recorded`. That is an absence claim from unrecognised evidence and violates admitted Q6. The report's trace is static; this cycle reproduces it by execution first.
* Existing vocabulary (read-only Core, `resident_decisions.py` lines 1619 and 1623): `Needs human review` and `Reviewed with supplied acceptance`. Core copies review records into the projection without validating the status (line 1058). No state is invented and Core is not changed.
* Project mypy from `final-main/mypy-project.log` reports 13 errors in this issue's own code: 8 in `tests/test_resident_choice_export.py` (lines 169, 184, 203, 212 x3, 283, 345), 4 in `tests/test_resident_choice_screen.py` (351, 353, 354, 372) and 1 in `checks/role_screens_browser_check.py:734` (`str + str | None`). (The earlier validation record said 2 for the checker; the log counts 1.) `server.py` is covered only by the project's existing `ignore_errors` override. That baseline stays and is disclosed, not described as fully typed.

## Bounded plan

Allowed hunks only: `src/api/src/zava_forward/api/resident_choice_export.py`, `src/api/tests/test_resident_choice_export.py`, the already-changed `src/api/tests/test_resident_choice_screen.py` typing and the existing `src/api/checks/role_screens_browser_check.py` typing. Any other file stops for Root. No Core, server semantics, web/UI, roles, schemas, registry, Capacity or shared serializer change; no dependency manifest change.

1. Red first: add focused regressions, run them against the unchanged serializer, retain the real failing output.
   * Serializer: empty and unknown string review statuses for Declined then Waiting must give `Unknown (evidence unavailable)` and never `None recorded`; keep explicit `None`, valid `Needs human review`, valid `Reviewed with supplied acceptance`, retained Declined and non-string or missing evidence cases.
   * HTTP: the same malformed review reaches the real projection path (seeded through the existing `detail` patch pattern) and the downloaded file says Unknown.
2. Smallest fix: in `_complete`, accept a review object only when its status is in the closed tuple `("Needs human review", "Reviewed with supplied acceptance")`. Explicit `None` stays no review. Unknown values go to the existing unavailable path. Eight-column contract unchanged.
3. Typing: fix the 13 errors with real annotations or guards (typed helper signatures, narrowed Optionals, an annotated container, a typed `App` use) following repository patterns; no broad ignore, unsafe cast, weakened test, disabled check or new server ignore.
4. Validate: red then green on the new regressions; the 124-case focused selection (count may rise) and the four SQLite and JSON intake tests; complete project mypy including tests and checks; changed-file Ruff check and format check (baseline proof for unrelated format hunks); node syntax; tool pins (mypy 2.4.0, Ruff 0.17.1) preferred in a task-private environment, installed with pip only at manifest-declared exact versions into the private venv if absent, with the unsatisfied prerequisite recorded first; ONE fresh bounded real Chromium story 232 under exactly one canonical heavy lock. The earlier browser observation is historical, not final-source equivalent.
5. Genuine dated C1 author Review, changes record and state, then one commit. Stop for Root and the same independent reviewer's reassessment. No push, PR, issue or board write, cloud, spending, cleanup or full gate.
