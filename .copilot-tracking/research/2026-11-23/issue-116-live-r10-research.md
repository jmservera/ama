# Research 2026-11-23, issue 116 live r10

Disposition: executed. Planning readiness: Ready.

Only unticked box: allowlists at every provider boundary. Others are owner-ticked and were skipped.

Finding: `approved_payload` in `core/ai.py` checks that an image part is `data:image/png|jpeg;base64,` and bounds `len(data)*3//4`, but never checks that the remainder is base64. A structured part such as `data:image/png;base64,<free text>` passes the allowlist, so unapproved raw text can reach the provider labelled as an image. `look_at` encodes real bytes, so only the shared boundary (`Ai.evidence`/`_chat` with list input, retained families) is exposed.

Fix: strict `base64.b64decode(validate=True)` in the shared check, refused as `input-type-not-approved` before any other gate. Existing fixtures (`AAAA`, encoded bytes) are valid base64, so they stay compatible. Magic-byte checks were rejected: existing tests send non-image bytes deliberately.

Live: the payload is invisible from the deployed apps (r7 to r9); live proof of this criterion is not possible for the demo.
