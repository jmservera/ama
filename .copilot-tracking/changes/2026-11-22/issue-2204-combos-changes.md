# Changes: issue 2204 combinations live (2026-11-22)

Tier: focused (no `src` change). Live effects were transient and are reversed: temporary Contractor roster row inserted and deleted (staff table 2 rows before and after); role assignments swapped per case; ProgrammeManager restored (final Graph read: only ProgrammeManager). Kat Larsson's row and assignments untouched.

Files: `docs/reference/research/issue-2204-contractor-capability-combos-live-2026-11-22.md` (+ evidence folder), `docs/reference/README.md`, `docs/reference/log.md`, tracking artifacts, evidence under `.copilot-tracking/evidence/2026-11-22/issue-2204-combos/`.

Divergence: `az containerapp exec` was rate limited (429, 600 s) once; waited. First capability pass did not record error text, so three cases were rerun.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Contractor with roster binding signs in and sees only permitted views | Proven (test account, temporary row); Kat's own sign-in unproven (no credential) | research note, Contractor table |
| Kat Larsson binding path | Proven present in Azure SQL (correct tid, oid, company, Contractor role in Entra); earlier unauthorised report not explained | research note, roster section |
| Four capability roles stacked on a staff role sign in | Proven (200, claim in `rule_roles`, staff views unchanged) | research note, capability table |
| Capability gate effect | Proven only for RegulatoryChat; RuleAuthor, RuleOwner, AIRestart unproven (law store not loaded; no drill) | research note |
| One wrong-role denial; no credentials | Proven; credential scan no match | note, scan |
| Original assignment restored | Proven (only ProgrammeManager) | live-combos.json `restored` |
| Issue criterion 1 overall | Partly proven; tick is the owner's decision | note |
