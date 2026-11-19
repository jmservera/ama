# Issue 117 research, fourth live pass (2026-11-18)

Unticked criterion: "Uploads are scanned before availability". Only one is unticked.
Prior notes (docs/reference/research/issue-117-live-*.md) proved the order offline and live, and recorded that the demo
default scanner (ZF_SCANNER unset -> local) is a synthetic marker scanner. Switching the demo API to Defender needs a
configuration change the owner has not authorised, and the demo storage firewall denies this identity.
Code gap found in src/core/src/zava_forward/core/doc_controls.py: LocalSignatureScanner recognises only a private
synthetic marker, so the industry-standard EICAR antivirus test file is scanned "clean" and becomes available.
Planning readiness: Ready. Research disposition: executed (code read, prior notes reviewed).
Action: add standard EICAR detection to the local scanner with tests; no Azure change.
