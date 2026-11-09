<!-- markdownlint-disable-file -->
# Plan critique: PR 1295 source freshness (2026-11-09)

* Task `pr-1295-source-freshness`; executed once by an independent read-only `rubber-duck` reviewer against the real sources. Verdict: Revise. All findings are compatible with confirmed decisions and were applied directly; no user decision is required. The critique is not repeated.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Structural proof removed fields only from per-element evidence arrays; locators also occur in canvas `customData.sources`, and stripping the SVG metadata line could hide unrelated changes | Applied: keep pre-change copies; compare native JSON and the SVG metadata object (parsed) against an explicit allowlist of `line`, `sha256`, `localLink` fields on the `sources` entries and per-element evidence; compare the rest, and the SVG minus metadata, exactly |
| 2 | Blocking | Build/Verify writes `verification.json`; the compact `source/validation.json` receipt binds candidate, PDF, pitch and catalog hashes, and default `Test-SourceHashes` does not check all of them | Applied: derive each receipt field from Verify/preview output; independently recompute candidate, PDF, both pitch and catalog hashes and compare with the receipt; historical metrics stay labelled historical |
| 3 | Non-blocking | PPTX embeds the PNG only, but ZIP bytes can depend on the build; pitch files embed the candidate hash | Applied: compare built and delivered bytes; if different, verify package contents and refresh pitch files and receipt bindings; if equal, change nothing |
| 4 | Non-blocking | A differing PNG would silently widen a source-reference-only fix | Applied: an unexpected PNG difference is a stop condition requiring an explicit decision; no catalog PNG edit |
| 5 | Non-blocking | `text-equivalent.md` R09 line links are stale; `docs/reference/README.md` says 54 slides | Applied: recorded as out-of-scope observations, not edited, and no claim that every journey reference is fresh |
