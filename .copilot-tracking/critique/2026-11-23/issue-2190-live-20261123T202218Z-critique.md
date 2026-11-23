# Critique: issue 2190, glued header (executed once)

Verdict: proceed. Risks reviewed:

* Splitting could invent a header from log text. Mitigation: the split needs a `test_*` name, a dotted class, `(..) ... ` shape, and applies only to lines that do not already start with a header; it only inserts a newline, so a result still needs its own `ok` and no FAIL/ERROR/skipped text.
* Relaxation: none. Failure patterns, exact-name matching and one-hit rule are unchanged; a glued header that fails is now attributed to its own test.
* Compatible findings applied directly: add a rejecting case (glued header whose test fails) beside the accepting one.
