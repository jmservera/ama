---
title: Generator coverage review repair phase details
description: Task ownership and validation for the bounded review fixes
ms.date: 2026-10-15
---

Task `167-review-fixes`, slug `generator-coverage-review-fixes-167`.
Research reused/Ready from supplied findings and direct source/public metadata
inspection. User explicitly permits honest shape-only issue validation.
No blockers, new dependencies or generated targets.

P01-T01 and P01-T02 complete. Nine focused tests, 307 full core tests, ruff
lint/format and mypy pass. Changes artifact records exact commands and the
initial formatter correction. P02-T01 remains; source implementation is
review-ready with no unresolved decision or unvalidated behavior change.

<!-- rpi:phase id=P01 -->
## P01: Repair and verify

<!-- rpi:task id=P01-T01 -->
### P01-T01: Consistency, open gaps and tests

Owner: primary agent. Modify only the existing coverage.py and
test_generator_coverage.py. Require covered iff delivered. Record missing or
deferred rows as sorted open_gaps IDs and exit 1 from CLI when nonempty.
Retain malformed-input stderr/no stdout. Declare issue_existence not-assessed,
rename routing_validated to routing_shape_validated. Do not derive a false
allowlist from child routes themselves or consuming epics.

Test owner: src/core/tests/test_generator_coverage.py. Add at most two focused
test methods, expanding existing cases for all four user mutations, CLI
exit/output semantics, inverse inconsistencies, ordering and nonmutation.
Use tempfile.TemporaryDirectory() with no repository-local cache scratch.
Existing baseline/determinism tests are regressions, not issue existence or
generated-output acceptance tests. Removals: none.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Documentation and checks

Update core README and pack gap-closure explanation, docs/reference/README.md
index and append docs/reference/log.md because the documented contract changes.
Keep public inventory, scenario binding and provenance unchanged.

Commands from src/core:

```bash
PYTHONPATH=src:tests python3 -m unittest discover -s tests -q
/tmp/zf164/bin/ruff check .
/tmp/zf164/bin/ruff format --check .
/tmp/zf164/bin/mypy
```

Run focused tests first, then all four required checks. Record exact commands,
counts and failures/corrections in changes. No dependency installation unless
the selected command reports missing dependencies; pip only.

<!-- rpi:phase id=P02 -->
## P02: Review and publish

<!-- rpi:task id=P02-T01 -->
### P02-T01: Review once and publish

Primary agent compares final diff with plan, tests and requested constraints.
Record one Review separately from critique; route unrelated acceptance gaps
without a new implementation/review cycle. Check staged paths/diff, authenticated
identity and local noreply author/committer. Commit Conventional Commits plus
requested Copilot trailer; push feat/src-generator-coverage-167 only.
Update existing PR #312 body to honest current claims with Refs #167 and
unmet criteria unticked. Verify remote head matches local and worktree clean.
