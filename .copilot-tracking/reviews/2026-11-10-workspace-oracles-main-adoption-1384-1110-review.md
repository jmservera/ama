---
title: Issue 1384 main adoption review
description: One post-implementation review of the staged ordinary merge of origin/main into the 1384 branch
ms.date: 2026-11-10
ms.topic: reference
---

## Review execution

* Executed once, by the implementing agent, over the staged merge (uncommitted, before the merge commit). Not an independent review: Root performs the independent exact-head assessment.
* Boundary: merge of `origin/main` `111847191d1fde5e8ea18c30c999e99f33721aff` into `90c6c1e4e50b249809442cae5b0d56cf8c24a112` (ancestry holds `3f1fa4810a79b8689aaa8d8e167aa6470b262420`).

## Evidence checked

* `git diff origin/main -- src/api/src` is empty: no production source differs from main.
* The diff of the merged tree against main in `src` is only `script_retry.py` (new), `employee_workspace_browser_check.py`, `workspace_scripts_browser_check.py` and `tests/test_workspace_scripts.py`.
* The single conflict kept both additive sides (imports, constants); the main poll loop and `delayed_companion` are unchanged.
* `workbench_browser_check.py` equals main's (sha256 `9a975543...`); no manifest recipe change needed.
* Validation: ruff, format, mypy (220 files), node --check, workspace units (10) and paging units (12) pass; whole `workspace_scripts_browser_check` and `employee_workspace_browser_check` exit 0 once each; `employee_chat_browser_check` exit 0 on the third execution after two import-path failures that never ran the check (preserved).

## Outcome

* Conformant for the adoption scope: no open material finding in the adoption.
* Outstanding and not claimed: original baseline `sign_out` empty failure remains UNKNOWN; original reds are not called green; whole 1384 acceptance and publication need Root independent review and hosted CI.
* Disclosures: the changes-record edit and the `implement-done` marker were issued in the same tool batch (edit applied first); a PYTHONPATH mistake caused two preserved import failures of the chat check.
