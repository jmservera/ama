# Research: issue 144 (2026-11-23, run 20261123T192353Z)

Disposition: executed. Planning Readiness: Ready.

Prior work read: 2026-11-22 research, 2026-11-23 changes (hardening verifier), hardening receipt 2026-11-23, deployed images tool.

Unticked criteria: (1) worker/job images real, versioned, pipeline-deployed; (2) hardening enforced in deployed app.

Gap found: `infra/scripts/pipeline.py` `WORKLOAD_IMAGE_PARAMETERS` (workload to image parameter) is not referenced by any test, so it can drift from `infra/modules/containerapps.bicep`, which would deploy a worker with a digest of the wrong project. Also no test proves each worker command module (`zava_forward.orchestrator.token_store`, `digest_blob`, `ranking_publish`, `importer`, `agents`) exists in the project whose image the workload receives, so a "real" worker image could start a missing module.

Angle: add an offline regression test in infra/tests linking Bicep workloads, pipeline mapping and src module files. Code/test only; owner-only items (read-only root exception, src-deploy run) skipped. Live Azure not needed; no throwaway resource.
