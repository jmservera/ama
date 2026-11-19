# Changes

* src/core/.../ai_consumption.py: helper plus report field cost_per_accepted_outcome.
* src/api/.../server.py: unavailable-branch field.
* Tests: core skill_breakdown (3 cases), api consumption tests updated.
Validation: core ai_consumption tests OK (55); api test_ai_consumption_api OK (40); accessibility baseline OK (13); mypy, ruff check/format clean in core and api. Not run: full suites, hosted CI. Note: installed editable packages point at another checkout, so PYTHONPATH pointed at this worktree.
