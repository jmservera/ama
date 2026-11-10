<!-- markdownlint-disable-file -->
# Research: issue 129 constructed learning-report CLI (initial composition)

* Opened (prospective, actual tool UTC): 2026-11-10T09:24:33Z (witness `research-open` seq 2; the research body above was drafted in the same pass, with the witness recorded once the file and state existed)
* Branch: `feat/demo-constructed-learning-cli-129-1110`; worktree `/home/azureuser/source/ama-demo-wt/issue-129-learning-cli-1110`
* Base/target: main `d52f20a5198de7269f39daf794911545aee01ced`; LOCAL ONLY, no push, no PR. Refs #129 and #123 only; no whole-issue closure.
* Mode: manual-sequenced full loop. Research disposition: `executed`. Planning Readiness: `Ready`.
* This is one admitted initial missing operator consumer. Historical correction balance is UNKNOWN; no reset, no allowance, no automatic post-review correction.

## Sources read

* `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md` (scanned for learning-test material), `docs/reference/README.md` (row for #129), `docs/reference/memory.md`.
* `docs/reference/research/ux/journey-learning-test-bundles.md` (protocol), ADR 0003 decisions 1 to 5 and the PRD "Candidate journey learning tests".
* Root admission snapshot of #129 (OPEN, full body, all three comments: 2026-10-15 ADR acceptance amendment, 2026-11-03 closure audit, 2026-11-05 closure audit) and the #129 section of the external source-questions screen.
* `src/core/src/zava_forward/core/learning_test_bundles.py` (blob `2c5483ccd20961ceb98264a3d86ec0409e3fa2f1`), `src/core/tests/test_learning_test_bundles.py` (blob `316834519216dd0da86195419918eb3516299b9a`), `src/core/README.md` (blob `1cc9a1c7a09fbca16b58650ab6ce23d10aa23a14`; no existing learning section) and the module-local CLI convention in `synthetic/cutover_audit.py` (`argparse`, `parser.exit(1, ...)` on `ValueError`).

## Findings

* The module delivers `run_report` (bundle, retention-false and O16 owner validation, then `compare_bundle`) and `render_report` (stop-first plain text). It has no `main`, no `__main__` guard and no input boundary.
* Actual baseline (executed, preserved externally as `phase129-learning-cli-evidence-1110/baseline.txt`): `python -m zava_forward.core.learning_test_bundles in.json`, the same with stdin, and `--help` each exit 0 with no output. The module is imported as `__main__`, defines functions and ends. A valid constructed input therefore silently produces no report; this is a worse failure than an error because it reads as success.
* Existing unit tests (12) pass at baseline in an own venv (`unittest`, `OK`).
* History and branch search found no equivalent or retained CLI attempt: the only #129 PRs are #899 (protocol), #1015 and #1027 (helper and run validation, merged) and #1008 (closed duplicate of #1015); `argparse` never appears in the module's history; the other 129 branches are #1015 ancestry and an unrelated old base. No comment owns or prohibits this exact boundary. The 2026-11-05 comment confirms the module runs no experiment, retains no representative data and that O16 supplied accounting is not owner ratification.
* The protocol holds screen wiring and stored run records until owner mapping and DPO retention decision. An ephemeral numeric stdin to stdout command stores nothing and is not that wiring. Protocol text remains authoritative; no contradiction found, so no shared-doc edit is needed.
* Existing validation gaps the boundary must close before calling `run_report` (they are input-boundary concerns, not scorer changes): `case_net_effort` accepts booleans, strings that compare, and nonfinite values (NaN passes `v < 0`); `compare_bundle` does not reject unknown count keys or non-integer counts, and a nonzero string count would be accepted. The CLI therefore performs strict type validation only and delegates bundle, retention and O16 checks to `run_report` unchanged.

## Design conclusions (inputs to plan)

* stdin only, one JSON object, at most 65,536 bytes; no file path, no discovery, no writes.
* Closed schema `learning-bundle-constructed-input-v1` with numeric run and case identifiers, six exact effort fields, exact per-bundle zero-count fields, explicit `representative_data_retained: false`.
* Exit 0 with report on stdout (a STOP outcome is a valid report); exit 1 with one refusal line on stderr for any refusal.
* Appended qualification lines: constructed and unverified input, Atlas mapping unconfirmed, O16 choice is the caller's accounting and not owner ratification, representative-data retention decision unsatisfied.

## Remaining gates (not satisfied here)

* No real experiment, participant, facilitator, owner or DPO decision; Atlas owner mapping unconfirmed; representative data retention Unknown; Finance validation of saved minutes.

Planning Readiness: `Ready`.
