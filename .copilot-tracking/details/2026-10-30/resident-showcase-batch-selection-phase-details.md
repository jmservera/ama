---
title: Resident showcase batch selection phase details
description: Task-level implementation and validation expectations
ms.date: 2026-10-30
---

## Task Identity

521-pr590-batch-selection; resident-showcase-batch-selection. Refs #521.
Initial direction: test-only correction supported by research C1-C5.
No unresolved implementation decisions.

<!-- rpi:phase id=P01 -->
## P01: Correct and validate batch selection

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement helper and semantic regression assertions

Add a private zero-argument helper near the renderer fixture constants.
Unpack the unique rendered batch containing the exact view-definition marker.
Use it for rebuild and restoration in the existing empty-sensor test.
Query sensor_home_id alongside sensors_json and require HOME-A/[].
Add at most two renderer tests using unittest.mock.patch.object: relocate the
real rendered view batch across positions; reject absent and duplicated matches.
No indexed selection elsewhere requires correction (research C1).
Completion: no index reliance, preserved empty fixture and cleanup.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Execute focused validation and record evidence

Depends on P01-T01. From src/core run python -m unittest discover -s tests
-p test_resident_showcase_sql.py -v, ruff check tests/test_resident_showcase_sql.py,
and ruff format --check tests/test_resident_showcase_sql.py.
System Python lacks the namespace package and Ruff. The existing pinned venv at
/tmp/ama-521-validation-20261030/venv successfully ran the baseline: 38 tests,
27 loopback SQL skips, Ruff check and format exit 0. Reuse it without reinstalling.
Report executed/skipped counts and exact commands in changes evidence.
Use a bounded in-memory mock-backed experiment: instantiate SqlBoundaryTests
and call test_empty_sensor_tables_preserve_valid_empty_history directly, with
add_case/q/reader mocked and as_user returning HOME-A/[] for baseline pass.
Then patch the helper to return the migration and as_user to return NULL/[]:
require AssertionError from the actual semantic assertion. Restore patches,
repeat the baseline and focused discovery. Additionally mutate the helper to
the old index and require the always-run selector regression to fail.
No skip decorator may substitute for directly executing this experiment.
This proves the assertion path with simulated query results, not SQL execution.
Heavy local SQL execution, if available, requires the shared flock; it may only
use a newly owned throwaway local container, never ambient DB settings.
No full publication gate or push is part of this bounded correction.

Critique PC-001 resolved by the explicit experiment above. PC-002's unsupported
filesystem prohibition rejected in the plan; preserve the user-authorized lock.

## Completion

P01-T01 and P01-T02 complete. Commands and results are recorded in the changes
artifact. No heavy execution occurred; local real SQL remains unperformed, with
27 opt-in skips explicit. Mutation evidence uses simulated query results and
the actual affected method, not a claim of SQL engine validation.
No remaining task, blocker, amendment or material divergence.
