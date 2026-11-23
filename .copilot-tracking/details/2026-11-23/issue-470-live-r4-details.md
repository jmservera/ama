# Details, issue 470 live r4

Phase 1: `render_markdown(report)` returns lines: verdict, then for COMPARABLE a table `| Arm | Receipts | Span median (s) | Min | Max |` and a delta line; for NONCOMPARABLE a bullet per reason. `main` prints it instead of JSON when `--markdown` is passed to `compare`; exit codes unchanged.

Phase 2: tests for comparable and noncomparable rendering using `CompareTests.arm`.
