# Critique: 157-c4-post1547-proof-1921

Executed once by rubber-duck. Verdict: Revise. All five findings applied directly to the plan and the changes table; no user decision needed.

1. Before-activation: a receipt is post-request, so only the status endpoint and widget ordering count; require timing evidence separately.
2. Thread and memory: the 30-turn cap is a turn count, not cumulative size; rejected turns are still stored; memory 1000-char cap applies before redaction. Classify NOT FULLY PROVEN.
3. AC-103 also requires agent depth reporting; do not claim AC-103 from call limits alone.
4. Provider-call limit and zero retries need adapter trace; only one allowed and two denied roles are tested, so qualify untested roles.
5. Fallback proves a flag and message, not end-to-end workflow continuation; denied roles get 403, not fallback.
