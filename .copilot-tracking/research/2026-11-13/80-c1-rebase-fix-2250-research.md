<!-- markdownlint-disable-file -->
# Research: C1 correction of the #80 list-export candidate

* Task: `80-c1-rebase-fix-2250`. Parent: `80-every-list-export-2035`. Branch `feat/demo-80-every-list-export-2035`. Date 2026-11-13.
* Research disposition: executed (code read plus the independent exact-head review, `80-list-exports-review-2220-review.md`, verdict FAIL). Planning Readiness: Ready.

## Findings to resolve

* Rebase: origin/main moved to `f427b8c4e` (it contains the requested `9c8c898`). The only conflict was the GET_ENDPOINTS list in `src/api/tests/test_role_endpoint_inventory.py`: main added `/proposal-freshness`; the candidate added `aftercare/concerns.csv` and `assistants/proposals.csv` (plus time, law CSV routes on neighbouring lines). Resolution keeps both.
* `test_list_export_inventory.py` raw-string regex used `\\b` (literal backslash), so it never matched; the `sorted(row) == sorted([*row])` assertion is a tautology.
* `src/importer/.../xlsx.py` `safe_cell` only checked the first character; `src/core/.../list_export.py` also checks after leading whitespace.
* Law row (`law_source_rows`) lacked `review_status`, `reviewed`, `authority_type`, `official_url`; the lawstore listing already carries them (`lawstore.py` `sources()`, `_source`). No supersession field exists in the store: a `historical` status is the only signal.
* Proposal row lacked source freshness and reviewer decision. The listing body carries `stale`, `epoch_current`, `relied_on`, `source_signature`, `verification{by,signature,note,at}` and `review{action,by,note,at}` (`assistants.py` listing and `_view`).
* `/proposal-freshness` is a per-draft form-review endpoint, not a workbench list: the inventory scan finds no screen list for it, so no new classification is needed. The inventory test is run at the rebased head to prove it.

## Decisions

* Proposals export: add `epoch_current`, `relied_on`, `source_state`, `source_verified` (signature matches), `source_verified_at`, `review_decision`, `reviewed_at`. Reviewer emails, notes, outputs and snapshots stay out.
* Law export: add the four requested fields plus a derived `supersession` text from `status`.
