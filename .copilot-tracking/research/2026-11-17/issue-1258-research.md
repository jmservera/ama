---
title: Issue 1258 research, ranking archive ancestor durability
ms.date: 2026-11-17
---

## Scope and disposition

* Issue #1258, tier FOCUSED (coordinator brief). Base `eb51af5c9ab0b1353ac380fc8960ee8dd96d17c4`.
* Research disposition: executed. Planning Readiness: Ready.
* Out of scope: #1818/#1641 (core mssqlstore, chat grounding), the unresolved PC3-1 mount-topology race, FULL receipt, hosted CI.

## Finding

The issue text describes `4ec4c280`. Current main already contains the fix. In
`src/core/src/zava_forward/core/ranking_publication.py`:

* `publish` creates missing ancestors with `os.makedirs(archive_dir, exist_ok=True)` and opens the folder once.
* `_confirmed` calls `_walk(held)` to open every parent folder up to the mount boundary, syncs the archive folder, then each parent (nearest first), then re-walks and compares identities.
* A failed sync or identity change raises `DurabilityUnconfirmedError` with the record kept and `written` preserved.

Existing tests in `AncestorDurabilityTests` (`test_ranking_publication.py`) cover: ordered syscalls for missing nested ancestors
(`file, link, archive, b, a, root`), post-link ancestor sync failure, retry, partial earlier creation, non-writable and symlinked parents.

## Measurement (executed 2026-11-17)

Environment note: the installed `zava_forward.core` is an editable install of the main checkout, so runs used `PYTHONPATH=src/core/src` to import this worktree.

| Check | Result |
| --- | --- |
| `python3 -m unittest discover -s tests -p test_ranking_publication.py -q` (from `src/core`) | 57 tests OK |
| Mutation: replace the parent-sync loop `for parent in opened:` with `for parent in []:` | 12 failures, including the nested-order and ancestor-failure tests |
| Source restored after mutation | `git status` clean |

The mutation reproduces the issue's defect (parents not synced) and shows the existing regression tests fail on it, so the first-publication ancestor contract is enforced by tests. This is a mocked/syscall-order result, not a crash or live filesystem result.

## Conclusion

No smallest source fix or new test is required for AC1 and AC3 on current main. Unmet by this task, unchanged: the original PC3-1 race, FULL receipt (AC5) and crash/live filesystem acceptance. Issue stays `Refs`.
