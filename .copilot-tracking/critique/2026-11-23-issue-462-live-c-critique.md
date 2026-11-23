# Critique: issue 462 third pass (2026-11-23)

Executed once on the final candidate plan. Verdict: proceed.

* Risk: HSTS on a `__Host-` cookie app could pin a bad host. Mitigation: the header is ignored over plain HTTP, ingress is HTTPS-only, `max-age=31536000` matches the employee API (`server.py`), and no `includeSubDomains` or `preload` is set, so there is no cross-host lock-in.
* Risk: a src change needs the full tier and a redeploy to be live. Decision: make the source and test change as a local commit; redeploy is not authorised here, so live HSTS stays unproven and is recorded as such.
* Risk: the existing test iterates `demo.HEADERS`, so a header added to the dict is already asserted. Mitigation: add one explicit assertion on the HSTS value so removal fails.
* Risk: over-claiming from the live check. Mitigation: state revision 0000027 and the digest prefix, and leave criteria 5 and 8 as recorded.
