# Plan: Registry observation parent transition (2026-11-10, Refs #440 #185)

Research: [research](../research/2026-11-10-registry-parent-transition-440-1110-research.md). Details: [details](../details/2026-11-10-registry-parent-transition-440-1110-details.md). Critique: [critique](./critiques/2026-11-10-registry-parent-transition-440-1110-plan-critique.md).

* Phase 1: `git merge --no-ff --no-commit origin/main` (`eff05737`); resolve the pack and README append conflicts keeping main's text then the Registry additions; log auto-merges.
* Phase 2: edit only dependency-dependent wording in the Registry section, README paragraph and log entry (parent merged as `eff05737`; `6cc59776` remains the historical pin; src/infra/tools ids equal).
* Phase 3: verify (no conflict markers, main's three docs files intact, ASCII, links), review, commit the merge, witness.

Constraints: no rebase, reset, amend, force; no product, test, config or infra edit; no runtime or gate; older observations unchanged.
