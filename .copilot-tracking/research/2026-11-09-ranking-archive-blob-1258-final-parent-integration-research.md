# Research: final integrated #1258 parent candidate (2026-11-09)

Refs #1258, Refs #1259, Refs #136. Slug `ranking-archive-blob-1258-final-parent-integration`. Research disposition: executed (read-only inspection) plus reused valid evidence; Planning Readiness: Ready. Native record only; independent coordinator assessment of the final head remains required.

## Actual state read

* Local branch `fix/ranking-archive-ancestor-durability` HEAD `99814198079c7c8fcd641497826986c706627b0f` (tree `0658fe7f883c5efa09ca286cb026be5cde16ada9`), clean, the C6 head.
* Remote topic `origin/fix/ranking-archive-ancestor-durability` `ac41cce5b1a7ded6a33fe5c57786affbca4783c0`, tree `81480e6c89086771353a2a6957568bf102986156`. The local HEAD is an ancestor of it (`merge-base` equals `99814198`); the remote adds `fbf0a0ab5` (#1325, child 1259) then `ac41cce5b` (#1327, child 136), 102 paths, +3331/-4.
* `origin/main` (fetched) `2be660e9d290f95ff05fc5a56d6539768576732b`; the topic carries main `5c3b8b4b`. Main movement since `5c3b8b4b` is 38 paths: tracking records plus `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `docs/reference/log.md`. Zero paths under `src/`, `infra/`, `tools/` or `.github/`.
* PR states (gh): #1325 and #1327 MERGED into the topic (base `fix/ranking-archive-ancestor-durability`), not main. #1325 merge `fbf0a0ab5`, #1327 merge `ac41cce5b`. Issue #1258 OPEN. No parent PR exists.
* `git merge-tree --write-tree origin/main origin/fix/...` is clean, tree `5f45a5491e9d2ecf4a846e6cba7f840d2c4f9a23`, equal to the coordinator figure. Local HEAD with the remote is also clean (a descendant).

## Source and input identity (git tree hashes, 12-char prefixes)

| Path | local C6 | remote ac41 | main 2be660e9 |
| --- | --- | --- | --- |
| `src` | 69a3ce28499f | f0df7dc42466 | 86bc00e19a16 |
| `infra` | b0969f8b7b8c | d94040329d54 | b0969f8b7b8c |
| `src/agents` | 237bf28b67cc | 237bf28b67cc | 237bf28b67cc |
| `src/core/pyproject.toml` | 88598decb2dd | 88598decb2dd | 88598decb2dd |
| `src/api/pyproject.toml` | 9b261f29fdcc | 9b261f29fdcc | 9b261f29fdcc |
| `.github/workflows` | 29eb03ea759e | 29eb03ea759e | 29eb03ea759e |
| `tools` | 74ad3cb586db | 74ad3cb586db | 74ad3cb586db |
| `docs` | 837accece692 | 837accece692 | 1191a55f6229 |

Meaning: workflows, tooling, package manifests and the agents project are identical across all three. `src` and `infra` change only through the two merged children, so the integrated `src` and `infra` must equal ac41's (`f0df7dc4...`, `d94040329...`, matching `136-combined-target-binding.txt`). Main's docs differ only by its own documentation additions.

## Valid evidence reused (not rerun)

* Parent C6 (originals unchanged): Core `test_ranking*` 127 OK with and without SDKs, API wiring 35, project-root ruff 0.17.1 check and format, mypy 2.4.0 clean (core 279 files, api 203 files); independent Functional review `functional-findings-final.json`: approve, 0 findings, source-level only.
* Child 1259 (#1325): Core 146 and API 36 checks, project-profile lint, format, mypy; independent review `functional-findings.json`: approve, 0 findings; hosted CI `Source projects CI` 10 of 10 pass (run 42679149150) on the PR head `c8cb220c`; merge `fbf0a0ab`, tree `2131877a`, recorded equal to the reviewed `c8cb`.
* Child 136 (#1327): infra 100 tests, Bicep build, lint, build-params, pinned ruff; independent reviews `functional-findings.json` and `combined-target-findings.json`: approve, 0 findings, including the five sibling source changes against the 136 infra delta, no new dependency check needed. Hosted CI 10 of 10 pass (run 42683860440, API 15m36s, MSSQL 6m23s, Core 5m5s) on PR head `96f69163`, merged as ac41 whose tree equals the independently qualified prospective tree `81480e6c`.
* `136-combined-target-binding.txt`: parent/src, child1259/src, prospective/src all `f0df7dc42466...`; child136/infra equals prospective/infra `d94040329d54...`.
* Limits carried: the 136 run recorded C6 raw logs only by attribution; the hosted run is a `pull_request` run on the PR head and its merge ref is not inspectable locally; the equality of the tested merge ref to ac41 rests on the recorded tree binding, not on an observed local rerun.

## Functional union to verify by reading, not assumed

Flag-off folder/manual; flag-on private Blob with no folder fallback; direct conditional-create versus runner listing admission; unknown/overdue status; managed identity environment wiring; default-off optional unlocked retention; no approved WORM, folder-record migration, delete-role narrowing or live provisioning implied. Unmerged 1288 quality excluded. No duplicate `NextMarker` hardening is asserted as a blocker (child review: retained critique edge, not a confirmed defect).

## Decisions for planning

* Source files will not be edited. Integration is two ordinary merges; the source/infra/tools/workflows tree must equal the declared bindings after each.
* No test rerun is required unless a source or dependency input differs from every qualified identity. A rerun is justified only on an input mismatch; the smallest existing check would then be chosen.
* No SQL, browser, Docker, `rpi-checks` or full gate; their absence is a stated limit.
* C6 stays spent, C7 to C10 four remain; this task is not a productive correction.
