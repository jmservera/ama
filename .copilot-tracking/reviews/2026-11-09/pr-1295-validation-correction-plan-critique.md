<!-- markdownlint-disable-file -->
# Plan critique: PR 1295 validation correction (2026-11-09)

* Task `pr-1295-validation-correction`; executed once by an independent read-only `rubber-duck` reviewer against the real source files. Verdict: Revise. All findings are compatible with confirmed decisions and were applied directly; no user decision is required. The critique is not repeated.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Proposed test over all four drawings also finds one executive and four technical outline/text intersections, so it could not pass after the fix | Applied: scope the new test to the two capstone drawings (`cxo-architecture`, `azure-architecture`); record the inherited `docs/architecture` crossings as out-of-scope observations; show fail-before/pass-after |
| 2 | Blocking | `test-architecture.mjs` line 69 rejects element type `line` | Applied: allow `line` only for the named boundary outline and assert it is closed |
| 3 | Blocking | Both pitch files embed the candidate hash; `validation.json` pitch hashes become stale | Applied: update and verify `pitch.speaker_script_sha256` and `pitch.questions_and_answers_sha256` from the build, and qualify preview metrics not reproduced |
| 4 | Non-blocking | Delivered PDF is the LibreOffice preview; README says preview is not native Render | Applied: label it a Linux preview in changes and handoff; verify its hash against the receipt; no native claim |
| 5 | Non-blocking | Closed polygon needs an editor-style round trip | Applied: check the CLI render against SVG/PNG and re-import the JSON through the Excalidraw restore path available in the CLI package; disclose that the interactive editor was not opened |
