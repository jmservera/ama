# Changes: issue 2204 live roles (2026-11-22)

Tier: focused (no src change). Refs #2204.

Files: docs/reference/research/issue-2204-all-roles-live-2026-11-22.md (new), docs/reference/README.md (index), docs/reference/log.md (entry), evidence folder .copilot-tracking/evidence/2026-11-22/issue-2204-live/ (script, JSON, 26 screenshots, logs, final assignments).

Live actions: 13 app roles assigned one at a time to the test account on zava-forward-api via Graph, each removed after use; ProgrammeManager restored and verified (final-assignments.txt). No other Azure change; nothing to delete. Divergence: a first full pass was cut by a tool timeout with RuleOwner assigned; restored by hand, script made incremental, claims verified, stale-claim runs repeated.

## Per-criterion table

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Proven for 8 roles incl. admin; 5 roles (Contractor, RuleAuthor, RuleOwner, RegulatoryChat, AIRestart) proven refused alone, combined-role live runs unproven | live-all-roles.json, screenshots, research note |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven | per-role 403/401 and denial screenshots; credential literal scan 0 matches |
| 3 | Evidence recorded | Proven | research note, evidence folder, this record |

Open: /api/retention 500 for ProgrammeManager (unexplained); /api/work-orders probe path unverified.
