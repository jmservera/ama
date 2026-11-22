# Issue 2254 verify changes (2026-11-22)

Tier: focused (no src change). Run: `test_sqlreads -k 2254` OK; live re-probe read-only.

## Changes

* docs/reference/research/issue-2254-verify-2026-11-22.md plus probe, result JSON and screenshot. No source edit; the fix is on main (1be6940b90 via a6c0910c97).

## Criteria

| Criterion (issue expectation) | Status | Evidence |
| --- | --- | --- |
| One definition of safety issue open across tile, map and list | Proven | live tile 23, map 23, list 23; regression test |
| Live demo shows equal counts | Proven (API level) | probe-safety-count-result.json, revision 0000053 |
| All cases page text shows the same count | Unproven | page text not captured; API list total used |
| Live row cause (stored column) | Unproven | SQL private; inferred, see earlier note |
| Deployed image equals the fixed commit | Unproven | digest not mapped to a commit |
