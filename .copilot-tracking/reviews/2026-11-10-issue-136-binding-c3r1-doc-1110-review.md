---
title: Review for issue-136-binding-c3r1-doc-1110
description: One author-inline review of the README seal-lifetime correction
ms.date: 2026-11-10
---

Executed once, author-inline, no nested agent. This is not independent approval; the Functional and Readiness reviewers assess the final delta separately.

## Outcome

Conformant for the one README sentence, with the qualifications below.

* The contradiction with valid-pair reuse is removed: seal invalidation is tied to loss or replacement of the store or key, and a retained valid pair does not itself revoke a seal.
* Replica-local volatile lifetime stays explicit (replica replacement or scale to zero). The enabled `maxReplicas` of 1 requirement, MSSQL accounting, manual fallback, default-off and auth guard text are untouched.
* The diff is 3 insertions and 1 deletion in `infra/README.md`; `git diff --check` exits 0; `src`, `infra/tests`, `infra/modules` and `infra/main.bicep` match the frozen tree.

## Qualifications

* The claim rests on `Lane.verify` source and the second-start `store_id` retention test. No new cross-restart seal runtime test was run.
* No runtime gate, lint or mypy rerun. Baseline mypy remains exit 1 with three baseline errors, not a strict pass.
* Earlier adverse items stand: original `core.hooksPath` override, C2 pre-research spike, and the recorded duplicate C3 launch (witness verify exit 1) plus the rejected `--actor author` CLI preflight.
* No whole-#136, #1288, live, human, production or model acceptance.

## Routing

No open findings. Optional later work: repair the three baseline mypy diagnostics.
