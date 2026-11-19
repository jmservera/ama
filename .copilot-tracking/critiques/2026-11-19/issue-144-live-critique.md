# Critique (executed once, 2026-11-19): verdict proceed

* Risk: a script cannot prove pipeline provenance. Accepted; it states provenance unproven and only classifies refs.
* Risk: infra tier. Script is read-only, no Bicep, workflow, permission or deploy-semantic change: FOCUSED. Doubt resolved by no write path (stdin or file JSON only, no az call inside).
* Risk: private registry unreachable. Script takes optional recorded tag manifest; absent tags report `tag-unverified`, never pass silently.
