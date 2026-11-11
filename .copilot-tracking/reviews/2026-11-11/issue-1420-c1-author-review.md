# Issue 1420 C1 author Review (2026-11-11)

One author Review of the C1 correction, separate from the original author Review and the pending independent reassessment. Changes record: `.copilot-tracking/changes/2026-11-11/issue-1420-c1-correction-changes.md`.

## Execution and outcome

* Execution: performed once, over the four C1 hunks and their validation.
* Outcome: conformant for the two coupled blockers, with open items listed below. It does not replace the independent reviewer's reassessment, which is required.

## Findings

* High (independent report, `issue-1420-fa497-independent-functional-findings-historical.json`): reproduced red by execution, fixed by the closed review-status vocabulary, covered by serializer and HTTP regressions; valid `Needs human review`, valid `Reviewed with supplied acceptance`, explicit `None`, retained Declined and non-string or missing evidence cases still pass. Not relabelled Pass; reassessment pending.
* Typing: all 13 errors cleared with real annotations and one narrowed Optional; pinned mypy 2.4.0 and unpinned 2.4.1 both pass on 232 files.
* One new narrow `# type: ignore[no-untyped-call]` on the existing untyped `App` constructor in the new test module, following existing repository usage. It is disclosed; it is not a broad ignore.
* Side effect checked: the canary test's review status `Resolved` is not in the vocabulary, so that row now reads unavailable; the test asserts only the absence of canary values and still passes.
* Fail-closed note: an unrecognised review status leaves the choice summary as is and marks the retained-review column unavailable for that measure, which is the Q6 meaning.

## Open items and routing

* Independent reassessment of the exact final head by the same reviewer (Root).
* `server.py` stays under the project `ignore_errors` baseline; not fully typed.
* The pre-existing format hunk at `role_screens_browser_check.py:225` remains by design (baseline identical on main).
* Hosted CI, human acceptance, live and privacy review and whole #80 and #73 remain open.
