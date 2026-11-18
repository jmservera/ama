# Review: issue 144 live evidence (2026-11-18, live2)

Executed once. Outcome: conformant for a documentation-only evidence record.

* Claims match probe output; adverse findings (writable root, absent hardening env) are stated, not softened.
* No criterion is ticked or claimed proven beyond evidence.
* Process note: a first write overwrote same-named tracked artifacts; they were restored from git and this run moved to the `live2` names.
* Open work routed to later tasks: redeploy a revision from current main with `ZF_CONTAINER_HARDENING=enforced` (needs owner authorisation); run `src-deploy.yml` on protected runners.
