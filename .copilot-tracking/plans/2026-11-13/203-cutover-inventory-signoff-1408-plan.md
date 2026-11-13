# Plan: #203 inventory refresh and owner decisions (1408)

1. Regenerate `docs/architecture/cutover-reference-inventory.tsv` with `cutover_audit.py --write`, then check mode, and run `test_cutover_audit` (stdlib unittest, no venv unless imports need it). Regenerate after all doc edits, since the inventory scans docs.
2. Append a dated evidence-pack section recording the owner decisions for #201/#202/#198 and #228 AC3, keeping live deployed parity and backup criteria pending, with no ticks or closing keywords.
3. Update `tokenomics-placement-draft.md` (55-slide deck, Slide 22, B25/B27 at pages 53/55, USD 0.44 as labelled scenario, up to USD 5 batch authorised and not run, timing unperformed) and the pitch `README.md` if it has a stale mapping.
4. Append one log entry and add an index row only if the README index lists the pack sections.
5. Validate: audit check, unit test, link check, ASCII, `git diff --check`. Review, commit with Refs only.

## Critique amendments (applied)

* PC-001: the evidence pack section also records the #435 AC1/AC4 decision with scenario and batch caveats.
* PC-002: the pitch draft's status statements and decisions-needed text are updated so they do not contradict the sign-off; rehearsal and measurement stay unperformed.
