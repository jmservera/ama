---
title: Issue 81 score-commit merge plan and details
description: Prospective plan and step details for one normal merge of pinned main 8af3aea6
ms.date: 2026-11-07
task_slug: issue-81-merge-8af3
status: prospective
research: ../../research/2026-11-07/issue-81-merge-8af3-research.md
---

Choice: one NORMAL `--no-ff` merge of `8af3aea6b042f5dfb3305e18334439717f7c5649`; no rebase, force or rewrite. Critique: the applicable convention (one critique per final candidate) was executed for the preceding merge plan; this is a repeat of the same metadata-only operation with identical proof design, so no new critique is run, and that is recorded as a deliberate reuse, not a waiver of the original Revise verdict.

Steps:

1. Commit these records as PRE; verify clean, HEAD equals PRE, `origin/main` still `8af3aea6`; otherwise stop.
2. Merge with repo-local noreply identity (fresh `gh api user`) and Copilot trailer. Stop on conflict.
3. Proof: parents are PRE and `8af3aea6`; `git diff --raw PRE HEAD` equals `git diff --raw 7551e50e 8af3aea6` including modes; blobs of `appointments.py`, `gates.py`, `procurement.py`, `quality.py`, `test_quality_procurement.py` and the full `src/` tree equal PRE; the incoming `latest.json` parses as JSON; `git diff --check` clean.
4. Write changes and one author Review (tracking only), commit, report status.

Exclusions: no tests, installs, services, FULL, push, PR, child change, ticks or approvals.
