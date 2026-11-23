# Research 2026-11-23 r2 (issue 2186)

Disposition: executed. Planning readiness: Ready.

Issue criteria (issue body has no checkboxes): relaxation recorded in receipt verify output; code/tool/image changes still invalidate; test added. The merged work (`RECEIPT_INERT_PREFIXES`, `receipt_inert_path`, `base_relaxation(inert_only=True)`) already satisfies all three; the previous run recorded them proven.

Follow-up routed by the previous review: derive a read-set so a docs subtree such as `docs/presentations` can again be inert for a full receipt.

Findings:

* `docs/presentations` holds only `legal-briefing-224.pptx`; no test reads it (grep of `*.py`, workflows, Dockerfiles, toml, json).
* `tools/check-repo-secrets.py:39` scans every path from `git ls-files`, and `tools/check-legacy-references.py:78` and `tools/rpi-preflight.py:129` enumerate all tracked files. A full receipt includes those checks, so any new file under `docs/`, binary or not, is gate input.
* Conclusion: no docs subtree is provably unread by a full gate; a derived read-set is unsafe without per-check manifests. No new relaxation is justified.
* Live Azure, browser and billing proof do not apply to a local gate tool.

Residual unproven: a real end-to-end full receipt across a docs-moved main (needs `--all`, forbidden here).

Plan: add one regression case pinning that a binary file under `docs/presentations/` invalidates a full receipt, with the scan rationale. Tooling-only, focused tier; no `src` change.
