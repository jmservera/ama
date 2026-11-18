# Critique: issue 130 live audit run 4 plan (executed once)

Verdict: proceed. Compatible findings applied directly.

* Risk: probes create demo data. Mitigation: same synthetic case and write shapes as run 3 plus one form-encoded POST; all refused, zero records verified before and after.
* Risk: repeating run 3 adds nothing. Mitigation: new angle (new revision, form-encoded 400 explained from source, Resident tab render).
* Risk: credential leakage. Mitigation: runtime read, e-mail scrub, literal scan of the evidence directory for all three credential files.
* Scope creep into the 403 fix: rejected; src/core security control needs FULL tier and redeploy.
* Claiming the unticked criterion: rejected; stated unproven with reason, nothing ticked.
