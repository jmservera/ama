---
title: Issue 79 r30 changes, merge of main 7c6d135d
ms.date: 2026-11-07
---

* One normal `--no-ff` merge of `origin/main` `7c6d135df740aec33ddb1961da3f5f0e8706c8ff` (hotfix 1263) into planning head `80d266acbda27520bebe23a790b0c120660f4e44`; merge commit `8598d06d03f893afa8811f080b543cfa9693e273`, tree `0dddb816feba58f9c46311ffb96bf703854baeaf`. Only `docs/reference/log.md` auto-merged; no conflict, rebase or rewrite. Old root `8010a486` preserved at `preserve/issue-79-pre-main7c6d`; remote 181a1c1b and child c18f45f2 untouched.
* Proofs: the three incoming source, check and manifest blobs equal main; every other non-tracking path equals the planning head, so root source (private staging, `_confirmed`, `written`, runner outcome) is unchanged; the merged log has zero deletions against both the root and main; `git diff --check` clean.

## Checks (own-source venv, `ranking_publication` imported from this worktree, `PYTHONDONTWRITEBYTECODE=1`, scratch `/tmp/g79-main7c6d-1107`)

* Core ranking publication and runner OK; API ranking wiring 18 OK; core scenario manifest 8 OK; workbench live defaults 7 OK (after a missing-dependency failure: the repository pins `playwright==1.64.0` but I installed unpinned `playwright` 1.64.1 into the existing venv, library only, no browser download or launch).
* Ruff check clean on four files; mypy core 268 files clean. `ruff format --check` reports the incoming `workbench_browser_check.py` (byte-identical to main) as unformatted; pre-existing and inherited, not changed here.
* Not run: FULL, `--changed`, browser, SQL, Docker, scanners, child. Hotfix 1263 receipts do not validate ranking.
