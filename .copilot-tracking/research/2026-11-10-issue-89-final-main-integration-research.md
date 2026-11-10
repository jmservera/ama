---
title: Issue 89 final main integration research
ms.date: 2026-11-10
---

## Task and boundary

* Task `issue-89-final-main-integration-1110`. Adoption of reviewed merged inputs only: child #133 PR 1385 (merged into the declared parent) and current main. No new product or source correction allowance. Held #132 not included; no private code consumed; whole #89 stays gated on #132, human and other criteria; whole 89/133/134 criteria stay unticked. Original Stage A, C4/C5 RPI, witness records and outcomes are preserved unchanged.
* Research disposition: executed.

## Source identities (observed)

* Local start `50e1d2147d04d0440318932f44e693a114ea7d9c`, clean. Published parent `origin/feat/demo-quality-workflows-89-1109` = `4f5dc382bfca69c286fca6e60aa24b9a8ebbeb0e`, tree `cc3a1dcdbe54714f8c8b885b37946c2324bb1a26`; local was an ancestor, so fast-forward only was performed (tree equals the frozen child tree cc3a1dcd).
* Main `origin/main` = `65c2ab9d947d1498dafd37e24a377d1ff503e86f`, tree `520d12561000e9dc596ed0b03f9f862a9240b32f`; merge base with the parent `a6002219581b983132465e9dd1680f78e6aca542`.
* Parent side delta since the previous freeze (50e1d21..4f5dc38): 30 files, 18 non-tracking (aftercare_store.py, server.py, workbench.py, projection.py, sqlstore.py, app.js, aftercare.js, index.html, workbench-manifest.json, aftercare_browser_check.py, tests, READMEs, pyproject files, scenario-manifest.json).
* Main side delta since a600: 27 non-tracking paths (nomination and UX parent changes: app.js, panels.js, style.css, workbench_browser_check.py, nomination and atlas browser checks, learning_test_bundles, agents evals, docs, scenario-manifest.json).

## Overlap and predicted merge

* Overlap: `docs/reference/log.md`, `src/api/README.md`, `src/core/README.md`, `src/api/.../web/app.js` auto-merge; `scenario-manifest.json` conflicts. `git merge-tree --write-tree` exits 1 with exactly that one conflict, matching Root's prediction.
* Conflict nature: the parent changed the `workbench` source hash (workbench-manifest.json changed by the child); main changed the `recipe` hash (workbench_browser_check.py changed by main). Different lines, same hunk neighbourhood; each side's hash is an entry about a different file. Mechanical resolution: keep both hash updates, verified against the actual resulting file hashes. Any other conflict, or a hash that does not equal the actual file, is HOLD.
* No sqlstore, store, serializer or dependency-manifest path is in main's delta, so the child SQL evidence inputs are unchanged by main (to be confirmed against the child evidence record).

## Open items preserved

* Two inherited Medium findings (1000-key order, raw blank FileStateStore) stay OPEN; no repair, no large-volume acceptance. Generic workspace oracles are separately owned (#1384, current red); no waiver.
* The new #440 nomination/UX stabilization record is parallel and not inferred from passing tests.

## Planning readiness

* Ready.
