---
title: Issue 176 status research (r8)
ms.date: 2026-11-04
---

* Task: rpi-176-r8, mode manual-equivalent, docs-only status record. Research disposition: executed.
* Merged PRs checked: #237, #257, #309, #368, #633, #703, #843, #1052. Open PRs referencing 176: none.
* Delivered: seeded replay audit (`determinism_audit`) covers scale fixture, sensor backfill, sensor scenarios, stock fabric, public pack, EPC, fictional stock register and register-backed sensor stream. Each manifest or descriptor records seed, version and a generator revision hash.
* Delivered: refresh policy (criterion 3, already ticked).
* Every generator in `src/` that records `generator_revision` is replayed by the audit (grep of `src/*/src` found seven modules, all covered).
* Unmet: original private 60,000-home OSM stock register generator and its pinned inputs are absent from the repository, so its byte replay and a new manifest cannot be produced. Historical public and private manifests stay untouched by policy.
* Conclusion: no engineering slice remains that advances criteria 1 or 2 without inventing the missing original. Planning readiness: Ready for a docs-only record.
