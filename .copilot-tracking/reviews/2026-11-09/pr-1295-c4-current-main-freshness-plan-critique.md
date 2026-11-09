<!-- markdownlint-disable-file -->
# Plan critique: PR 1295 C4 current-main freshness (2026-11-09)

* Task `pr-1295-c4-current-main-freshness`; executed once by an independent read-only `rubber-duck` reviewer against the real sources. Verdict: Revise. All findings are compatible with confirmed decisions and were applied directly; no user decision is required. The critique is not repeated.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | `docs/architecture/update-architecture.mjs` writes two legacy Excalidraw files (lines 73, 123), and their SVG provenance hashes can go stale (`test-architecture.mjs:161`) | Applied: run update only as `--check` first; a write is limited to files whose check fails, with a before/after diff recorded; the legacy files are named in the changes record |
| 2 | Blocking | Diagram SVG and native hashes are package inputs (`Invoke-Capstone.ps1:482`, `validation.json:40`); a catalog refresh also changes the receipt binding; unchanged PNGs alone do not prove the delivered deck is reproducible | Applied: if any SVG or native input changes, the delivered PPTX/PDF are compared (by a rebuild into scratch, not the delivered path) and the outcome is reported; no delivered binary is overwritten without the comparison; catalog and receipt are touched only if `Test-SourceHashes` says so |
| 3 | Blocking | `test-geometry.mjs:99` needs the `excalidraw` package and a browser; `pwsh` is not on `PATH` | Applied: use existing isolated runtimes only (scratch install of npm dependencies, no global install); any prerequisite that cannot be obtained is recorded as unverified, never skipped silently |
| 4 | Non-blocking | The journey directory has no `test-*.mjs`; commands need repository-root paths and `pwsh -File` | Applied in the phase details commands |
| 5 | Non-blocking | The three planning files are untracked at merge time | Applied: they are committed before the merge as the prospective RPI evidence commit so the tree is clean |
| 6 | Non-blocking | The `sensor_analysis_store` locator at `text-equivalent.md:127` may already be current | Applied: every locator is verified before editing; no blind replacement |
| 7 | Non-blocking | The optional architecture-guide edit may exceed the stale-only scope | Applied: it is made only if a check or text read proves a stale statement |
