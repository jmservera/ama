# Research: issue 144 container hardening guard on Container Apps (2026-11-20)

Disposition: executed. Planning readiness: Ready.

## Evidence

* Guard: `src/core/src/zava_forward/core/container_hardening.py` (`enforce_container_hardening`, `enforce_from_env`). It sets NoNewPrivs, then requires CapInh, CapPrm, CapEff and CapAmb to be zero, then probes scratch dirs and rejects world-writable directories without the sticky bit.
* Owner-measured live facts (uid 10001 replica): CapInh equals CapBnd (0xa80425fb) while CapPrm, CapEff and CapAmb are 0; EmptyDir `/tmp` and `/state` are root:root 0777 without sticky.
* Callers of `enforce_from_env`: server.py, resident_demo/__main__.py, agents worker.py, orchestrator document_rescan.py, source_monitor.py, token_store.py (the six named), plus importer, orchestrator `__main__`, digest_blob, ranking_publish, api live_receiver and live_simulator (they pass an env mapping).
* Bicep sets TMPDIR=/tmp and ZF_STATE=/state (`infra/modules/containerapps.bicep` lines 153-164); `resident-demo` omits ZF_STATE because `FORBIDDEN_ENV_PREFIXES` in `resident_showcase.py` denies it, so the helper only repoints ZF_STATE when it is already configured.
* `src/check-container.py` uses `--cap-drop=ALL`, a sticky tmpfs `/tmp` and a /state owned by 10001, which hid both defects.

## Acceptance criteria in scope (unticked)

* Worker and job images real, versioned, deployed through the pipeline: not addressed by this change.
* Container hardening enforced in the deployed app: this change fixes the startup refusal; live receipt needs an owner-authorised Azure write and is not captured.
