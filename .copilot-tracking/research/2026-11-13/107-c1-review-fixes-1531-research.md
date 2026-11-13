# Research: #107 review fixes F1-F4 (1531)

Source: review 107-allowlist-independent-review-1513 (REQUEST_CHANGES on 03915d42d).

* Identity filter: `ai_consumption.safe_identity`/`bounded_model` (limit 512), `_SECRET` regex; callers `assistants.sanitize_identity`, `ai.py` (4 uses), `assistants.py:1588`.
* F1: `Limits.__init__`, `shape_result`, `sanitize_identity` untyped; core mypy fails in new test file.
* F2/F3: values are truncated to 120 before validation; only `sk-` shapes rejected.
* F4: `sk-[A-Za-z0-9_-]{16}` alternative matches inside `task-summarisation-v1`.
* Decision: one 80-char limit, oversized strings map to sentinel (no prefix kept); `_SECRET` = boundary `sk-`, anchored `gh[pousr]_`, `github_pat_`, `AKIA...`, `eyJ...\.`, plus 32+ hex or 32+ unbroken `[A-Za-z0-9_]` run.
* Planning Readiness: Ready.
