---
title: Issue 96 C4 changes
description: Implementation record for the baseline eighth invalid-field site correction
ms.date: 2026-11-13
---

## Changes

| Path | Change |
| --- | --- |
| `src/api/tests/test_accessibility_baseline.py` | Expected `aria-invalid` site count 7 to 8; the failing message is unchanged and no prior assertion weakened. New `test_saved_held_copy_field_is_tied_to_its_visible_message`, scoped to the `fundingSavedCopyCheck` body: describedby target, `field-error` element with the same id, `show()` text, unhide and `aria-invalid` set and clear, label `for` and one-paragraph placement |
| `docs/reference/research/ux/wcag-conformance-baseline.md` | Dated 2026-11-13 (96 C4) entry on the Error identification row naming the saved Held copy field, message and association, with limits and no conformance claim |
| `docs/reference/log.md` | One appended entry |

Divergence from details: the specific association check is a separate focused test method rather than inline in the count test (critique CR-1 scoping made it clearer). Same module, same intent.

## Validation (2026-11-13)

* Failing-first on the exact candidate before any edit: 12 tests, 1 failure `8 != 7` ([log](../../audits/2026-11-13/issue-96-c4-ci-baseline-0208-failing-first.log)).
* After the change: `python3 -m unittest tests.test_accessibility_baseline` from `src/api`: 13 tests OK. This is the fresh covering result for the changed WCAG record input, which that module reads. Other lanes that read the record were not rerun.
* Mutation check of the new assertions: 7 scratch mutations of a copy of the web directory (drop describedby, change error id, drop class, never unhide, no `aria-invalid`, label `for` removed, error not rendered) all fail the new test ([log](../../audits/2026-11-13/issue-96-c4-ci-baseline-0208-mutation-check.log)). The worktree product file was not edited.
* RoleScreens and RoleScreenConformance: 21 tests OK (`PYTHONPATH=../core/tests:../agents/tests`, from `src/api`).
* `ruff check` on the changed test: pass. `mypy` on the changed test: no issues. Installed tools were ruff 0.17.3 and mypy 2.4.1, not the pinned 0.17.1 and 2.4.0 (not installed, not needed after a successful run; difference recorded). `ruff format --check` reports the file was already unformatted before this change; not enforced and not fixed here.
* Not run: whole API suite, full gate, browser check (no focused browser observation was needed because the existing check already covers `aria-invalid` and the message for this field).
* Hosted failure (run 43347366743, job 131630021882, `8 != 7`) preserved; new hosted CI is required after one independently assessed push.

## Audit result

The eighth site is a truthful association (see research). No product defect found, no product change.
