# Plan: 153-btns-rebase-main-2013

1. Rebase `--onto 2489d839e9 b1d4bc59d` before creating state (linear history).
2. Confirm `git diff 2489d839e9..HEAD -- src/` holds only app.js and test_app_js_notices_content.py.
3. Scratch pip venv `/tmp/venv-153rb-2013`: run listed api/core tests, ruff check/format, mypy.
4. Remove only that venv; commit artifacts (`Refs #153`); witness `commit-complete`; no push.

Critique: see `critiques/2026-11-13/153-btns-rebase-main-2013-critique.md`.
