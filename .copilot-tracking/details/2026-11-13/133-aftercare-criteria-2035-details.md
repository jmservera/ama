---
title: Issue 133 aftercare criteria phase details
task_id: 133-aftercare-criteria-2035
date: 2026-11-13
---

## Phase 2

* `src/core/src/zava_forward/core/aftercare.py`: new patterns in `PARAPHRASE_PATTERNS`; `propose_pack` no longer touches `rec["history"]`; `from_state` refuses a closed remedy lacking outcome or evidence.

## Phase 3

* `src/core/tests/test_aftercare.py`: four closure and restore tests, guard phrasing test, pack no-mutation test; existing pack review test now asserts whole-view equality.
* `src/core/tests/test_aftercare_intake.py`: restart closure test, no pack route test.

## Phase 4

* `src/api/src/zava_forward/api/web/aftercare.js`: helpers `acWhole`, `acHouseholds`, `acRowUnresolved`, `acCountLine`, `AC_WINDOW_LABELS`; malformed values read Unknown.
* `src/api/tests/test_aftercare_screen.py`: evaluator content test and malformed-totals test.

## Validation

pip-only venv `/tmp/venv-133ac-2035`; commands as in the task statement.
