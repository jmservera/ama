<!-- markdownlint-disable-file -->
---
title: Issue 350 current-main readiness plan critique
description: One independent pre-merge critique of the current-main readiness plan
ms.date: 2026-10-25
---

Execution: complete, once, read-only `rubber-duck`, run after the research, plan and details and before the merge. Verdict: **Revise**. Blocking 1, non-blocking 2.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-301 | Blocking | The fresh-environment check is underspecified; the checker imports installed `src/core`, `src/agents` and `src/api`, and main changed `src/core`, so a stale venv would not test the merged tree. | Accepted. Disclosure (RV-302): the plan and phase details were not amended and still read conditionally; the stricter procedure was applied at execution only. Procedure: extract `git archive` of the merged HEAD to a new `/tmp` directory, create a new venv, `pip install` the three archive packages (about a few hundred MB, pip cache), record the imported `zava_forward` package paths, run the tests with that venv, then delete the directory. The older `/tmp/c1-350` venv is not used as evidence. |
| PC-302 | Non-blocking | Fetch `origin/main` and re-verify the target SHA immediately before merging. | Applied: `git fetch origin main` and a SHA check against `ea5577b2` (or the new SHA, recorded) before `git merge --no-ff`. If main moved, the new SHA is recorded and used only if no new conflict needs a behaviour decision; otherwise stop. |
| PC-303 | Non-blocking | State that merge plus focused tests establish candidate gate readiness only. | Applied: the previous receipt for a9bdae31 is invalidated by any new head; a fresh complete gate, push and acceptance remain outstanding. |

Reviewer assessments: RV-201 is non-blocking and needs no owner decision for the bounded merge; overall acceptance of the retry review stays an owner or coordinator decision. No direct risk to the checker contract from main (identity, projection, ranking, taskqueues and workbench navigation are unchanged; main did change `sqlstore.py` and `seed_merge.py`, which are outside the checker contract; wording narrowed after review finding RV-303). Disposition wording avoids invented acceptance.
