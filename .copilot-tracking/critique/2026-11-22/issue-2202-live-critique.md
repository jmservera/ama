# Critique: issue 2202 live deploy plan (one pass)

Verdict: approve with direct dispositions.

* Build from a clean origin/main checkout so the image matches merged code. Applied.
* Push only through /tmp/acr-push.sh and require the ACR to read Disabled afterwards; never use Bicep. Applied.
* Update the API app and both live jobs to the same digest; record the old digest as the rollback. Applied.
* Disable-state of ACR must be checked even on failure. Applied.
* Proofs must not print credentials; Playwright reads them at runtime only. Applied.
* Throwaway resources: none planned; delete any created. Applied.
