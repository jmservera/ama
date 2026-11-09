<!-- markdownlint-disable-file -->
# Plan: PR 1295 owner-head reconciliation (2026-11-09)

* Task: `pr-1295-owner-reconcile`. Research: [research](../../research/2026-11-09/pr-1295-owner-reconcile-research.md). Details: [phase details](../../details/2026-11-09/pr-1295-owner-reconcile-phase-details.md).
* Tier: owner-selected demo-targeted. No `rpi-checks --all`; no gate for purely textual docs.

## Phases

* [x] P1 Refresh and record identities (remote head re-read; stop if it moved).
* [x] P2 Critique this plan once (executed; verdict Revise; compatible findings applied in the details; see [critique](../../reviews/2026-11-09/pr-1295-owner-reconcile-plan-critique.md)).
* [ ] P3 Merge `origin/docs/capstone-cxo-story` into the run branch with `git merge --no-ff` (no rebase, reset or force); preserve the 12 recovery tracking files and all owner paths; no conflict is expected.
* [ ] P4 Verify ancestry and path preservation: both parents, owner commit reachable, tracking files intact, delivered PPTX/PDF bytes equal remote bytes.
* [ ] P5 Run targeted checks into external scratch `/tmp/ama-pr1295-owner-val-*`: README-defined PowerShell checks, Python preview test, Node diagram checks and tests, Build/Verify/Linux preview, source/delivery hashes.
* [ ] P6 Compare Build output with the delivered bytes. If equal, leave source and delivery frozen; if not, reproduce and record the smallest consistent fix without replacing delivery.
* [ ] P7 Inspect rendered affected pages (12, 13, 28, 38, 55) from the generated preview; compare with expected slide order and text equivalents.
* [ ] P8 Write changes, review (one Review) and state records; commit tracking only with repository-local identity and Copilot trailer; refresh remote head again; write handoff.

## Exit criteria

* A failed selected check is recorded and not waived. Any further owner change requires reconciliation. No push, PR, board, Azure or model action.
