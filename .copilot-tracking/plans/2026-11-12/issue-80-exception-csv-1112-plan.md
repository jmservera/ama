<!-- markdownlint-disable-file -->
# Plan: #80 browser-built exception-summary CSV, synthetic demo (issue-80-exception-csv-1112)

Research: [research](../../research/2026-11-12/issue-80-exception-csv-1112-research.md). Details: [details](../../details/2026-11-12/issue-80-exception-csv-1112-details.md). Critique: [critique](./issue-80-exception-csv-1112-critique.md). Contract: [PR1462 details](../../details/2026-11-11/issue-80-exception-contract-2122-details.md).

Branch feat/demo-exception-summary-csv-80-1112, base 139176fa0382add781b1830b1ac9db785ed086fe, local-only. Eventual PR targets main with `Refs #80` only.

Tier classification: focused tier. Basis: web-only change inside the existing screen, no permission, secret, deployment, dependency, workflow, Dockerfile, gate-semantics or security-control change, no new endpoint or data exposure. Run only targeted unit, lint, type and the one browser check; no full gate, no `--changed` receipt claimed.

## Phases

* [x] P1 Research
* [x] P2 Details
* [x] P3 One critique of the final candidate plan and details; apply compatible findings
* [x] P4 Implement role-screens.js, tests, browser check, README note
* [x] P5 Validate with targeted checks and the fresh web-design-guidelines review
* [x] P6 One author review after implementation
* [ ] P7 Commit locally with the repo-local noreply identity and the Copilot trailer

## Boundaries

No push, PR, issue, board, merge or branch-protection action. No server, store, endpoint, producer, appointment, permission, importer, infra or workflow change. No second API call. No Capacity C6, defaultfive renewal, #135 recovery or operational export approval. No named human, operational or assistive-technology acceptance claim and no issue tick. The PR1462 proposal files are unchanged.

## Decisions carried

* Existing audit-on-view and audit-on-denial stay; no blanket zero-audit claim is made.
* No download for empty, incomplete, malformed, failed, roles-not-named or denied views.
* Reference is per-view, not a stable identity.
