---
title: Changes for issue-136-binding-c3r1-doc-1110
description: Change record for the README seal-lifetime correction
ms.date: 2026-11-10
---

## Product change

`infra/README.md`, Accounting bullet of the public simulation lane section (frozen line 3915): the sentence "A seal minted before a restart cannot be verified after it." is replaced by "Losing or replacing the simulation store or key (replica replacement or scale to zero) invalidates prior seals; a restart that retains the valid pair does not itself revoke them, and expiry and single-use checks still apply." Diff: 3 insertions, 1 deletion.

## Validation (documentation tier)

* `git diff --check`: exit 0.
* `git diff --name-only HEAD` lists only `infra/README.md` as a tracked change; `src`, `infra/tests`, `infra/modules` and `infra/main.bicep` match the frozen tree (tree ids `1c5d7c287`, `e92f3e3dc`, `10e931b8c`, blob `7074af59d`).
* No runtime gate, Docker, SQL, lint, mypy or unit rerun. Earlier runtime evidence is carried only by those unchanged identities; baseline mypy remains exit 1 with three baseline errors, not a strict pass.
* Raw captures: `phase136-binding-c3r1-doc-evidence-1110/proof/` under the session files root.

## Divergences

None.
