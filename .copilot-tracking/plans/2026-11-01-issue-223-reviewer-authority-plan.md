---
title: Issue 223 reviewer authority gate plan
date: 2026-11-01
---

Phases
1. Golden file: add `reviewer_authority` (status provisional, task, authorised reviewers, required evidence, OQ-017 note).
2. Module: gate requires authorised reviewer and complete evidence; add unauthorised-reviewer negative control (same competent panel, reviewer not in authority) that must fail; report authority in evidence; new check.
3. Tests for the above; README line update.
4. Validate: unittest, ruff check, ruff format --check, mypy in src/agents.

Critique (single pass, self): keep authority provisional and data-driven; do not claim OQ-017 resolved; no new service. Applied directly.

Correction cycle (2026-11-01): enforce authority task match and required_evidence mapping in gate_satisfied; source_reason is exempt for correct controls (no discrepancy to cite); add negative tests.

## Correction cycle 2026-11-01

* Move unittest.main() to end of file (done).
