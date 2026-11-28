# Issue 1259 live r11 details

Phase 1: in `src/core/tests/test_ranking_publication_runner.py`, add a helper that wraps `os.stat` so the first call on the archive path raises FileNotFoundError after creating the replacement (file or dangling link). Assert `go("verify")` gives `problem`, latest None, overdue None, one path-free problem; `go("schedule")` gives `problem` with due None; replacement left untouched.
Phase 2: `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_ranking_publication_runner test_ranking_publication -q`; mutate `_names` to `return []` after the FileNotFoundError and expect the new test red.
