<!-- markdownlint-disable-file -->
# Review: issue 129 constructed learning-report CLI (single post-implementation pass)

* Executed once after `implement-done` by the implementing agent as a separate adversarial pass (no nested agent). It is not independent assessment; Root exact-head assessment remains required before publication. No second Review and no automatic post-review correction (owner direction); open findings are routed.
* Assessed boundary: working tree diff against `d52f20a5198de7269f39daf794911545aee01ced` for three files (module, test file, Core README) plus the RPI artifacts, before the local commit.
* Outcome: conformant for the admitted boundary, with open finding R1 (low) routed to a later correction and R2 (documentation) routed to Root serialization. Not "no findings".

## Checks performed

* Scope: `git diff --name-only` lists only the three owned files; no knowledge-base, protocol, registry, API, config or dependency edit; module diff has no removed lines, so scorer, comparators, zero rules, bundle enums and renderer are byte-for-byte as before.
* Boundary probes run against the real command: valid numeric input, malformed text, 6,000-digit integer (refused, exit 1), `1e-400` (accepted as 0), `o16_counted_under: null` on a non-O16 bundle (accepted, no O16 line, as `run_report` does), extra positional argument (argparse usage error, exit 2), no files written in any case.
* Labels: output states constructed/unverified, Atlas mapping unconfirmed, retention unsatisfied, capacity-only, nothing stored; O16 choice is labelled the caller's accounting, not ratification. No favourable result is generated when input is absent (empty input is refused).
* Tests assert behaviour through the real scorer/renderer in a subprocess and check for no created files; they would fail without the CLI (red run recorded in the changes file).
* Validation actually run and read: 20 module tests, Core configured ruff check, ruff format check and mypy, all exit 0 (logs external). Hosted CI not observed; blanket gates skipped by tier.

## Findings

* R1 (low, open, routed to a later correction): with standard input closed (`<&-`), `sys.stdin` is `None` and `main` raises an `AttributeError` traceback (exit 1) instead of the one-line `Learning report refused:` convention. No report, no output file and no data are produced, so it is a message-convention gap only. Evidence: probe `python -m zava_forward.core.learning_test_bundles <&-`. Not covered by a test.
* R2 (documentation, routed to Root serialization): `docs/reference/README.md` (row for #129) and the protocol "Next slices" do not mention the new command. They are not contradicted, and this task was forbidden from editing them while another owner appends to those files.
* R3 (note, accepted): a STOP exits 0; documented in the README. Exit 2 for extra positional arguments comes from argparse and is non-zero, as required.

## Routing

* R1: follow-up small correction (treat a missing stdin as a refusal, add one test); needs an owner decision because the owner directed no automatic post-review correction.
* R2: Root to serialize the index, log and protocol mention after the append work.
* Not satisfied and not claimed: real five-bundle experiment, participants or facilitators, Atlas owner mapping confirmation, DPO retention decision, Finance validation of saved minutes, whole-issue closure of #129 or #123.
