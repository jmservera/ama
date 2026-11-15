# Plan: every list offers a read-only export (issue 80 criterion 2)

Research: [research](../../research/2026-11-13/80-every-list-export-2035-research.md). Details: [details](../../details/2026-11-13/80-every-list-export-2035-details.md).

## Phases

* [x] Phase 1: close the four row-list gaps with GET-only CSV routes that reuse the JSON store call and role limits (time mine and report, law sources, assistant proposals metadata, aftercare concern tracking fields).
* [x] Phase 2: add plain-language download links to each screen, with the read-only copy sentence.
* [x] Phase 3: refuse an exported workbook in the importer preview so it cannot be staged as an authoritative write-back.
* [x] Phase 4: add a complete inventory test (every endpoint the screens read is exported or explained), end-to-end export tests proving unchanged stored state, formula neutralisation, role denial and preview-only import-back.
* [x] Phase 5: validate in `/tmp/venv-80ex-2035` (pip only), remove only that venv, commit with `Refs #80`.

## Decisions

* CSV satisfies the criterion; no new XLSX route.
* Resident free text, assistant provenance and conversation content stay out of files.
* Time report keeps its minimum-group suppression; it exports only the suppressed `by_activity` rows.
* No push, no GitHub edits, no criterion tick; criterion 2 evidence is reported for the owner.
