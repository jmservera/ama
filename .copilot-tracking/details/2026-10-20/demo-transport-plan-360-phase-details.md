<!-- markdownlint-disable-file -->
# Phase details: demo-transport-plan-360

## Phase 3 content map (infra/README.md section)

1. Status and preserved evidence: three attempts, removal confirmation, unchanged original roster, no SQL projection. Source: issue comment 6277108234. Contradiction F1 flagged.
2. Requirement-to-mechanism table (run, query, worker, manifest, image, authorization, confidentiality, integrity, freshness, completeness, fail-closed parsing), each with current state and gap.
3. Options table T1-T7 and selected proposal T1 with synthetic feasibility.
4. Proposed binding extension (design only): AEAD associated data v2 = `[2, run, operation, input digest, query id, worker script SHA-256, manifest SHA-256, image digest, result schema, not-after]`, controller recomputes from repository files and ARM-read job image before trusting; worker claim self-asserted caveat.
5. Fail-closed rules: strict tag name grammar, per-run prefix only, contiguous indexes, `count` consistency, maximum frames/lengths, unknown prefix-matching or duplicate/extra frames refuse, AEAD failure refuse, terminal Succeeded required, deadline refuse, no partial use, no decompression without a bound, cleanup confirmed.
6. Script-oriented plan S0-S7 with offline tests (all synthetic) and exit criteria; no execution.
7. Costed execution preconditions (later): no new resource for T1; one temporary job at most 600 s one replica; cost from official pricing at plan time; approval after #126 plan, not before.
8. Tenant-administrator/operator checklist with evidence fields and stop conditions.
9. Non-claims.

## Validation

Markdown/link review, git diff, existing infra tests unaffected (docs only), full local gate.
