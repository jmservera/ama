# Changes: issue 203 sixth run (2026-11-23)

Refs #203. Not pushed. Tier: full on doubt (gate-tool allowlist edit); targeted tests only, `rpi-checks.py --all` not run (coordinator owns the gate).

## Files

* `tools/check-legacy-references.py`: `.github/rubric/scripts/test_prepare.py` added to `GUARD_FILES`.
* `docs/reference/research/issue-203-live-20261123-2026-11-23.md` and `issue-203-live-20261123-evidence/` (new); `docs/reference/README.md` index row; `docs/reference/log.md` appended entry.
* `.copilot-tracking/` research, critique, plan, details, changes, review, state (dated 2026-11-23).

Divergence: the witness recorded that the source edit raced the `implement-start` call (issued in parallel); the changes record was persisted first.

## Per-criterion table

| # | Criterion | Status | Evidence |
| --- | --- | --- | --- |
| 1 | Search returns only intentional historical references | Proven after fix (checker exit 1 before, 0 after; 26 tests OK) | research note, `legacy-check-*.txt` |
| 2 | Relative links in changed docs resolve (ticked) | Checker links: 0 violations in 8 documents | checker output |
| 3 | Index and log updated (ticked) | Applied for this note; earlier entries untouched | diff |
| 4 | Rubric comparison (ticked) | Not re-proven | |
| 5 | Deployed app and CI green from `src/` | Partly proven. Unproven: image built from `src/` (`src-deploy.yml` 0 runs, registry private), push CI on `main` (workflow runs on PR and dispatch). Closing needs a deploy, out of demo scope | research note section Result |

## Validation

* `python3 tools/check-legacy-references.py`: exit 0.
* Four legacy-reference unittest modules: 26 OK. `ruff check` and `ruff format --check` on the edited file pass. mypy and src suites not applicable (no `src/` project change).
* Hosted CI for the exact head: not observed (no push).
