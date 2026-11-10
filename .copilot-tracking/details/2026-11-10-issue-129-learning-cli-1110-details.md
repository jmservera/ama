<!-- markdownlint-disable-file -->
# Details: issue 129 constructed learning-report CLI

## Command

`python -m zava_forward.core.learning_test_bundles < input.json` reads standard input only (no path argument, no discovery) and writes the report to standard output. `-h` is the only option. Exit 0 with a report (a STOP outcome is a valid report; read the STOP line, not the exit status); exit 1 with one `Learning report refused: ...` line (truncated to 200 characters, plus a refusal when stdin is a terminal) on standard error and nothing on standard output for any refusal.

## Envelope: `learning-bundle-constructed-input-v1`

One JSON object, at most `MAX_INPUT_BYTES = 65536` bytes, UTF-8, closed key sets, no duplicate keys, no `NaN`/`Infinity` constants:

```json
{
  "schema_version": "learning-bundle-constructed-input-v1",
  "run": 1,
  "bundle": "pre-visit-pack",
  "representative_data_retained": false,
  "o16_counted_under": "change-impact",
  "cases": [
    {"case": 1, "arms": {
      "comparator": {"effort": {"preparation": 2, "checking": 2, "correction": 2,
                                "coordination": 2, "resident_effort": 2, "support_cost": 2},
                     "counts": {"offers_misread_as_commitments": 0}},
      "workflow": {"effort": {...six...}, "counts": {...}}}}
  ]
}
```

* Top-level keys: `schema_version`, `run`, `bundle`, `representative_data_retained`, `cases` and, only for O16 bundles, `o16_counted_under`. Unknown keys refused. `run` and each `case` are integers 1 to 1,000,000 (not booleans); case identifiers unique; 1 to `MAX_CASES = 50` cases.
* `bundle` must be one of the five existing keys (same `Unknown bundle` message). `representative_data_retained` must be present and `false`, O16 rules, owner enum: delegated unchanged to `run_report`.
* `arms` keys exactly `comparator` and `workflow`; each arm keys exactly `effort` and `counts`. `effort` keys exactly the six `COMPONENTS`; values are int or float (not bool), finite, 0 to `MAX_MINUTES = 100000`. `counts` keys exactly the bundle's `zero_measures`; values are non-negative integers (not bool, not float) up to 1,000,000.
* Strings appear only in `schema_version`, `bundle` and `o16_counted_under`, each matched against fixed values; no free text, names or contacts can be carried.

## Output

The first line is `CONSTRUCTED, UNVERIFIED INPUT (run N).`; then `render_report(run_report(run))` unchanged (so a STOP precedes every effort figure); then fixed qualification lines: the caller declared the input; not verified synthetic provenance, a real experiment or measured user benefit; Atlas owner bundle-to-opportunity mapping unconfirmed; representative-data retention decision (DPO) unsatisfied, none retained or stored; if O16 present, the counted-under choice is the caller's constructed accounting choice, not owner mapping ratification; nothing is stored.

## Implementation steps

* Phase 1 in the module: `import argparse, json, math, sys`; constants; `_reject_constant`, `_unique_pairs`; `_number`, `_count`, `_exact_keys`, `_validate_input(raw) -> dict`; `main(argv=None) -> int`; `if __name__ == "__main__": sys.exit(main())`. Catch `ValueError`, `RecursionError` only.
* Phase 2 tests (subprocess of the real module in a fresh empty temp cwd, comparing directory listing): all five bundles succeed with expected medians; STOP line precedes median lines and exit 0; comparator-lower valid; O16 required, qualified, and absent-for-non-O16 refused; retention true/missing refused; refusals for empty, non-JSON, oversize, duplicate keys, NaN/Infinity/`1e999`, bool numbers, string numbers, negative, float count, unknown/extra/free-text keys, wrong schema, deep nesting, wrong counts keys, duplicate or boolean case IDs, too many cases; unchanged scorer (`compare_bundle` output identical for a case via CLI parse equivalence is covered by values); import of the module has no side effects.
* Phase 3 README: `## Constructed learning-test report command (#129, Refs #123)` with command, limits, qualifications and non-goals.
