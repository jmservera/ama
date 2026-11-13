<!-- markdownlint-disable-file -->
# Details: #74 home case regression slice (issue-74-home-case-regression-2300)

## P1 API tests (HTTP over the existing loopback server)

* Reuse `setUp` (fixture plus CON-1 provider). Sam is `store.data["staff"][0]` and logs in with "synthetic-only".
* Non-finance: for ZF-2 and ZF-3, `home.cost_allocation_restricted is True`, `home.cost_allocation is None`, `building.costs_restricted is True`, `building.get("costs") is None`; serialise the response and assert "6000.00", "12000.00" and "SYN-ESTIMATE" are absent.
* Finance: pam sees allocation `[{shared_cost_id COST-1, amount_gbp 6000.00, source SYN-ALLOCATION}]` for both homes, building costs `[{id COST-1, work_id WORK-1, amount_gbp 12000.00, source SYN-ESTIMATE}]`, `cost_allocation_restricted` false and `building.get("costs_restricted")` falsy (the key is absent for finance roles; CR-001).
* API mutation controls are listed under Browser check mutation controls below (scratch only).

## P2 Browser check

* `home_case_data()` adds to ZF-2 document id `OWN-EVIDENCE`, name "Synthetic own-home survey" kind Survey, and quality measure "Ventilation extract" state Accepted (shape copied from the sibling quality in `building_fixture`).
* A small helper reads home, building and main text for a case id after navigating the hash. Tokens: `OWN_ONLY = ("Synthetic own-home survey", "Ventilation extract")`; `SIBLING_ONLY` stays as is (ids such as SIBLING-EVIDENCE are not rendered, names are).
* Existing sibling-absence check stays ZF-2 only (CR-002). The isolation claim covers the sentinel records only (CR-006).
* ZF-2: own tokens in home region, not in building region; sibling tokens nowhere in main; the exact item `SYS-1: Shared ventilation. Source: SYN-SURVEY` in the building region, not the home region (CR-004; "Shared ventilation" alone also matches WORK-1). ZF-3: sibling documents ("Synthetic survey metadata only") and quality ("Loft insulation") in home region; own tokens nowhere in main; same SYS-1 rule; GBP 6000.00 in home region and GBP 12000.00 only in the building region.
* The existing read-only, heading count, reflow, axe and write-guard checks run after both pages, so they also cover ZF-3 reads.
* Mutation controls (CR-003, CR-005): copy `src/` and the check to an external scratch tree, run the whole check from there, verify the served `app.js` hash, then mutate only the scratch `app.js` or check, one control per family: sibling document rendered in home list; sibling quality rendered; own quality dropped; system item moved into the home region; seed without the own document. For the API tests, scratch-copy mutations of the amount-leak assertion (allow amounts in a restricted body via a pam cookie) and finance assertion. The named new assertion must fail, not merely the run.

## Validation

Focused tier per owner decision D4 and #1294: affected unit tests and the modified browser check read locally; hosted CI for the exact head is not read here (no push).
