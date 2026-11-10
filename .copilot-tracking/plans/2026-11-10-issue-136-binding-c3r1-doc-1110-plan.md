---
title: Plan for issue-136-binding-c3r1-doc-1110
description: Documentation-only correction of one README sentence
ms.date: 2026-11-10
---

## Objective

Replace the sentence at `infra/README.md:3915`, "A seal minted before a restart cannot be verified after it.", with wording that ties seal invalidation to loss or replacement of the simulation store or key.

## Phases

* [ ] Phase 1: Edit the one sentence in `infra/README.md` (details file).
* [ ] Phase 2: Documentation-tier validation: git diff and `git diff --check`, wording and link review, and unchanged source, test, Bicep and config hashes against the frozen input.
* [ ] Phase 3: Review once, then commit with the privacy-safe author, committer and Copilot trailer.

## Constraints

* Product path is only `infra/README.md`; no src, test, Bicep, CI, config, image or helper change.
* Keep replica-local volatile lifetime, enabled `maxReplicas` of 1, MSSQL accounting, manual fallback, default-off and auth guards unchanged in meaning.
* No runtime gate, Docker, SQL, lint, mypy or unit rerun; earlier runtime evidence is carried only by verified unchanged identities. Baseline mypy stays exit 1 with three baseline errors.
* No push, PR, GitHub, cloud or model action.
