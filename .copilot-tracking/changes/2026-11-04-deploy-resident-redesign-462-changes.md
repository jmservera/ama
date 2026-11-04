# Changes: deploy resident redesign (2026-11-04)

* Live: demo API `--0000025`, resident `--0000010`; expiry 2027-01-31T23:59:00Z to 2028-01-01T00:00:00Z. Registry readback Disabled/Deny/no rules/exports disabled.
* Docs: infra/README.md, ux/zava-forward-prototype-profile-review.md, log.md.
* Evidence: .copilot-tracking/evidence/2026-11-04-resident-live/signedin-390.png (79 KB).
* Divergence: `--export-policy` flag does not exist; `--allow-exports` used (first attempt failed before any change; trap restored the registry).
