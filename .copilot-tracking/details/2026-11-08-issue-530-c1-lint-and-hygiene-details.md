---
title: Issue 530 C1 chat checker lint and ignored-input hygiene details
ms.date: 2026-11-08
---

## Phase 2

* Run `ruff format` and `ruff check --fix --select I` with the gate profile (`--isolated --select E,F,I,B,UP --target-version py312 --line-length 100`) using `RUFF_CACHE_DIR` outside the worktree.
* Split over-long string literals with implicit concatenation only, so every string value is byte-identical. Prove it with an AST comparison of all string constants joined per expression, and a comparison of the AST after normalising the formatting (`ast.dump` equality except the B023 binding and string-constant splitting).
* B023: bind `denied` as a keyword-only default (`def denied_reply(route: Route, *, denied: int = denied)`), never positional, because Playwright passes route and request positionally. Add a lightweight dispatch proof that the callback invoked with one positional route still returns the bound status. Stop if this needs any other change.

## Phase 3

* Add `"employee_chat_browser_check"` to the tuple in the plan (`required_checks` browser group) and in `Runner.browser`. Prefer one shared constant only if the diff stays minimal; otherwise extend both tuples.
* Regression: assert that both the planned commands and the executed `lint` calls for the browser group include `checks/employee_chat_browser_check.py` and that the checker passes the same profile. Verify, for each of the two tuples independently, that the regression fails when only that tuple omits the checker, and assert both the ruff check and the ruff format command for it.

## Phase 5

* Journal: record each ignored path with a file list and SHA-256 per file (opaque identities) in a new external folder under `/tmp/rpi-530-c1-meta`, prove provenance (timestamps after 285280edb, `git check-ignore` rule, no tracked file, editable install origin) and move (not delete) the directories. Anything of uncertain provenance stops the phase.
* After the move, re-point the venv checks with external `PYTHONPYCACHEPREFIX`, `RUFF_CACHE_DIR` and `MYPY_CACHE_DIR`. The venv has separate editable `.dist-info` and `.pth` files, so moving source egg-info is not assumed to break imports; re-prove module origins afterwards and do not replace editable installs.
