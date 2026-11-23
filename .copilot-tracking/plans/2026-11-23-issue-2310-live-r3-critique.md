# Critique (executed once)

Verdict: accept. Checks: the change must not weaken any protection (authenticated and non-API verbs keep 501, so no new method surface); the 401 body must match the existing "Please sign in." contract; no redirect header. Risk: low, additive handlers. Alternative of a generic `__getattr__` rejected as obscure. No conflict with confirmed decisions.
