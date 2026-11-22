---
title: Issue 1847 live changes
ms.date: 2026-11-22
---
# Changes
No source or test change. Artifacts and a research note only. Refs #1847 (no closing keyword; criterion 6 unproven). Head tested: dcaf271ad3. Tier: FOCUSED.

| # | Criterion | Demo status | Evidence |
| --- | --- | --- | --- |
| 1 | Layouts documented, rejection behaviour | Proven | src/core/README.md "Nomination test layouts (#1847)"; docs/reference/research/nomination-bootstrap-isolation-proof-1847-2026-11-22.md |
| 2 | Both orders, fresh processes | Proven | Source 55/55 OK both orders; editable both imported; noneditable bulk-first rejected explicitly (research note outputs) |
| 3 | Origins and identities | Proven | Probe: store_file under worktree src, all identity flags true |
| 4 | Regression fails on original, passes with fix | Proven | Original: failures=1 errors=20 and bootstrap failures=2; fixed: 58 OK |
| 5 | No family purge, foreign checks kept | Proven | sys.modules read-only scan only |
| 6 | Full gate and external receipt | Unproven | Forbidden for the demo by the brief; not triggered (no src change) |

Validation: ruff format --isolated --line-length 100 --check on both test files: pass. Test file temporarily reverted for the adverse run and restored; git status clean of src changes. Unmet DEMO criteria: none.
