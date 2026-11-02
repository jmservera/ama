---
title: Issue 470 gate speedups review
ms.date: 2026-11-02
---

Review executed once. Outcome: conformant for the covered unit-level behaviour; runtime behaviour unproven. Matrix of the six approved items: 1 parallel groups and auto jobs (implemented, scheduler unchanged and already tested); 2 API shards (implemented, unit-tested, never executed against the real suite); 3 scoped skips recorded (implemented, tested); 4 layer cache (implemented, tested, build speed unmeasured); 5 base relaxation (implemented with fail-closed matrix, tested on fixture repos); 6 batch stack gating (implemented as record and validate; end-to-end merge sequence unexercised).

Residual risks, routed to later work: (a) shards run all modules' imports in each process and rely on `-k` module ids, so a TestCase defined in a non-test helper module and only imported would run once in its importing module only when the id prefix matches; none found in `src/api/tests`; (b) layer cache can hide a stale `apt-get upgrade` layer until Trivy flags it, hence `--fresh-images` for releases; (c) relaxation treats docs, tracking, support and markdown as inert, matching the existing changed-path tier, but a test reading docs would be missed; (d) complete-gate run and before/after timing remain required for criterion 4. Human review checkboxes remain unchecked; independent exact-head review and hosted CI remain required.
