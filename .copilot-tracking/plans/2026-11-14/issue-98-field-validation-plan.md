# Issue #98 plan (2026-11-14)

1. Treat a field as confirmed only if its last history event is a reviewer accept/correct matching state and value; otherwise report a Fail issue.
2. Add template_version and input_version to each exported field (own last review version, 0 if never) and each attachment (pack version).
3. Add focused tests in test_form_export.py; run targeted tests, ruff, mypy.

Critique: executed once inline; compatible. Per-field input_version uses the field's own review version so unrelated reviews do not stale it.
