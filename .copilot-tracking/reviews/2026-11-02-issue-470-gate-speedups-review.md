---
title: Issue 470 gate speedups review
ms.date: 2026-11-02
---

Review executed once. Outcome: conformant for the covered unit-level behaviour; runtime behaviour unproven. Matrix of the six approved items: 1 parallel groups and auto jobs (implemented, scheduler unchanged and already tested); 2 API shards (implemented, unit-tested, never executed against the real suite); 3 scoped skips recorded (implemented, tested); 4 layer cache (implemented, tested, build speed unmeasured); 5 base relaxation (implemented with fail-closed matrix, tested on fixture repos); 6 batch stack gating (implemented as record and validate; end-to-end merge sequence unexercised).

Residual risks, routed to later work: (a) shards run all modules' imports in each process and rely on `-k` module ids, so a TestCase defined in a non-test helper module and only imported would run once in its importing module only when the id prefix matches; none found in `src/api/tests`; (b) layer cache can hide a stale `apt-get upgrade` layer until Trivy flags it, hence `--fresh-images` for releases; (c) relaxation treats docs, tracking, support and markdown as inert, matching the existing changed-path tier, but a test reading docs would be missed; (d) complete-gate run and before/after timing remain required for criterion 4. Human review checkboxes remain unchecked; independent exact-head review and hosted CI remain required.

## Correction notes (2026-11-03)

The review above is preserved. It was run by the implementing author, not an independent reviewer; the critique in the plan artifact was likewise author-run. An independent reviewer then assessed PR #792 and returned Pass with fixes. This correction applies those fixes.

Additions the original omitted: `plan_shards` (shards are planned from `--jobs` when `project-api` remains, and recorded in `test_shards`), and the `--jobs` default changed from 1 to 0 (auto), which also changes scheduling for every unflagged run.

Corrections to the original residual risks:

* (a) was wrong. A TestCase defined in a non-`test*.py` helper and imported into a test module has a helper-module id, matches no `-k MODULE.*` pattern, and would never run in any shard, not once. Fixed: discovery lists every id before sharding and the run fails closed when any id matches no shard; tested.
* (c) was understated. Relaxation ignored the preflight, namespace and static groups, so a main-side move those groups read could be accepted against a candidate that never ran it, and a docs-only candidate accepted arbitrary non-inert moves. Fixed: such moves, tooling and extras, markdown under `src/`, and any non-inert move against a candidate with no project group now block.
* Stack gating binds only the tip `HEAD`; intermediate heads are not individually gated and rely on hosted CI. Now documented; `--stack-member` also requires the member to be an ancestor of the verified `HEAD`.
* `image_cache=layer` was accepted for full receipts. Policy now: full scope requires fresh images, built automatically and enforced in verify across the resume chain.
* Old partial receipts fail verification because `selection` now carries `skipped`; documented.
* The outcome "conformant at unit level" stands only for the tested behaviour; the complete gate, real shard execution and timings were still not run by the author.
