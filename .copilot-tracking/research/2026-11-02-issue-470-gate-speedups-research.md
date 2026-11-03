---
title: Issue 470 gate speedups research
ms.date: 2026-11-02
---

Research executed (existing evidence reused plus code reading). Issue #470 criteria 1 to 3 and 5 are already met on main (`--changed` selection with partial scope, `--verify-receipt` scope rejection, `--jobs` with a single heavy lock, selection/scope tests). Criterion 4 (measured before/after full-run time) is unmet and stays unmet: the owner forbade running the full gate in this task.

Owner approval 2026-11-02 (jmservera): six gate-speed recommendations, all approved. Code evidence in `tools/rpi-checks.py`:

* Scheduler already overlaps independent groups; `docker_lock` serialises SQL and images; `worker_limit` budgets 2 CPUs and 4 GiB per worker (2 workers on the 4 vCPU, 15 GiB box). `--jobs` defaulted to 1.
* `project-api` is one `unittest discover` command (about 750 s) next to `project-core` (about 460 s) in a roughly 1800 s focused gate (owner figures).
* `changed_groups` already skips untouched projects and images but the receipt did not record skipped groups or reasons.
* Scanned images always used `--no-cache`; Trivy gates every built image regardless.
* `clean_identity` requires the reviewed base to equal current `origin/main`, so any unrelated main move invalidated every receipt.
* `verify_commands` matches receipt rows to the trusted matrix in order within a group, so concurrent shards need a deterministic row order.
* Discovery is by `tests/test*.py` top-level modules for `src/api` (89 modules at this head, no nested test packages); `unittest discover -k 'module.*'` selects a module by test id and was verified on a fixture.

Decisions taken: shard only `api` (max 3) by `-k` module patterns balanced by blob size; keep SQL and image builds serial under the existing lock; make layer cache the default with `--fresh-images` as the opt-out; relax the base only for partial receipts and only with explicit proof; add `--stack` and `--stack-member` for batch gating. Planning readiness: Ready.
