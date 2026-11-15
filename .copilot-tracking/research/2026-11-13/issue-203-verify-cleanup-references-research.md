<!-- markdownlint-disable-file -->
# Research: Issue #203 criteria 1 and 2 (legacy references and relative links)

* Task: `issue-203-verify-cleanup-refs`; branch `docs/demo-203-verify-cleanup-refs-2220`; base `origin/main` 36a2a57335dc95273292d6fda54fe60ff9f9b4f9
* Research disposition: executed. Planning Readiness: Ready.

## Scope

Issue #203 criterion 1: repository-wide search for `mvp/` and `prototype/` returns only intentional historical references naming the archive tag (`v0.21.0`), and `zavaforward_mvp` appears only in dated historical records. Criterion 2: relative links in changed docs resolve. Criteria 4 and 5 and the closure decision are out of scope.

## Evidence

* Issue comments (closure audits 2026-10-31, 2026-11-05 and later): C1 and C2 unproved. PR #499 retained historical debt; no all-link audit existed; inventory TSV is a classification, not a deterministic pass/fail check. The existing `cutover_audit.py` generates the inventory but does not assert the invariant.
* `README.md` lines 42-51 and `src/README.md` lines 19-20: cut-over signed off 2026-10-27, archive tag `v0.21.0` (BRD version format).
* `git grep` over tracked files outside `docs/reference/regulatory/` and `.copilot-tracking/`: 51 files carry `mvp/`, `prototype/`, `zavaforward_mvp` or `properwarm_mvp`. 1744 of ~2900 lines are the generated `cutover-reference-inventory.tsv`; `cutover-parity-audit.tsv`, the parity matrix, the evidence pack, ADR 0006 and `log.md` are dated or generated records.
* The bare `prototype/` token also matches the generic phrase `prototype/PoC/MVP` (no path meaning); a precise matcher must exclude it.

## Findings by class

| Class | Files | Disposition |
| --- | --- | --- |
| Immutable or append-only | `docs/reference/regulatory/`, `.copilot-tracking/`, `docs/reference/log.md` | Out of scope, never edited |
| Generated or dated cut-over evidence | inventory and parity TSVs, parity matrix, evidence pack, Azure evidence JSON, ADR 0006, dated RAI report, capstone history and metrics | Historical records, no edit |
| Regression guards and migration fixtures | `cutover_audit.py` and test, `rename-zava-tests.py`, `rpi-checks.py`, `infra/tests/test_pipeline.py`, `mvp-validation.yml`, `src-ci.yml`, rubric safe-output test, `update-architecture.mjs` | Allowlist with reason; workflow check names stay (Issue #202) |
| Live docs naming `mvp/` without the tag | ADR 0001 and 0002, proper-warm PRD, gap analysis, Decision 1 specification, synthetic data README, `infra/README.md`, `src/*/README.md`, `src/*/pyproject.toml` comments, `tools/rename-zava.md` | Add `v0.21.0` archive-tag wording |
| Stale live tooling data | `zava-forward-{executive,technical}-architecture.excalidraw` flow and element `sources` still point at `mvp/zavaforward_mvp/...` and `mvp/web/app.js`; `update-architecture.mjs` already maps them to `src/` | Repoint to the migrated `src/` paths that exist |
| Package name in live prose | rubric README dated entries, gap analysis, Decision 1 specification, ADR 0002 pinned URL | Dated records; name allowed only there |

## Decisions

* Add `tools/check-legacy-references.py` plus unittest: deterministic file-class policy for C1 and a changed-file relative-link resolver for C2 (path existence; anchors not validated).
* Do not rewrite immutable or historical records; extend the allowlist rather than the records.
* Historical link debt in untouched documents stays out of the changed-file gate; an `--all-links` mode reports it informationally.

## Risks

* Line-level classification of the generated inventory is author classification, not proof; the checker proves the file-class invariant only.
* Excalidraw metadata edits must not change rendered output (SVG and PNG contain no `mvp/` strings).
