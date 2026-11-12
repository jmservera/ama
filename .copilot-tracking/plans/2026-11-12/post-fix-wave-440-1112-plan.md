<!-- markdownlint-disable-file -->
# Plan: post-fix-wave checkpoint for #440 (2026-11-12)

* Task ID: `post-fix-wave-440-1112`; branch `docs/demo-fix-wave-checkpoint-440-1112` at `e155c88ed6357259a11520e7150b7ad9d349b9f8`.
* Research: .copilot-tracking/research/2026-11-12/post-fix-wave-440-1112-research.md (`executed`, Ready). Details: .copilot-tracking/details/2026-11-12/post-fix-wave-440-1112-phase-details.md. Critique: .copilot-tracking/plans/2026-11-12/post-fix-wave-440-1112-critique.md. Changes (created by implement): .copilot-tracking/changes/2026-11-12/post-fix-wave-440-1112-changes.md.

## Executive summary

One documentation-and-evidence candidate: append a dated section to the existing `docs/architecture/cutover-evidence-pack.md`, one index paragraph in `docs/reference/README.md` and an append-only entry in `docs/reference/log.md`, recording bounded local evidence for the merged wave PRs 1481 (#128), 1483 (#115) and 1482 (#98) on `main` `e155c88ed`. No source, test, tool, workflow, requirement or ADR change; no new issue, no tick, no push.

## User decisions and requirements

* Existing issue #440; this checkpoint is new and does not reset earlier correction budgets. Scope: paired diagnostic, held form-export validation-issue freshness, scheduled ledger failure and manual path. Excluded: unmerged 107, 134, 153, 157, 435, 82 and siblings.
* Focused local-first ladder, not the full gate; no cloud, provider, model, deployment, spend, private data or credential change; SQL and browser stay explicit not-run; pip only, no uv; no shared heavy resource.
* Existing pack, no new generic report page; preserve every adverse qualification (128 critique after draft; 98 under-scoped first mypy and hosted failure; 115 wrong-tool/config checks; 1483 GraphQL UNKNOWN then guarded merge).
* Proposed BRD, PRD and ADR documents stay unapproved; fixture providers and approvals are synthetic; preserve permission, consent, human-approval and AI-unavailable/manual-path safeguards.
* Commit locally with the privacy-safe identity and Copilot trailer; no push, PR, merge, criterion tick or board change.

## Goals

* G1 Pin source, main commit, trees, PRs, issues and exclusions.
* G2 Run the smallest affected checks and record command, environment, identity, exit, counts and skips; label each result.
* G3 Document-qualified requirement and code/test/journey/backlog traceability; exact remaining risks, owners and a continue/fix/proposed-pivot recommendation with affected and independent lanes.

## Phases

* [ ] Phase 1: preflight and origin proof (clean tree, editable installs resolve to this worktree, module blobs equal `HEAD:<path>`, tool versions).
* [ ] Phase 2: ladder. L1 core unit: `test_paired_equity.py`, `test_journey_register.py`, `test_form_export.py`, `test_form_dependencies.py`; orchestrator `test_digest_blob.py`; static ruff and configured mypy for `src/core` and `src/orchestrator` (read-only, no format writes). L2 cross-package: infra `tests.test_bicep_policy` ledger alert test (and full module, 61 tests); API `test_form_held_download_api.py` (local HTTP fixture). No SQL Server, browser, Docker.
* [ ] Phase 3: write the pack section, README index paragraph and log entry; changes record; state.
* [ ] Phase 4: one independent post-implementation Review; commit locally; verify clean tree, exact commit and tree.

## Check classification

Focused tier with a documentation-only change; full local gate and external receipt are not claimed. A blanket `rpi-checks --changed` run is optional and not planned. Basis: no source, workflow, dependency, Dockerfile or infrastructure file is edited here; the observed wave touched infra tests, so hosted CI results for the exact head and independent review remain required and unclaimed.

## Risks and non-goals

* Tools installed may differ from pinned versions (ruff 0.17.3, mypy 2.4.1 versus `pyproject.toml` pins); record the difference and do not claim hosted parity.
* A failing check is recorded as is; no source fix is authorised. A confirmed defect goes to the matching existing issue (#128, #98, #115) as a routed finding in the record, not a new ticket.
* Do not claim retention lock, hosted alert, scheduler run, fairness evidence, population cohort, resident outcome, browser or AT results.

## Critique dispositions (applied after the one critique)

* PC-001: the exclusion is SQL Server and shared services; in-process SQLite test stores are executed local coverage and are stated as such.
* PC-002: core freshness evidence and API held-download regression evidence are recorded separately; no HTTP freshness surface exists.
* PC-003: preflight baseline is a clean tracked tree plus untracked paths limited to `post-fix-wave-440-1112` artifacts.
* PC-004: infra runs with `REQUIRE_AZ_BICEP=1`; the focused marker test must run and pass, a skip is unverified.
