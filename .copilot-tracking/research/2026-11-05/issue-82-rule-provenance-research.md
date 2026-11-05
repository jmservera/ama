---
title: Issue 82 quality rule provenance research (2026-11-05, increment 4)
ms.date: 2026-11-05
---

* Pins: branch fix/quality-rule-provenance-82 at parent cd271cfa5 (tree 6bc669420), main bb3a3b03c, ignored-clean. Prior branch and 10161 source preserved.
* RV-001 (checkpoint finding, preserved): `QUALITY_RULE.source` cites `docs/brds/agentic-retrofit-programme-brd.md FR-008`.
* Actual documents read: BRD FR-008 (line 1523) covers a material change invalidating downstream approvals (AC-011 reused evidence never transfers an approval). PRD FR-008 in `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (v0.21.0, line 1383) and the proper-warm PRD (line 617) say the product enforces deterministic evidence, eligibility, authority, safety, resident, funding, capacity, quality and finance gates before a controlled transition. PRD FR-017 (line 626 in proper-warm; zava-forward equivalent) ties the quality-disposition record's consequential gates to FR-008. So PRD FR-008 governs the quality gate; BRD FR-008 does not substantively govern a checklist-evidence gate.
* Metadata and caller contract: `GateRule.source` is validated only as a non-empty string; consumers are `GateRule.as_record` and `GateResult.as_record` (display). It is not hashed, persisted, in SQL schema or asserted by any test or doc (grep of src and docs). The sibling booking rules already cite `PRD FR-008`, unqualified by path.
* Decision: behavior-preserving annotation. Replace the BRD FR-008 citation with the document-qualified governing requirement. No new rule, version, effective date, reviewer, threshold or approval. The `_UNREVIEWED` reviewer, date 2026-11-05 and version 1 are unchanged.
* Tier: FOCUSED (a string annotation outside SQL, security, finance, infra and deployment). Reassess to FULL and stop if behavior is touched.
* Planning Readiness: Ready.
