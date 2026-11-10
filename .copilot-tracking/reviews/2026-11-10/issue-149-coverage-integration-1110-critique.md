---
title: Issue 149 coverage parent integration critique
description: Single critique of the final candidate plan, performed by the primary agent before plan-done
ms.date: 2026-11-10
---

## Execution

One critique pass by the primary agent of the plan and details (no nested agent, not independent, not repeated). Verdict: proceed with changes. Compatible findings are applied directly; none conflicts with a confirmed decision and none needs a user decision.

## Findings and dispositions

1. The details named an unspecified Core exception-register selector. Checked: no Core test file references `exception_register`; the Core delta is `test_import_refusals` only, and the exception-register tests live in the API suite. Applied: Core selector is `test_import_refusals`; importer selector is `python3 -m unittest discover -s tests` in `src/importer` (README command).
2. The index convention lists each cutover-pack checkpoint in a paragraph near `docs/reference/README.md` line 1316. A new section is a material addition, so one index paragraph and one log entry are required. Applied in P3.
3. A merge commit cannot be verified against the prospective tree after hand edits; the identity check must happen before any other edit. Applied: P1 verifies tree `a9b51381` immediately after the merge, before documentation changes.
4. Checks run after the merge commit but before the documentation commit. The documentation commit changes only Markdown and tracking files, so the checks cover the final source tree; the record states this and the final source-tree equality (`git diff <merge-commit> HEAD --name-only` outside docs and tracking is empty) is verified at P4.
5. `mypy` runs against the installed editable tree: the worktree path is unchanged, so no reinstall of core, agents or api is needed; the importer is the only new install. Applied.
6. Browser exit codes must be preserved separately from a busy lock (`flock -n` exit 1 with no log). Applied: the runner records each check's own exit, and a busy admission is recorded as blocked.
7. Risk: the `held_form_download_browser_check` is main's own check and was not in the brief's list. It is retained because it exercises the shared `role-screens.js` and `server.py` hunks together with the parent's shell paths; it is labelled main-owned and not a parent claim.
8. Risk: the PR 1371 Core failure is in `test_resident_showcase`, not in any selected suite; the record must say it is not hit, not waived. Applied.
9. #156 M1 and #1362 must remain unresolved in the record; recommendation wording must not imply either is settled. Applied in P3 criteria.
10. Out of critique scope, noted: the first witness boundary was recorded after the research file was written, as the brief permits.
