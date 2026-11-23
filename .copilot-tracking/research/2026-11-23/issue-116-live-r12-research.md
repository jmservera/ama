# Research 2026-11-23, issue 116 live r12

Disposition: executed. Planning Readiness: Ready.

Scope: the one unticked box (allowlists at every provider boundary). r8 to r11 fixed ordering, string size, image data and unencodable text in `approved_payload` (`src/core/src/zava_forward/core/ai.py`).

Finding: `approved_payload` caps each image at `MAX_IMAGE_BYTES` (4 MiB) but sums only text bytes. A structured payload with many images, each under the cap, passes the size allowlist and reaches the provider, so total input size is unbounded. The only real caller (`look_at`, line 386) sends one image, so a total cap of `MAX_IMAGE_BYTES` breaks nothing. All provider families reach the boundary through `_request_body` (single call site, line 209).

Not provable for the demo: live payload content (not observable from deployed apps), independent review, hosted CI.
