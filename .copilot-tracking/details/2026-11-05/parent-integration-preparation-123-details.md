<!-- markdownlint-disable-file -->
# Details: parent topic integration preparation (#123), 2026-11-05

Plan: [plan](../../plans/2026-11-05/parent-integration-preparation-123-plan.md).

## Phase 2 and 3: merges

* Files: whole-tree merge of `origin/feat/discovery-assurance-integration-123` (`63dd5798`) then `origin/main` (`bb3a3b03`).
* Success: both tips are ancestors of the local head; no reset, rebase or force; `git merge-base --is-ancestor` proofs recorded.
* Conflict rule: only `docs/reference/log.md` is expected to conflict. Keep every entry from both sides, ordered by date heading, with no rewording of earlier entries. Stop and return if any other conflict or ambiguous intent appears.

## Phase 4: scope

* Compute `git diff --stat origin/main HEAD` and name status; separate source and test files from RPI evidence and docs; confirm main-only files are absent from the diff.

## Phase 5: documents

* `docs/architecture/cutover-evidence-pack.md`: new section after the seventh checkpoint continuation, with identities (source, intake, merge, main baseline), covered #128 and #440 children (#1211, #1212, #1213, #1221), BRD, PRD, ADR blob and status identities, document-qualified traceability, evidence classification, actual bounded commands, findings and criteria state.
* `docs/reference/README.md`: one link in the cut-over evidence list near the seventh checkpoint link.
* `docs/reference/log.md`: one appended entry; earlier entries untouched.

## Phase 6: light observation

* `PYTHONDONTWRITEBYTECODE=1`, external `RUFF_CACHE_DIR`, `MYPY_CACHE_DIR`, `XDG_CACHE_HOME` under `/tmp`; interpreter `/tmp/ama-96-venv/bin/python` with explicit `PYTHONPATH=<worktree>/src/core/src:<worktree>/src/core/tests`; assert `__file__` of imported modules lies under this worktree.
* Skip heavy breadth; do not run `tools/rpi-checks.py`.
