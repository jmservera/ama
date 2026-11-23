# Research 2026-11-23, issue 116 live r11

Disposition: executed. Planning Readiness: Ready.

Only the provider-boundary box is unticked; the four role/visibility boxes and six other RAI boxes are ticked from earlier rounds (r3 to r10). Rereading `approved_payload` (`src/core/src/zava_forward/core/ai.py`) found a defect: text containing a lone surrogate (for example `"\ud800"`) makes `str.encode("utf-8")` raise `UnicodeEncodeError` instead of `InputRefused`. No provider call happens, but `Ai.evidence` reports `provider-unavailable` rather than `input-refused`, so the refusal is not visible as an input refusal (criterion: "fail visibly before any provider call"). Probe output: `UnicodeEncodeError` for system, string user and list text part.

Unprovable for the demo: live payload contents (not observable from deployed apps), independent review, hosted CI. Live Azure was not touched; no credential read.
