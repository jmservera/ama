---
title: Issue 79 r32 research, main b284d0d3 score-only adoption
ms.date: 2026-11-07
---

* Preflight: root `9dad2aba7b10d28e567ccaae3da4453906748f5f`/tree `9b20ae641f470e0cb7adb010fedf69f4007babf8`, branch `feat/ranking-publication-runner-79`, `git status --short --ignored` empty. Fetched `origin/main` is `b284d0d3e8ebed24d40bf9eb1e23de1ae9101d01`, a direct child of `7c6d135d` (an ancestor of HEAD).
* Delta `7c6d135d..b284d0d3`: only `.github/rubric/scores/latest.json`, 4 insertions and 4 deletions (scored_at, source commit 7c6d135d, run URL, solution-code fingerprint). No source, test, docs log or RPI change.
* The root's latest.json equals the 7c6d135d version, so the merge is a clean auto-merge (`git merge-tree` tree `0e43f52a`, no conflict).
* The score JSON is generated provenance for main 7c6d135d. It is not an assessment of this candidate and not approval.
* Light-only: the earlier 9dad executable regressions (Core 60, API wiring 18, defaults 7, pinned-venv correction) stay source-equal history, not new-head FULL. A score-only merge does not need repeated runtime checks.
* The command-correction explicit-path format diagnostic (exit 1) stays recorded: `checks/*.py` is configured-excluded and only bypassed by explicit paths. Not a claim that the checker is formatted.
* Child 1231 (`14ea298a`) incorporated 9dad and needs one further propagation of the final root; not touched here.
