# Plan: fix gate blockers (Refs #572)

* [x] Annotate `detail` as `dict[str, object]` in the core test.
* [x] Iterate tabs by index (`tab_buttons`) in the journey check instead of exact snapshotted names.
* [x] `git rm --cached` tools/__pycache__ pyc files.
* [x] Focused validation: mypy, unittest, ruff, journey check x4, `rpi-checks.py --changed`.

Critique: executed once inline; verdict compatible, no conflicting findings.
