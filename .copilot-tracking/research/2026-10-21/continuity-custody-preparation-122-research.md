# Research: non-operative custody, recovery and witness-authority preparation (#122)

Date: 2026-10-21. Task: `continuity-custody-preparation-122`. Base: `origin/main` ca4baf75837de57c99718f7423716d5dc0b0e244. Disposition: executed.

## Live issue evidence (gh, 2026-10-21)

* #122 is OPEN, partially delivered. Its three acceptance criteria and eight incident/restart criteria are all unticked and stay unchanged. The last owner comments record PR #398 (merged at 9d625a09) delivered bounded source remediation only; actual OQ-017 authority, witnessed authorised drill, immutable external Azure-head custody, Azure SQL drill and enforceable legacy-image exclusion remain unmet.
* #113 body (Azure platform, security and data protection epic): Dependencies "None". Its criteria need children closed or deferred and no production claim without measured load, recovery and DPO or Legal approvals. It is a hierarchy parent, not an ordering constraint on #122 preparation. The `gh issue view` GraphQL call hit a rate limit, so the REST API was used.
* Owner preparation authority: preparation of a non-operative protocol only. Witnessed drills, actual authority, Azure immutable storage/SQL configuration, participants and paid execution are not authorised.

## Repository evidence reconciled

| Topic | Source | Observed |
| --- | --- | --- |
| Continuity controls | `src/core/README.md` issue #122 section | Suspend, epoch recheck, restart gate, change register, `zf-evidence-export/1` with `verify_export(expected_head)`. Authority reference is recorded, not verified. Open owner items listed. |
| Constructed incident/restart | `src/core/README.md` issue #221 section | Only a constructed restart drill exists. `actual_hold` stays true; no actual restart route while OD-35/RULE-020 evidence is unavailable. |
| Ledger head custody | `src/core/README.md` issue #114 section | `--seal-years` digests belong in an immutable Blob container; immutability policy is infrastructure and unproven; Azure SQL restore drill (DH-005) not run. |
| Authority | PRD OQ-017 (holders of RAI release, incident suspension/restart and competent review authority); BRD OD-35 under RULE-020 | Unresolved; no named holder. |
| Old-image behaviour | ADR 0002 (rollback disables assistance); #122 criterion "legacy-image exclusion" | An exclusion of pre-gate images is not enforced or evidenced. |

## Gaps (unknown owner/platform decisions)

* Actual incident-restart authority and delegates: UNASSIGNED (OQ-017, OD-35).
* Distinct witness authorisation: UNAPPROVED.
* External immutable Azure head location, retention policy, writer and reader roles: UNAPPROVED, not configured.
* Azure SQL recovery drill, recovery/response limits, supplier contract terms: not run / not agreed.
* Communication owner and audience for a real incident: UNASSIGNED.
* Enforceable exclusion of pre-gate images: no evidence.

## Planning readiness

Ready. Only the existing core README section plus tracking changes are needed. No dependency on the four concurrent issue owners (agents README, cutover pack, KB index/log, CSS/browser, map docs). No runtime code or tests required.
