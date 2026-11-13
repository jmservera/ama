# Critique: #107 identity-field sanitisation (1440)

Execution: complete (rubber-duck, one pass). Verdict: Revise. All findings compatible with confirmed decisions; applied directly, no user decision.

| ID | Finding | Disposition |
| --- | --- | --- |
| PC-001 | `complete_result` post-back bypasses `shape_result` | Sanitise identity in `complete` and before `_settle_meter` |
| PC-002 | Replacement marker could equal a released/reserved identity | `_settle_meter` passes None when sanitising rewrote the model; release check also rejects the marker |
| PC-003 | Boundary regex lets `abcsk-SECRET` through | Reject `sk-` anywhere (case-insensitive) |
| PC-004 | `ai.py` evidence envelope and `out` return raw model/deployment | Sanitise at those boundaries |
| PC-005 | Slice before type check | Check exact type before slicing |
