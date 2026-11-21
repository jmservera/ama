# Critique (single pass): issue 144 plan

Verdict: proceed.

* Dropping inheritable caps weakens nothing: the check stays and a failed drop fails closed. Accepted.
* Risk: repointing ZF_STATE for resident-demo would trip FORBIDDEN_ENV_PREFIXES. Applied: only repoint when already set.
* Risk: the `/state/public-simulation` absolute paths in bicep are not under `/state/zf`; they are explicit configuration, not guard-checked. Documented, not changed.
* Risk: agents worker heartbeat defaults to `/state` when ZF_STATE is unset. Acceptable: /state stays writable by uid 10001 per the owner (guard checks ZF_STATE only when set).
* Mapping-passing entrypoints get the helper with their own env mapping. Applied.
