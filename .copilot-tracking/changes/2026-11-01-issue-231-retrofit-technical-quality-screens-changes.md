# Changes: issue 231 technical queue and quality screens (2026-11-01)

* Added: `technical-queue` and `quality-queue` read-only role screens in `src/api/src/zava_forward/api/web/role-screens.js`, reusing the #226 helpers.
* Added: `src/api/tests/test_technical_quality_screens.py` (9 node-vm tests).
* Validation: new, role_screens, asset_board, workspace_scripts, design_system, accessibility_baseline tests pass (36); ruff check, ruff format --check, mypy src clean for `src/api`. Run in a throwaway venv with pip.
* Divergence: none from plan. Browser and axe keyboard checks not run locally; CI is the evidence.
* Review fixes (PR #656 Copilot threads): technical readiness no longer requires a stock conflict register and treats a sign-off as valid unless core moved it to "Needs reassessment" (scoped design changes). Core now supplies `quality_handover_blockers` (`quality.handover_blockers`: checklist coverage by recorded checklist, safety hold, resident scope) and the quality screen blocks readiness on it or when it is not supplied. A handed-over defect record keeps "Passed" reinspection. Tests added for each; ruff clean.

## PR review round 2

* `src/core/src/zava_forward/core/quality.py`: `handover_blockers` uses `[]` instead of `None` for unbound accepted records.
* `src/core/tests/test_quality_procurement.py`: added unbound-evidence regression.

## Merge of origin/main (2026-11-01, PR #656)

* Resolved `role-screens.js`: kept this PR's technical and quality screens and every role screen merged to main (resident choice, hazard triage, data operator, contractor job pack, finance, funding).
* origin/main had unclosed `registerRoleScreen` blocks (a syntax error from earlier overlapping merges); closing `});` added so `node --check` passes.
* `.github/rubric/scores/latest.json` kept the branch side; `docs/reference/log.md` kept both entries.
* Validation: node --check, ruff check/format clean, API unittest 1490 run, only 2 import errors (azure.eventhub not installed locally); mypy only reports pre-existing azure.iot stub errors.

## Correction cycle 3 (PR #656)

* Merged origin/main again; `role-screens.js` conflicts were blank-line only, `node --check` passes.
* Four Copilot threads showed an earlier merge had reverted main content outside this issue. Restored from origin/main: `determinism_audit.py` and its test (six generators, per-generator exception boundary), `generate_pack.py` (`version`, `generator_revision`), `chat-memory-dpia.md`, `chat_privacy.py` and its test, `docs/reference/log.md`, both README indexes and the issue 163 and 176 tracking files. The PR diff now carries only issue 231 work.
* Validation: ruff check and format clean, mypy src/core clean, core tests for determinism, chat privacy and quality procurement pass (149), API suite 1490 run with only the 2 known azure.eventhub import errors.
