<!-- markdownlint-disable-file -->
# Review: issue 196 src layout and cut-over ADR

Execution: executed once, post-implementation. Outcome: conformant for the documentation scope; owner approval of the ADR remains open by design.

## Acceptance criteria

* [x] Standard `src` layout and tree stated.
* [x] Name candidates with trade-offs; owner selection `zava_forward` recorded.
* [x] Move-not-copy rule, including CI repointing.
* [x] Phases and cut-over gate.
* [x] When `src/` and `mvp/` count, and the registry exclude prerequisite.
* [x] Private `mvp/data/` relocation out of git and images.
* [ ] Owner approves the ADR: pending (human boundary, left unchecked).

## Findings routed to later work

* Rank 1: #198 registry PR for vendor and data excludes before the first move.
* Rank 2: #197 parity matrix to confirm per-file mapping, including `chat_fixture` placement and the synthetic tools sub-package.
* Rank 3: #200 repoint of Bicep job commands, `az acr build` context and generator output path.
* Rank 4: coordinate #287 (edits `assistants.py`) before the agents move.

## Evidence

[ADR 0006](../../../docs/adrs/0006-src-layout-and-cutover.md), [changes](../../changes/2026-10-15-issue-196-src-layout-adr-changes.md).
