---
title: "#521 unified evidence pack changes"
ms.date: 2026-11-13
---

* Cherry-picked 85b49947c, 0f3710e12, e4b47e767 onto 8ca5685b7 without conflicts (now 42b1d988a, 02da2bbf1, 5d55e5805).
* Fixed #152 plan line 3 links to `../../research/2026-11-13/` and `../../details/2026-11-13/`.
* Markdown link check over 45 changed .md files (added lines only for pre-existing files; anchors included): 25 links, 0 broken. Pre-existing broken links in `docs/reference/log.md` and `infra/README.md` were not touched.
* Regenerated `docs/architecture/cutover-reference-inventory.tsv` (5 line-number shifts in src/agents, src/api, src/core READMEs) with `cutover_audit --write`; check mode PASS (130 matrix rows, 1913 locations).
* Tests: `test_cutover_audit` 9 OK; `infra.tests.test_bicep_policy` 61 OK (core and orchestrator pip-installed in a temporary venv, removed); `docs/capstone/history/cowork-main-presentation/test_build_assets.py` 26 passed (`tools/capstone/test_build_assets.py` does not exist).
* `docs/capstone/source/validation.json` hashes for baseline, candidate, manifest, catalog, speaker script and Q&A match current files; builder and native helper hashes are untouched because no tooling changed.

## Review disposition

Independent `code-review-readiness` found no blocking issue. Low findings applied: link check method was a throwaway script resolving every inline and reference link and heading anchor in files changed vs 8ca5685b7 (added lines only for pre-existing files); inventory diff is 5 insertions and 5 deletions in the TSV only. Pre-existing broken links in `docs/reference/log.md` and `infra/README.md` are deferred as out of scope. No active reference to `tools/capstone/test_build_assets.py` was found outside tracking history.
