# Research: issue-203-readme-tag-live

Disposition: executed. Refs #203. Base `1dddac2e0`.

## Opening evidence

* `python3 tools/check-legacy-references.py` exits 1: one violation, `docs/reference/README.md:1359` (retired path without archive tag v0.21.0). Links: 0 violations.
* Unticked criteria: (1) repo-wide search for `mvp/` and `prototype/`; (5) deployed app and CI green from `src/`.
