# Details: tools/ verification

* Modules: the twelve test_*.py files plus rename-zava-tests.py listed in the research file.
* Command per module: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v tools.<module>` is not importable as a package, so use `python3 -m unittest discover -s tools -p <file> -v`.
* Logs go to /tmp/tools-verify-1222/<module>.log; the exit code goes to <module>.rc via `$?` captured immediately.
* Counts parsed from the "Ran N tests" and "skipped=" lines.
* Success: all exit codes 0, no untracked files besides .copilot-tracking.
