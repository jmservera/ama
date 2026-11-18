# Details: issue 153 live audit

Phase 1: scripts audit.py, spa.py, errors.py, resident.py read sign-in files at runtime; outputs JSON and PNG.
Phase 2: findings F1 to F5 and passes P1 to P6; criteria table; unticked criterion stays unproven.
Phase 3: append dated section to ux/content-standard.md (ms.date bumped); README index row; log entry.
Phase 4: verify relative links resolve; git diff --stat; no pycache or secrets staged.
Non-applicable: mypy, ruff, unit tests (no src or infra Python change); rpi-checks not run.
