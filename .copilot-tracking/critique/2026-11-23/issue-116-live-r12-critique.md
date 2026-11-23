# Critique 2026-11-23, issue 116 live r12

Executed once. Verdict: proceed.

* A per-request total image cap of `MAX_IMAGE_BYTES` matches the single-image real caller; a higher aggregate cap would need a justified use case. Accepted.
* Count total on the decoded estimate (`len(data) * 3 // 4`), as the per-image check does, to stay consistent. Accepted.
* Reuse reason `input-image-too-large`; no new reason string. Accepted.
* Raising the aggregate only after the base64 check keeps malformed data refused as `input-type-not-approved`. Accepted.
