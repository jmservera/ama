<!-- markdownlint-disable-file -->
# Plan: recovery main reconciliation (#123), 2026-11-09

Research: [research](../../research/2026-11-09/recovery-main-reconcile-123-research.md). Details: [details](../../details/2026-11-09/recovery-main-reconcile-123-details.md). Tier: owner-selected demo-targeted (no `rpi-checks --all`).

## Phases

* [ ] Phase 1: commit this prospective research, plan, details and state before the merge.
* [ ] Phase 2: re-fetch; if `origin/main` is not `b46a9ad9` stop and replan. Ordinary `git merge origin/main`; no rebase, reset, amend, force or push.
* [ ] Phase 3: verify both tips are ancestors; the append-only `docs/reference/log.md`, `README.md` and evidence pack keep every line from both sides; `paired_equity.py` and its tests are unchanged by the merge.
* [ ] Phase 4: run targeted core tests (paired equity and coupled comparability, subject/anchor identity), core ruff, format check and mypy; `git diff --check`.
* [ ] Phase 5: record changes and one review; commit; report clean HEAD for new exact-head independent assessment and hosted CI after coordinator publication.

## Stop conditions

Unresolved intent conflict; main moved; failing selected test; new scope (SQL, security, policy). No push, PR edit, issue tick, model or cloud call. Refs only.
