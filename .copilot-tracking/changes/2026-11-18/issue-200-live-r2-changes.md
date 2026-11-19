---
title: Issue 200 live audit changes (Refs #200)
description: Changes record and per-criterion table for the issue 200 live audit
ms.date: 2026-11-18
---

Changes (documentation only, FOCUSED tier): research note, evidence folder, index row and log entry. No src, infra, SQL or deployment change.

Files: `docs/reference/research/issue-200-live-20261118T1618Z-2026-11-18.md`, evidence folder `issue-200-live-20261118T1618Z-evidence/`, index row, log entry.

The prior tracked `issue-200-live-*` plan, details, research and changes files from an earlier run were preserved; this run uses `-r2` names. The mandated state file path was reused and overwrote the earlier state (recoverable from Git history).

## Per-criterion table

| Criterion | Result |
| --- | --- |
| 1 Packaging via `pyproject.toml` src layout | Ticked; spot-check holds |
| 2 Paths, context, requirements, workflow names | Ticked; spot-check holds |
| 3a Non-root, no-data, read-only behaviour from `src/` image | Proven (local check PASS; live uid 10001, empty `/data`, CapEff 0) |
| 3b Verified on existing Container Apps | Proven (demo API `--0000031`, resident `--0000012`) |
| 3c Historical revisions keep tags | Proven (52 revisions, tags `:4d56cf609`, `:8b9553d8b`, `:1f465bf5e`, `:891-1022` retained) |
| 3d New tag deployed | Unproven: registry private, short public window and new demo revision not authorised for this run |
| 4 to 7 | Ticked; not re-audited |

Production-only or not-for-demo items: registry public window (owner-allowed, separate approval); billing reconciliation, DPO/Legal approval and person-run assistive-technology testing not needed for the demo.

Validation: documentation-only, FOCUSED. `docker build` of `src/api/Dockerfile` plus `python3 src/check-container.py api` PASS; link and diff review. mypy, ruff and unit tests not applicable (no code change). `rpi-checks.py --all` not run.
